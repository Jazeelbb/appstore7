// AppStore7 — menu do celular, animações ao rolar e demonstrações interativas.
(function () {
  "use strict";

  // Menu do celular
  const botao = document.querySelector(".menu-botao");
  const menu = document.querySelector(".menu");
  if (botao && menu) {
    botao.addEventListener("click", () => {
      const aberto = menu.classList.toggle("aberto");
      botao.setAttribute("aria-expanded", String(aberto));
    });
  }

  // Revelar ao rolar
  const alvos = document.querySelectorAll(".revelar");
  if ("IntersectionObserver" in window) {
    const obs = new IntersectionObserver((itens) => {
      itens.forEach((i) => { if (i.isIntersecting) { i.target.classList.add("visivel"); obs.unobserve(i.target); } });
    }, { threshold: 0.12 });
    alvos.forEach((a) => obs.observe(a));
  } else {
    alvos.forEach((a) => a.classList.add("visivel"));
  }

  // Ano no rodapé
  document.querySelectorAll("[data-ano]").forEach((e) => { e.textContent = new Date().getFullYear(); });

  // QR Code ilustrativo (desenho, não é um código de verdade)
  document.querySelectorAll("svg.qr").forEach((svg) => {
    const n = 25, ns = "http://www.w3.org/2000/svg";
    svg.setAttribute("viewBox", `0 0 ${n} ${n}`);
    let semente = 7;
    const sorte = () => (semente = (semente * 9301 + 49297) % 233280) / 233280;
    const quadrado = (x, y) => {
      const r = document.createElementNS(ns, "rect");
      r.setAttribute("x", x); r.setAttribute("y", y); r.setAttribute("width", 1); r.setAttribute("height", 1);
      svg.append(r);
    };
    const localizador = (ox, oy) => {
      for (let y = 0; y < 7; y++) for (let x = 0; x < 7; x++) {
        const borda = x === 0 || y === 0 || x === 6 || y === 6;
        const miolo = x >= 2 && x <= 4 && y >= 2 && y <= 4;
        if (borda || miolo) quadrado(ox + x, oy + y);
      }
    };
    localizador(0, 0); localizador(n - 7, 0); localizador(0, n - 7);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      const naCanto = (x < 8 && y < 8) || (x >= n - 8 && y < 8) || (x < 8 && y >= n - 8);
      if (!naCanto && sorte() > 0.52) quadrado(x, y);
    }
  });

  // Demonstração do StoreBT: telas do celular que se alternam
  document.querySelectorAll("[data-demo-celular]").forEach((demo) => {
    const telas = [...demo.querySelectorAll(".tela")];
    const pontos = demo.querySelector(".pontos-tela");
    const legenda = demo.querySelector(".demo-legenda");
    let atual = 0, timer = null;
    const ir = (i) => {
      atual = (i + telas.length) % telas.length;
      telas.forEach((t, k) => t.classList.toggle("ativa", k === atual));
      [...pontos.children].forEach((p, k) => p.classList.toggle("ativo", k === atual));
      if (legenda) legenda.textContent = telas[atual].dataset.legenda || "";
    };
    telas.forEach((t, k) => {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", t.dataset.legenda || `Tela ${k + 1}`);
      b.addEventListener("click", () => { ir(k); reiniciar(); });
      pontos.append(b);
    });
    const reiniciar = () => { clearInterval(timer); timer = setInterval(() => ir(atual + 1), 3200); };
    ir(0); reiniciar();
  });
})();
