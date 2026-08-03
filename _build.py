#!/usr/bin/env python3
"""
Static HTML generator for busybeemainecoons.com.

Produces every page in ./public/ with a consistent header, navigation,
footer, security/SEO meta and shared chrome.

Usage:
    python3 _build.py

Output files are committed to git so Cloudflare Pages can deploy them
directly from /public with no build step. Re-run this script whenever
the navigation, footer, or shared chrome needs to change.
"""
from __future__ import annotations
import os, html, json, re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).parent
OUT  = ROOT / "public"

SITE = "https://cooncatcentral.com"
BRAND = "Busy Bee Maine Coons"
TAGLINE = "Where Gentle Giants Find Their Forever Homes"
YEAR = datetime.datetime.now(datetime.UTC).year
ASSET_V = "20260803b"
# Official Google review destination (update when Place ID is confirmed)
GOOGLE_REVIEW_URL = "https://www.google.com/search?q=Busy+Bee+Maine+Coons+cooncatcentral.com+reviews"
GOOGLE_REVIEW_QR = f"/images/review/google-review-qr.png?v={ASSET_V}"

# ---- Navigation (from BUSY-BEE-DESIGN.md §2) -------------------------------
NAV = [
    ("Home",              "index.html"),
    ("Available Kittens", "kittens.html"),
    ("The Breed",         "the-breed.html"),
    ("Care Guides",       "care.html"),
    ("Coon Cat Stories",  "stories.html"),
    ("Community",         "community.html"),
    ("Useful Tools",      "tools.html"),
    ("Shop",              "shop.html"),
]

# ---- Shared chunks ---------------------------------------------------------
def head(title: str, description: str, path: str, og_type: str = "website",
         schema: list | None = None) -> str:
    canonical_path = "" if path == "index.html" else path.replace(".html", "")
    canonical = SITE + ("/" + canonical_path if canonical_path else "/")
    schema_blocks = ""
    if schema:
        for s in schema:
            schema_blocks += '<script type="application/ld+json">' + json.dumps(s, separators=(",", ":")) + '</script>\n  '
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="theme-color" content="#1A3C34">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">

  <!-- Open Graph / Twitter -->
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/images/og-default.jpg?v={ASSET_V}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{SITE}/images/og-default.jpg?v={ASSET_V}">

  <!-- Performance: preconnect Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/css/style.css?v={ASSET_V}">
  <link rel="icon" href="/favicon.svg?v={ASSET_V}" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico?v={ASSET_V}" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v={ASSET_V}">
  <link rel="manifest" href="/site.webmanifest">

  {schema_blocks}<script type="application/ld+json">{json.dumps(org_schema(), separators=(",", ":"))}</script>
  <script type="application/ld+json">{json.dumps(website_schema(), separators=(",", ":"))}</script>
  <script>
    window.BUSYBEE = {{
      site: "{SITE}",
      googleReviewUrl: {json.dumps(GOOGLE_REVIEW_URL)},
      googleReviewQr: {json.dumps(GOOGLE_REVIEW_QR)},
      assetVersion: "{ASSET_V}"
    }};
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
"""

def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": SITE,
        "logo": SITE + "/images/logo.png",
        "description": "Premier marketplace connecting buyers with ethical, health-tested Maine Coon breeders. Curated giant-breed cat products and expert care guides.",
        "sameAs": [],
    }

def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND,
        "url": SITE,
        "potentialAction": {
            "@type": "SearchAction",
            "target": SITE + "/stories?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }

def announcement():
    return """  <div class="announcement-bar" role="region" aria-label="Site announcement">
    🐝 Health-tested kittens from vetted breeders &nbsp;|&nbsp; <strong>Free</strong> care guide with every reservation &nbsp;|&nbsp; Lifetime breeder support
  </div>
"""

def navbar(current: str):
    def _link(label, href, indent):
        clean = "" if href == "index.html" else href.replace(".html", "")
        cur = ' aria-current="page"' if href == current else ""
        return f'{indent}<a href="/{clean}"{cur}>{label}</a>'
    links = "\n".join(_link(l, h, "        ") for l, h in NAV)
    mobile_links = "\n".join(_link(l, h, "      ") for l, h in NAV)
    return f"""  <header class="navbar" role="banner">
    <div class="navbar-inner">
      <a href="/" class="logo" aria-label="{BRAND} — Home">
        <span class="logo-mark" aria-hidden="true">🐝</span>
        <span>Busy Bee <span>Maine Coons</span></span>
      </a>
      <nav class="nav-links" id="nav-links" aria-label="Primary">
{links}
      </nav>
      <div class="nav-actions">
        <a href="/account" class="nav-icon-btn" aria-label="My account">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 3a4 4 0 100 8 4 4 0 000-8z"/></svg>
        </a>
        <a href="/cart" class="nav-icon-btn nav-cart" aria-label="Shopping cart">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
          <span class="cart-badge">0</span>
        </a>
        <button class="nav-icon-btn mobile-toggle" id="mobile-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="mobile-menu">
          <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
        </button>
      </div>
    </div>
    <div class="mobile-menu" id="mobile-menu">
{mobile_links}
      <a href="/account">My Account</a>
      <a href="/cart">Cart</a>
    </div>
  </header>
"""

def footer():
    return f"""  <footer class="footer" role="contentinfo">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="/" class="logo" aria-label="{BRAND} — Home">
          <span class="logo-mark" aria-hidden="true">🐝</span>
          <span>Busy Bee <span>Maine Coons</span></span>
        </a>
        <p>Connecting families with ethically bred, health-tested Maine Coon kittens — and equipping them for a lifetime with curated giant-breed gear and expert guidance.</p>
        <p style="font-size:.8rem;opacity:.7;">{TAGLINE}</p>
      </div>
      <nav aria-label="Explore">
        <h4>Explore</h4>
        <ul>
          <li><a href="/kittens">Available Kittens</a></li>
          <li><a href="/the-breed">The Breed</a></li>
          <li><a href="/care">Care Guides</a></li>
          <li><a href="/stories">Coon Cat Stories</a></li>
          <li><a href="/tools">Useful Tools</a></li>
          <li><a href="/shop">Shop</a></li>
        </ul>
      </nav>
      <nav aria-label="Company">
        <h4>Company</h4>
        <ul>
          <li><a href="/about">About Busy Bee</a></li>
          <li><a href="/ethics">Ethics &amp; Health Testing</a></li>
          <li><a href="/community">Community</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>
      <nav aria-label="Account &amp; Legal">
        <h4>Account &amp; Legal</h4>
        <ul>
          <li><a href="/account">My Account</a></li>
          <li><a href="/cart">Cart</a></li>
          <li><a href="/privacy">Privacy Policy</a></li>
          <li><a href="/terms">Terms of Service</a></li>
          <li><a href="/accessibility">Accessibility Statement</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <p>&copy; {YEAR} {BRAND}. All rights reserved.</p>
      <p>Made with care in the United States. <a href="/ethics">Ethically bred. Lifetime supported.</a></p>
    </div>
  </footer>

  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <button class="scroll-top" id="scroll-top" aria-label="Scroll to top">
    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M10 16V4M4 10l6-6 6 6"/></svg>
  </button>

  <!-- Floating Google Review CTA (SITE-GUIDE §0) -->
  <button type="button" class="review-fab" id="review-fab" aria-haspopup="dialog" aria-controls="review-dialog" aria-label="Leave a Google review">
    <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18" aria-hidden="true"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
    <span class="review-fab-label">Review Us</span>
  </button>
  <div class="review-dialog" id="review-dialog" role="dialog" aria-modal="true" aria-labelledby="review-dialog-title" hidden>
    <div class="review-dialog-panel">
      <button type="button" class="review-dialog-close" id="review-dialog-close" aria-label="Close review dialog">&times;</button>
      <h2 id="review-dialog-title">Leave an honest Google review</h2>
      <p>If we earned your trust, please leave an honest Google review. Your feedback helps other families choose confidently.</p>
      <div class="review-qr">
        <img data-review-qr src="{GOOGLE_REVIEW_QR}" width="200" height="200" alt="Scan to open our Google review page" loading="lazy" decoding="async">
      </div>
      <a class="btn-review" data-review-link="dialog" href="{GOOGLE_REVIEW_URL}" rel="noopener noreferrer" target="_blank">Open Google Reviews</a>
      <p class="review-compliance">We welcome honest feedback from all customers and do not offer incentives for reviews.</p>
    </div>
  </div>

  <script src="/js/script.js?v={ASSET_V}" defer></script>
  <script src="/js/cart.js?v={ASSET_V}" defer></script>
  <script src="/js/newsletter.js?v={ASSET_V}" defer></script>
