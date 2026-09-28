(() => {
  const doc = document;
  const root = doc.documentElement;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const EASE = "cubic-bezier(0.22, 0.8, 0.2, 1)";

  // Footer year
  doc.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // Nav background + scroll progress bar
  const nav = doc.querySelector("[data-nav]");
  const bar = doc.querySelector(".progress span");
  let ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    if (nav) nav.classList.toggle("is-scrolled", y > 8);
    if (bar) {
      const max = root.scrollHeight - window.innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? Math.min(1, y / max) : 0})`;
    }
    ticking = false;
  };
  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(onScroll);
      }
    },
    { passive: true }
  );
  onScroll();

  // Mobile menu
  const toggle = doc.querySelector(".nav-toggle");
  const menu = doc.getElementById("nav-menu");
  const setMenu = (open) => {
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", String(open));
    doc.body.classList.toggle("menu-open", open);
  };
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", (e) => {
      if (e.target.closest("a")) setMenu(false);
    });
    doc.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && doc.body.classList.contains("menu-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 801px)").addEventListener("change", (m) => {
      if (m.matches) setMenu(false);
    });
  }

  // Illustrations draw themselves in, line by line
  const drawArt = (svg) => {
    if (reduce || svg.dataset.drawn) return;
    svg.dataset.drawn = "1";
    const shapes = svg.querySelectorAll("path, line, polyline, rect, circle");
    let n = 0;
    shapes.forEach((el) => {
      if (el.closest("defs, .flow") || el.classList.contains("dim") || !el.getTotalLength) return;
      let len = 0;
      try {
        len = el.getTotalLength();
      } catch {
        return;
      }
      if (!len) return;
      el.style.strokeDasharray = len;
      el.style.strokeDashoffset = len;
      el.getBoundingClientRect();
      el.style.transition = `stroke-dashoffset 1.3s ${EASE} ${Math.min(n * 28, 700)}ms`;
      el.style.strokeDashoffset = "0";
      el.addEventListener(
        "transitionend",
        () => {
          el.style.strokeDasharray = "";
          el.style.strokeDashoffset = "";
          el.style.transition = "";
        },
        { once: true }
      );
      n += 1;
    });
    svg.querySelectorAll("text").forEach((t) => {
      t.style.opacity = "0";
      requestAnimationFrame(() => requestAnimationFrame(() => (t.style.opacity = "")));
    });
  };

  // Reveal on scroll (and start the drawing when a card comes into view)
  const items = doc.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || reduce) {
    items.forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("in");
          entry.target.querySelectorAll("[data-draw]").forEach(drawArt);
          io.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    items.forEach((el) => io.observe(el));
  }

  // Soft spotlight that follows the pointer across project cards
  doc.querySelectorAll("a.card").forEach((card) => {
    const art = card.querySelector(".card-art");
    if (!art) return;
    card.addEventListener("pointermove", (e) => {
      const r = art.getBoundingClientRect();
      art.style.setProperty("--mx", `${e.clientX - r.left}px`);
      art.style.setProperty("--my", `${e.clientY - r.top}px`);
    });
  });

  // Experience accordion: animate open / close
  doc.querySelectorAll("details.acc").forEach((d) => {
    const summary = d.querySelector("summary");
    const body = d.querySelector(".acc-body");
    if (!summary || !body || reduce || !body.animate) return;
    let anim = null;
    summary.addEventListener("click", (e) => {
      e.preventDefault();
      if (anim) anim.cancel();
      if (d.open && !d.classList.contains("closing")) {
        d.classList.add("closing");
        anim = body.animate(
          [{ height: `${body.offsetHeight}px`, opacity: 1 }, { height: "0px", opacity: 0 }],
          { duration: 320, easing: EASE }
        );
        anim.onfinish = () => {
          d.open = false;
          d.classList.remove("closing");
          anim = null;
        };
      } else {
        d.classList.remove("closing");
        d.open = true;
        anim = body.animate(
          [{ height: "0px", opacity: 0 }, { height: `${body.offsetHeight}px`, opacity: 1 }],
          { duration: 420, easing: EASE }
        );
        anim.onfinish = () => (anim = null);
      }
    });
  });

  // Copy email
  doc.querySelectorAll("[data-copy]").forEach((btn) => {
    const label = btn.querySelector("[data-copy-label]");
    const original = label ? label.textContent : "";
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        if (label) {
          label.textContent = "Copied!";
          setTimeout(() => (label.textContent = original), 1800);
        }
      } catch {
        window.location.href = `mailto:${text}`;
      }
    });
  });

  // Résumé: fall back to buttons when the browser has no inline PDF viewer
  const pdf = doc.querySelector("[data-pdf]");
  if (pdf && navigator.pdfViewerEnabled === false) pdf.classList.add("no-pdf");
})();
