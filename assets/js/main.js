(() => {
  const doc = document;
  const root = doc.documentElement;

  // Footer year
  doc.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // Nav background + shift lights (scroll progress)
  const nav = doc.querySelector("[data-nav]");
  const leds = doc.querySelectorAll(".shift i");
  let ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    if (nav) nav.classList.toggle("is-scrolled", y > 8);
    if (leds.length) {
      const max = root.scrollHeight - window.innerHeight;
      const lit = max > 0 ? Math.round((Math.min(1, y / max)) * leds.length) : 0;
      leds.forEach((led, i) => led.classList.toggle("lit", i < lit));
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

  // Reveal on scroll
  const items = doc.querySelectorAll(".reveal");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!("IntersectionObserver" in window) || reduce) {
    items.forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -6% 0px", threshold: 0.06 }
    );
    items.forEach((el) => io.observe(el));
  }

  // Copy email
  doc.querySelectorAll("[data-copy]").forEach((btn) => {
    const label = btn.querySelector("[data-copy-label]");
    const original = label ? label.textContent : "";
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        if (label) {
          label.textContent = "Copied to clipboard";
          setTimeout(() => (label.textContent = original), 1800);
        }
      } catch {
        window.location.href = `mailto:${text}`;
      }
    });
  });

  // Session clock in the hero dash (time on page)
  const clock = doc.querySelector("[data-clock]");
  if (clock) {
    const start = Date.now();
    const pad = (n) => String(n).padStart(2, "0");
    const tick = () => {
      const s = Math.floor((Date.now() - start) / 1000);
      clock.textContent = `${pad(Math.floor(s / 60))}:${pad(s % 60)}`;
    };
    tick();
    setInterval(tick, 1000);
  }

  // Résumé: fall back to buttons when the browser has no inline PDF viewer
  const pdf = doc.querySelector("[data-pdf]");
  if (pdf && navigator.pdfViewerEnabled === false) pdf.classList.add("no-pdf");
})();