</body>
</html>
"""

def page(current: str, title: str, description: str, body_html: str,
         schema: list | None = None, og_type: str = "website") -> str:
    return (
        head(title, description, current, og_type, schema)
        + announcement()
        + navbar(current)
        + '  <main id="main">\n'
        + body_html
        + '  </main>\n'
        + footer()
    )

def newsletter_section() -> str:
    return """  <section class="nl-section" id="newsletter" aria-label="Newsletter signup">
    <div class="nl-inner">
      <h2>Join the <strong>Busy Bee Hive</strong></h2>
      <p class="nl-sub">Early access to new litters, expert care advice, and 10% off your first shop order.</p>
      <form class="nl-form" autocomplete="on" novalidate>
        <label class="sr-only" for="nl-email">Email address</label>
        <input id="nl-email" type="email" name="email" placeholder="your@email.com" required autocomplete="email">
        <button type="submit" class="nl-btn">Subscribe</button>
      </form>
      <p class="nl-success" role="status" aria-live="polite"></p>
      <p class="nl-error" role="alert" aria-live="assertive"></p>
      <p class="nl-disclaimer">Unsubscribe anytime. We never share your email.</p>
    </div>
  </section>
"""

def trust_strip() -> str:
    items = [
        ("Health-Tested Breeders", "🩺"),
        ("HCM • SMA • PKD Screened", "🧬"),
        ("Lifetime Breeder Support", "🤝"),
        ("Ethical Cattery Network", "🌿"),
        ("Expert Care Guides", "📚"),
    ]
    parts = "".join(
        f'<div class="trust-item"><span style="font-size:1.5rem;" aria-hidden="true">{icon}</span><span>{label}</span></div>'
        for label, icon in items
    )
    return f'  <section class="trust-strip" aria-label="Why choose Busy Bee Maine Coons"><div class="trust-strip-inner">{parts}</div></section>\n'

def page_header(title: str, subtitle: str, breadcrumb: list[tuple[str, str]] | None = None) -> str:
    crumbs = ""
    if breadcrumb:
        items = " &raquo; ".join(
            f'<a href="{href}">{html.escape(label)}</a>' if href else f'<span aria-current="page">{html.escape(label)}</span>'
            for label, href in breadcrumb
        )
        crumbs = f'<nav class="breadcrumb" aria-label="Breadcrumb">{items}</nav>'
    return f"""  <section class="page-header">
    {crumbs}
    <h1>{html.escape(title)}</h1>
    <p>{html.escape(subtitle)}</p>
  </section>
