#!/usr/bin/env python3
"""
build_tutorials.py
Renders Markdown tutorials into publication-grade, responsive HTML documents
matching ChronAeon visual styling and MathJax mathematics.
"""

import os
import re
import markdown

PORTAL_DIR = os.path.dirname(os.path.abspath(__file__))
TUTORIALS_DIR = os.path.join(PORTAL_DIR, "tutorials")
os.makedirs(TUTORIALS_DIR, exist_ok=True)

def render_markdown(text):
    math_placeholders = []
    def save_math(m):
        idx = len(math_placeholders)
        math_placeholders.append(m.group(0))
        return f"___MATH_BLOCK_{idx}___"

    # Protect display math first, then inline math
    text_prot = re.sub(r"\$\$(.*?)\$\$", save_math, text, flags=re.DOTALL)
    text_prot = re.sub(r"(?<!\\)\$([^\$\n]+?)\$", save_math, text_prot)

    html = markdown.markdown(text_prot, extensions=["fenced_code", "tables", "toc"])

    for idx, raw_math in enumerate(math_placeholders):
        html = html.replace(f"___MATH_BLOCK_{idx}___", raw_math)

    return html

def build_tutorial_html(title, subtitle, badge_text, md_file, out_file, prev_link=None, next_link=None):
    with open(md_file, "r") as f:
        md_text = f.read()

    body_html = render_markdown(md_text)

    # Wrap code blocks with nice header & copy button
    body_html = re.sub(
        r'<pre><code class="language-([a-zA-Z0-9_-]+)">',
        r'<div class="code-wrapper"><div class="code-header"><span class="code-lang">\1</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-\1">',
        body_html
    )
    body_html = re.sub(
        r'<pre><code>',
        r'<div class="code-wrapper"><div class="code-header"><span class="code-lang">terminal</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code>',
        body_html
    )
    body_html = body_html.replace('</code></pre>', '</code></pre></div>')

    prev_btn = f'<a href="{prev_link[1]}" class="study-nav-btn">&larr; {prev_link[0]}</a>' if prev_link else '<span></span>'
    next_btn = f'<a href="{next_link[1]}" class="study-nav-btn">{next_link[0]} &rarr;</a>' if next_link else '<span></span>'

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | ChronAeon Tutorial</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      }},
      options: {{
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      }}
    }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    .tutorial-container {{
      max-width: 960px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem;
    }}
    .tutorial-header {{
      margin-bottom: 2.5rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--border-color);
    }}
    .tutorial-meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      margin-top: 1rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .tutorial-content {{
      line-height: 1.78;
      font-size: 1.02rem;
      color: var(--text-secondary);
    }}
    .tutorial-content h1 {{ display: none; }} /* Rendered in header */
    .tutorial-content h2 {{
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-top: 2.5rem;
      margin-bottom: 1rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border-color);
    }}
    .tutorial-content h3 {{
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--text-primary);
      margin-top: 1.8rem;
      margin-bottom: 0.75rem;
    }}
    .tutorial-content p {{
      margin-bottom: 1.25rem;
    }}
    .tutorial-content ul, .tutorial-content ol {{
      margin-bottom: 1.25rem;
      padding-left: 1.5rem;
    }}
    .tutorial-content li {{
      margin-bottom: 0.45rem;
    }}
    .tutorial-content table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.75rem 0;
      font-size: 0.9rem;
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }}
    .tutorial-content th {{
      background: var(--bg-card-subtle);
      color: var(--text-primary);
      font-weight: 600;
      text-align: left;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
    }}
    .tutorial-content td {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
    }}
    .tutorial-content tr:last-child td {{
      border-bottom: none;
    }}
    .code-wrapper {{
      margin: 1.5rem 0;
      background: #0f172a;
      border-radius: var(--radius-md);
      overflow: hidden;
      border: 1px solid #1e293b;
      box-shadow: var(--shadow-sm);
    }}
    .code-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 1rem;
      background: #1e293b;
      border-bottom: 1px solid #334155;
    }}
    .code-lang {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: #94a3b8;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.05em;
    }}
    .copy-btn {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #e2e8f0;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      font-size: 0.75rem;
      cursor: pointer;
      font-family: var(--font-sans);
      transition: all 0.15s ease;
    }}
    .copy-btn:hover {{
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }}
    .code-wrapper pre {{
      margin: 0;
      padding: 1.25rem;
      overflow-x: auto;
      background: #0f172a;
    }}
    .code-wrapper code {{
      font-family: var(--font-mono);
      font-size: 0.88rem;
      color: #f8fafc;
      line-height: 1.6;
    }}
    .tutorial-nav-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 3.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-color);
    }}
  </style>
