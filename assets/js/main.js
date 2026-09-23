// ChronAeon Benchmark Compendium - Portal Interactive Scripts

document.addEventListener("DOMContentLoaded", () => {
  initLightbox();
  initCopyButtons();
  initTableFilters();
  initConcordancePlot();
  initAutoClockExplorer();
});

// Lightbox Modal for Figures
function initLightbox() {
  const modal = document.getElementById("lightbox-modal");
  if (!modal) return;
  const modalImg = document.getElementById("lightbox-img");
  const modalCaption = document.getElementById("lightbox-caption");
  const closeBtn = document.getElementById("lightbox-close");

  document.querySelectorAll(".figure-wrapper").forEach((el) => {
    el.addEventListener("click", () => {
      const img = el.querySelector("img");
      if (!img) return;
      modalImg.src = img.src;
      modalCaption.textContent = img.alt || "";
      modal.classList.add("active");
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal || e.target === modalImg) {
      modal.classList.remove("active");
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      modal.classList.remove("active");
    }
  });
}

// Copy Code Button
function initCopyButtons() {
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const codeId = btn.getAttribute("data-target");
      const codeEl = document.getElementById(codeId);
      if (!codeEl) return;
      const text = codeEl.innerText || codeEl.textContent;
      navigator.clipboard.writeText(text).then(() => {
        const orig = btn.textContent;
        btn.textContent = "Copied!";
        btn.style.color = "#10b981";
        setTimeout(() => {
          btn.textContent = orig;
          btn.style.color = "";
        }, 2000);
      });
    });
  });
}

// Table Filtering and Search on Portal Index
function initTableFilters() {
  const searchInput = document.getElementById("study-search");
  const table = document.getElementById("benchmarks-table");
  const taxonomyButtons = document.querySelectorAll(".filter-btn[data-taxonomy]");
  const clockButtons = document.querySelectorAll(".filter-btn[data-clock]");
  const concordanceButtons = document.querySelectorAll(".filter-btn[data-concordance]");
  const countDisplay = document.getElementById("filter-count");

  if (!table) return;

  let activeTaxonomy = "all";
  let activeClock = "all";
  let activeConcordance = "all";
  let searchQuery = "";

  function filterRows() {
    const rows = table.querySelectorAll("tbody tr");
    let visibleCount = 0;

    rows.forEach((row) => {
      const rowTaxonomy = row.getAttribute("data-taxonomy") || "";
      const rowClock = row.getAttribute("data-clock") || "";
      const rowConcordance = row.getAttribute("data-concordance") || "";
      const rowText = row.textContent.toLowerCase();

      const matchTaxonomy = (activeTaxonomy === "all" || rowTaxonomy === activeTaxonomy);
      const matchClock = (activeClock === "all" || rowClock === activeClock);
      const matchConcordance = (activeConcordance === "all" || rowConcordance === activeConcordance);
      const matchSearch = (!searchQuery || rowText.includes(searchQuery));

      if (matchTaxonomy && matchClock && matchConcordance && matchSearch) {
        row.style.display = "";
        visibleCount++;
      } else {
        row.style.display = "none";
      }
    });

    if (countDisplay) {
      countDisplay.textContent = `${visibleCount} of ${rows.length} studies shown`;
    }
  }

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      filterRows();
    });
  }

  taxonomyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      taxonomyButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeTaxonomy = btn.getAttribute("data-taxonomy");
      filterRows();
    });
  });

  clockButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      clockButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeClock = btn.getAttribute("data-clock");
      filterRows();
    });
  });

  concordanceButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      concordanceButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeConcordance = btn.getAttribute("data-concordance");
      filterRows();
    });
  });

  // Stop propagation on table links so clicking links doesn't trigger row navigation
  if (table) {
    table.querySelectorAll("tbody a").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.stopPropagation();
      });
    });
  }

}