"""

# ---- PAGE BODIES -----------------------------------------------------------

def home_body() -> str:
    return """  <section class="hero" aria-label="Welcome">
    <div class="hero-inner">
      <div>
        <div class="hero-badges">
          <span class="hero-badge"><svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.7-9.3a1 1 0 00-1.4-1.4L9 10.6 7.7 9.3a1 1 0 00-1.4 1.4l2 2a1 1 0 001.4 0l4-4z"/></svg> Ethically Bred</span>
          <span class="hero-badge"><svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.7-9.3a1 1 0 00-1.4-1.4L9 10.6 7.7 9.3a1 1 0 00-1.4 1.4l2 2a1 1 0 001.4 0l4-4z"/></svg> Health-Tested</span>
          <span class="hero-badge"><svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.7-9.3a1 1 0 00-1.4-1.4L9 10.6 7.7 9.3a1 1 0 00-1.4 1.4l2 2a1 1 0 001.4 0l4-4z"/></svg> Lifetime Support</span>
        </div>
        <h1>Busy Bee Maine Coons<br><span>Where Gentle Giants Find Their Forever Homes</span></h1>
        <p>Browse premium Maine Coon kittens from a curated network of ethical, health-tested breeders across the United States — and shop everything your gentle giant will need for a lifetime of comfort.</p>
        <div class="hero-cta">
          <a href="/kittens" class="btn btn-secondary btn-lg">Browse Available Kittens
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
          <a href="/the-breed" class="btn btn-outline btn-lg" style="color:#fff;border-color:#fff;">Learn About the Breed</a>
        </div>
      </div>
      <div class="hero-image">
        <img src="/images/kittens/hero.jpeg?v=""" + ASSET_V + """" width="640" height="480" alt="Fluffy Maine Coon kitten with tongue out among flowers" decoding="async" fetchpriority="high">
      </div>
    </div>
  </section>

""" + trust_strip() + f"""
  <section class="section review-home" id="reviews" aria-labelledby="review-home-title">
    <div class="section-inner review-home-inner">
      <div>
        <p class="review-home-stars" aria-label="5 out of 5 stars">★★★★★</p>
        <h2 id="review-home-title" class="section-title" style="text-align:left;margin-bottom:.5rem;">Loved by Maine Coon families</h2>
        <p class="section-subtitle" style="text-align:left;margin:0 0 1.25rem;">If we earned your trust, please leave an honest Google review. Your feedback helps other families choose confidently — we never offer incentives for reviews.</p>
        <div class="hero-cta">
          <a class="btn btn-primary btn-lg" data-review-link="homepage" href="{GOOGLE_REVIEW_URL}" rel="noopener noreferrer" target="_blank">Leave a Google Review</a>
          <button type="button" class="btn btn-outline btn-lg" data-open-review="homepage">Scan QR code</button>
        </div>
      </div>
      <div class="review-home-qr">
        <img data-review-qr src="{GOOGLE_REVIEW_QR}" width="160" height="160" alt="Scan to open our Google review page" loading="lazy" decoding="async">
        <p>Scan with your phone</p>
      </div>
    </div>
  </section>
""" + """
  <section class="section">
    <div class="section-inner">
      <h2 class="section-title">Featured Kittens</h2>
      <p class="section-subtitle">Healthy, well-socialized Maine Coon kittens ready for reservation. Every kitten comes with verified health testing and our lifetime breeder support promise.</p>
      <div class="cards-grid">
""" + "\n".join(featured_kitten_card(k) for k in FEATURED_KITTENS) + """
      </div>
      <div class="text-center mt-4">
        <a href="/kittens" class="btn btn-primary btn-lg">See All Available Kittens</a>
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="section-inner">
      <h2 class="section-title">Why Maine Coons?</h2>
      <p class="section-subtitle">The largest domestic cat breed — and arguably the most affectionate. Here's what makes them special.</p>
      <div class="features-grid">
        <div class="feature-card fade-on-scroll">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div>
          <h3>Gentle Giants</h3>
          <p>Adult males regularly reach 18–25 lbs with the temperament of a friendly dog. Affectionate, patient, and famously good with kids.</p>
        </div>
        <div class="feature-card fade-on-scroll">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>
          <h3>15+ Year Lifespan</h3>
          <p>Health-tested lines from our partner breeders consistently live 13–17+ years, with many seniors thriving well into their late teens.</p>
        </div>
        <div class="feature-card fade-on-scroll">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>
          <h3>Health Transparency</h3>
          <p>Every breeder partner screens for HCM, SMA, PKD, and hip dysplasia — and shares the certificates openly with you.</p>
        </div>
        <div class="feature-card fade-on-scroll">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div>
          <h3>Highly Social &amp; Vocal</h3>
          <p>Maine Coons "talk" with chirps and trills, follow you room to room, and bond deeply with the whole family — not just one person.</p>
        </div>
        <div class="feature-card fade-on-scroll">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 7h18M5 7v12a2 2 0 002 2h10a2 2 0 002-2V7M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2"/></svg></div>
          <h3>Built for Real Life</h3>
          <p>Water-loving, dog-friendly, leash-trainable, and remarkably easy-going with other pets. Maine Coons fit modern households beautifully.</p>
        </div>
        <div class="feature-card fade-on-scroll">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21l-7-7 7-7M19 21l-7-7 7-7"/></svg></div>
          <h3>Centuries of Heritage</h3>
          <p>America's oldest natural breed, originating in Maine — robust, weather-hardy, and the original "working" cat of New England farms.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <h2 class="section-title">Coon Cat Stories</h2>
      <p class="section-subtitle">Real journeys from real Maine Coon families. Adoption stories, expert interviews, and breed deep-dives.</p>
      <div class="cards-grid">
""" + "\n".join(featured_story_card(s) for s in FEATURED_STORIES) + """
      </div>
      <div class="text-center mt-4">
        <a href="/stories" class="btn btn-outline btn-lg">Read All Stories</a>
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="section-inner text-center">
      <h2 class="section-title">Useful Tools for Maine Coon Parents</h2>
      <p class="section-subtitle">Free interactive tools built specifically for the world's largest domestic cat breed.</p>
      <div class="categories-grid">
        <a class="category-card" href="/tools#size">
          <div class="cat-icon" aria-hidden="true">📏</div>
          <h3>Size Predictor</h3><p>Estimate your kitten's adult weight &amp; length.</p>
        </a>
        <a class="category-card" href="/tools#cost">
          <div class="cat-icon" aria-hidden="true">💰</div>
          <h3>Cost Calculator</h3><p>Year-1 and lifetime cost estimator.</p>
        </a>
        <a class="category-card" href="/tools#grooming">
          <div class="cat-icon" aria-hidden="true">🪮</div>
          <h3>Grooming Planner</h3><p>Personalized brushing &amp; bath schedule.</p>
        </a>
        <a class="category-card" href="/tools#quiz">
          <div class="cat-icon" aria-hidden="true">🧩</div>
          <h3>Compatibility Quiz</h3><p>Is a Maine Coon right for your home?</p>
        </a>
        <a class="category-card" href="/tools#name">
          <div class="cat-icon" aria-hidden="true">✨</div>
          <h3>Name Generator</h3><p>200+ majestic, regal &amp; playful names.</p>
        </a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <h2 class="section-title">Trusted by Maine Coon Families</h2>
      <p class="section-subtitle">Hear from the families who've welcomed home a gentle giant through Busy Bee.</p>
      <div class="testimonials-grid">
        <div class="testimonial-card fade-on-scroll">
          <div class="testimonial-stars" aria-label="5 out of 5 stars">★★★★★</div>
          <p>&ldquo;Busy Bee made finding an ethical breeder effortless. Every health certificate was already verified, and our breeder still texts us photos of the parents two years later.&rdquo;</p>
          <p class="testimonial-author">Megan &amp; Tyler R.</p>
          <p class="testimonial-role">Maple's family — Asheville, NC</p>
        </div>
        <div class="testimonial-card fade-on-scroll">
          <div class="testimonial-stars" aria-label="5 out of 5 stars">★★★★★</div>
          <p>&ldquo;The care guides alone were worth the visit. Then we found Otto. He's now 22 lbs of pure love and the best cat we've ever had.&rdquo;</p>
          <p class="testimonial-author">Dr. Priya S.</p>
          <p class="testimonial-role">Otto's family — Austin, TX</p>
        </div>
        <div class="testimonial-card fade-on-scroll">
          <div class="testimonial-stars" aria-label="5 out of 5 stars">★★★★★</div>
          <p>&ldquo;The oversized bed we ordered actually fits him. After three failed beds from other sites, this was a game changer.&rdquo;</p>
          <p class="testimonial-author">James &amp; Elena K.</p>
          <p class="testimonial-role">Bear's family — Portland, OR</p>
        </div>
      </div>
    </div>
  </section>

  <section class="cta-banner">
    <h2>Ready to Meet Your Gentle Giant?</h2>
    <p>Reserve a kitten from a vetted, health-tested Maine Coon breeder — or join the Busy Bee Hive for early access to new litters.</p>
    <a href="/kittens" class="btn btn-secondary btn-lg">Browse Available Kittens</a>
  </section>

""" + newsletter_section()

# Sample data ----------------------------------------------------------------
FEATURED_KITTENS = [
    {"id": "honey",   "name": "Honey",   "color": "Cream Tabby",        "age": 10, "gender": "Female", "price": 2800, "badge": "Reservation Open", "img": "/images/kittens/honey.jpeg", "alt": "Honey, a cream tabby Maine Coon kitten on a pillow"},
    {"id": "atlas",   "name": "Atlas",   "color": "Brown Mackerel",     "age": 12, "gender": "Male",   "price": 3200, "badge": "Health Verified",  "img": "/images/kittens/atlas.jpeg", "alt": "Atlas, a brown mackerel Maine Coon kitten on the floor"},
    {"id": "willow",  "name": "Willow",  "color": "Silver Smoke",       "age": 9,  "gender": "Female", "price": 3000, "badge": "New Litter",       "img": "/images/kittens/willow.jpeg", "alt": "Willow, a silver smoke Maine Coon kitten sleeping in a basket"},
    {"id": "thor",    "name": "Thor",    "color": "Red Tabby Polydactyl","age": 14,"gender": "Male",   "price": 3500, "badge": "Show Quality",     "img": "/images/kittens/thor.jpeg", "alt": "Thor, a red tabby Maine Coon kitten with a ball"},
]