</head>
<body>

  <!-- Site Navigation -->
  <header class="site-header">
    <div class="nav-container">
      <div class="brand-group">
        <a href="../index.html" class="brand-logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          ChronAeon
        </a>
        <span class="brand-badge">{badge_text}</span>
      </div>
      <nav class="nav-links">
        <a href="../index.html">&larr; Home</a>
        <a href="index.html" style="color: var(--primary); font-weight: 600;">Tutorials Hub</a>
        <a href="../index.html#benchmarks">42 BEAST Benchmarks</a>
        <a href="../index.html#grand-challenges">Grand Challenges</a>
        <a href="https://github.com/veg/chronaeon" target="_blank" rel="noopener">GitHub &nearr;</a>
      </nav>
    </div>
  </header>

  <main class="tutorial-container">
    <!-- Breadcrumbs -->
    <nav class="breadcrumbs" style="margin-bottom: 1.5rem;">
      <a href="../index.html">Home</a>
      <span class="separator">/</span>
      <a href="index.html">Tutorials</a>
      <span class="separator">/</span>
      <span class="current">{title}</span>
    </nav>

    <!-- Header -->
    <header class="tutorial-header">
      <span class="badge badge-pos-rna" style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;">Tutorial</span>
      <h1 style="font-size: 2.1rem; font-weight: 800; color: var(--text-primary); margin: 0.75rem 0 0.5rem 0; line-height: 1.25;">{title}</h1>
      <p style="font-size: 1.15rem; color: var(--text-muted); line-height: 1.5;">{subtitle}</p>
      
      <div class="tutorial-meta-bar">
        <span><strong>Platform:</strong> ChronAeon / HyphAeon</span> &bull;
        <span><strong>Format:</strong> Markdown &amp; HTML</span> &bull;
        <a href="{os.path.basename(md_file)}" download style="color: var(--primary); font-weight: 600; display: inline-flex; align-items: center; gap: 0.25rem;">Download Markdown Source (.md) &darr;</a>
      </div>
    </header>

    <!-- Body -->
    <article class="tutorial-content">
      {body_html}
    </article>

    <!-- Navigation Footer -->
    <footer class="tutorial-nav-footer">
      {prev_btn}
      <a href="index.html" class="study-nav-btn" style="background: var(--bg-card-subtle);">Tutorials Index</a>
      {next_btn}
    </footer>
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-text">
        &copy; 2026 ChronAeon Authors &bull; Department of Biology, Temple University &bull; Institute for Genomics and Evolutionary Medicine (iGEM).
      </div>
    </div>
  </footer>

  <script>
    function copyCode(btn) {{
      const pre = btn.closest('.code-wrapper').querySelector('pre');
      navigator.clipboard.writeText(pre.innerText).then(() => {{
        const orig = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.background = '#059669';
        setTimeout(() => {{
          btn.innerText = orig;
          btn.style.background = '';
        }}, 2000);
      }});
    }}
  </script>
