/* SIGNAL — live mode.
   Active only when the page is served by engine/server.py (http://127.0.0.1:8765).
   Opened as a plain file, the prototype keeps its synthetic replay. */
(function () {
  "use strict";
  const C = window.SIGNAL_CORE;
  if (!C || location.protocol === "file:") return;
  const { $, $$, h } = C;
  const LIVE = (window.SIGNAL_LIVE = { active: false, result: null });
  let universe = [];
  let poll = null;

  const esc = (s) =>
    String(s == null ? "" : s).replace(
      /[&<>"]/g,
      (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c],
    );

  fetch("/api/health")
    .then((r) => r.json())
    .then((j) => {
      if (!j.ok) return;
      LIVE.active = true;
      document.body.classList.add("live");
      setupInput();
      fetch("/api/universe")
        .then((r) => r.json())
        .then((u) => {
          universe = u;
          fillList();
          updateMeta();
        });
      fetch("/api/cached/KOTAKBANK")
        .then((r) => (r.ok ? r.json() : null))
        .then((k) => {
          if (k && !LIVE.result) {
            LIVE.result = k;
            setContext(k, false);
            if (k.discovery) {
              renderDiscovery(k);
              renderFalsification(k);
              renderDocs(k);
            }
          }
        })
        .catch(() => {});
    })
    .catch(() => {});

  /* ---------------- research form ---------------- */
  function setupInput() {
    const box = $(".company-input");
    box.innerHTML =
      '<input id="liveSymbol" list="liveList" spellcheck="false" autocomplete="off" value="ICICIBANK" ' +
      'style="font:inherit;font-size:22px;font-weight:500;letter-spacing:-.01em;border:0;outline:0;background:transparent;width:100%;color:var(--ink);text-transform:uppercase" />' +
      '<datalist id="liveList"></datalist>';
    $(".runbar .hint").innerHTML =
      "<b style='color:var(--ink)'>Live</b> · fetches public NSE XBRL filings now · type any listed bank, NBFC or financial company";
    const chip = $(".top-right .chip");
    chip.textContent = "LIVE · NSE FILINGS";
    chip.classList.add("solid");
    $(".field .meta").innerHTML = "NSE symbol<br>any listed company";
    const inp = $("#liveSymbol");
    inp.addEventListener("input", updateMeta);
    inp.addEventListener("keydown", (e) => {
      if (e.key === "Enter") LIVE.run();
    });
  }
  function fillList() {
    $("#liveList").innerHTML = universe
      .map((u) => `<option value="${esc(u.symbol)}">${esc(u.name)}</option>`)
      .join("");
  }
  function updateMeta() {
    const s = ($("#liveSymbol").value || "").trim().toUpperCase();
    const u = universe.find((x) => x.symbol === s);
    const arch = {
      bank: "Bank",
      nbfc: "NBFC / HFC",
      insurer: "Insurer",
      generic: "Market infra / holdco",
    };
    $("#companyMeta").textContent = u
      ? `${u.name} · NSE: ${s} · archetype: ${arch[u.archetype]} · peers from the same archetype`
      : s
        ? `NSE: ${s} · archetype detected from exchange industry data at run time`
        : "type an NSE symbol";
  }

  /* ---------------- run ---------------- */
  LIVE.run = function () {
    const sym = ($("#liveSymbol").value || "").trim().toUpperCase();
    if (!sym) return;
    C.clearTimers();
    C.setRunState("running");
    LIVE.result = null;
    C.go("run");
    C.renderRunShell();
    $("#runDone").classList.remove("on");
    $$(".funnel-row .count").forEach((el) => (el.textContent = "·"));
    $("#rejects").innerHTML = "";
    $("#runClock").textContent = "LIVE · 00:00";
    setContext(
      {
        company: sym,
        symbol: sym,
        archetype_label: "detecting…",
        period: "",
        peers: [],
      },
      true,
    );
    fetch("/api/run?symbol=" + encodeURIComponent(sym))
      .then((r) => r.json())
      .then((j) => {
        if (j.error) return fail(j.error);
        let since = 0;
        poll = setInterval(() => {
          fetch(`/api/job/${j.job}?since=${since}`)
            .then((r) => (r.ok ? r.json() : null))
            .then((st) => {
              if (!st) return;
              since = st.log_len;
              applyState(st);
              if (st.done) {
                clearInterval(poll);
                if (st.error) fail(st.error);
                else finish(st.result);
              }
            })
            .catch(() => {});
        }, 450);
      })
      .catch((e) => fail(String(e)));
  };

  function applyState(st) {
    const log = $("#log");
    st.log.forEach((l) => {
      log.appendChild(
        h(
          "div",
          "log-line" + (l.k === "stage" ? " stage" : l.k === "hl" ? " hl" : ""),
          `<span class="s">${l.k === "stage" ? "▸" : "·"}</span><span>${esc(l.t)}</span>`,
        ),
      );
    });
    log.scrollTop = log.scrollHeight;
    $$(".rail-step").forEach((el, k) => {
      const done = k < st.stage || (st.done && !st.error);
      el.classList.toggle("done", done);
      el.classList.toggle("active", k === st.stage && !st.done);
      el.querySelector(".st").textContent =
        st.stats[k] || (k === st.stage && !st.done ? "running…" : "—");
      el.querySelector(".bar i").style.width = done
        ? "100%"
        : k === st.stage
          ? "55%"
          : "0";
    });
    const s = Math.floor(st.elapsed);
    $("#runClock").textContent =
      `LIVE · ${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
    if (st.partial && st.partial.funnel)
      setFunnel(st.partial.funnel, st.funnel_on);
  }

  function setFunnel(rows, on) {
    const max = Math.max(1, rows[0].c);
    $$(".funnel-row").forEach((row, i) => {
      const f = rows[i];
      if (!f) return;
      row.querySelector(".count").textContent = f.c;
      row.querySelector(".flabel span").textContent = f.l;
      row.querySelector(".flabel .gate").textContent = f.g;
      if (i < on) {
        row.classList.add("on");
        row.querySelector(".fbar i").style.width = f.c
          ? Math.max(4, 100 * Math.sqrt(f.c / max)) + "%"
          : "0";
      }
    });
    $("#funnelFoot").textContent = `${rows[0].c} → ${rows[rows.length - 1].c}`;
  }

  function fail(msg) {
    C.setRunState("done");
    $("#runDone").classList.add("on");
    $("#runDone .msg").innerHTML = `<b>Run stopped.</b> ${esc(msg)}`;
    $("#runDone a").style.display = "none";
  }

  function finish(r) {
    LIVE.result = r;
    C.setRunState("done");
    setFunnel(r.funnel, 6);
    const lab = $$("#view-run .run-col-head .label")[2];
    if (lab) lab.textContent = "sample of " + r.funnel[0].c + " breaches";
    $("#rejects").innerHTML = r.rejects
      .map(
        (x) =>
          `<div class="rej on"><div class="top"><span class="name">${esc(x.name)}</span><span class="verdict ${x.kept ? "kept" : ""}">${x.kept ? "Retained" : "Rejected"}</span></div><div class="why">${x.why}</div><div class="at">${x.at}</div></div>`,
      )
      .join("");
    const d = r.discovery;
    $("#runDone").classList.add("on");
    $$("#runDone a").forEach((el) => (el.style.display = d ? "" : "none"));
    $("#runDone .msg").innerHTML = d
      ? `<b>Discovery ready.</b> ${esc(r.company)} · ${esc(d.metric)} · strength <b>${esc(d.strength)}</b> · ${r.funnel[0].c} breaches tested · ${r.n_filings} filings in ${Math.round(r.run_seconds)}s`
      : `<b>No discovery.</b> ${esc(r.note || "")}`;
    setContext(r, false);
    if (d) {
      renderDiscovery(r);
      renderFalsification(r);
      renderDocs(r);
    }
  }

  function setContext(r, running) {
    const bar = $("#contextbar");
    bar.innerHTML = `<span class="ctx"><strong>${esc(r.company)}</strong><span class="mono small">NSE: ${esc(r.symbol)}</span></span>
      <span class="ctx">Archetype · ${esc(r.archetype_label)}</span>
      ${r.period ? `<span class="ctx mono small">${esc(r.period)}</span>` : ""}
      <span class="ctx">${r.peers.length ? r.peers.length + "-peer panel" : "peer panel"}</span>
      <span class="ctx mono small">${running ? "running" : "Live run · " + new Date().toLocaleTimeString()}</span>
      <span class="spacer"></span>
      <span class="ctx mono small">Live · computed from NSE XBRL filings</span>`;
    $$(".disclaimer").forEach((el) => {
      el.innerHTML = `<b>LIVE RUN</b><span>Computed now from ${esc(r.company)}'s and ${r.peers.length} peers' exchange XBRL filings. Every number links to its filing. Not investment advice.</span>`;
    });
    const sym = r.symbol || "KOTAKBANK";
    const repUrl = `/api/report/${encodeURIComponent(sym)}`;
    $$(".btn-report-link").forEach((a) => {
      a.href = repUrl;
    });
  }

  /* ---------------- charts ---------------- */
  const W = 400,
    H = 210,
    PL = 40,
    PR = 8,
    PT = 14,
    PB = 26;
  function frame(n, lo, hi) {
    const x = (i) => PL + (i * (W - PL - PR)) / Math.max(1, n - 1);
    const y = (v) => PT + ((hi - v) * (H - PT - PB)) / (hi - lo || 1);
    return { x, y };
  }
  function range(arrs, pad) {
    const all = [].concat(...arrs).filter((v) => v != null && isFinite(v));
    let lo = Math.min(...all),
      hi = Math.max(...all);
    const p = (hi - lo) * (pad || 0.15) || 1;
    return [lo - p, hi + p];
  }
  const fmtv = (v, kind) =>
    v == null
      ? "—"
      : kind === "growth"
        ? (v > 0 ? "+" : "") + v.toFixed(0) + "%"
        : v.toFixed(v < 10 ? 2 : 1) + "%";
  function axes(f, lo, hi, labels, kind) {
    let s = "";
    [0, 0.33, 0.66, 1].forEach((t) => {
      const v = lo + (hi - lo) * t;
      s += `<line x1="${PL}" x2="${W - PR}" y1="${f.y(v)}" y2="${f.y(v)}" stroke="#ececee"/>`;
      s += `<text x="${PL - 6}" y="${f.y(v) + 3}" text-anchor="end" font-family="JetBrains Mono" font-size="8.5" fill="#8e8e94">${fmtv(v, kind)}</text>`;
    });
    labels.forEach((l, i) => {
      if (i % 2 === (labels.length - 1) % 2)
        s += `<text x="${f.x(i)}" y="${H - 8}" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#8e8e94">${esc(l)}</text>`;
    });
    return s;
  }
  const pathOf = (vals, f) =>
    vals
      .map((v, i) =>
        v == null
          ? ""
          : `${i && vals[i - 1] != null ? "L" : "M"}${f.x(i).toFixed(1)},${f.y(v).toFixed(1)}`,
      )
      .join(" ");
  const dotsOf = (vals, f) =>
    vals
      .map((v, i) =>
        v == null
          ? ""
          : `<circle cx="${f.x(i)}" cy="${f.y(v)}" r="2.8" fill="#fff" stroke="#0a0a0b" stroke-width="1.5"/>`,
      )
      .join("");
  function chartSelf(c) {
    const [lo, hi] = range([c.values, c.band]);
    const f = frame(c.values.length, lo, hi);
    const ws = f.x(c.win_start) - 8;
    let s =
      `<rect x="${ws}" y="${PT}" width="${W - PR - ws}" height="${H - PT - PB}" fill="#f4f4f5"/>` +
      axes(f, lo, hi, c.labels, c.kind);
    s += `<rect x="${PL}" y="${f.y(c.band[1])}" width="${W - PL - PR}" height="${f.y(c.band[0]) - f.y(c.band[1])}" fill="#e6e6e8" fill-opacity=".6" stroke="#8e8e94" stroke-dasharray="3 2" stroke-width=".8"/>`;
    s += `<text x="${PL + 6}" y="${f.y(c.band[1]) - 5}" font-family="JetBrains Mono" font-size="8.5" fill="#5f5f65">expected band · own history</text>`;
    if (c.cp != null)
      s += `<line x1="${f.x(c.cp)}" x2="${f.x(c.cp)}" y1="${PT - 6}" y2="${H - PB}" stroke="#0a0a0b" stroke-dasharray="2 2"/><text x="${f.x(c.cp) + 4}" y="${PT + 2}" font-family="JetBrains Mono" font-size="8.5">change point</text>`;
    const n = c.values.length - 1;
    s += `<path d="${pathOf(c.values, f)}" fill="none" stroke="#0a0a0b" stroke-width="2"/>${dotsOf(c.values, f)}`;
    s += `<text x="${f.x(n) - 4}" y="${f.y(c.values[n]) - 8}" text-anchor="end" font-family="JetBrains Mono" font-size="9" font-weight="600">${fmtv(c.values[n], c.kind)}</text>`;
    return `<svg viewBox="0 0 ${W} ${H}">${s}</svg>`;
  }
  function chartPeer(c) {
    const [lo, hi] = range([c.values, c.median].concat(c.peers));
    const f = frame(c.values.length, lo, hi);
    const ws = f.x(c.win_start) - 8;
    let s =
      `<rect x="${ws}" y="${PT}" width="${W - PR - ws}" height="${H - PT - PB}" fill="#f4f4f5"/>` +
      axes(f, lo, hi, c.labels, c.kind);
    s += c.peers
      .map(
        (p) =>
          `<path d="${pathOf(p, f)}" fill="none" stroke="#c4c4c9" stroke-width="1"/>`,
      )
      .join("");
    s += `<path d="${pathOf(c.median, f)}" fill="none" stroke="#2e2e31" stroke-width="1.4" stroke-dasharray="5 3"/>`;
    s += `<path d="${pathOf(c.values, f)}" fill="none" stroke="#0a0a0b" stroke-width="2"/>${dotsOf(c.values, f)}`;
    s += `<rect x="${PL + 4}" y="${H - PB - 16}" width="168" height="12" fill="#fff"/><text x="${PL + 8}" y="${H - PB - 7}" font-family="JetBrains Mono" font-size="8.5" fill="#2e2e31">- - peer median — peers ━ subject</text>`;
    return `<svg viewBox="0 0 ${W} ${H}">${s}</svg>`;
  }
  function chartDriver(c) {
    const d = c.driver;
    if (!d) {
      const dist = c.values.map((v) => v - (c.band[0] + c.band[1]) / 2);
      const [lo, hi] = range([dist, [0]]);
      const f = frame(dist.length, lo, hi);
      let s = axes(f, lo, hi, c.labels, c.kind);
      dist.forEach((v, i) => {
        const y0 = f.y(0),
          y1 = f.y(v);
        s += `<rect x="${f.x(i) - 7}" y="${Math.min(y0, y1)}" width="14" height="${Math.abs(y1 - y0)}" fill="${i >= c.win_start ? "#0a0a0b" : "#c4c4c9"}"/>`;
      });
      return `<svg viewBox="0 0 ${W} ${H}">${s}</svg>`;
    }
    const arrs = [d.num].concat(d.den ? [d.den] : []);
    const [lo, hi] = range(arrs);
    const f = frame(d.num.length, lo, hi);
    let s = axes(f, lo, hi, c.labels, "index");
    if (d.den)
      s += `<path d="${pathOf(d.den, f)}" fill="none" stroke="#8e8e94" stroke-width="1.5" stroke-dasharray="5 3"/>`;
    s += `<path d="${pathOf(d.num, f)}" fill="none" stroke="#0a0a0b" stroke-width="2"/>${dotsOf(d.num, f)}`;
    s += `<rect x="${PL + 4}" y="${PT}" width="${W - PL - PR - 8}" height="12" fill="#fff"/><text x="${PL + 8}" y="${PT + 9}" font-family="JetBrains Mono" font-size="8.5" fill="#2e2e31">━ ${esc(d.num_label)}${d.den ? " · - - " + esc(d.den_label) : ""} (index, first = 100)</text>`;
    return `<svg viewBox="0 0 ${W} ${H}">${s.replace(/(\d+(\.\d+)?)%<\/text>/g, "$1</text>")}</svg>`;
  }

  /* ---------------- discovery ---------------- */
  function renderDiscovery(r) {
    const d = r.discovery,
      ch = d.charts;
    $(".disc-kicker .label").textContent =
      `01 of 1 · ${d.metric} · ${r.archetype_label} archetype`;
    $("#discSentence").innerHTML = d.sentence_html;
    $(".disc-sub").textContent = d.sub;
    $("#contract").innerHTML = [
      "Discovery",
      "Why it matters",
      "Evidence",
      "Timeline",
      "Numbers",
      "Counterargument",
      "Falsification condition",
      "Evidence strength",
    ]
      .map((c) => `<span>${c}</span>`)
      .join("");
    const lvl = { STRONG: 3, MODERATE: 2, WEAK: 1 }[d.strength] || 1;
    $(".strength-card").innerHTML =
      `<div class="top"><div><div class="label">Evidence strength</div><div class="grade">${esc(d.strength)}</div></div><div class="meter">${[0, 1, 2].map((i) => `<i class="${i < lvl ? "" : "off"}"></i>`).join("")}</div></div>` +
      d.kv
        .map(
          ([k, v]) =>
            `<div class="kv"><span class="k">${esc(k)}</span><span class="v">${esc(v)}</span></div>`,
        )
        .join("");
    $("#six").innerHTML = d.six
      .map(
        ([q, a]) =>
          `<div><div class="q">${esc(q)}</div><div class="a">${a}</div></div>`,
      )
      .join("");
    const rows = (rs) =>
      rs
        .map(
          ([k, v], i) =>
            `<div class="xrow ${i === rs.length - 1 ? "breach" : ""}"><span class="k">${esc(k)}</span><span class="v">${esc(v)}</span></div>`,
        )
        .join("");
    const drvRows = ch.driver
      ? [
          [
            `${ch.driver.num_label} (index)`,
            ch.driver.num[ch.driver.num.length - 1] == null
              ? "—"
              : ch.driver.num[ch.driver.num.length - 1].toFixed(0),
          ],
          [
            ch.driver.den ? `${ch.driver.den_label} (index)` : "Denominator",
            ch.driver.den
              ? (ch.driver.den[ch.driver.den.length - 1] || 0).toFixed(0)
              : "reported ratio",
          ],
          [
            "Denominator test (AE4)",
            (r.tests.find((t) => t[0] === "AE4") || [])[5] || "—",
          ],
        ]
      : [
          ["Distance from expected band", "per quarter"],
          ["Window quarters", "dark bars"],
          ["Persistence", d.kv[2][1]],
        ];
    $("#expectGrid").innerHTML = [
      [
        "SELF",
        "expectation 01",
        "What does its own history predict?",
        chartSelf(ch),
        rows(d.expect_rows.self),
      ],
      [
        "PEER",
        "expectation 02",
        "What do same-archetype peers show, same quarters?",
        chartPeer(ch),
        rows(d.expect_rows.peer),
      ],
      [
        "DRIVER",
        "decomposition",
        ch.driver
          ? "What moved the ratio — numerator or base?"
          : "How far outside the band, quarter by quarter?",
        chartDriver(ch),
        rows(drvRows),
      ],
    ]
      .map(
        ([n, idx, q, svg, rws]) =>
          `<div class="expect"><div class="xh"><span class="xname">${n}</span><span class="xidx">${idx}</span></div><div class="xq">${q}</div>${svg}<div class="xrows">${rws}</div></div>`,
      )
      .join("");
    const eq = $$("#equation .term .t");
    eq[0].textContent = d.equation.exp;
    eq[1].textContent = d.equation.obs;
    eq[2].textContent = d.equation.breach;
    $("#equation .term.breach .label").textContent =
      "Breach · own history and peers";
    $("#whyList").innerHTML = d.why
      .map(
        (w, i) =>
          `<li><span class="i">0${i + 1}</span><span>${esc(w)}</span></li>`,
      )
      .join("");
    $("#numbersTable").innerHTML =
      `<tr><th>Metric</th><th class="r">Value</th><th class="r">Peer median</th><th>Source</th></tr>` +
      d.numbers
        .map(
          ([m, v, p, s, ev]) =>
            `<tr><td>${esc(m)}</td><td class="r"><span class="linknum" data-ev="${ev}">${esc(v)}</span></td><td class="r mono">${esc(p)}</td><td><span class="srcref">${esc(s)}</span></td></tr>`,
        )
        .join("");
    renderTimeline(d.timeline, d.metric);
    const soft = $("#view-discovery .callout.soft");
    soft.querySelector(".label").textContent = d.counter.label;
    soft.querySelector(".t").textContent = d.counter.text;
    soft.querySelector(".s").textContent = d.counter.sub;
    $("#falsCond1").textContent = d.falsification;
    $("#falsCond1").parentElement.querySelector(".s").textContent =
      d.falsification_sub;
    $("#falsCond1").parentElement.querySelector(".label").textContent =
      "Computed from the expected band · monitored each quarter";
    $("#families").innerHTML = d.families
      .map(
        (f) =>
          `<div class="family ${f.excluded ? "excluded" : ""}"><div class="fn">${esc(f.fn)}</div><div class="fd">${esc(f.fd)}</div><div class="fc">${esc(f.fc)}</div></div>`,
      )
      .join("");
  }

  function renderTimeline(t, metric) {
    const n = t.labels.length;
    let g = `<div class="tl-grid" style="grid-template-columns:150px repeat(${n},1fr)">`;
    const cell = (cls, html) =>
      `<div class="tl-cell ${cls}" style="border-right:1px solid var(--rule)">${html}</div>`;
    g +=
      cell("tl-head", "Lane") +
      t.labels
        .map((l, i) => cell("tl-head" + (t.outside[i] ? " win" : ""), esc(l)))
        .join("");
    g +=
      cell("tl-lane", `Company<small>${esc(metric)}</small>`) +
      t.values
        .map((v, i) =>
          cell(
            t.outside[i] ? "win" : "",
            `<div class="tl-val ${t.outside[i] ? "up" : ""}">${esc(v)}</div>${t.outside[i] ? '<div class="tl-mark" style="color:#8e8e94">outside band</div>' : ""}`,
          ),
        )
        .join("");
    g +=
      cell("tl-lane", "Peer median<small>same quarter</small>") +
      t.peer
        .map((v, i) =>
          cell(
            t.outside[i] ? "win" : "",
            `<div class="tl-val">${esc(v)}</div>${t.peer_out[i] ? '<div class="tl-mark" style="color:#8e8e94">subject outside IQR</div>' : ""}`,
          ),
        )
        .join("");
    g +=
      cell("tl-lane", "Filing date<small>knowledge time</small>") +
      t.filed
        .map((v, i) =>
          cell(
            t.outside[i] ? "win" : "",
            `<div class="tl-val" style="color:#5f5f65">${esc(v)}</div>`,
          ),
        )
        .join("");
    g +=
      cell("tl-lane", "Sector events<small>RBI calendar</small>") +
      t.events
        .map((v, i) =>
          cell(
            t.outside[i] ? "win" : "",
            v
              ? `<span class="tl-ev">RBI</span><div class="tl-mark">${esc(v)}</div>`
              : "",
          ),
        )
        .join("");
    g += `</div>`;
    const pos = (lbl) => {
      const i = t.labels.indexOf(lbl);
      return i < 0 ? null : ((i + 0.5) / n) * 100;
    };
    const a = pos(t.cp),
      b = pos(t.first_detect),
      c = pos(t.last);
    let track = "";
    if (a != null && c != null) {
      track += `<div class="gap-line" style="left:${a}%;right:${100 - c}%"></div>`;
      track += `<div class="gap-pt" style="left:${a}%"><div class="gt">NUMBERS<br>CHANGE</div><div class="gm"></div><div class="gs">${esc(t.cp)}</div></div>`;
      if (b != null && b !== a && b !== c)
        track += `<div class="gap-pt sys" style="left:${b}%"><div class="gt">FIRST DETECTABLE<br>IN FILINGS</div><div class="gm"></div><div class="gs">filed ${esc(t.detect_filed)}</div></div>`;
      track += `<div class="gap-pt" style="left:${c}%"><div class="gt">LATEST<br>FILING</div><div class="gm"></div><div class="gs">${esc(t.last)}</div></div>`;
      track += `<div class="gap-label" style="left:${(a + c) / 2}%;top:84px">KNOWLEDGE TIME · when each quarter's numbers became public</div>`;
    }
    g += `<div class="gap-row"><div class="tl-lane">Visibility<small>knowledge time</small></div><div class="gap-track">${track}</div></div>`;
    $("#timeline").innerHTML = g;
  }

  /* ---------------- falsification ---------------- */
  function renderFalsification(r) {
    const pill = (v) =>
      ({
        pass: '<span class="pill pass">PASS</span>',
        partial: '<span class="pill partial">PARTIAL</span>',
        fail: '<span class="pill fail">FAIL</span>',
        "n/a": '<span class="pill pending">N/A</span>',
      })[v] || '<span class="pill pending">NOT RUN</span>';
    $("#squares").innerHTML = r.tests
      .map(
        (t) =>
          `<i class="${t[5] === "partial" ? "partial" : ""}" style="${t[5] === "pass" ? "" : t[5] === "partial" ? "" : "background:#e6e6e8"}"></i>`,
      )
      .join("");
    $(".survived .big").innerHTML =
      `PASSED ${r.survived.pass} <small>/ ${r.survived.run} RUN</small>`;
    $(".survived .note").textContent =
      r.survived.note +
      ". AE6 and AE9 are not in this build and are shown as not run.";
    $(".prereg").innerHTML =
      `<span>Gates fixed in code before the run</span><span>Executed ${new Date().toLocaleTimeString()}</span><span>${esc(r.discovery.metric)} · 9 tests · ${r.survived.run} run</span>`;
    $("#testsTable").innerHTML =
      `<tr><th>ID</th><th>Test</th><th>Alternative explanation</th><th>Procedure (code)</th><th>Result</th><th style="text-align:right">Verdict</th></tr>` +
      r.tests
        .map(
          ([id, n, a, p, res, v]) =>
            `<tr><td class="id">${id}</td><td class="name">${esc(n)}</td><td class="alt">${esc(a)}</td><td class="proc">${esc(p)}</td><td class="res">${esc(res)}</td><td class="verdict">${pill(v)}</td></tr>`,
        )
        .join("");
    const ae8 = r.tests.find((t) => t[0] === "AE8");
    $("#corollaries").innerHTML = ae8
      ? `<div class="co"><span class="p">If the breach is real and ${ae8[5] === "n/a" ? "material" : "material"}, profitability should diverge from peers in the same direction.</span><span class="r">${esc(ae8[4])}</span><span style="text-align:right">${pill(ae8[5])}</span></div>`
      : "";
    $("#falsCond2").textContent = r.discovery.falsification;
    $("#falsCond2").parentElement.querySelector(".s").textContent =
      r.discovery.falsification_sub;
    const rules = [
      [
        "STRONG",
        [
          "No test failed · at most one partial",
          "Outside own band ≥3 of 4 quarters",
          "Outside peer IQR ≥3 of 4 quarters",
          "Numbers reconcile (AE7 pass)",
        ],
      ],
      [
        "MODERATE",
        [
          "No test failed · at most two partial",
          "Persistence ≥2 of 4 quarters",
        ],
      ],
      [
        "WEAK",
        [
          "Anything else — reported only as the best available candidate, clearly labelled",
        ],
      ],
    ];
    $("#strengthRules").innerHTML = rules
      .map(
        ([g, cs]) =>
          `<div class="srule ${g === r.discovery.strength ? "active" : ""}"><div class="sh"><span class="g">${g}</span><span class="label" style="color:inherit">${g === r.discovery.strength ? "assigned" : ""}</span></div>${cs.map((c) => `<div class="crit"><span class="c">${g === r.discovery.strength ? "✓" : "·"}</span><span>${esc(c)}</span></div>`).join("")}</div>`,
      )
      .join("");
  }

  /* ---------------- evidence ---------------- */
  LIVE.renderEvidence = function (id) {
    const ev = LIVE.result.evidence;
    if (!ev) return;
    const cur = ev.items[id] ? id : ev.order[0];
    const e = ev.items[cur];
    $("#evList").innerHTML = ev.order
      .map(
        (k) =>
          `<button class="ev-item ${k === cur ? "active" : ""}" data-ev="${k}"><div class="v">${esc(ev.items[k].v)}</div><div class="k">${esc(ev.items[k].k)}</div><div class="tag">${esc(ev.items[k].tag)}</div></button>`,
      )
      .join("");
    const formula =
      e.formula
        .map(
          ([op, t]) => `<div><span class="op">${esc(op)}</span>${esc(t)}</div>`,
        )
        .join("") +
      `<div><span class="op"></span><span class="res">${esc(e.res)}</span></div>`;
    const link = e.url
      ? `<a class="btn-ghost" style="padding:5px 10px;font-size:10px" href="${esc(e.url)}" target="_blank" rel="noopener">Open filing ↗</a>`
      : "";
    $("#chain").innerHTML = `
      <div class="chain-step"><div class="lab" data-n="01">Derived value</div><div><div class="derived-v">${esc(e.v)}</div><div class="derived-k">${esc(e.k)}</div></div></div>
      <div class="chain-step"><div class="lab" data-n="02">Formula</div><div class="formula">${formula}</div></div>
      <div class="chain-step"><div class="lab" data-n="03">Input check</div><div><span class="recon">${esc(e.check)}</span><div class="srcref" style="margin-top:8px">Inputs are tagged XBRL facts with value, period and context. The language model never types a number.</div></div></div>
      <div class="chain-step"><div class="lab" data-n="04">Source document</div><div class="doc"><div><div class="dn">${esc(e.doc)}</div><div class="dm">${esc(e.dm)}${e.url ? "<br>" + esc(e.url) : ""}</div></div>${link}</div></div>
      <div class="chain-step" style="border-bottom:0"><div class="lab" data-n="05">Tagged facts</div><div><div class="page-mock"><div class="ph"><span>${esc(e.passage.title)}</span><span>exchange XBRL</span></div><table>${e.passage.rows.map(([k, v, hl]) => `<tr class="${hl ? "hl" : ""}"><td style="font-family:var(--mono);font-size:11px">${esc(k)}</td><td class="r">${esc(v)}</td></tr>`).join("")}</table></div><div class="page-cap">Values exactly as filed with the exchange</div></div></div>`;
  };

  function renderDocs(r) {
    $("#docsTable").innerHTML =
      `<tr><th>Document</th><th>Publisher</th><th>Family</th><th>Tier</th><th>Period</th><th class="r">Scope</th></tr>` +
      r.docs
        .map(
          (d) =>
            `<tr><td>${esc(d[0])}</td><td>${esc(d[1])}</td><td>${esc(d[2])}</td><td class="mono">${esc(d[3])}</td><td class="mono">${esc(d[4])}</td><td class="r mono">${esc(d[5])}</td></tr>`,
        )
        .join("") +
      r.filings
        .slice()
        .reverse()
        .map(
          (f) =>
            `<tr><td colspan="4" style="color:var(--ink-3)">↳ ${esc(r.company)} · ${esc(f.label)} · filed ${esc(f.filed)}</td><td colspan="2" class="r"><a class="srcref" href="${esc(f.url)}" target="_blank" rel="noopener" style="text-decoration:underline">open XBRL ↗</a></td></tr>`,
        )
        .join("");
  }
})();