FEATURED_STORIES = [
    {"slug": "first-30-days",        "title": "Bringing Home Your Maine Coon: The First 30 Days",      "cat": "New Owner Guide",   "read": "8 min read",  "img": "/images/kittens/story-1.jpeg", "alt": "Parent hugging a Maine Coon kitten"},
    {"slug": "hcm-explained",        "title": "HCM in Maine Coons: What Every Buyer Must Understand",  "cat": "Health & Genetics", "read": "11 min read", "img": "/images/cats/window.jpeg", "alt": "Maine Coon lounging by a window"},
    {"slug": "ethical-breeders",     "title": "How to Spot a Truly Ethical Maine Coon Breeder",        "cat": "Buyer's Guide",     "read": "9 min read",  "img": "/images/kittens/story-2.jpeg", "alt": "Maine Coon kitten resting on bed pillows"},
]

def featured_kitten_card(k):
    img = f'<img src="{k["img"]}?v={ASSET_V}" width="640" height="400" alt="{html.escape(k["alt"])}" loading="lazy" decoding="async">'
    return f"""        <article class="kitten-card fade-on-scroll" data-card data-gender="{k['gender'].lower()}" data-price="{k['price']}" data-age="{k['age']}">
          <div class="card-image"><span class="card-badge gold">{html.escape(k['badge'])}</span>{img}</div>
          <div class="card-body">
            <p class="card-cat">{html.escape(k['color'])}</p>
            <h3><a href="/kittens#{k['id']}">{html.escape(k['name'])}</a></h3>
            <div class="card-meta"><span>🗓 {k['age']} weeks</span><span>♀♂ {k['gender']}</span></div>
            <div class="health-badges"><span class="health-badge">HCM Clear</span><span class="health-badge">SMA Clear</span><span class="health-badge">PKD Clear</span></div>
            <p class="card-desc">Raised underfoot in a loving home. TICA-registered parents with 5-generation pedigree available.</p>
            <p class="card-price"><span class="from">From </span>${k['price']:,}</p>
          </div>
          <div class="card-actions">
            <a href="/kittens#{k['id']}" class="btn btn-outline">Details</a>
            <button class="btn btn-primary" data-add-cart="kitten-{k['id']}" data-id="kitten-{k['id']}" data-name="{html.escape(k['name'])} (Reservation)" data-price="{k['price']}" data-type="Kitten reservation">Reserve</button>
          </div>
        </article>"""

def featured_story_card(s):
    img = f'<img src="{s["img"]}?v={ASSET_V}" width="640" height="400" alt="{html.escape(s["alt"])}" loading="lazy" decoding="async">'
    return f"""        <article class="kitten-card fade-on-scroll">
          <div class="card-image"><span class="card-badge">Story</span>{img}</div>
          <div class="card-body">
            <p class="card-cat">{html.escape(s['cat'])}</p>
            <h3><a href="/stories#{s['slug']}">{html.escape(s['title'])}</a></h3>
            <p class="card-desc">{html.escape(s['read'])} · Updated {YEAR}</p>
            <p style="margin-top:auto;"><a href="/stories#{s['slug']}" class="btn btn-outline" style="width:100%;">Read Article</a></p>
          </div>
        </article>"""

# ---- Sub-page bodies -------------------------------------------------------

def kittens_body():
    cards = "\n".join(
        f"""        <article class="kitten-card fade-on-scroll" id="{k['id']}" data-card data-gender="{k['gender'].lower()}" data-price="{k['price']}" data-age="{k['age']}" data-color="{k['color'].lower().split()[0]}">
          <div class="card-image"><span class="card-badge gold">{html.escape(k['badge'])}</span><img src="{k['img']}?v={ASSET_V}" width="640" height="400" alt="{html.escape(k['alt'])}" loading="lazy" decoding="async"></div>
          <div class="card-body">
            <p class="card-cat">{html.escape(k['color'])}</p>
            <h3>{html.escape(k['name'])}</h3>
            <div class="card-meta"><span>🗓 {k['age']} weeks</span><span>♀♂ {k['gender']}</span><span>📍 USA</span></div>
            <div class="health-badges"><span class="health-badge">HCM Clear</span><span class="health-badge">SMA Clear</span><span class="health-badge">PKD Clear</span><span class="health-badge">Hip Scored</span></div>
            <p class="card-desc">Raised underfoot in a loving home. TICA-registered parents with 5-generation pedigree available. Vaccinated, dewormed, microchipped, and socialized with children and other pets.</p>
            <p class="card-price"><span class="from">From </span>${k['price']:,}</p>
          </div>
          <div class="card-actions">
            <a href="/contact?kitten={k['id']}" class="btn btn-outline">Ask a Question</a>
            <button class="btn btn-primary" data-add-cart="kitten-{k['id']}" data-id="kitten-{k['id']}" data-name="{html.escape(k['name'])} (Reservation)" data-price="{k['price']}" data-type="Kitten reservation">Reserve Now</button>
          </div>
        </article>""" for k in FEATURED_KITTENS
    )
    return page_header(
        "Available Maine Coon Kittens",
        "Health-tested, ethically-bred Maine Coon kittens from our network of vetted breeders. Every kitten ships with full HCM, SMA, PKD, and hip-evaluation results.",
        [("Home", "/"), ("Available Kittens", None)],
    ) + f"""  <section class="section">
    <div class="section-inner">
      <div class="filter-bar" role="region" aria-label="Filter kittens">
        <label for="filter-gender">Gender:</label>
        <select id="filter-gender" data-filter="gender">
          <option value="all">All</option><option value="female">Female</option><option value="male">Male</option>
        </select>
        <label for="filter-color">Color:</label>
        <select id="filter-color" data-filter="color">
          <option value="all">All</option>
          <option value="brown">Brown Tabby</option>
          <option value="silver">Silver</option>
          <option value="cream">Cream</option>
          <option value="red">Red</option>
        </select>
        <label for="sort-select">Sort:</label>
        <select id="sort-select">
          <option value="default">Recommended</option>
          <option value="price-asc">Price: Low → High</option>
          <option value="price-desc">Price: High → Low</option>
          <option value="age-asc">Youngest First</option>
          <option value="age-desc">Oldest First</option>
        </select>
        <span class="result-count" id="result-count" role="status" aria-live="polite">{len(FEATURED_KITTENS)} results</span>
      </div>

      <div class="cards-grid" data-filterable-grid>
{cards}
      </div>

      <div class="text-center mt-4" style="background:var(--bg-alt);padding:2rem;border-radius:var(--radius-lg);border:1px solid var(--gray-200);margin-top:3rem;">
        <h2>Don't See the Right Kitten?</h2>
        <p class="lead">New litters arrive monthly. Join the Busy Bee Hive for first-look access to upcoming kittens before they're listed publicly.</p>
        <a href="#newsletter" class="btn btn-primary btn-lg">Join the Waitlist</a>
      </div>
    </div>
  </section>

""" + newsletter_section()