// Interactive SVG Concordance Scatter Plot
function initConcordancePlot() {
  const container = document.getElementById("concordance-plot-container");
  if (!container || typeof BENCHMARK_DATA === "undefined") return;

  container.innerHTML = "";

  const plotData = BENCHMARK_DATA.filter((d) => {
    const b = parseFloat(d.beast_tmrca.replace(/,/g, ''));
    const c = parseFloat(d.chronaeon_tmrca.replace(/,/g, ''));
    return !isNaN(b) && !isNaN(c) && b > 1850 && b < 2030 && c > 1800 && c < 2030;
  });

  const width = 840;
  const height = 480;
  const margin = { top: 30, right: 40, bottom: 55, left: 70 };

  const minYear = 1860;
  const maxYear = 2028;

  function scaleX(val) {
    return margin.left + ((val - minYear) / (maxYear - minYear)) * (width - margin.left - margin.right);
  }

  function scaleY(val) {
    return height - margin.bottom - ((val - minYear) / (maxYear - minYear)) * (height - margin.top - margin.bottom);
  }

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.style.width = "100%";
  svg.style.height = "auto";
  svg.style.display = "block";

  // Grid lines
  const gridGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  for (let yr = 1880; yr <= 2020; yr += 20) {
    const x = scaleX(yr);
    const y = scaleY(yr);

    const vLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vLine.setAttribute("x1", x);
    vLine.setAttribute("x2", x);
    vLine.setAttribute("y1", margin.top);
    vLine.setAttribute("y2", height - margin.bottom);
    vLine.setAttribute("stroke", "#e2e8f0");
    vLine.setAttribute("stroke-dasharray", "3,3");
    gridGroup.appendChild(vLine);

    const hLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    hLine.setAttribute("x1", margin.left);
    hLine.setAttribute("x2", width - margin.right);
    hLine.setAttribute("y1", y);
    hLine.setAttribute("y2", y);
    hLine.setAttribute("stroke", "#e2e8f0");
    hLine.setAttribute("stroke-dasharray", "3,3");
    gridGroup.appendChild(hLine);

    const xText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    xText.setAttribute("x", x);
    xText.setAttribute("y", height - margin.bottom + 20);
    xText.setAttribute("text-anchor", "middle");
    xText.setAttribute("font-size", "11");
    xText.setAttribute("fill", "#64748b");
    xText.textContent = yr;
    gridGroup.appendChild(xText);

    const yText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    yText.setAttribute("x", margin.left - 12);
    yText.setAttribute("y", y + 4);
    yText.setAttribute("text-anchor", "end");
    yText.setAttribute("font-size", "11");
    yText.setAttribute("fill", "#64748b");
    yText.textContent = yr;
    gridGroup.appendChild(yText);
  }
  svg.appendChild(gridGroup);

  // Identity Line (y = x)
  const identityLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
  identityLine.setAttribute("x1", scaleX(minYear));
  identityLine.setAttribute("y1", scaleY(minYear));
  identityLine.setAttribute("x2", scaleX(maxYear));
  identityLine.setAttribute("y2", scaleY(maxYear));
  identityLine.setAttribute("stroke", "#94a3b8");
  identityLine.setAttribute("stroke-width", "1.5");
  identityLine.setAttribute("stroke-dasharray", "5,5");
  svg.appendChild(identityLine);

  // Axis Titles
  const xTitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
  xTitle.setAttribute("x", margin.left + (width - margin.left - margin.right) / 2);
  xTitle.setAttribute("y", height - 12);
  xTitle.setAttribute("text-anchor", "middle");
  xTitle.setAttribute("font-size", "12");
  xTitle.setAttribute("font-weight", "600");
  xTitle.setAttribute("fill", "#334155");
  xTitle.textContent = "Published BEAST Point Estimate t_MRCA (CE)";
  svg.appendChild(xTitle);

  const yTitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
  yTitle.setAttribute("transform", `rotate(-90)`);
  yTitle.setAttribute("x", -(margin.top + (height - margin.top - margin.bottom) / 2));
  yTitle.setAttribute("y", 22);
  yTitle.setAttribute("text-anchor", "middle");
  yTitle.setAttribute("font-size", "12");
  yTitle.setAttribute("font-weight", "600");
  yTitle.setAttribute("fill", "#334155");
  yTitle.textContent = "ChronAeon Inferred Point Estimate t_MRCA (CE)";
  svg.appendChild(yTitle);

  // Tooltip Div
  let tooltip = document.getElementById("plot-tooltip");
  if (!tooltip) {
    tooltip = document.createElement("div");
    tooltip.id = "plot-tooltip";
    tooltip.style.position = "absolute";
    tooltip.style.padding = "8px 12px";
    tooltip.style.background = "#0f172a";
    tooltip.style.color = "#ffffff";
    tooltip.style.borderRadius = "6px";
    tooltip.style.fontSize = "0.78rem";
    tooltip.style.pointerEvents = "none";
    tooltip.style.display = "none";
    tooltip.style.zIndex = "100";
    tooltip.style.boxShadow = "0 4px 6px -1px rgba(0, 0, 0, 0.2)";
    document.body.appendChild(tooltip);
  }

  // Data Points
  plotData.forEach((d) => {
    const b = parseFloat(d.beast_tmrca.replace(/,/g, ''));
    const c = parseFloat(d.chronaeon_tmrca.replace(/,/g, ''));

    const cx = scaleX(b);
    const cy = scaleY(c);

    let fillColor = "#2563eb";
    if (d.concordance === "NON-LINEAR") fillColor = "#059669";
    else if (d.concordance === "STEM-VS-CROWN") fillColor = "#d97706";
    else if (d.concordance === "DECONVOLUTED") fillColor = "#7c3aed";

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", cx);
    circle.setAttribute("cy", cy);
    circle.setAttribute("r", "6");
    circle.setAttribute("fill", fillColor);
    circle.setAttribute("stroke", "#ffffff");
    circle.setAttribute("stroke-width", "1.5");
    circle.style.cursor = "pointer";
    circle.style.transition = "r 0.15s ease, fill 0.15s ease";

    circle.addEventListener("mouseenter", (e) => {
      circle.setAttribute("r", "9");
      tooltip.innerHTML = `
        <div style="font-weight: 700; margin-bottom: 2px;">${d.pathogen}</div>
        <div style="color: #94a3b8; font-size: 0.72rem; margin-bottom: 4px;">${d.taxonomy} &bull; Model: ${d.active_model}</div>
        <div>BEAST: <strong>${d.beast_tmrca}</strong> (${d.mcmc_states})</div>
        <div>ChronAeon: <strong>${d.chronaeon_tmrca}</strong> (${d.sec}s)</div>
        <div style="margin-top: 4px; font-size: 0.7rem; color: #38bdf8;">Click to inspect dossier &rarr;</div>
      `;
      tooltip.style.display = "block";
    });

    circle.addEventListener("mousemove", (e) => {
      tooltip.style.left = e.pageX + 15 + "px";
      tooltip.style.top = e.pageY - 30 + "px";
    });

    circle.addEventListener("mouseleave", () => {
      circle.setAttribute("r", "6");
      tooltip.style.display = "none";
    });

    circle.addEventListener("click", () => {
      window.location.href = `studies/${d.study_id}/index.html`;
    });

    svg.appendChild(circle);
  });

  container.appendChild(svg);
}























