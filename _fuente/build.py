#!/usr/bin/env python3
"""Genera el portal en dos versiones:
   site/    → sitio real para GitHub Pages (documentos completos, archivos separados)
   preview/ → vista previa privada (Artifact): CSS y JS en línea, logo como data URI
"""
import base64, json, os, shutil, html, hashlib
from pathlib import Path
import politica

ROOT = Path(__file__).parent
SRC = ROOT / "src"
SITE = ROOT / "site"
PREV = ROOT / "preview"
DOMAIN = "https://recursos.solucioncontableyfiscal.com"
MAIN = "https://solucioncontableyfiscal.com/"
AGENDA = "https://calendar.app.google/NaQe5qqNjgy27SrF7"
FORM_CONTACTO = "https://forms.gle/e7yWGi6NWT7gZv5R6"
FORM_FORMATOS = os.environ.get("FORM_FORMATOS", "#formatos-pendiente")
WA = "https://wa.me/573005074934"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,600..800&family=IBM+Plex+Mono:wght@500;600&family=Source+Sans+3:wght@400;600;700&display=swap">'

CSS = (SRC / "site.css").read_text()
DATA_JS = (SRC / "data.js").read_text()
CALC_JS = (SRC / "calc.js").read_text()
UI_JS = (SRC / "ui.js").read_text()
LOGO96 = base64.b64encode((ROOT / "assets/logo-96.png").read_bytes()).decode()
# Versión de los archivos para que el navegador no use una copia vieja después de publicar.
VER = hashlib.sha1((CSS + DATA_JS + CALC_JS + UI_JS).encode()).hexdigest()[:8]

ORG_LD = {
    "@context": "https://schema.org", "@type": "AccountingService",
    "name": "Solución Contable y Fiscal", "legalName": "SOLUCION CONTABLE Y FISCAL S.A.S.",
    "url": MAIN, "telephone": "+57 300 507 4934", "email": "solucontfisc@gmail.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Vía 40 #73-290, Edificio Mix, Oficina 612",
                "addressLocality": "Barranquilla", "addressRegion": "Atlántico", "postalCode": "080001", "addressCountry": "CO"},
    "areaServed": "CO",
    "sameAs": ["https://www.instagram.com/soluconfis/", "https://www.facebook.com/solucioncontableyfiscal.co/",
               "https://www.tiktok.com/@solucin.contable1", "https://www.youtube.com/channel/UC9xpKEirltQN0SBlPLFSmeg"],
}

def header(prefix, logo_src):
    p = prefix
    return f'''<header class="top"><div class="wrap">
  <a class="brand" href="{p}index.html"><img src="{logo_src}" alt="Logo de Solución Contable y Fiscal" width="40" height="40"><span><b>Recursos tributarios</b><small>Solución Contable y Fiscal</small></span></a>
  <nav class="nav" aria-label="Secciones">
    <a href="{p}index.html#calendario">Calendario</a><a href="{p}index.html#calculadoras">Calculadoras</a><a href="{p}index.html#indicadores">Indicadores</a><a href="{p}index.html#articulos">Artículos</a><a href="{p}index.html#formatos">Formatos</a>
  </nav>
  <a class="btn btn-primary" href="{AGENDA}" target="_blank" rel="noopener">Agenda tu cita</a>
</div></header>'''

def cta_footer(prefix):
    return f'''<section class="cta"><div class="wrap">
  <div><h2>¿Prefieres que lo hagamos por ti?</h2>
  <p>Llevamos tu contabilidad, presentamos tus declaraciones a tiempo y revisamos si puedes aprovechar los alivios vigentes. Atención presencial en Barranquilla y virtual en toda Colombia.</p></div>
  <div class="btns"><a class="btn btn-gold" href="{WA}" target="_blank" rel="noopener">Escríbenos por WhatsApp</a><a class="btn btn-ghost" href="{FORM_CONTACTO}" target="_blank" rel="noopener">Solicita asesoría</a></div>
</div></section>
<footer class="foot"><div class="wrap">
  <p>La información de este sitio es de referencia y no reemplaza la asesoría profesional. Fechas del Calendario Tributario 2026 de la DIAN (versión del 1 de julio de 2026). Tasas y valores actualizados al 22 de octubre de 2026.</p>
  <p>SOLUCION CONTABLE Y FISCAL S.A.S. · Vía 40 #73-290, Edificio Mix, Oficina 612, Barranquilla · WhatsApp <span class="num">300 507 4934</span> · solucontfisc@gmail.com · <a href="{MAIN}" target="_blank" rel="noopener">solucioncontableyfiscal.com</a> · <a href="{prefix}politica-de-datos.html">Política de tratamiento de datos</a></p>
</div></footer>'''