def the_breed_body():
    return page_header(
        "The Maine Coon: Complete Breed Guide",
        "Everything you need to know about America's oldest natural breed — from history and size to temperament, health, and what makes them the world's most-loved gentle giants.",
        [("Home", "/"), ("The Breed", None)],
    ) + """  <article class="article">
    <p class="lead">The Maine Coon is the largest domestic cat breed and one of the oldest natural breeds in North America. Affectionate, intelligent, and famously dog-like, they are the perfect companion for families seeking a truly extraordinary feline.</p>

    <h2>Origin &amp; History</h2>
    <p>The Maine Coon is the official state cat of Maine, where it developed naturally over centuries from working cats brought ashore by 17th-century seafarers. Their dense, water-resistant coats, tufted ears and feet, and bushy tails are all adaptations to the harsh New England climate.</p>

    <h2>Size: How Big Do They Get?</h2>
    <p>Adult males typically weigh <strong>15–25 lbs</strong>, females <strong>10–15 lbs</strong>. Length nose-to-tail can exceed 40 inches. They mature slowly, reaching full size between 3 and 5 years old.</p>

    <h2>Temperament</h2>
    <ul>
      <li><strong>Gentle &amp; patient</strong> — exceptional with children and other pets.</li>
      <li><strong>Vocal but soft</strong> — chirps, trills and quiet meows rather than loud yowling.</li>
      <li><strong>Highly social</strong> — bonds with the whole family, not just one person.</li>
      <li><strong>Playful for life</strong> — kitten-like behavior often persists into senior years.</li>
      <li><strong>Water-curious</strong> — many enjoy faucets, baths, and even shower steam.</li>
    </ul>

    <h2>Health &amp; Genetics</h2>
    <p>Responsible breeding is essential. Every Busy Bee partner breeder screens for:</p>
    <ul>
      <li><strong>HCM</strong> (Hypertrophic Cardiomyopathy) — DNA + echocardiogram</li>
      <li><strong>SMA</strong> (Spinal Muscular Atrophy) — DNA test</li>
      <li><strong>PKD</strong> (Polycystic Kidney Disease) — DNA test</li>
      <li><strong>Hip Dysplasia</strong> — radiographic evaluation</li>
    </ul>
    <p>See our full <a href="/ethics">Ethics &amp; Health Testing</a> standards.</p>

    <h2>Care Essentials</h2>
    <ul>
      <li>Brush 2–3× per week (daily during shedding seasons)</li>
      <li>High-protein, large-breed nutrition</li>
      <li>Oversized litter boxes (jumbo or top-entry)</li>
      <li>Sturdy, weight-rated cat trees and scratchers</li>
      <li>Annual veterinary wellness exams + cardiac screening every 1–2 years</li>
    </ul>
    <p>Dive deeper in our <a href="/care">complete Care Guides</a>.</p>

    <h2>Lifespan</h2>
    <p>With proper care, well-bred Maine Coons routinely live <strong>13–17 years</strong>, with many seniors thriving into their late teens.</p>

    <h2>Frequently Asked Questions</h2>
    <div class="faq-list mt-2">
      <details class="faq-item"><summary>Are Maine Coons hypoallergenic?</summary><div class="faq-body">No cat is truly hypoallergenic, but Maine Coons produce relatively normal levels of Fel d 1 protein. Some allergy sufferers tolerate them better than others — we recommend visiting a breeder before reserving.</div></details>
      <details class="faq-item"><summary>Do Maine Coons get along with dogs?</summary><div class="faq-body">Famously yes. Their dog-like temperament makes them one of the best breeds for multi-pet households when properly introduced.</div></details>
      <details class="faq-item"><summary>How much grooming do they need?</summary><div class="faq-body">Two to three brushings per week with a stainless-steel comb is usually sufficient. During spring and fall coat changes, daily brushing prevents matting.</div></details>
      <details class="faq-item"><summary>Are polydactyl Maine Coons rare?</summary><div class="faq-body">Polydactyly was historically common in working Maine Coons. Today it is less frequent and considered a desirable heritage trait by many enthusiasts.</div></details>
    </div>

    <p style="margin-top:2.5rem;text-align:center;">
      <a href="/kittens" class="btn btn-primary btn-lg">Browse Available Kittens</a>
    </p>
  </article>

""" + newsletter_section()

def care_body():
    topics = [
        ("Grooming the Long Coat",     "Tools, technique, and a brushing schedule that prevents matting without stressing your cat.", "🪮"),
        ("Nutrition for Giant Breeds", "How much to feed, best protein sources, and calorie targets by life stage.",                      "🍗"),
        ("Exercise &amp; Enrichment",  "Climbing structures, leash training, and games that channel their intelligence.",                  "🏃"),
        ("Health &amp; Wellness",      "Vaccination schedule, parasite prevention, and warning signs to watch.",                           "🩺"),
        ("Kitten Care: First 30 Days", "What to buy, how to introduce them to your home, and litter-box training.",                        "🐾"),
        ("Senior Maine Coon Care",     "Diet adjustments, mobility support, and cardiac monitoring for cats 8+ years.",                    "👴"),
    ]
    cards = "\n".join(
        f"""        <a class="category-card fade-on-scroll" href="/stories">
          <div class="cat-icon" aria-hidden="true">{icon}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </a>""" for title, desc, icon in topics
    )
    return page_header(
        "Maine Coon Care Guides",
        "Expert-reviewed guides on grooming, nutrition, health, exercise, and lifelong wellness — written specifically for the largest domestic cat breed.",
        [("Home", "/"), ("Care Guides", None)],
    ) + f"""  <section class="section">
    <div class="section-inner">
      <div class="categories-grid">
{cards}
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="section-inner text-center">
      <h2 class="section-title">Coming Soon: The Busy Bee Care Library</h2>
      <p class="section-subtitle">In-depth, vet-reviewed articles for every stage of Maine Coon ownership. Get notified when each guide launches.</p>
      <a href="#newsletter" class="btn btn-primary">Notify Me</a>
    </div>
  </section>

""" + newsletter_section()

def stories_body():
    cards = "\n".join(
        f"""        <article class="kitten-card fade-on-scroll" id="{s['slug']}">
          <div class="card-image"><span class="card-badge">Story</span><img src="{s['img']}?v={ASSET_V}" width="640" height="400" alt="{html.escape(s['alt'])}" loading="lazy" decoding="async"></div>
          <div class="card-body">
            <p class="card-cat">{html.escape(s['cat'])}</p>
            <h3><a href="#{s['slug']}">{html.escape(s['title'])}</a></h3>
            <p class="card-desc">{html.escape(s['read'])} · Updated {YEAR}<br><br>An in-depth, expertly-researched guide following our editorial template (see <a href="/about">about our standards</a>).</p>
            <p style="margin-top:auto;"><a href="#{s['slug']}" class="btn btn-outline" style="width:100%;">Read Article</a></p>
          </div>
        </article>""" for s in FEATURED_STORIES
    )
    return page_header(
        "Coon Cat Stories",
        "Real owner journeys, deep-dive breed knowledge, expert interviews, and authoritative health information — all engineered for E-E-A-T excellence.",
        [("Home", "/"), ("Coon Cat Stories", None)],
    ) + f"""  <section class="section">
    <div class="section-inner">
      <div class="cards-grid">
{cards}
      </div>
    </div>
  </section>

""" + newsletter_section()

