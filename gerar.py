# AppStore7 — monta as páginas finais (topo + conteúdo + rodapé) a partir de fonte/*.html
# e refaz o sitemap.xml. Rodar depois de editar qualquer arquivo em fonte/:
#   python gerar.py
# Cada arquivo de fonte/ começa com um comentário JSON: <!--{"titulo": ..., "descricao": ..., "menu": ...}-->
import json, pathlib, re, datetime

RAIZ = pathlib.Path(__file__).parent
SITE = "https://appstore7.com.br"
PUB = "ca-pub-2393598762421817"
GA4 = "G-80M1R3WVJ1"  # Google Analytics 4 (G-XXXXXXXXXX); vazio = sem Analytics
VERSAO = "8"  # sobe a cada publicação (cache do css/js)

MENU = [
    ("/", "Início", "inicio"),
    ("/#apps", "Apps", "apps"),
    ("guias.html", "Guias", "guias"),
    ("sobre.html", "Sobre", "sobre"),
    ("contato.html", "Contato", "contato"),
]

def analytics():
    if not GA4:
        return ""
    return f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>
  <script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag("js", new Date()); gtag("config", "{GA4}");</script>
"""

def cabeca(m, arquivo):
    url = f"{SITE}/" if arquivo == "index.html" else f"{SITE}/{arquivo}"
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="google-adsense-account" content="{PUB}" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}" crossorigin="anonymous"></script>
{analytics()}  <title>{m['titulo']}</title>
  <link rel="canonical" href="{url}" />
  <meta name="description" content="{m['descricao']}" />
  <meta property="og:title" content="{m['titulo']}" />
  <meta property="og:description" content="{m['descricao']}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta name="theme-color" content="#111111" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='32' fill='%23111111'/%3E%3Ctext x='32' y='44' font-size='34' font-family='Arial' font-weight='700' text-anchor='middle' fill='white'%3E7%3C/text%3E%3C/svg%3E" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,800..900&family=Inter:wght@400;500;600;700&display=swap" />
  <link rel="stylesheet" href="assets/site.css?v={VERSAO}" />
</head>
<body>
"""

def topo(ativo):
    itens = "\n".join(
        f'        <li><a href="{h}"{" aria-current=\"page\"" if c == ativo else ""}>{t}</a></li>'
        for h, t, c in MENU
    )
    return f"""  <header class="topo">
    <div class="envoltorio">
      <a class="marca" href="/"><span class="marca-icone">7</span>AppStore7</a>
      <button class="menu-botao" type="button" aria-label="Abrir menu" aria-expanded="false">☰</button>
      <ul class="menu">
{itens}
      </ul>
    </div>
  </header>
"""

RODAPE = """  <footer class="rodape">
    <div class="envoltorio">
      <div class="rodape-grade">
        <div>
          <a class="marca" href="/"><span class="marca-icone">7</span>AppStore7</a>
          <p>Ferramentas web feitas no Brasil para quem estuda para o ENEM, vende em marketplaces e organiza eventos.</p>
        </div>
        <div>
          <h4>Apps</h4>
          <ul>
            <li><a href="capigo.html">CapiGO</a></li>
            <li><a href="plpdanfe7.html">PLPDANFE7</a></li>
            <li><a href="storebt.html">StoreBT</a></li>
            <li><a href="dropstore7.html">DropStore7</a></li>
          </ul>
        </div>
        <div>
          <h4>AppStore7</h4>
          <ul>
            <li><a href="guias.html">Guias</a></li>
            <li><a href="sobre.html">Sobre</a></li>
            <li><a href="contato.html">Contato</a></li>
          </ul>
        </div>
        <div>
          <h4>Legal</h4>
          <ul>
            <li><a href="privacidade.html">Política de privacidade</a></li>
            <li><a href="termos.html">Termos de uso</a></li>
          </ul>
        </div>
      </div>
      <div class="rodape-base">
        <span>© <span data-ano>2026</span> AppStore7. Todos os direitos reservados.</span>
        <span>Feito no Brasil 🇧🇷</span>
      </div>
    </div>
  </footer>
  <script src="assets/site.js?v=%s"></script>
</body>
</html>
""" % VERSAO

def main():
    urls = []
    for fonte in sorted((RAIZ / "fonte").glob("*.html")):
        texto = fonte.read_text(encoding="utf-8")
        cab = re.match(r"\s*<!--(\{.*?\})-->\s*", texto, re.S)
        meta = json.loads(cab.group(1))
        corpo = texto[cab.end():]
        html = cabeca(meta, fonte.name) + topo(meta.get("menu", "")) + corpo + RODAPE
        (RAIZ / fonte.name).write_text(html, encoding="utf-8", newline="\n")
        urls.append((f"{SITE}/" if fonte.name == "index.html" else f"{SITE}/{fonte.name}", meta.get("prioridade", "0.7")))
    hoje = datetime.date.today().isoformat()
    linhas = "\n".join(f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod><priority>{p}</priority></url>" for u, p in sorted(urls, key=lambda x: -float(x[1])))
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n',
        encoding="utf-8", newline="\n")
    print(f"{len(urls)} páginas geradas")

if __name__ == "__main__":
    main()