// AutoClock Multi-Rate Interactive Visualizer
function initAutoClockExplorer() {
  document.querySelectorAll(".autoclock-explorer").forEach((container) => {
    const scriptEl = container.querySelector(".autoclock-data");
    if (!scriptEl) return;
    let data;
    try {
      data = JSON.parse(scriptEl.textContent);
    } catch (e) {
      console.error("Failed to parse autoclock data", e);
      return;
    }
    renderAutoClockExplorer(container, data);
  });
}

function renderAutoClockExplorer(container, data) {
  const svg = container.querySelector(".autoclock-svg");
  const tooltip = container.querySelector(".autoclock-tooltip");
  const detailEl = container.querySelector(".autoclock-detail-card");
  const controlsEl = container.querySelector(".autoclock-controls");
  if (!svg || !data || !data.comms || data.comms.length === 0) return;

  let activeCommId = "all";

  // Build controls pills
  if (controlsEl && controlsEl.children.length === 0) {
    const allBtn = document.createElement("button");
    allBtn.className = "autoclock-pill active";
    allBtn.setAttribute("data-comm", "all");
    allBtn.innerHTML = `All Communities (K*=${data.k_star})`;
    allBtn.addEventListener("click", () => selectCommunity("all"));
    controlsEl.appendChild(allBtn);

    data.comms.forEach((c) => {
      const btn = document.createElement("button");
      btn.className = "autoclock-pill";
      btn.setAttribute("data-comm", c.id);
      const rateText = c.mu >= 1e-3 ? `${(c.mu * 1000).toFixed(2)}e-3` : c.mu.toExponential(2);
      btn.innerHTML = `<span class="autoclock-dot" style="background:${c.color};"></span>Comm ${c.id}: &mu;=${rateText} (N=${c.n})`;
      btn.addEventListener("click", () => selectCommunity(c.id));
      controlsEl.appendChild(btn);
    });
  }

  function selectCommunity(id) {
    activeCommId = id;
    container.querySelectorAll(".autoclock-pill").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-comm") === String(id));
    });
    updateChartVisuals();
    updateDetailCard();
  }

  // Draw SVG
  const W = 920;
  const H = 370;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.innerHTML = "";

  // Left Panel (Time vs Divergence)
  const pL = { x: 65, y: 35, w: 525, h: 285 };
  // Right Panel (Rate Bar Comparator)
  const pR = { x: 660, y: 35, w: 235, h: 285 };

  // Collect data range for Left Panel
  let allDates = [];
  let allDists = [];
  data.comms.forEach((c) => {
    if (c.pts) {
      c.pts.forEach((p) => {
        allDates.push(p.t);
        allDists.push(p.d);
      });
    }
  });

  if (allDates.length === 0) return;

  const minObsDate = Math.min(...allDates);
  const maxObsDate = Math.max(...allDates);
  const obsSpan = maxObsDate - minObsDate || 1.0;

  const mrcaDates = data.comms.map((c) => c.t_mrca).filter((t) => t != null && !isNaN(t));
  const earliestMrca = mrcaDates.length > 0 ? Math.min(...mrcaDates) : minObsDate;

  let xDomainMin, xDomainMax;
  if (earliestMrca >= minObsDate - 2.5 * obsSpan) {
    xDomainMin = Math.min(earliestMrca - 0.05 * obsSpan, minObsDate - 0.1 * obsSpan);
  } else {
    xDomainMin = minObsDate - 0.4 * obsSpan;
  }
  xDomainMax = maxObsDate + 0.06 * (maxObsDate - xDomainMin);

  const maxObsDist = Math.max(...allDists, 1e-4);
  const yDomainMin = 0;
  const yDomainMax = maxObsDist * 1.15;

  function sx(t) {
    return pL.x + ((t - xDomainMin) / (xDomainMax - xDomainMin)) * pL.w;
  }
  function sy(d) {
    return pL.y + pL.h - ((d - yDomainMin) / (yDomainMax - yDomainMin)) * pL.h;
  }

  // Defs: clipPath for Left Panel
  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  const clip = document.createElementNS("http://www.w3.org/2000/svg", "clipPath");
  const clipId = `clip-${Math.random().toString(36).substr(2, 9)}`;
  clip.id = clipId;
  const clipRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  clipRect.setAttribute("x", pL.x);
  clipRect.setAttribute("y", pL.y);
  clipRect.setAttribute("width", pL.w);
  clipRect.setAttribute("height", pL.h);
  clip.appendChild(clipRect);
  defs.appendChild(clip);
  svg.appendChild(defs);

  // Left Panel Background
  const bgL = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  bgL.setAttribute("x", pL.x);
  bgL.setAttribute("y", pL.y);
  bgL.setAttribute("width", pL.w);
  bgL.setAttribute("height", pL.h);
  bgL.setAttribute("fill", "#fafafa");
  bgL.setAttribute("stroke", "#e2e8f0");
  bgL.setAttribute("rx", "4");
  svg.appendChild(bgL);

  // Left Panel Title
  const titleL = document.createElementNS("http://www.w3.org/2000/svg", "text");
  titleL.setAttribute("x", pL.x);
  titleL.setAttribute("y", pL.y - 12);
  titleL.setAttribute("font-size", "12");
  titleL.setAttribute("font-weight", "700");
  titleL.setAttribute("fill", "#1e293b");
  titleL.textContent = "A. Lineage Molecular Clock Trajectories & Root Anchors";
  svg.appendChild(titleL);

  // Grid & Axes for Left Panel
  const gridGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  for (let i = 0; i <= 4; i++) {
    const frac = i / 4;
    const tVal = xDomainMin + frac * (xDomainMax - xDomainMin);
    const xPos = sx(tVal);
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", xPos);
    line.setAttribute("x2", xPos);
    line.setAttribute("y1", pL.y);
    line.setAttribute("y2", pL.y + pL.h);
    line.setAttribute("stroke", "#e2e8f0");
    line.setAttribute("stroke-dasharray", "3,3");
    gridGroup.appendChild(line);

    const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
    txt.setAttribute("x", xPos);
    txt.setAttribute("y", pL.y + pL.h + 16);
    txt.setAttribute("text-anchor", "middle");
    txt.setAttribute("font-size", "10");
    txt.setAttribute("fill", "#64748b");
    txt.textContent = tVal < 0 ? `${Math.abs(Math.round(tVal))} BCE` : (obsSpan < 5 ? tVal.toFixed(2) : Math.round(tVal));
    gridGroup.appendChild(txt);
  }

  for (let i = 0; i <= 3; i++) {
    const frac = i / 3;
    const dVal = yDomainMin + frac * (yDomainMax - yDomainMin);
    const yPos = sy(dVal);
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", pL.x);
    line.setAttribute("x2", pL.x + pL.w);
    line.setAttribute("y1", yPos);
    line.setAttribute("y2", yPos);
    line.setAttribute("stroke", "#e2e8f0");
    line.setAttribute("stroke-dasharray", "3,3");
    gridGroup.appendChild(line);

    const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
    txt.setAttribute("x", pL.x - 8);
    txt.setAttribute("y", yPos + 3);
    txt.setAttribute("text-anchor", "end");
    txt.setAttribute("font-size", "10");
    txt.setAttribute("fill", "#64748b");
    txt.textContent = dVal.toExponential(1);
    gridGroup.appendChild(txt);
  }
  svg.appendChild(gridGroup);

  // Left Panel Axis Labels
  const xLabelL = document.createElementNS("http://www.w3.org/2000/svg", "text");
  xLabelL.setAttribute("x", pL.x + pL.w / 2);
  xLabelL.setAttribute("y", pL.y + pL.h + 34);
  xLabelL.setAttribute("text-anchor", "middle");
  xLabelL.setAttribute("font-size", "11");
  xLabelL.setAttribute("font-weight", "600");
  xLabelL.setAttribute("fill", "#475569");
  xLabelL.textContent = "Calendar Date (Years CE)";
  svg.appendChild(xLabelL);

  const yLabelL = document.createElementNS("http://www.w3.org/2000/svg", "text");
  yLabelL.setAttribute("transform", "rotate(-90)");
  yLabelL.setAttribute("x", -(pL.y + pL.h / 2));
  yLabelL.setAttribute("y", 18);
  yLabelL.setAttribute("text-anchor", "middle");
  yLabelL.setAttribute("font-size", "11");
  yLabelL.setAttribute("font-weight", "600");
  yLabelL.setAttribute("fill", "#475569");
  yLabelL.textContent = "Root Divergence (subs / site)";
  svg.appendChild(yLabelL);

  // Clipped Trajectories Group
  const trajGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  trajGroup.setAttribute("clip-path", `url(#${clipId})`);

  // Global reference line
  if (data.g_mu && data.g_mu > 0 && data.g_tmrca != null) {
    const t0 = Math.max(xDomainMin, data.g_tmrca);
    const d0 = Math.max(0, data.g_mu * (t0 - data.g_tmrca));
    const t1 = xDomainMax;
    const d1 = Math.max(0, data.g_mu * (t1 - data.g_tmrca));

    const gLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    gLine.setAttribute("x1", sx(t0));
    gLine.setAttribute("y1", sy(d0));
    gLine.setAttribute("x2", sx(t1));
    gLine.setAttribute("y2", sy(d1));
    gLine.setAttribute("stroke", "#94a3b8");
    gLine.setAttribute("stroke-width", "1.6");
    gLine.setAttribute("stroke-dasharray", "5,4");
    gLine.setAttribute("opacity", "0.75");
    trajGroup.appendChild(gLine);
  }

  const linesByComm = {};
  const pointsByComm = {};

  data.comms.forEach((c) => {
    linesByComm[c.id] = [];
    pointsByComm[c.id] = [];

    if (c.mu && c.t_mrca != null && c.pts && c.pts.length > 0) {
      const maxPtDate = Math.max(...c.pts.map((p) => p.t));
      const tStart = Math.max(xDomainMin, c.t_mrca);
      const dStart = Math.max(0, c.mu * (tStart - c.t_mrca));
      const tEnd = maxPtDate + 0.02 * (maxPtDate - tStart);
      const dEnd = Math.max(0, c.mu * (tEnd - c.t_mrca));

      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", sx(tStart));
      line.setAttribute("y1", sy(dStart));
      line.setAttribute("x2", sx(tEnd));
      line.setAttribute("y2", sy(dEnd));
      line.setAttribute("stroke", c.color);
      line.setAttribute("stroke-width", "2.8");
      line.setAttribute("class", `comm-line comm-line-${c.id}`);
      line.style.transition = "opacity 0.2s ease, stroke-width 0.2s ease";
      trajGroup.appendChild(line);
      linesByComm[c.id].push(line);

      if (c.t_mrca >= xDomainMin && c.t_mrca <= xDomainMax) {
        if (c.ci && c.ci.length === 2 && !isNaN(c.ci[0]) && !isNaN(c.ci[1])) {
          const ciX0 = Math.max(sx(c.ci[0]), pL.x);
          const ciX1 = Math.min(sx(c.ci[1]), pL.x + pL.w);
          if (ciX1 >= ciX0) {
            const ciLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
            ciLine.setAttribute("x1", ciX0);
            ciLine.setAttribute("x2", ciX1);
            ciLine.setAttribute("y1", sy(0));
            ciLine.setAttribute("y2", sy(0));
            ciLine.setAttribute("stroke", c.color);
            ciLine.setAttribute("stroke-width", "3.0");
            ciLine.setAttribute("opacity", "0.5");
            ciLine.setAttribute("class", `comm-ci comm-ci-${c.id}`);
            trajGroup.appendChild(ciLine);
            linesByComm[c.id].push(ciLine);
          }
        }

        const rootDot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        rootDot.setAttribute("cx", sx(c.t_mrca));
        rootDot.setAttribute("cy", sy(0));
        rootDot.setAttribute("r", "5");
        rootDot.setAttribute("fill", c.color);
        rootDot.setAttribute("stroke", "#ffffff");
        rootDot.setAttribute("stroke-width", "1.5");
        rootDot.setAttribute("class", `comm-root comm-root-${c.id}`);
        rootDot.style.cursor = "pointer";
        rootDot.addEventListener("mouseenter", (e) => {
          showTooltip(e, `
            <strong>Community ${c.id} Inferred Root</strong><br/>
            t_MRCA: <strong>${c.t_mrca < 0 ? `${Math.abs(c.t_mrca).toFixed(1)} BCE` : `${c.t_mrca.toFixed(2)} CE`}</strong><br/>
            95% Fieller CI: [${c.ci[0]}, ${c.ci[1]}]<br/>
            Rate &mu;: <strong>${c.mu.toExponential(3)}</strong> subs/site/yr<br/>
            Taxa: ${c.n} sequences
          `);
        });
        rootDot.addEventListener("mouseleave", hideTooltip);
        trajGroup.appendChild(rootDot);
        linesByComm[c.id].push(rootDot);
      }
    }

    if (c.pts) {
      c.pts.forEach((pt) => {
        const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        dot.setAttribute("cx", sx(pt.t));
        dot.setAttribute("cy", sy(pt.d));
        dot.setAttribute("r", pt.o ? "4.5" : "3.5");
        dot.setAttribute("fill", pt.o ? "#ef4444" : c.color);
        dot.setAttribute("stroke", "#ffffff");
        dot.setAttribute("stroke-width", "1.0");
        dot.setAttribute("opacity", "0.75");
        dot.setAttribute("class", `comm-pt comm-pt-${c.id}`);
        dot.style.cursor = "pointer";
        dot.style.transition = "opacity 0.2s ease, r 0.15s ease";

        dot.addEventListener("mouseenter", (e) => {
          dot.setAttribute("r", "6");
          dot.setAttribute("opacity", "1.0");
          showTooltip(e, `
            <strong>Community ${c.id} Sequence</strong><br/>
            Sample Date: <strong>${pt.t < 0 ? `${Math.abs(pt.t).toFixed(1)} BCE` : `${pt.t.toFixed(3)} CE`}</strong><br/>
            Divergence: <strong>${pt.d.toExponential(3)}</strong> subs/site<br/>
            Community Rate: ${c.mu.toExponential(2)} subs/site/yr<br/>
            ${pt.o ? '<span style="color:#f87171;font-weight:bold;">Flagged Outlier (|Z| &ge; 2.5)</span>' : 'Temporal Consensus Pass'}
          `);
        });
        dot.addEventListener("mouseleave", () => {
          dot.setAttribute("r", pt.o ? "4.5" : "3.5");
          updateChartVisuals();
          hideTooltip();
        });
        trajGroup.appendChild(dot);
        pointsByComm[c.id].push(dot);
      });
    }
  });

  svg.appendChild(trajGroup);

  // Right Panel: Within-Lineage Rate Bar Comparator
  const bgR = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  bgR.setAttribute("x", pR.x);
  bgR.setAttribute("y", pR.y);
  bgR.setAttribute("width", pR.w);
  bgR.setAttribute("height", pR.h);
  bgR.setAttribute("fill", "#fafafa");
  bgR.setAttribute("stroke", "#e2e8f0");
  bgR.setAttribute("rx", "4");
  svg.appendChild(bgR);

  const titleR = document.createElementNS("http://www.w3.org/2000/svg", "text");
  titleR.setAttribute("x", pR.x);
  titleR.setAttribute("y", pR.y - 12);
  titleR.setAttribute("font-size", "12");
  titleR.setAttribute("font-weight", "700");
  titleR.setAttribute("fill", "#1e293b");
  titleR.textContent = "B. Within-Lineage Rate Comparison (\u03bc_k)";
  svg.appendChild(titleR);

  const allMus = data.comms.map((c) => c.mu).concat(data.g_mu && data.g_mu > 0 ? [data.g_mu] : []);
  const maxMu = Math.max(...allMus, 1e-5) * 1.25;
  const barLeftX = pR.x + 80;
  const barAvailW = pR.w - 125;

  function sBarW(mu) {
    return Math.max(2, (mu / maxMu) * barAvailW);
  }

  if (data.g_mu && data.g_mu > 0) {
    const gBarX = barLeftX + sBarW(data.g_mu);
    const gLineR = document.createElementNS("http://www.w3.org/2000/svg", "line");
    gLineR.setAttribute("x1", gBarX);
    gLineR.setAttribute("x2", gBarX);
    gLineR.setAttribute("y1", pR.y + 10);
    gLineR.setAttribute("y2", pR.y + pR.h - 25);
    gLineR.setAttribute("stroke", "#94a3b8");
    gLineR.setAttribute("stroke-width", "1.5");
    gLineR.setAttribute("stroke-dasharray", "4,3");
    svg.appendChild(gLineR);

    const gTextR = document.createElementNS("http://www.w3.org/2000/svg", "text");
    gTextR.setAttribute("x", gBarX);
    gTextR.setAttribute("y", pR.y + pR.h - 10);
    gTextR.setAttribute("text-anchor", "middle");
    gTextR.setAttribute("font-size", "9");
    gTextR.setAttribute("fill", "#64748b");
    gTextR.textContent = "Global \u03bc";
    svg.appendChild(gTextR);
  }

  const K = data.comms.length;
  const slotH = (pR.h - 50) / K;
  const barH = Math.min(24, Math.max(14, slotH * 0.65));

  const barsByComm = {};

  data.comms.forEach((c, idx) => {
    barsByComm[c.id] = [];
    const cy = pR.y + 25 + idx * slotH + slotH / 2;

    const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
    lbl.setAttribute("x", barLeftX - 10);
    lbl.setAttribute("y", cy + barH / 4);
    lbl.setAttribute("text-anchor", "end");
    lbl.setAttribute("font-size", "10");
    lbl.setAttribute("font-weight", "600");
    lbl.setAttribute("fill", "#334155");
    lbl.textContent = `Comm ${c.id}`;
    svg.appendChild(lbl);
    barsByComm[c.id].push(lbl);

    const bW = sBarW(c.mu);
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", barLeftX);
    rect.setAttribute("y", cy - barH / 2);
    rect.setAttribute("width", bW);
    rect.setAttribute("height", barH);
    rect.setAttribute("fill", c.color);
    rect.setAttribute("rx", "3");
    rect.setAttribute("class", `comm-bar comm-bar-${c.id}`);
    rect.style.cursor = "pointer";
    rect.style.transition = "opacity 0.2s ease, width 0.2s ease";

    if (c.se_mu && c.se_mu > 0) {
      const xLow = barLeftX + sBarW(Math.max(0, c.mu - c.se_mu));
      const xHigh = barLeftX + sBarW(c.mu + c.se_mu);
      const whisker = document.createElementNS("http://www.w3.org/2000/svg", "line");
      whisker.setAttribute("x1", xLow);
      whisker.setAttribute("x2", xHigh);
      whisker.setAttribute("y1", cy);
      whisker.setAttribute("y2", cy);
      whisker.setAttribute("stroke", "#0f172a");
      whisker.setAttribute("stroke-width", "1.5");
      whisker.setAttribute("class", `comm-whisker comm-whisker-${c.id}`);
      svg.appendChild(whisker);
      barsByComm[c.id].push(whisker);
    }

    rect.addEventListener("mouseenter", (e) => {
      showTooltip(e, `
        <strong>Community ${c.id} Substitution Rate</strong><br/>
        &mu; = <strong>${c.mu.toExponential(3)}</strong> subs/site/yr<br/>
        SE(&mu;) = &plusmn;${c.se_mu ? c.se_mu.toExponential(2) : 'N/A'}<br/>
        Relative Pace: <strong>${c.ratio}x</strong> vs. unpartitioned global<br/>
        Taxa Count: <strong>${c.n}</strong> genomes
      `);
    });
    rect.addEventListener("mouseleave", hideTooltip);
    rect.addEventListener("click", () => selectCommunity(c.id));
    svg.appendChild(rect);
    barsByComm[c.id].push(rect);

    const valText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    valText.setAttribute("x", barLeftX + bW + 6);
    valText.setAttribute("y", cy + barH / 4);
    valText.setAttribute("font-size", "9.5");
    valText.setAttribute("font-family", "ui-monospace, SFMono-Regular, monospace");
    valText.setAttribute("font-weight", "600");
    valText.setAttribute("fill", "#1e293b");
    valText.textContent = c.mu.toExponential(2);
    svg.appendChild(valText);
    barsByComm[c.id].push(valText);
  });

  function updateChartVisuals() {
    data.comms.forEach((c) => {
      const isTarget = (activeCommId === "all" || activeCommId === c.id || activeCommId === String(c.id));
      const lineOpacity = isTarget ? "1.0" : "0.10";
      const ptOpacity = isTarget ? "0.75" : "0.08";
      const barOpacity = isTarget ? "1.0" : "0.22";

      if (linesByComm[c.id]) {
        linesByComm[c.id].forEach((el) => {
          el.style.opacity = lineOpacity;
          if (el.tagName === "line") el.setAttribute("stroke-width", isTarget && activeCommId !== "all" ? "3.8" : "2.8");
        });
      }
      if (pointsByComm[c.id]) {
        pointsByComm[c.id].forEach((el) => el.style.opacity = ptOpacity);
      }
      if (barsByComm[c.id]) {
        barsByComm[c.id].forEach((el) => el.style.opacity = barOpacity);
      }
    });
  }

  function updateDetailCard() {
    if (!detailEl) return;
    if (activeCommId === "all") {
      const totalTaxa = data.comms.reduce((acc, c) => acc + c.n, 0);
      const minMu = Math.min(...data.comms.map((c) => c.mu));
      const maxMu = Math.max(...data.comms.map((c) => c.mu));
      const spreadRatio = minMu > 0 ? (maxMu / minMu).toFixed(1) : "N/A";
      detailEl.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; border-bottom:1px solid var(--border-color); padding-bottom:0.5rem;">
          <div>
            <strong style="color:var(--text-primary); font-size:0.95rem;">Multi-Lineage AutoClock Synthesis (All ${data.k_star} Communities)</strong>
            <div style="color:var(--text-muted); font-size:0.75rem;">Showing comprehensive evolutionary divergence across all ${totalTaxa} genomes</div>
          </div>
          <span class="badge badge-neutral" style="font-size:0.75rem; font-weight:700;">Rate Dynamic Spread: ${spreadRatio}&times;</span>
        </div>
        <div class="autoclock-detail-grid">
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Partition Structure</div>
            <div class="autoclock-stat-val">K* = ${data.k_star} Clocks</div>
          </div>
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Global Clock Rate</div>
            <div class="autoclock-stat-val">${data.g_mu ? data.g_mu.toExponential(2) : 'Deconvoluted'}</div>
          </div>
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Fastest Lineage</div>
            <div class="autoclock-stat-val" style="color:#dc2626;">${maxMu.toExponential(2)}</div>
          </div>
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Slowest Lineage</div>
            <div class="autoclock-stat-val" style="color:#2563eb;">${minMu.toExponential(2)}</div>
          </div>
        </div>
        ${data.interpretation ? `<div style="margin-top:0.75rem; font-size:0.83rem; color:var(--text-secondary); line-height:1.5;"><strong>Biological &amp; Epidemiological Context:</strong> ${data.interpretation}</div>` : ''}
      `;
    } else {
      const c = data.comms.find((x) => x.id === activeCommId || String(x.id) === String(activeCommId));
      if (!c) return;
      const totalTaxa = data.comms.reduce((acc, x) => acc + x.n, 0);
      const pct = ((c.n / totalTaxa) * 100).toFixed(1);
      const paceLabel = c.ratio >= 1.05 ? `<span style="color:#dc2626; font-weight:700;">+${Math.round((c.ratio - 1) * 100)}% Accelerated</span>` : (c.ratio <= 0.95 ? `<span style="color:#2563eb; font-weight:700;">-${Math.round((1 - c.ratio) * 100)}% Decelerated</span>` : `<span style="color:#059669; font-weight:700;">Baseline Paced (1.0x)</span>`);
      detailEl.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; border-bottom:1px solid var(--border-color); padding-bottom:0.5rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:${c.color};"></span>
            <strong style="color:var(--text-primary); font-size:0.95rem;">Community ${c.id} Evolutionary Regime</strong>
            <span class="badge badge-neutral" style="font-size:0.75rem;">N = ${c.n} (${pct}% of cohort)</span>
          </div>
          <div>${paceLabel}</div>
        </div>
        <div class="autoclock-detail-grid">
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Substitution Rate (\u03bc_${c.id})</div>
            <div class="autoclock-stat-val">${c.mu.toExponential(3)}</div>
          </div>
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Calibrated Root (t_MRCA)</div>
            <div class="autoclock-stat-val">${c.t_mrca < 0 ? `${Math.abs(c.t_mrca).toFixed(1)} BCE` : `${c.t_mrca.toFixed(2)} CE`}</div>
          </div>
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">95% Fieller CI</div>
            <div class="autoclock-stat-val" style="font-size:0.85rem;">[${c.ci[0]}, ${c.ci[1]}]</div>
          </div>
          <div class="autoclock-stat-card">
            <div class="autoclock-stat-label">Variance Fit (R\u00b2)</div>
            <div class="autoclock-stat-val">${c.r2}</div>
          </div>
        </div>
        <div style="margin-top:0.75rem; font-size:0.83rem; color:var(--text-secondary); line-height:1.5;">
          <strong>Sampling Window:</strong> ${c.timespan[0]} &ndash; ${c.timespan[1]} CE &bull; 
          <strong>Phylogenetic Signal (Pagel's &lambda;*):</strong> ${c.lambda != null ? c.lambda : '0.000'}
        </div>
      `;
    }
  }

  function showTooltip(e, htmlContent) {
    if (!tooltip) return;
    const rect = container.getBoundingClientRect();
    const x = e.clientX - rect.left + 15;
    const y = e.clientY - rect.top - 15;
    tooltip.innerHTML = htmlContent;
    tooltip.style.left = `${Math.min(x, rect.width - 250)}px`;
    tooltip.style.top = `${Math.max(10, y)}px`;
    tooltip.style.display = "block";
  }

  function hideTooltip() {
    if (tooltip) tooltip.style.display = "none";
  }

  updateChartVisuals();
  updateDetailCard();
}
















