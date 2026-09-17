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
  const countDisplay = document.getElementById("filter-count");

  if (!table) return;

  let activeTaxonomy = "all";
  let activeClock = "all";
  let searchQuery = "";

  function filterRows() {
    const rows = table.querySelectorAll("tbody tr");
    let visibleCount = 0;

    rows.forEach((row) => {
      const rowTaxonomy = row.getAttribute("data-taxonomy") || "";
      const rowClock = row.getAttribute("data-clock") || "";
      const rowText = row.textContent.toLowerCase();

      const matchTaxonomy = (activeTaxonomy === "all" || rowTaxonomy === activeTaxonomy);
      const matchClock = (activeClock === "all" || rowClock === activeClock);
      const matchSearch = (!searchQuery || rowText.includes(searchQuery));

      if (matchTaxonomy && matchClock && matchSearch) {
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
}

// Interactive SVG Concordance Scatter Plot
function initConcordancePlot() {
  const container = document.getElementById("concordance-plot-container");
  if (!container || typeof BENCHMARK_DATA === "undefined") return;

  // Filter out macroevolution / extreme ancient deep time for scatter plot focus (focus on viral/epidemic 1850-2025 CE)
  const plotData = BENCHMARK_DATA.filter((d) => {
    const b = parseFloat(d.beast_tmrca);
    const c = parseFloat(d.chronaeon_tmrca);
    return !isNaN(b) && !isNaN(c) && b > 1850 && b < 2030 && c > 1800 && c < 2030;
  });

  const width = 800;
  const height = 450;
  const margin = { top: 30, right: 30, bottom: 50, left: 65 };

  const minYear = 1880;
  const maxYear = 2025;

  function scaleX(val) {
    return margin.left + ((val - minYear) / (maxYear - minYear)) * (width - margin.left - margin.right);
  }

  function scaleY(val) {
    return height - margin.bottom - ((val - minYear) / (maxYear - minYear)) * (height - margin.top - margin.bottom);
  }

  // Create SVG
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.style.width = "100%";
  svg.style.height = "auto";
  svg.style.display = "block";

  // Grid lines
  const gridGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  for (let yr = 1900; yr <= 2020; yr += 20) {
    const x = scaleX(yr);
    const y = scaleY(yr);

    // Vertical grid
    const vLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vLine.setAttribute("x1", x);
    vLine.setAttribute("x2", x);
    vLine.setAttribute("y1", margin.top);
    vLine.setAttribute("y2", height - margin.bottom);
    vLine.setAttribute("stroke", "#e2e8f0");
    vLine.setAttribute("stroke-dasharray", "3,3");
    gridGroup.appendChild(vLine);

    // Horizontal grid
    const hLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    hLine.setAttribute("x1", margin.left);
    hLine.setAttribute("x2", width - margin.right);
    hLine.setAttribute("y1", y);
    hLine.setAttribute("y2", y);
    hLine.setAttribute("stroke", "#e2e8f0");
    hLine.setAttribute("stroke-dasharray", "3,3");
    gridGroup.appendChild(hLine);

    // X Axis Label
    const xText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    xText.setAttribute("x", x);
    xText.setAttribute("y", height - margin.bottom + 20);
    xText.setAttribute("text-anchor", "middle");
    xText.setAttribute("font-size", "11");
    xText.setAttribute("fill", "#64748b");
    xText.textContent = yr;
    gridGroup.appendChild(xText);

    // Y Axis Label
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

  // Parity line y = x
  const parityLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
  parityLine.setAttribute("x1", scaleX(minYear));
  parityLine.setAttribute("y1", scaleY(minYear));
  parityLine.setAttribute("x2", scaleX(maxYear));
  parityLine.setAttribute("y2", scaleY(maxYear));
  parityLine.setAttribute("stroke", "#94a3b8");
  parityLine.setAttribute("stroke-width", "1.5");
  parityLine.setAttribute("stroke-dasharray", "4,4");
  svg.appendChild(parityLine);

  // Axis Titles
  const xTitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
  xTitle.setAttribute("x", margin.left + (width - margin.left - margin.right) / 2);
  xTitle.setAttribute("y", height - 12);
  xTitle.setAttribute("text-anchor", "middle");
  xTitle.setAttribute("font-size", "12");
  xTitle.setAttribute("font-weight", "600");
  xTitle.setAttribute("fill", "#334155");
  xTitle.textContent = "Published BEAST 1.x / 2.x MCMC Estimated tMRCA (Calendar Year CE)";
  svg.appendChild(xTitle);

  const yTitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
  yTitle.setAttribute("x", -(margin.top + (height - margin.top - margin.bottom) / 2));
  yTitle.setAttribute("y", 20);
  yTitle.setAttribute("text-anchor", "middle");
  yTitle.setAttribute("transform", "rotate(-90)");
  yTitle.setAttribute("font-size", "12");
  yTitle.setAttribute("font-weight", "600");
  yTitle.setAttribute("fill", "#334155");
  yTitle.textContent = "ChronAeon Tree-Free Geometric tMRCA (Calendar Year CE)";
  svg.appendChild(yTitle);

  // Color mapping
  const colorMap = {
    "Retroviruses": "#8b5cf6",
    "Negative-Sense RNA": "#2563eb",
    "Positive-Sense RNA": "#059669",
    "DNA Viruses": "#d97706",
    "Bacteria & Ancient DNA": "#e11d48",
    "Macroevolution": "#475569",
  };

  // Tooltip div
  const tooltip = document.createElement("div");
  tooltip.style.position = "absolute";
  tooltip.style.display = "none";
  tooltip.style.background = "#0f172a";
  tooltip.style.color = "#ffffff";
  tooltip.style.padding = "0.5rem 0.75rem";
  tooltip.style.borderRadius = "6px";
  tooltip.style.fontSize = "0.78rem";
  tooltip.style.pointerEvents = "none";
  tooltip.style.boxShadow = "0 4px 6px -1px rgba(0, 0, 0, 0.2)";
  tooltip.style.zIndex = "100";
  container.style.position = "relative";
  container.appendChild(tooltip);

  // Plot Points
  plotData.forEach((d) => {
    const b = parseFloat(d.beast_tmrca);
    const c = parseFloat(d.chronaeon_tmrca);
    const cx = scaleX(b);
    const cy = scaleY(c);
    const color = colorMap[d.taxonomy] || "#2563eb";

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", cx);
    circle.setAttribute("cy", cy);
    circle.setAttribute("r", "5.5");
    circle.setAttribute("fill", color);
    circle.setAttribute("fill-opacity", "0.85");
    circle.setAttribute("stroke", "#ffffff");
    circle.setAttribute("stroke-width", "1.2");
    circle.style.cursor = "pointer";
    circle.style.transition = "transform 0.15s ease, r 0.15s ease";

    circle.addEventListener("mouseenter", (e) => {
      circle.setAttribute("r", "8.5");
      circle.setAttribute("fill-opacity", "1.0");
      tooltip.innerHTML = `<strong>${d.pathogen}</strong><br>BEAST: ${d.beast_tmrca} CE<br>ChronAeon: ${d.chronaeon_tmrca} CE<br>Speedup: ${d.speedup}<br><em>Click to view study page</em>`;
      tooltip.style.display = "block";
      const rect = container.getBoundingClientRect();
      tooltip.style.left = `${e.clientX - rect.left + 12}px`;
      tooltip.style.top = `${e.clientY - rect.top - 20}px`;
    });

    circle.addEventListener("mousemove", (e) => {
      const rect = container.getBoundingClientRect();
      tooltip.style.left = `${e.clientX - rect.left + 12}px`;
      tooltip.style.top = `${e.clientY - rect.top - 20}px`;
    });

    circle.addEventListener("mouseleave", () => {
      circle.setAttribute("r", "5.5");
      circle.setAttribute("fill-opacity", "0.85");
      tooltip.style.display = "none";
    });

    circle.addEventListener("click", () => {
      window.location.href = `studies/${d.dir}/index.html`;
    });

    svg.appendChild(circle);
  });

  container.appendChild(svg);
}