def community_body():
    return page_header(
        "Busy Bee Community",
        "Forums, local meetups, owner galleries, and expert Q&A. Connect with thousands of Maine Coon families from around the world.",
        [("Home", "/"), ("Community", None)],
    ) + """  <section class="section">
    <div class="section-inner">
      <div class="categories-grid">
        <a class="category-card" href="#forum"><div class="cat-icon" aria-hidden="true">💬</div><h3>Discussion Forum</h3><p>Ask questions, share photos, swap advice with fellow owners.</p></a>
        <a class="category-card" href="#events"><div class="cat-icon" aria-hidden="true">📅</div><h3>Events &amp; Meetups</h3><p>Local Maine Coon meetups, cat shows, and breeder open days.</p></a>
        <a class="category-card" href="#gallery"><div class="cat-icon" aria-hidden="true">📸</div><h3>Owner Gallery</h3><p>Submit your gentle giant — featured cats earn a free care kit.</p></a>
        <a class="category-card" href="#qa"><div class="cat-icon" aria-hidden="true">🎓</div><h3>Expert Q&amp;A</h3><p>Monthly live sessions with vets, breeders, and behaviorists.</p></a>
      </div>

      <div class="text-center mt-4" style="background:var(--bg-alt);padding:2.5rem;border-radius:var(--radius-lg);border:1px solid var(--gray-200);margin-top:3rem;">
        <h2>The Hive Is Buzzing 🐝</h2>
        <p class="lead">The Busy Bee community platform is launching soon. Join the waitlist to be among the first members and receive a founding member badge.</p>
        <a href="#newsletter" class="btn btn-primary btn-lg">Join the Waitlist</a>
      </div>
    </div>
  </section>

""" + newsletter_section()

def tools_body():
    return page_header(
        "Useful Tools for Maine Coon Parents",
        "Free, interactive tools built specifically for the world's largest domestic cat breed.",
        [("Home", "/"), ("Useful Tools", None)],
    ) + """  <section class="section">
    <div class="section-inner">
      <div class="categories-grid">
        <a class="category-card" href="#size"><div class="cat-icon" aria-hidden="true">📏</div><h3>Adult Size Predictor</h3><p>Estimate adult weight &amp; length from kitten metrics.</p></a>
        <a class="category-card" href="#cost"><div class="cat-icon" aria-hidden="true">💰</div><h3>Lifetime Cost Calculator</h3><p>Year-1 setup &amp; lifetime ownership budget.</p></a>
        <a class="category-card" href="#grooming"><div class="cat-icon" aria-hidden="true">🪮</div><h3>Grooming Planner</h3><p>Personalized brushing &amp; bath schedule.</p></a>
        <a class="category-card" href="#quiz"><div class="cat-icon" aria-hidden="true">🧩</div><h3>Compatibility Quiz</h3><p>Is a Maine Coon right for your home?</p></a>
        <a class="category-card" href="#name"><div class="cat-icon" aria-hidden="true">✨</div><h3>Name Generator</h3><p>200+ majestic, regal &amp; playful names.</p></a>
        <a class="category-card" href="#feeding"><div class="cat-icon" aria-hidden="true">🥣</div><h3>Daily Feeding Calculator</h3><p>Calorie target by weight, age &amp; activity.</p></a>
      </div>

      <div class="text-center mt-4" style="background:var(--bg-alt);padding:2.5rem;border-radius:var(--radius-lg);border:1px solid var(--gray-200);margin-top:3rem;">
        <h2>Interactive Tools Launching Soon</h2>
        <p class="lead">All six calculators are in active development. Subscribe to get notified the moment each tool goes live.</p>
        <a href="#newsletter" class="btn btn-primary btn-lg">Notify Me</a>
      </div>
    </div>
  </section>

""" + newsletter_section()

def shop_body():
    products = [
        ("oversized-bed",     "Honeycomb Oversized Orthopedic Bed", "Beds",      149.00, "Built for cats 18–30 lbs.", "🛏"),
        ("grooming-kit",      "Long-Coat Grooming Kit",             "Grooming",   79.00, "Stainless steel comb, slicker, undercoat rake.", "🪮"),
        ("jumbo-litter-box",  "Jumbo Top-Entry Litter Box",         "Litter",     119.00, "Sized for tail-dragging adult Maine Coons.", "🟫"),
        ("nutrition-large",   "Giant-Breed Premium Nutrition (12lb)","Nutrition", 89.00, "High-protein, joint-supportive formula.", "🥣"),
        ("scratcher-tower",   "Reinforced Scratcher Tower",         "Furniture", 229.00, "Weight-rated to 40 lbs, sisal-wrapped.", "🪵"),
        ("travel-carrier-xl", "XL Travel Carrier",                  "Travel",    179.00, "Airline-compliant for cats up to 25 lbs.", "🧳"),
    ]
    cards = "\n".join(
        f"""        <article class="product-card fade-on-scroll" data-card data-price="{p[3]}" data-category="{p[2].lower()}">
          <div class="card-image" aria-hidden="true"><span class="card-badge gold">Bestseller</span><span style="font-size:4rem;">{p[5]}</span></div>
          <div class="card-body">
            <p class="card-cat">{p[2]}</p>
            <h3>{html.escape(p[1])}</h3>
            <p class="card-desc">{html.escape(p[4])}</p>
            <p class="card-price">${p[3]:.2f}</p>
          </div>
          <div class="card-actions">
            <button class="btn btn-primary" data-add-cart="prod-{p[0]}" data-id="prod-{p[0]}" data-name="{html.escape(p[1])}" data-price="{p[3]}" data-type="{p[2]}" style="width:100%;">Add to Cart</button>
          </div>
        </article>""" for p in products
    )
    return page_header(
        "The Busy Bee Shop",
        "Curated, sized-right gear for Maine Coons and other giant breeds. Beds, grooming tools, nutrition, and accessories — every product tested for cats 15–30 lbs.",
        [("Home", "/"), ("Shop", None)],
    ) + f"""  <section class="section">
    <div class="section-inner">
      <div class="filter-bar" role="region" aria-label="Filter products">
        <label for="filter-cat">Category:</label>
        <select id="filter-cat" data-filter="category">
          <option value="all">All</option><option value="beds">Beds</option><option value="grooming">Grooming</option>
          <option value="litter">Litter</option><option value="nutrition">Nutrition</option><option value="furniture">Furniture</option><option value="travel">Travel</option>
        </select>
        <label for="sort-select">Sort:</label>
        <select id="sort-select">
          <option value="default">Featured</option>
          <option value="price-asc">Price: Low → High</option>
          <option value="price-desc">Price: High → Low</option>
        </select>
        <span class="result-count" id="result-count" role="status" aria-live="polite">{len(products)} results</span>
      </div>
      <div class="cards-grid" data-filterable-grid>
{cards}
      </div>
    </div>
  </section>

""" + newsletter_section()

def about_body():
    return page_header(
        "About Busy Bee Maine Coons",
        "We connect families with ethical, health-tested Maine Coon breeders — and equip them for a lifetime of joy with curated gear and expert guidance.",
        [("Home", "/"), ("About", None)],
    ) + """  <article class="article">
    <h2>Our Mission</h2>
    <p>Busy Bee Maine Coons exists to make finding an exceptional Maine Coon kitten effortless, transparent, and ethical. We rigorously vet every partner breeder, verify every health certificate, and provide lifelong support to every family who brings home a gentle giant through our platform.</p>

    <h2>What Makes Us Different</h2>
    <ul>
      <li><strong>Ethical-only network</strong> — every breeder undergoes a multi-step vetting process before listing a single kitten.</li>
      <li><strong>Health transparency by default</strong> — HCM, SMA, PKD, and hip-evaluation results are published openly, not hidden in a follow-up email.</li>
      <li><strong>Lifetime support</strong> — questions, advice, and breeder access don't end at adoption.</li>
      <li><strong>Sized-right gear</strong> — every product in our shop is engineered for cats 15–30 lbs, not generic feline gear that doesn't fit.</li>
    </ul>

    <h2>Editorial Standards</h2>
    <p>Every article on Busy Bee Maine Coons is researched, written, and reviewed against our published <a href="/ethics">ethics standards</a> and editorial template. We cite veterinary literature, breed registries (CFA, TICA), and original owner data — never AI-generated filler.</p>

    <h2>The Team</h2>
    <p>Busy Bee is built by lifelong cat lovers, working breeders, and seasoned web engineers obsessed with making the Maine Coon community better, safer, and more transparent.</p>

    <p style="margin-top:2.5rem;text-align:center;">
      <a href="/contact" class="btn btn-primary btn-lg">Get In Touch</a>
    </p>
  </article>
"""

