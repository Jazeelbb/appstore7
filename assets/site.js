// AppStore7 — menu do celular, animações ao rolar e vídeo com narração.
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

  // Vídeo do StoreBT: começa mudo em loop; o botão reinicia com a narração
  document.querySelectorAll("[data-ouvir]").forEach((botao) => {
    const video = botao.parentElement.querySelector("video[data-video-narrado]");
    if (!video) return;
    botao.addEventListener("click", () => {
      video.muted = false;
      video.loop = false;
      video.controls = true;
      video.currentTime = 0;
      video.play().catch(() => {});
      botao.hidden = true;
    });
  });
})();