def mora_options():
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre"]
    out = []
    for i, m in enumerate(meses, 1):
        k = f"2026-{i:02d}"
        sel = " selected" if k == "2026-10" else ""
        out.append(f'<option value="{k}"{sel}>{m.capitalize()} 2026</option>')
    return "".join(out)

def index_body(prefix, logo_src):
    return header(prefix, logo_src) + f'''
<main>
<section class="hero" id="calendario"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">Calendario tributario 2026 · DIAN</span>
    <h1>¿Cuándo vencen tus impuestos?</h1>
    <p class="lede">Escribe los dos últimos dígitos de tu NIT y elige tus obligaciones. Te mostramos cada fecha de 2026 según el calendario oficial de la DIAN y puedes agregarla a tu Google Calendar.</p>
    <p class="note">Solo usamos los dos últimos dígitos y el cálculo se hace en tu navegador: no guardamos ni enviamos tu NIT.</p>
    <div class="checks"><a class="btn btn-ghost" href="#calculadoras">Ver calculadoras</a><a class="btn btn-ghost" href="{prefix}articulos/decreto-1419-2026-alivios-dian.html">Alivios hasta el 19 de noviembre</a></div>
  </div>
  <div class="cal-card">
    <form id="cal-form" class="cal-form" autocomplete="off">
      <div class="nit-row">
        <label class="field" for="cal-nit"><span>Dos últimos dígitos del NIT</span>
          <span class="nit-box"><input class="nit" id="cal-nit" name="cal-nit" inputmode="numeric" pattern="[0-9]*" maxlength="2" value="34" aria-describedby="nit-cap"></span></label>
        <p class="nit-cap" id="nit-cap">Ejemplo cargado: empresa con NIT terminado en 34, responsable de IVA y agente de retención. Cambia los datos por los tuyos.</p>
      </div>
      <div class="cal-grid2">
        <label class="field" for="cal-tipo"><span>Tipo de contribuyente</span>
          <select id="cal-tipo"><option value="pn">Persona natural</option><option value="pj" selected>Persona jurídica (empresa)</option><option value="gc">Gran contribuyente</option></select></label>
        <label class="field" for="cal-iva"><span>Responsable de IVA</span>
          <select id="cal-iva"><option value="">No soy responsable de IVA</option><option value="bim" selected>Sí, bimestral</option><option value="cuat">Sí, cuatrimestral</option></select></label>
      </div>
      <div class="checks">
        <label class="check" for="cal-ret"><input type="checkbox" id="cal-ret" checked> Soy agente de retención</label>
        <label class="check" for="cal-rst"><input type="checkbox" id="cal-rst"> Estoy en el Régimen Simple</label>
      </div>
    </form>
    <div class="next" id="cal-next" aria-live="polite"></div>
    <div id="cal-res"></div>
    <p class="note">Renta 2026 corresponde al año gravable 2025. Las declaraciones de activos en el exterior vencen en las mismas fechas de renta. El calendario 2027 se publica en diciembre.</p>
  </div>
</div></section>

<section class="section" id="indicadores"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Indicadores · actualizados al 22 de octubre de 2026</span><h2>Cifras que usas todos los meses</h2></div>
  <div class="ind-grid">
    <div class="ind"><span class="ind-k">UVT 2026</span><span class="ind-v">$52.374</span><span class="ind-s">Resolución DIAN 000238 de 2025</span></div>
    <div class="ind"><span class="ind-k">UVT 2025</span><span class="ind-v">$49.799</span><span class="ind-s">Resolución DIAN 000193 de 2024</span></div>
    <div class="ind"><span class="ind-k">Salario mínimo 2026</span><span class="ind-v">$1.750.905</span><span class="ind-s">Decreto 1469 de 2025 · el Consejo de Estado levantó su suspensión en julio de 2026</span></div>
    <div class="ind"><span class="ind-k">Auxilio de transporte 2026</span><span class="ind-v">$249.095</span><span class="ind-s">Decreto 1470 de 2025</span></div>
    <div class="ind"><span class="ind-k">Interés moratorio DIAN · octubre</span><span class="ind-v">26,59 %</span><span class="ind-s">Efectiva anual · tasa de usura menos 2 puntos (art. 635 ET)</span></div>
    <div class="ind"><span class="ind-k">Tasa de usura · octubre</span><span class="ind-v">28,59 %</span><span class="ind-s">Consumo y ordinario · Resolución Superfinanciera 1472 de 2026</span></div>
    <div class="ind"><span class="ind-k">Interés bancario corriente · octubre</span><span class="ind-v">19,06 %</span><span class="ind-s">Efectiva anual · consumo y ordinario</span></div>
    <div class="ind"><span class="ind-k">Sanción mínima 2026</span><span class="ind-v">$524.000</span><span class="ind-s">10 UVT · art. 639 ET</span></div>
    <div class="ind"><span class="ind-k">Tasa especial Decreto 1419</span><span class="ind-v">4,5 %</span><span class="ind-s">Efectiva anual · solo para alivios pagados hasta el 19 de noviembre de 2026</span></div>
  </div>
</div></section>

<section class="section" id="calculadoras"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Calculadoras gratuitas</span><h2>Haz la cuenta antes de pagar</h2><p class="lede">Cada calculadora muestra el paso a paso y la norma que aplica. Vienen con un ejemplo cargado: cambia los valores por los tuyos.</p></div>
  <div class="tablist" role="tablist" aria-label="Calculadoras">
    <button role="tab" id="t-rt" aria-controls="rt" aria-selected="true">Retención por salarios</button>
    <button role="tab" id="t-dd" aria-controls="dd" aria-selected="false" tabindex="-1">¿Debo declarar renta?</button>
    <button role="tab" id="t-mo" aria-controls="mo" aria-selected="false" tabindex="-1">Intereses de mora</button>
    <button role="tab" id="t-sa" aria-controls="sa" aria-selected="false" tabindex="-1">Sanción por extemporaneidad</button>
    <button role="tab" id="t-pr" aria-controls="pr" aria-selected="false" tabindex="-1">Prestaciones sociales</button>
    <button role="tab" id="t-uvt" aria-controls="uvt" aria-selected="false" tabindex="-1">Conversor de UVT</button>
  </div>

  <div class="panel" role="tabpanel" id="rt" aria-labelledby="t-rt">
    <form id="f-rt"><h3>Retención en la fuente por salarios</h3><p class="src">Procedimiento 1 · arts. 383, 387 y 388 ET · UVT 2026</p>
      <label class="field" for="rt-sal"><span>Salario del mes</span><input type="text" inputmode="numeric" data-money id="rt-sal" value="15.000.000"></label>
      <label class="field" for="rt-otros"><span>Otros pagos laborales del mes (horas extra, comisiones)</span><input type="text" inputmode="numeric" data-money id="rt-otros" value=""></label>
      <label class="check" for="rt-dep"><input type="checkbox" id="rt-dep"> Tengo dependientes económicos</label>
      <label class="field" for="rt-viv"><span>Intereses de crédito de vivienda (promedio mensual)</span><input type="text" inputmode="numeric" data-money id="rt-viv" value=""></label>
      <label class="field" for="rt-pre"><span>Medicina prepagada (pago mensual)</span><input type="text" inputmode="numeric" data-money id="rt-pre" value=""></label>
      <label class="field" for="rt-vol"><span>Aportes voluntarios a pensión o AFC del mes</span><input type="text" inputmode="numeric" data-money id="rt-vol" value=""></label>
      <p class="src">Salario ordinario. Los topes anuales se aplican en doceavas partes. No incluye salario integral ni pagos por indemnización.</p>
    </form>
    <div id="rt-res" aria-live="polite"></div>
  </div>

  <div class="panel" role="tabpanel" id="dd" aria-labelledby="t-dd" hidden>
    <form id="f-dd"><h3>¿Debo declarar renta?</h3><p class="src">Personas naturales residentes · arts. 592, 593 y 594-3 ET</p>
      <label class="field" for="dd-ag"><span>Año gravable</span><select id="dd-ag"><option value="2026" selected>2026 (se declara en 2027)</option><option value="2025">2025 (se declaró en 2026)</option></select></label>
      <label class="field" for="dd-pat"><span>Patrimonio bruto al 31 de diciembre</span><input type="text" inputmode="numeric" data-money id="dd-pat" value="180.000.000"></label>
      <label class="field" for="dd-ing"><span>Ingresos brutos del año</span><input type="text" inputmode="numeric" data-money id="dd-ing" value="80.000.000"></label>
      <label class="field" for="dd-tc"><span>Consumos con tarjeta de crédito</span><input type="text" inputmode="numeric" data-money id="dd-tc" value=""></label>
      <label class="field" for="dd-com"><span>Compras y consumos totales</span><input type="text" inputmode="numeric" data-money id="dd-com" value=""></label>
      <label class="field" for="dd-con"><span>Consignaciones, depósitos o inversiones</span><input type="text" inputmode="numeric" data-money id="dd-con" value=""></label>
      <label class="check" for="dd-iva"><input type="checkbox" id="dd-iva"> Soy responsable de IVA</label>
    </form>
    <div id="dd-res" aria-live="polite"></div>
  </div>

  <div class="panel" role="tabpanel" id="mo" aria-labelledby="t-mo" hidden>
    <form id="f-mo"><h3>Intereses de mora con la DIAN</h3><p class="src">Arts. 634 y 635 ET · interés simple diario con la tasa vigente al momento del pago</p>
      <label class="field" for="mo-cap"><span>Impuesto o retención en mora (capital)</span><input type="text" inputmode="numeric" data-money id="mo-cap" value="5.000.000"></label>
      <div class="cal-grid2">
        <label class="field" for="mo-venc"><span>Fecha de vencimiento</span><input type="date" id="mo-venc" value="2026-07-24"></label>
        <label class="field" for="mo-pago"><span>Fecha de pago</span><input type="date" id="mo-pago" value="2026-10-23" data-today></label>
      </div>
      <label class="field" for="mo-mes"><span>Mes del pago (define la tasa)</span><select id="mo-mes">{mora_options()}</select></label>
      <p class="src">Los intereses se calculan sobre el impuesto, no sobre las sanciones. La tasa de noviembre se publica a fin de mes.</p>
    </form>
    <div id="mo-res" aria-live="polite"></div>
  </div>

  <div class="panel" role="tabpanel" id="sa" aria-labelledby="t-sa" hidden>
    <form id="f-sa"><h3>Sanción por extemporaneidad</h3><p class="src">Antes de emplazamiento · art. 641 ET · con impuesto a cargo</p>
      <label class="field" for="sa-imp"><span>Impuesto a cargo de la declaración</span><input type="text" inputmode="numeric" data-money id="sa-imp" value="3.000.000"></label>
      <div class="cal-grid2">
        <label class="field" for="sa-venc"><span>Fecha de vencimiento</span><input type="date" id="sa-venc" value="2026-09-04"></label>
        <label class="field" for="sa-pres"><span>Fecha de presentación</span><input type="date" id="sa-pres" value="2026-10-23" data-today></label>
      </div>
      <p class="src">Puede reducirse al 50 % o al 75 % si cumples los requisitos del art. 640 ET. Si la declaración no tiene impuesto a cargo, la sanción se calcula sobre los ingresos: consúltanos.</p>
    </form>
    <div id="sa-res" aria-live="polite"></div>
  </div>

  <div class="panel" role="tabpanel" id="pr" aria-labelledby="t-pr" hidden>
    <form id="f-pr"><h3>Prestaciones sociales</h3><p class="src">Cesantías, intereses, prima y vacaciones · Código Sustantivo del Trabajo</p>
      <label class="field" for="pr-sal"><span>Salario mensual</span><input type="text" inputmode="numeric" data-money id="pr-sal" value="1.750.905"></label>
      <div class="cal-grid2">
        <label class="field" for="pr-ini"><span>Desde</span><input type="date" id="pr-ini" value="2026-01-01"></label>
        <label class="field" for="pr-fin"><span>Hasta</span><input type="date" id="pr-fin" value="2026-10-23" data-today></label>
      </div>
      <label class="check" for="pr-aux"><input type="checkbox" id="pr-aux" checked> Incluir auxilio de transporte (salario hasta 2 SMMLV)</label>
      <p class="src">Supone que no se han pagado cesantías ni tomado vacaciones en el período. Salario fijo, sin recargos ni comisiones.</p>
    </form>
    <div id="pr-res" aria-live="polite"></div>
  </div>

  <div class="panel" role="tabpanel" id="uvt" aria-labelledby="t-uvt" hidden>
    <form id="f-uvt"><h3>Conversor de UVT</h3><p class="src">Art. 868 ET</p>
      <label class="field" for="uvt-anio"><span>Año</span><select id="uvt-anio"><option value="2026" selected>2026 · $52.374</option><option value="2025">2025 · $49.799</option></select></label>
      <label class="field" for="uvt-pesos"><span>Pesos a UVT</span><input type="text" inputmode="numeric" data-money id="uvt-pesos" value="1.000.000"></label>
      <label class="field" for="uvt-uvt"><span>UVT a pesos</span><input type="number" step="0.01" min="0" id="uvt-uvt" value="10"></label>
    </form>
    <div id="uvt-res" aria-live="polite"></div>
  </div>
</div></section>

<section class="section" id="articulos"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Artículos</span><h2>Lo que cambió y lo que viene</h2></div>
  <div class="cards3">
    <a class="card" href="{prefix}articulos/decreto-1419-2026-alivios-dian.html"><span class="tag">Alivios DIAN</span><h3>Decreto 1419 de 2026: paga solo el 15 % de las sanciones hasta el 19 de noviembre</h3><p>Varios alivios del decreto del sismo aplican en todo el país. Quién puede usarlos y cuánto se ahorra.</p><span class="meta">23 de octubre de 2026 · 5 min</span><span class="go">Leer artículo</span></a>
    <a class="card" href="{prefix}articulos/vencimientos-noviembre-2026.html"><span class="tag">Calendario</span><h3>Vencimientos tributarios de noviembre de 2026</h3><p>Retención, IVA bimestral y anticipos del Régimen Simple vencen entre el 11 y el 25 de noviembre.</p><span class="meta">23 de octubre de 2026 · 3 min</span><span class="go">Leer artículo</span></a>
    <a class="card" href="{prefix}articulos/quien-debe-declarar-renta-2027.html"><span class="tag">Renta personas naturales</span><h3>¿Quién debe declarar renta en 2027 por el año 2026?</h3><p>Los topes en UVT y en pesos con la UVT de 2026, y qué revisar desde ya.</p><span class="meta">23 de octubre de 2026 · 4 min</span><span class="go">Leer artículo</span></a>
  </div>
</div></section>

<section class="section" id="formatos"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Formatos en Excel</span><h2>Plantillas listas para usar</h2><p class="lede">Gratis. Te pedimos tu nombre y tu WhatsApp; al enviar el formulario aparece el enlace de descarga.</p></div>
  <div class="cards3">
    <div class="card"><span class="tag">Excel · fórmulas</span><h3>Calendario tributario 2026 por NIT</h3><p>Escribe tus dos últimos dígitos y la hoja te muestra todas tus fechas de renta, IVA, retención y Régimen Simple.</p><a class="btn btn-primary" href="{FORM_FORMATOS}" target="_blank" rel="noopener">Descargar gratis</a></div>
    <div class="card"><span class="tag">Excel · fórmulas</span><h3>Retención en la fuente por salarios 2026</h3><p>Depuración completa del procedimiento 1 con los topes de 2026, para cada empleado.</p><a class="btn btn-primary" href="{FORM_FORMATOS}" target="_blank" rel="noopener">Descargar gratis</a></div>
    <div class="card"><span class="tag">Excel · fórmulas</span><h3>Liquidador de prestaciones sociales 2026</h3><p>Cesantías, intereses, prima y vacaciones con el salario mínimo y el auxilio de transporte de 2026.</p><a class="btn btn-primary" href="{FORM_FORMATOS}" target="_blank" rel="noopener">Descargar gratis</a></div>
  </div>
</div></section>
</main>
''' + cta_footer(prefix)