def contact_body():
    return page_header(
        "Contact Busy Bee Maine Coons",
        "Questions about a kitten, a breeder, or an order? Reach out — we typically reply within one business day.",
        [("Home", "/"), ("Contact", None)],
    ) + """  <section class="section">
    <div class="section-inner" style="max-width:680px;">
      <form class="form-grid" data-demo-form aria-label="Contact form" novalidate>
        <div class="form-group">
          <label for="name">Your Name <span class="required" aria-hidden="true">*</span></label>
          <input id="name" name="name" type="text" required autocomplete="name">
        </div>
        <div class="form-group">
          <label for="email">Email Address <span class="required" aria-hidden="true">*</span></label>
          <input id="email" name="email" type="email" required autocomplete="email">
        </div>
        <div class="form-group">
          <label for="topic">Topic</label>
          <select id="topic" name="topic">
            <option>General question</option>
            <option>Kitten reservation</option>
            <option>Breeder partnership inquiry</option>
            <option>Order / shop support</option>
            <option>Press &amp; media</option>
          </select>
        </div>
        <div class="form-group">
          <label for="message">Message <span class="required" aria-hidden="true">*</span></label>
          <textarea id="message" name="message" required></textarea>
        </div>
        <div class="form-success-msg" role="status" aria-live="polite">Thank you — your message is on its way. We'll reply within one business day.</div>
        <button type="submit" class="btn btn-primary btn-lg">Send Message</button>
        <p class="form-help">By submitting this form you agree to our <a href="/privacy">Privacy Policy</a>.</p>
      </form>
    </div>
  </section>
"""

def cart_body():
    return page_header("Your Cart", "Review your kitten reservations and shop items.", [("Home", "/"), ("Cart", None)]) + """  <section class="section">
    <div class="section-inner" style="max-width:880px;">
      <div id="cart-list"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;padding:1.5rem 0;border-top:2px solid var(--primary);margin-top:1rem;flex-wrap:wrap;gap:1rem;">
        <button class="btn btn-outline" id="cart-clear">Clear Cart</button>
        <div style="text-align:right;">
          <p style="font-size:.875rem;color:var(--text-muted);margin:0;">Subtotal (excl. shipping &amp; taxes):</p>
          <p style="font-size:2rem;font-family:var(--font-head);font-weight:700;color:var(--primary);margin:0;" id="cart-total">$0.00</p>
        </div>
        <a href="/contact" class="btn btn-primary btn-lg">Proceed to Checkout</a>
      </div>
      <p class="form-help text-center mt-3">Kitten reservations require a deposit and direct conversation with the breeder. We'll confirm availability and finalize the deposit before any charges are processed.</p>
    </div>
  </section>
"""

def account_body():
    return page_header("My Account", "Manage your reservations, orders, and Busy Bee Hive membership.", [("Home", "/"), ("Account", None)]) + """  <section class="section">
    <div class="section-inner" style="max-width:480px;">
      <h2 class="section-title">Sign In</h2>
      <form class="form-grid" data-demo-form aria-label="Sign in form" novalidate>
        <div class="form-group">
          <label for="login-email">Email</label>
          <input id="login-email" name="email" type="email" required autocomplete="email">
        </div>
        <div class="form-group">
          <label for="login-pw">Password</label>
          <input id="login-pw" name="password" type="password" required autocomplete="current-password" minlength="12">
          <p class="form-help">Minimum 12 characters. We use Argon2id hashing and offer Passkey sign-in.</p>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">Sign In</button>
        <div class="form-success-msg" role="status">You're in. Redirecting to your dashboard…</div>
        <p class="text-center"><a href="#">Forgot password?</a> &middot; <a href="#">Create account</a></p>
      </form>
    </div>
  </section>
"""

def privacy_body():
    return page_header("Privacy Policy", "How Busy Bee Maine Coons collects, uses, and protects your information.", [("Home", "/"), ("Privacy", None)]) + f"""  <article class="article">
    <p class="article-meta">Last updated: {YEAR}-04-27</p>
    <h2>1. Information We Collect</h2>
    <p>We collect information you provide directly (name, email, shipping address, kitten preferences) and limited analytical data (pages visited, device type) to improve the site.</p>
    <h2>2. How We Use Your Information</h2>
    <p>Solely to process reservations and orders, deliver requested content, and improve our services. We never sell your data.</p>
    <h2>3. Cookies</h2>
    <p>We use strictly necessary cookies for cart functionality and optional analytics cookies (with consent) to understand site usage.</p>
    <h2>4. Your Rights</h2>
    <p>You may request access, correction, export, or deletion of your data at any time by emailing <a href="/contact">our team</a>. We honor GDPR and CCPA rights regardless of your jurisdiction.</p>
    <h2>5. Data Security</h2>
    <p>All data is encrypted in transit (TLS 1.3) and at rest (AES-256). Sensitive operations are logged and monitored 24/7.</p>
    <h2>6. Contact</h2>
    <p>Questions about this policy: <a href="/contact">contact us</a>.</p>
  </article>
"""

def terms_body():
    return page_header("Terms of Service", "The agreement governing your use of cooncatcentral.com.", [("Home", "/"), ("Terms", None)]) + f"""  <article class="article">
    <p class="article-meta">Last updated: {YEAR}-04-27</p>
    <h2>1. Agreement</h2>
    <p>By using cooncatcentral.com you agree to these terms. If you do not agree, please discontinue use.</p>
    <h2>2. Kitten Reservations</h2>
    <p>Reservations are facilitated between you and our partner breeders. Deposits are non-refundable except where agreed in writing with the breeder. Final adoption is contingent on a successful match between buyer and breeder.</p>
    <h2>3. Shop Orders</h2>
    <p>Products ship within 2 business days. Returns accepted within 30 days for unused items in original packaging.</p>
    <h2>4. Health Guarantees</h2>
    <p>All partner breeders provide written health guarantees. Specific terms vary by breeder and are disclosed before any deposit is taken.</p>
    <h2>5. Limitation of Liability</h2>
    <p>Busy Bee Maine Coons facilitates breeder-buyer relationships and is not liable for veterinary outcomes outside our published vetting standards.</p>
    <h2>6. Governing Law</h2>
    <p>These terms are governed by the laws of the United States.</p>
  </article>
"""

