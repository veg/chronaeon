// ChronAeon Benchmark Compendium - Portal Interactive Scripts

document.addEventListener("DOMContentLoaded", () => {
  initLightbox();
  initCopyButtons();
  initTableFilters();
  initConcordancePlot();
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