</body>
</html>"""

    with open(out_file, "w") as f:
        f.write(doc)
    print(f"Generated {out_file} ({len(doc):,} bytes)")

def build_tutorials_hub():
    hub_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tutorials & Guides | ChronAeon</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <style>
    .hub-container {
      max-width: 1040px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
    }
    .hub-header {
      margin-bottom: 2.5rem;
      text-align: center;
    }
    .hub-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
      gap: 2rem;
      margin-bottom: 3rem;
    }
    .hub-card {
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 2rem;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .hub-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }
    .hub-card-title {
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-primary);
      margin: 0.75rem 0 0.5rem 0;
      line-height: 1.3;
    }
    .hub-card-desc {
      font-size: 0.92rem;
      color: var(--text-secondary);
      line-height: 1.6;
      margin-bottom: 1.5rem;
    }
    .hub-features {
      list-style: none;
      padding: 0;
      margin: 0 0 1.5rem 0;
      font-size: 0.85rem;
      color: var(--text-muted);
    }
    .hub-features li {
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .hub-features li svg {
      color: var(--primary);
      flex-shrink: 0;
    }
    .cli-quick-card {
      background: #0f172a;
      border-radius: var(--radius-md);
      padding: 1.75rem;
      color: #f8fafc;
      margin-top: 2rem;
      border: 1px solid #1e293b;
    }
    .cli-quick-title {
      font-size: 1rem;
      font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
  </style>
</head>
<body>

  <!-- Site Navigation -->
  <header class="site-header">
    <div class="nav-container">
      <div class="brand-group">
        <a href="../index.html" class="brand-logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          ChronAeon
        </a>
        <span class="brand-badge">Tutorials &amp; User Guides</span>
      </div>
      <nav class="nav-links">
        <a href="../index.html">&larr; Main Portal</a>
        <a href="../index.html#benchmarks">42 BEAST Benchmarks</a>
        <a href="../index.html#grand-challenges">Grand Challenges</a>
        <a href="https://github.com/veg/chronaeon" target="_blank" rel="noopener">GitHub &nearr;</a>
      </nav>
    </div>
  </header>

  <main class="hub-container">
    <nav class="breadcrumbs" style="margin-bottom: 2rem;">
      <a href="../index.html">Home</a>
      <span class="separator">/</span>
      <span class="current">Tutorials</span>
    </nav>

    <div class="hub-header">
      <h1 style="font-size: 2.3rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.75rem;">ChronAeon Tutorials &amp; Practitioner Guides</h1>
      <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 760px; margin: 0 auto; line-height: 1.5;">
        Step-by-step guides for calibrating molecular clocks, interpreting analytical Denny-Fieller confidence bounds, deconvolving multi-rate epidemic lineages, and migrating from traditional Bayesian MCMC (BEAST).
      </p>
    </div>

    <div class="hub-grid">
      <!-- Tutorial 1 Card -->
      <div class="hub-card">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="badge badge-pos-rna">Tutorial 01</span>
            <span style="font-size: 0.8rem; color: var(--text-muted);">20 min read</span>
          </div>
          <h2 class="hub-card-title">
            <a href="dating.html" style="color: inherit; text-decoration: none;">Practical Molecular Clock Calibration &amp; Emergence Dating</a>
          </h2>
          <p class="hub-card-desc">
            A comprehensive operational guide for computational virologists and epidemiologists. Covers sequence data hygiene, reading-frame verification, single-clock estimators (OLS and foundation PGLS), exact analytical Denny-Fieller confidence bounds, Leave-One-Out Cross-Validation (LOOCV), and a step-by-step worked example on the 2019 Cuban Zika virus epidemic.
          </p>
          <ul class="hub-features">
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Zero-imputation data hygiene &amp; decimal date harmonization
            </li>
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Attention PGLS with exact REML Pagel's &lambda; optimization
            </li>
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Analytical Fieller intervals ($g$-ratio bounding)
            </li>
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Spectral AutoClock multi-rate deconvolution
            </li>
          </ul>
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center; pt: 1rem; border-top: 1px solid var(--border-color); margin-top: 1rem; padding-top: 1rem;">
          <a href="dating.html" class="dossier-view-btn" style="padding: 0.5rem 1.25rem; font-size: 0.9rem;">Read Web Tutorial &rarr;</a>
          <a href="CHRONAEON_DATING_TUTORIAL.md" download style="font-size: 0.82rem; color: var(--text-muted);">Download .md &darr;</a>
        </div>
      </div>

      <!-- Tutorial 2 Card -->
      <div class="hub-card">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="badge badge-concordant">Tutorial 02</span>
            <span style="font-size: 0.8rem; color: var(--text-muted);">25 min read</span>
          </div>
          <h2 class="hub-card-title">
            <a href="beast.html" style="color: inherit; text-decoration: none;">ChronAeon for BEAST Users: The Rosetta Stone</a>
          </h2>
          <p class="hub-card-desc">
            A translation guide for Bayesian phylogeneticists moving from BEAUti, BEAST 1.x/2.x, and Tracer into ChronAeon's geometric framework. Maps demographic priors, Tracer ESS, relaxed clocks (UCLN), and trace diagnostics to their analytical geometric equivalents, featuring direct ingestion of native <code>beast.xml.gz</code> files and a worked comparison on Dengue Virus Type 4.
          </p>
          <ul class="hub-features">
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Rosetta stone translation table (BEAST &harr; ChronAeon)
            </li>
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Direct ingestion of native <code>beast.xml.gz</code> without conversion
            </li>
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              From Tracer ESS to Denny-Fieller diagnostics
            </li>
            <li>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Scaling comparison: 3,200x speedup on 1,600 Ebola genomes
            </li>
          </ul>
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center; pt: 1rem; border-top: 1px solid var(--border-color); margin-top: 1rem; padding-top: 1rem;">
          <a href="beast.html" class="dossier-view-btn" style="padding: 0.5rem 1.25rem; font-size: 0.9rem;">Read Web Tutorial &rarr;</a>
          <a href="CHRONAEON_FOR_BEAST_USERS.md" download style="font-size: 0.82rem; color: var(--text-muted);">Download .md &darr;</a>
        </div>
      </div>
    </div>

    <!-- Quick Reference CLI Card -->
    <div class="cli-quick-card">
      <div class="cli-quick-title">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>
        Quick CLI Reference
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;">
        <div>
          <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 600; margin-bottom: 0.5rem;">1. Date Directly from Compressed BEAST XML</div>
          <pre style="margin: 0; background: #020617; padding: 0.75rem 1rem; border-radius: 6px; font-family: var(--font-mono); font-size: 0.82rem; color: #e2e8f0; overflow-x: auto;">chronaeon date --beast dataset.xml.gz --loocv</pre>
        </div>
        <div>
          <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 600; margin-bottom: 0.5rem;">2. Date from In-Frame FASTA &amp; Dates CSV</div>
          <pre style="margin: 0; background: #020617; padding: 0.75rem 1rem; border-radius: 6px; font-family: var(--font-mono); font-size: 0.82rem; color: #e2e8f0; overflow-x: auto;">chronaeon date -a alignment.fasta -d dates.csv --loocv</pre>
        </div>
        <div>
          <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 600; margin-bottom: 0.5rem;">3. AutoClock Multi-Rate Lineage Deconvolution</div>
          <pre style="margin: 0; background: #020617; padding: 0.75rem 1rem; border-radius: 6px; font-family: var(--font-mono); font-size: 0.82rem; color: #e2e8f0; overflow-x: auto;">chronaeon autoclock --beast dataset.xml.gz</pre>
        </div>
        <div>
          <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 600; margin-bottom: 0.5rem;">4. Generate Publication-Grade Diagnostic Figures</div>
          <pre style="margin: 0; background: #020617; padding: 0.75rem 1rem; border-radius: 6px; font-family: var(--font-mono); font-size: 0.82rem; color: #e2e8f0; overflow-x: auto;">chronaeon date --beast dataset.xml.gz --plot</pre>
        </div>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-text">
        &copy; 2026 ChronAeon Authors &bull; Department of Biology, Temple University &bull; Institute for Genomics and Evolutionary Medicine (iGEM).
      </div>
    </div>
  </footer>
</body>
</html>"""

    out_file = os.path.join(TUTORIALS_DIR, "index.html")
    with open(out_file, "w") as f:
        f.write(hub_html)
    print(f"Generated {out_file} ({len(hub_html):,} bytes)")

def main():
    build_tutorial_html(
        title="Practical Molecular Clock Calibration & Emergence Dating",
        subtitle="A comprehensive operational guide for single-clock calibration, reading-frame verification, analytical Denny-Fieller bounds, LOOCV, and Cuban Zika case study.",
        badge_text="Tutorial 01",
        md_file="tutorials/CHRONAEON_DATING_TUTORIAL.md",
        out_file="tutorials/dating.html",
        prev_link=None,
        next_link=("ChronAeon for BEAST Users", "beast.html")
    )

    build_tutorial_html(
        title="ChronAeon for BEAST Users: The Rosetta Stone",
        subtitle="Translating Bayesian MCMC concepts, priors, Tracer ESS, UCLN relaxed clocks, and XML configs into ChronAeon's continuous geometric framework.",
        badge_text="Tutorial 02",
        md_file="tutorials/CHRONAEON_FOR_BEAST_USERS.md",
        out_file="tutorials/beast.html",
        prev_link=("Practical Dating Tutorial", "dating.html"),
        next_link=None
    )

    build_tutorials_hub()

if __name__ == "__main__":
    main()