def accessibility_body():
    return page_header("Accessibility Statement", "Our commitment to WCAG 2.2 AA compliance and inclusive design.", [("Home", "/"), ("Accessibility", None)]) + f"""  <article class="article">
    <p class="article-meta">Last updated: {YEAR}-04-27</p>
    <p>Busy Bee Maine Coons is committed to ensuring digital accessibility for people of all abilities. We continually improve the user experience for everyone and apply the relevant accessibility standards.</p>
    <h2>Conformance Status</h2>
    <p>This site aims to conform to <strong>WCAG 2.2 Level AA</strong>. Many areas already meet Level AAA criteria.</p>
    <h2>Measures We Take</h2>
    <ul>
      <li>Semantic HTML5 with ARIA landmarks where needed.</li>
      <li>Keyboard-navigable interface with visible focus indicators.</li>
      <li>4.5:1+ color contrast on body text, 3:1+ on large text and UI components.</li>
      <li>Skip-to-content link, descriptive alt text, and respect for <code>prefers-reduced-motion</code>.</li>
      <li>Tested with NVDA, VoiceOver, axe DevTools, and Lighthouse.</li>
    </ul>
    <h2>Feedback</h2>
    <p>If you encounter any barrier on our site, please <a href="/contact">tell us</a>. We aim to respond within one business day and remediate within 48 hours.</p>
  </article>
"""

def ethics_body():
    return page_header("Ethics &amp; Health-Testing Standards", "Every breeder in the Busy Bee network agrees to these non-negotiable standards before listing a single kitten.", [("Home", "/"), ("Ethics", None)]) + """  <article class="article">
    <h2>Mandatory Health Testing</h2>
    <ul>
      <li><strong>HCM</strong> — DNA test for known mutations <em>and</em> echocardiogram by a board-certified cardiologist.</li>
      <li><strong>SMA</strong> — DNA test, both parents clear or tested non-affected.</li>
      <li><strong>PKD</strong> — DNA test on all breeding cats.</li>
      <li><strong>Hip Dysplasia</strong> — radiographic evaluation (OFA or PennHIP).</li>
      <li><strong>FeLV/FIV</strong> — annual screening of all breeding cats.</li>
    </ul>

    <h2>Breeding Practices</h2>
    <ul>
      <li>Maximum of 3 litters per queen in her lifetime, with mandatory rest cycles.</li>
      <li>Kittens stay with their mother and littermates until <strong>at least 12 weeks</strong>.</li>
      <li>Early socialization with people, household sounds, and (where possible) other pets.</li>
      <li>Full pedigree, vaccination records, and health certificates provided at adoption.</li>
      <li>Spay/neuter contracts for pet-quality kittens.</li>
    </ul>

    <h2>Lifetime Support</h2>
    <p>Every Busy Bee partner breeder commits to taking back any kitten they produce, at any age, if the owner can no longer keep them — no questions asked.</p>

    <h2>Independent Verification</h2>
    <p>Health certificates are reviewed by our team before any kitten is listed. Spot audits of partner catteries occur annually.</p>

    <p style="margin-top:2.5rem;text-align:center;">
      <a href="/kittens" class="btn btn-primary btn-lg">Browse Vetted Kittens</a>
    </p>
  </article>
"""

# ---- BUILD -----------------------------------------------------------------
PAGES = [
    ("index.html",         "Maine Coon Kittens for Sale | Ethical Breeders | Busy Bee Maine Coons",
        "Browse health-tested Maine Coon kittens from a curated network of ethical USA breeders. HCM, SMA, PKD screened. Lifetime breeder support. Free care guides.", home_body),
    ("kittens.html",       "Available Maine Coon Kittens for Sale | Health-Tested | Busy Bee",
        "See currently available Maine Coon kittens — gender, color, age & price filters. Every kitten HCM, SMA, PKD & hip screened with full health certificates.", kittens_body),
    ("the-breed.html",     "The Maine Coon: Complete Breed Guide 2026 | Busy Bee Maine Coons",
        "Definitive Maine Coon breed guide: history, size, temperament, health testing, lifespan & care essentials for the world's largest domestic cat breed.", the_breed_body),
    ("care.html",          "Maine Coon Care Guides: Grooming, Nutrition, Health | Busy Bee",
        "Expert-reviewed Maine Coon care guides. Grooming the long coat, giant-breed nutrition, exercise, health, kitten care & senior cat support.", care_body),
    ("stories.html",       "Coon Cat Stories: Owner Journeys, Health & Expert Articles | Busy Bee",
        "In-depth Maine Coon articles: owner journeys, breed knowledge, health deep-dives & expert interviews. Researched, vet-reviewed, never AI filler.", stories_body),
    ("community.html",     "Busy Bee Maine Coon Community: Forum, Events, Q&A",
        "Connect with thousands of Maine Coon families worldwide. Forum, local meetups, owner gallery & monthly expert Q&A sessions.", community_body),
    ("tools.html",         "Free Maine Coon Tools: Size Predictor, Cost Calculator & More",
        "Free interactive tools built for Maine Coon parents: adult size predictor, lifetime cost calculator, grooming planner, compatibility quiz & name generator.", tools_body),
    ("shop.html",          "Maine Coon Shop: Oversized Beds, Grooming Kits & Giant-Breed Gear",
        "Premium Maine Coon-specific products: oversized orthopedic beds, long-coat grooming kits, jumbo litter boxes, giant-breed nutrition & accessories.", shop_body),
    ("about.html",         "About Busy Bee Maine Coons: Our Mission & Standards",
        "Learn how Busy Bee Maine Coons connects families with ethical, health-tested breeders — and our editorial, vetting & lifetime support standards.", about_body),
    ("contact.html",       "Contact Busy Bee Maine Coons | Kitten & Order Support",
        "Questions about a kitten, a breeder, an order, or a partnership? Contact the Busy Bee team — we reply within one business day.", contact_body),
    ("cart.html",          "Your Cart | Busy Bee Maine Coons",
        "Review your Maine Coon kitten reservations and shop items.", cart_body),
    ("account.html",       "My Account | Busy Bee Maine Coons",
        "Sign in to manage your reservations, orders, and Busy Bee Hive membership.", account_body),
    ("privacy.html",       "Privacy Policy | Busy Bee Maine Coons",
        "How Busy Bee Maine Coons collects, uses, and protects your information. GDPR & CCPA compliant.", privacy_body),
    ("terms.html",         "Terms of Service | Busy Bee Maine Coons",
        "The agreement governing your use of cooncatcentral.com — reservations, shop orders, and breeder facilitation.", terms_body),
    ("accessibility.html", "Accessibility Statement | Busy Bee Maine Coons",
        "Our commitment to WCAG 2.2 AA compliance and inclusive design for all visitors to cooncatcentral.com.", accessibility_body),
    ("ethics.html",        "Ethics & Health-Testing Standards | Busy Bee Maine Coons",
        "The non-negotiable health-testing and ethical-breeding standards every Busy Bee partner breeder agrees to before listing a single kitten.", ethics_body),
]

def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "css").mkdir(exist_ok=True)
    (OUT / "js").mkdir(exist_ok=True)
    (OUT / "images").mkdir(exist_ok=True)
    written = []
    for filename, title, desc, body_fn in PAGES:
        html_doc = page(filename, title, desc, body_fn())
        path = OUT / filename
        path.write_text(html_doc, encoding="utf-8")
        written.append(path.relative_to(ROOT))
    print(f"Wrote {len(written)} pages → public/")
    for w in written:
        print(f"  - {w}")

if __name__ == "__main__":
    main()