# ---------- Artículos ----------
def table(head, rows, num_cols=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = []
    for r in rows:
        tds = "".join(f'<td class="n">{c}</td>' if i in num_cols else f"<td>{c}</td>" for i, c in enumerate(r))
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'

ARTICLES = []

ARTICLES.append({
 "slug": "decreto-1419-2026-alivios-dian",
 "title": "Decreto 1419 de 2026: paga solo el 15 % de las sanciones hasta el 19 de noviembre",
 "desc": "Los alivios del Decreto 1419 de 2026 para deudas, omisiones y correcciones aplican en todo el país hasta el 19 de noviembre. Quién puede usarlos y cuánto se ahorra.",
 "tag": "Alivios DIAN", "min": 5,
 "body": f'''
<p>El 17 de septiembre de 2026 el Gobierno expidió el Decreto Legislativo 1419 por la emergencia del sismo del 10 de agosto. Aunque nació por el terremoto, <b>varios de sus alivios aplican en todo el país</b>, según el ABECÉ publicado por la DIAN. El plazo para usarlos vence el <b>19 de noviembre de 2026</b>.</p>

<h2>Alivios para contribuyentes de todo el país</h2>
<ul>
<li><b>Deudas en mora al 10 de agosto de 2026.</b> Pagas el 100 % del impuesto, solo el 15 % de las sanciones y su actualización, e intereses a una tasa del 4,5 % anual. La tasa normal en octubre es 26,59 %. (art. 9)</li>
<li><b>Declaraciones que debías haber presentado antes del 10 de agosto y no presentaste.</b> La sanción por extemporaneidad queda en el 15 % y los intereses se pagan al 4,5 %. (art. 10, num. 1)</li>
<li><b>Correcciones</b> de declaraciones presentadas hasta el 10 de agosto que aumentan el impuesto o disminuyen el saldo a favor: sanción por corrección del 15 % y sin intereses de mora. (art. 10, num. 2)</li>
<li><b>Obligaciones formales incumplidas</b>, como información exógena o precios de transferencia: sanción del 15 %. (art. 10, num. 4)</li>
<li><b>Procesos judiciales con la DIAN</b> con demanda presentada antes del 10 de agosto: conciliación pagando el 100 % del impuesto en discusión y el 15 % de las sanciones en primera instancia, o el 20 % en segunda. (art. 11)</li>
</ul>
<div class="box">En todos los casos la sanción que pagues no puede ser menor que la sanción mínima de 2026: <b class="num">$524.000</b> (10 UVT).</div>

<h2>Cuánto se ahorra: un ejemplo</h2>
<p>Ejemplo con cifras ficticias. Una empresa no presentó la declaración de IVA del período marzo–abril de 2026, que vencía el 26 de mayo. El impuesto es de $20.000.000 y la presenta y paga el 10 de noviembre de 2026, 168 días después.</p>
{table(["Concepto", "Sin el decreto", "Con el Decreto 1419"], [
  ["Impuesto", "$20.000.000", "$20.000.000"],
  ["Sanción por extemporaneidad (6 meses × 5 %)", "$6.000.000", "$900.000 (15 %)"],
  ["Intereses de mora, 168 días", "$2.448.000 (26,59 %)", "$414.000 (4,5 %)"],
  ["Total a pagar", "$28.448.000", "$21.314.000"],
], num_cols=(1, 2))}
<p>El ahorro en este ejemplo es de <b class="num">$7.134.000</b>. Para los intereses sin el decreto usamos la tasa de octubre; la de noviembre puede variar.</p>

<h2>Alivios solo para las zonas afectadas por el sismo</h2>
<p>Las facilidades de pago de hasta 24 meses sin garantía (hasta 36 meses con garantía personal si la deuda no supera 6.000 UVT) y la reprogramación de facilidades vigentes son solo para quienes tenían su domicilio fiscal en las zonas afectadas el 10 de agosto de 2026. Estas medidas no aplican a los grandes contribuyentes.</p>

<h2>Qué hacer antes del 19 de noviembre</h2>
<ol>
<li>Revisa en el portal de la DIAN si tienes obligaciones en mora, declaraciones sin presentar o correcciones pendientes con corte al 10 de agosto de 2026.</li>
<li>Calcula el impuesto, el 15 % de la sanción y los intereses al 4,5 % hasta la fecha de pago.</li>
<li>Presenta y paga dentro del plazo. Para estos alivios no se aceptan compensaciones como medio de pago.</li>
</ol>
<p>Es un decreto de emergencia, así que la Corte Constitucional lo revisa de forma automática. Mientras esté vigente, los alivios se pueden usar.</p>
<p class="sources">Fuentes: <a href="https://normograma.dian.gov.co/dian/compilacion/docs/decreto_1419_2026.htm" target="_blank" rel="noopener">Decreto Legislativo 1419 de 2026</a> · <a href="https://www.dian.gov.co/dian/Documents/Abece-beneficios-tributarios-Decreto-1419-de-2026.pdf" target="_blank" rel="noopener">ABECÉ de beneficios tributarios, DIAN</a>.</p>
'''})

ARTICLES.append({
 "slug": "vencimientos-noviembre-2026",
 "title": "Vencimientos tributarios de noviembre de 2026",
 "desc": "Retención en la fuente de octubre, IVA bimestral septiembre–octubre y anticipos del Régimen Simple vencen entre el 11 y el 25 de noviembre de 2026 según el último dígito del NIT.",
 "tag": "Calendario", "min": 3,
 "body": f'''
<p>En noviembre de 2026 coinciden tres obligaciones que dependen del <b>último dígito del NIT</b>: la retención en la fuente del mes de octubre, el IVA bimestral del período septiembre–octubre y el anticipo bimestral del Régimen Simple del mismo período. Las tres vencen el mismo día para cada dígito.</p>
{table(["Último dígito del NIT", "Fecha límite"], [
  ["1", "11 de noviembre"], ["2", "12 de noviembre"], ["3", "13 de noviembre"], ["4", "17 de noviembre"], ["5", "18 de noviembre"],
  ["6", "19 de noviembre"], ["7", "20 de noviembre"], ["8", "23 de noviembre"], ["9", "24 de noviembre"], ["0", "25 de noviembre"],
], num_cols=(0,))}
<p>Los festivos de noviembre son el lunes 2 y el lunes 16, por eso no hay vencimientos esos días.</p>

<h2>Otras fechas del mes</h2>
{table(["Fecha", "Obligación"], [
  ["3 de noviembre", "Actualización del Registro Único de Beneficiarios Finales (RUB), para quienes deben reportar cambios"],
  ["17 de noviembre", "Impuesto nacional a la gasolina y al ACPM, período octubre"],
  ["17 de noviembre", "Impuesto al carbono, bebidas ultraprocesadas azucaradas, IVA de prestadores de servicios desde el exterior y pagos anticipados de contribuyentes con presencia económica significativa, período septiembre–octubre"],
  ["19 de noviembre", "Último día para usar los alivios del Decreto 1419 de 2026"],
], num_cols=(0,))}

<h2>Dos recordatorios</h2>
<ul>
<li>La declaración de retención en la fuente presentada sin el pago total no produce efecto legal, salvo las excepciones del art. 580-1 del Estatuto Tributario.</li>
<li>Si pagas tarde, los intereses de mora se liquidan con la tasa vigente el día del pago. En octubre es 26,59 % efectiva anual. <a href="../index.html#mo" data-tab="mo">Calcula tus intereses</a>.</li>
</ul>
<p>¿Quieres ver todas tus fechas del año? Usa el <a href="../index.html#calendario">calendario por NIT</a>.</p>
<p class="sources">Fuente: <a href="https://www.dian.gov.co/Calendarios/Calendario_Tributario_2026.pdf" target="_blank" rel="noopener">Calendario Tributario 2026, DIAN</a>.</p>
'''})

ARTICLES.append({
 "slug": "quien-debe-declarar-renta-2027",
 "title": "¿Quién debe declarar renta en 2027 por el año 2026?",
 "desc": "Topes para declarar renta en 2027 por el año gravable 2026 con la UVT de 2026: patrimonio de $235.683.000 e ingresos de $73.323.600, entre otros.",
 "tag": "Renta personas naturales", "min": 4,
 "body": f'''
<p>La declaración de renta que se presenta en 2027 corresponde al <b>año gravable 2026</b>. Los topes se calculan con la UVT de 2026, que es de <b class="num">$52.374</b> según la Resolución DIAN 000238 de 2025.</p>

<h2>Los topes</h2>
<p>Una persona natural residente que no esté en el Régimen Simple debe declarar si en 2026 cumplió al menos una de estas condiciones:</p>
{table(["Condición en 2026", "Tope en UVT", "Tope en pesos"], [
  ["Patrimonio bruto al 31 de diciembre mayor a", "4.500", "$235.683.000"],
  ["Ingresos brutos iguales o superiores a", "1.400", "$73.323.600"],
  ["Consumos con tarjeta de crédito mayores a", "1.400", "$73.323.600"],
  ["Compras y consumos totales mayores a", "1.400", "$73.323.600"],
  ["Consignaciones, depósitos o inversiones mayores a", "1.400", "$73.323.600"],
], num_cols=(1, 2))}
<p>También debe declarar quien sea responsable de IVA, sin importar sus ingresos.</p>

<div class="box">Para comparar: por el año 2025 los topes eran de $224.095.500 en patrimonio y $69.718.600 en ingresos, con la UVT de $49.799.</div>

<h2>Qué revisar desde ya</h2>
<ul>
<li>Suma todos tus ingresos de 2026: salarios, honorarios, arriendos, dividendos e intereses.</li>
<li>Revisa tus extractos: los consumos con tarjeta y las consignaciones cuentan por separado de los ingresos.</li>
<li>Guarda los certificados de ingresos y retenciones, los de intereses de vivienda y los de medicina prepagada.</li>
<li>Aunque no estés obligado, declarar puede convenirte si te practicaron retenciones: podrías tener un saldo a favor para pedir en devolución.</li>
</ul>
<p>Las fechas de 2027 se conocen cuando la DIAN publique el calendario, normalmente en diciembre. Con el Decreto 2229 de 2023, las personas naturales declaran entre agosto y octubre según los dos últimos dígitos del NIT.</p>
<p><a href="../index.html#dd" data-tab="dd">Haz la prueba con la calculadora ¿Debo declarar renta?</a></p>
<p class="sources">Fuentes: arts. 592, 593 y 594-3 del <a href="https://normograma.dian.gov.co/dian/compilacion/docs/estatuto_tributario.htm" target="_blank" rel="noopener">Estatuto Tributario</a> · <a href="https://normograma.dian.gov.co/dian/compilacion/docs/resolucion_dian_0238_2025.htm" target="_blank" rel="noopener">Resolución DIAN 000238 de 2025</a>.</p>
'''})

def article_body(a, prefix, logo_src):
    return header(prefix, logo_src) + f'''
<main class="article"><div class="wrap">
  <a class="back" href="{prefix}index.html#articulos">← Todos los recursos</a>
  <span class="eyebrow" style="margin-top:18px">{a["tag"]}</span>
  <h1>{a["title"]}</h1>
  <p class="meta">Por Solución Contable y Fiscal · 23 de octubre de 2026 · {a["min"]} min de lectura</p>
  {a["body"]}
  <div class="box"><b>¿Necesitas ayuda con esto?</b> Escríbenos por <a href="{WA}" target="_blank" rel="noopener">WhatsApp al 300 507 4934</a> o <a href="{AGENDA}" target="_blank" rel="noopener">agenda una cita de 30 minutos</a>.</div>
</div></main>''' + cta_footer(prefix)

def policy_body(prefix, logo_src):
    return header(prefix, logo_src) + f'''
<main class="article"><div class="wrap">
  <a class="back" href="{prefix}index.html">← Volver al portal</a>
  <span class="eyebrow" style="margin-top:18px">Protección de datos</span>
  <h1>{politica.TITLE}</h1>
  <p class="meta">SOLUCION CONTABLE Y FISCAL S.A.S. · NIT <span class="num">902.118.737-1</span> · {politica.VERSION}</p>
  {politica.body_html()}
</div></main>''' + cta_footer(prefix)

TODAY_JS = '''(function(){var d=new Date(),s=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
document.querySelectorAll("input[data-today]").forEach(function(e){e.value=s;});
var m=document.getElementById("mo-mes");if(m){var k=s.slice(0,7);var ok=[].some.call(m.options,function(o){return o.value===k;});if(ok)m.value=k;}})();'''

def full_doc(title, desc, canonical, body, css_href, scripts, ld=None, og_type="website"):
    ldtag = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{DOMAIN}/assets/logo-512.png"><meta property="og:locale" content="es_CO">
<link rel="icon" href="{css_href.rsplit('/',1)[0]}/logo-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{css_href.rsplit('/',1)[0]}/logo-192.png">
{FONTS}
<link rel="stylesheet" href="{css_href}?v={VER}">
{ldtag}
</head>
<body>
{body}
{scripts}
</body>
</html>
'''

def build_site():
    if SITE.exists(): shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "articulos").mkdir()
    for f in ["logo-32.png", "logo-96.png", "logo-192.png", "logo-512.png"]:
        shutil.copy(ROOT / "assets" / f, SITE / "assets" / f)
    (SITE / "assets/site.css").write_text(CSS)
    (SITE / "assets/data.js").write_text(DATA_JS)
    (SITE / "assets/calc.js").write_text(CALC_JS)
    (SITE / "assets/ui.js").write_text(UI_JS)
    scripts = f'<script src="assets/data.js?v={VER}"></script><script src="assets/calc.js?v={VER}"></script><script>' + TODAY_JS + f'</script><script src="assets/ui.js?v={VER}"></script>'
    idx = full_doc("Calendario tributario 2026 y calculadoras | Solución Contable y Fiscal",
                   "Consulta tus fechas del calendario tributario 2026 con los dos últimos dígitos del NIT y usa calculadoras gratis de retención en la fuente, intereses de mora, sanciones y prestaciones sociales.",
                   DOMAIN + "/", index_body("", "assets/logo-96.png"), "assets/site.css", scripts, ORG_LD)
    (SITE / "index.html").write_text(idx)
    for a in ARTICLES:
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
              "datePublished": "2026-10-23", "inLanguage": "es-CO",
              "author": {"@type": "Organization", "name": "Solución Contable y Fiscal", "url": MAIN},
              "publisher": {"@type": "Organization", "name": "Solución Contable y Fiscal", "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/logo-512.png"}},
              "mainEntityOfPage": f"{DOMAIN}/articulos/{a['slug']}.html"}
        doc = full_doc(a["title"] + " | Solución Contable y Fiscal", a["desc"], f"{DOMAIN}/articulos/{a['slug']}.html",
                       article_body(a, "../", "../assets/logo-96.png"), "../assets/site.css", "", ld, "article")
        (SITE / "articulos" / f"{a['slug']}.html").write_text(doc)
    pdoc = full_doc(politica.TITLE + " | Solución Contable y Fiscal", politica.DESC, f"{DOMAIN}/{politica.SLUG}.html",
                    policy_body("", "assets/logo-96.png"), "assets/site.css", "")
    (SITE / f"{politica.SLUG}.html").write_text(pdoc)
    urls = [DOMAIN + "/"] + [f"{DOMAIN}/articulos/{a['slug']}.html" for a in ARTICLES] + [f"{DOMAIN}/{politica.SLUG}.html"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc><lastmod>2026-10-23</lastmod></url>\n" for u in urls) + "</urlset>\n"
    (SITE / "sitemap.xml").write_text(sm)
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    (SITE / "CNAME").write_text("recursos.solucioncontableyfiscal.com\n")
    (SITE / "formatos").mkdir()

def build_preview():
    if PREV.exists(): shutil.rmtree(PREV)
    (PREV / "articulos").mkdir(parents=True)
    logo = "data:image/png;base64," + LOGO96
    (PREV / f"{politica.SLUG}.html").write_text('<!doctype html>\n<html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>' + politica.TITLE + '</title>' + FONTS + "<style>" + CSS + "</style></head><body>" + policy_body("", logo) + "</body></html>")
    inline = "<script>" + DATA_JS + "</script><script>" + CALC_JS + "</script><script>" + TODAY_JS + "</script><script>" + UI_JS + "</script>"
    top = '<title>Recursos Tributarios SCF</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + FONTS + "\n<style>\n" + CSS + "\n</style>\n"
    (PREV / "index.html").write_text(top + index_body("", logo) + inline)
    for a in ARTICLES:
        doc = '<!doctype html>\n<html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>' + html.escape(a["title"]) + '</title>' + FONTS + "<style>" + CSS + "</style></head><body>" + article_body(a, "../", logo) + "</body></html>"
        (PREV / "articulos" / f"{a['slug']}.html").write_text(doc)

if __name__ == "__main__":
    build_site(); build_preview()
    print("ok", sorted(str(p.relative_to(ROOT)) for p in SITE.rglob("*") if p.is_file()))
