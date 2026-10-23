(function () {
  var D = SCF_DATA, S = SCF;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var nf = new Intl.NumberFormat("es-CO", { maximumFractionDigits: 0 });
  var nf2 = new Intl.NumberFormat("es-CO", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function pesos(v) { return (v < 0 ? "−$" : "$") + nf.format(Math.abs(Math.round(v))); }
  function num(el) { var s = String(el.value || "").replace(/[^\d]/g, ""); return s ? parseInt(s, 10) : 0; }
  var MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
  var MES3 = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  var DIAS = ["dom","lun","mar","mié","jue","vie","sáb"];
  function fechaObj(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function fechaLarga(s) { var d = fechaObj(s); return d.getDate() + " de " + MESES[d.getMonth()] + " de " + d.getFullYear(); }
  function hoyISO() { var d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }

  // Campos de dinero: separador de miles mientras se escribe
  $$("input[data-money]").forEach(function (el) {
    el.addEventListener("input", function () {
      var n = num(el);
      el.value = n ? nf.format(n) : "";
    });
  });

  // ---------- Calendario ----------
  var calForm = $("#cal-form");
  function gcalLink(v) {
    var d = v.fecha.replace(/-/g, "");
    var n = fechaObj(v.fecha); n.setDate(n.getDate() + 1);
    var d2 = n.getFullYear() + String(n.getMonth() + 1).padStart(2, "0") + String(n.getDate()).padStart(2, "0");
    var q = "action=TEMPLATE&text=" + encodeURIComponent("Vence: " + v.tipo) +
      "&dates=" + d + "/" + d2 +
      "&details=" + encodeURIComponent(v.detalle + ". Fecha según el Calendario Tributario DIAN 2026. Recursos: Solución Contable y Fiscal · WhatsApp 300 507 4934");
    return "https://calendar.google.com/calendar/render?" + q;
  }
  function renderCal() {
    var dos = $("#cal-nit").value.replace(/\D/g, "");
    var opts = {
      dos: dos,
      tipo: $("#cal-tipo").value,
      iva: $("#cal-iva").value,
      ret: $("#cal-ret").checked,
      rst: $("#cal-rst").checked
    };
    $("#cal-tipo").disabled = opts.rst;
    var box = $("#cal-res"), sum = $("#cal-next");
    if (dos.length < 2) {
      box.innerHTML = '<p class="hint">Escribe los dos últimos dígitos de tu NIT, sin el dígito de verificación.</p>';
      sum.innerHTML = "";
      return;
    }
    var list = S.vencimientos(opts);
    var hoy = hoyISO();
    var prox = list.filter(function (v) { return v.fecha >= hoy; })[0];
    if (prox) {
      var dias = S.diasEntre(hoy, prox.fecha);
      sum.innerHTML = '<span class="eyebrow">Tu próximo vencimiento</span>' +
        '<strong class="next-date">' + fechaLarga(prox.fecha) + '</strong>' +
        '<span class="next-what">' + prox.tipo + ' · ' + prox.detalle + '</span>' +
        '<span class="pill ' + (dias <= 7 ? "pill-urgent" : "pill-soon") + '">' + (dias === 0 ? "Vence hoy" : dias === 1 ? "Falta 1 día" : "Faltan " + dias + " días") + '</span>';
    } else {
      sum.innerHTML = '<span class="eyebrow">Tu próximo vencimiento</span><strong class="next-date">Sin vencimientos pendientes en 2026</strong><span class="next-what">El calendario 2027 se publica en diciembre.</span>';
    }
    if (!list.length) { box.innerHTML = '<p class="hint">Marca al menos una obligación.</p>'; return; }
    box.innerHTML = '<ol class="due-list">' + list.map(function (v) {
      var d = fechaObj(v.fecha), past = v.fecha < hoy, isNext = prox && v === prox;
      return '<li class="due' + (past ? " is-past" : "") + (isNext ? " is-next" : "") + '">' +
        '<time datetime="' + v.fecha + '"><span class="d">' + d.getDate() + '</span><span class="m">' + MES3[d.getMonth()] + ' ' + String(d.getFullYear()).slice(2) + '</span><span class="w">' + DIAS[d.getDay()] + '</span></time>' +
        '<div class="due-txt"><b>' + v.tipo + '</b><span>' + v.detalle + '</span></div>' +
        (past ? '<span class="due-st">Vencido</span>' : '<a class="due-add" href="' + gcalLink(v) + '" target="_blank" rel="noopener">Agregar a Google Calendar</a>') +
        '</li>';
    }).join("") + '</ol>';
  }
  if (calForm) {
    calForm.addEventListener("input", renderCal);
    calForm.addEventListener("change", renderCal);
    calForm.addEventListener("submit", function (e) { e.preventDefault(); renderCal(); });
    renderCal();
  }

  // ---------- Pestañas de calculadoras ----------
  var tabs = $$("[role=tab]");
  function openTab(id, focus) {
    tabs.forEach(function (t) {
      var on = t.getAttribute("aria-controls") === id;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    $$("[role=tabpanel]").forEach(function (p) { p.hidden = p.id !== id; });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { openTab(t.getAttribute("aria-controls")); });
    t.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        var j = (i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
        openTab(tabs[j].getAttribute("aria-controls"), true);
      }
    });
  });
  if (location.hash && $(location.hash) && $(location.hash).getAttribute("role") === "tabpanel") openTab(location.hash.slice(1));
  $$("a[data-tab]").forEach(function (a) { a.addEventListener("click", function () { openTab(a.getAttribute("data-tab")); }); });

  function rows(arr) {
    return '<dl class="ledger">' + arr.map(function (r) {
      return '<div class="' + (r[2] || "") + '"><dt>' + r[0] + '</dt><dd>' + r[1] + '</dd></div>';
    }).join("") + '</dl>';
  }

  // UVT
  function calcUVT() {
    var y = $("#uvt-anio").value, U = D.uvt[y];
    var p = num($("#uvt-pesos")), u = parseFloat(String($("#uvt-uvt").value).replace(",", ".")) || 0;
    $("#uvt-res").innerHTML = rows([
      ["Valor de la UVT " + y, pesos(U)],
      [nf.format(p) + " pesos equivalen a", nf2.format(p / U) + " UVT", "total"],
      [nf2.format(u) + " UVT equivalen a", pesos(u * U), "total"],
      ["Redondeado al múltiplo de mil (art. 868 ET)", pesos(S.redMil(u * U))]
    ]);
  }
  // ¿Debo declarar?
  function calcDeclarar() {
    var ag = $("#dd-ag").value;
    var r = S.debeDeclarar(ag, {
      patrimonio: num($("#dd-pat")), ingresos: num($("#dd-ing")), tarjeta: num($("#dd-tc")),
      compras: num($("#dd-com")), consignaciones: num($("#dd-con")), iva: $("#dd-iva").checked
    });
    var head = r.debe
      ? '<p class="verdict yes"><b>Sí debes declarar renta</b> por el año gravable ' + ag + '. Motivo: ' + r.motivos.join("; ") + '.</p>'
      : '<p class="verdict no"><b>Con estos datos no estarías obligado</b> a declarar por el año gravable ' + ag + '. Aun así, declarar puede convenirte si te practicaron retenciones.</p>';
    $("#dd-res").innerHTML = head + rows(r.topes.map(function (t) {
      return [t.txt + " · tope " + nf.format(t.uvt) + " UVT", pesos(t.pesos) + (t.supera ? " · <em>superado</em>" : ""), t.supera ? "flag" : ""];
    }));
  }
  // Retención
  function calcRet() {
    var r = S.retencionSalarios({
      salario: num($("#rt-sal")), otros: num($("#rt-otros")), depend: $("#rt-dep").checked,
      vivienda: num($("#rt-viv")), prepagada: num($("#rt-pre")), voluntarios: num($("#rt-vol"))
    });
    var tr = r.rango.tarifa ? "(" + nf2.format(r.baseUVT) + " − " + r.rango.base + ") × " + Math.round(r.rango.tarifa * 100) + " %" + (r.rango.mas ? " + " + r.rango.mas + " UVT" : "") : "0 %";
    $("#rt-res").innerHTML = rows([
      ["Ingresos laborales del mes", pesos(r.ingresos)],
      ["(−) Aporte obligatorio a salud 4 %", pesos(r.salud)],
      ["(−) Aporte obligatorio a pensión 4 %", pesos(r.pension)],
      ["(−) Fondo de solidaridad pensional", pesos(r.solidaridad)],
      ["Ingreso neto", pesos(r.neto), "sub"],
      ["(−) Dependientes (10 %, máx. 32 UVT)", pesos(r.dDep)],
      ["(−) Intereses de vivienda (máx. 100 UVT)", pesos(r.dViv)],
      ["(−) Medicina prepagada (máx. 16 UVT)", pesos(r.dPre)],
      ["(−) Aportes voluntarios / AFC", pesos(r.vol)],
      ["(−) Renta exenta 25 % (máx. 790 UVT al año)", pesos(r.exenta25)],
      ["Límite 40 % y 1.340 UVT al año", "se aplican " + pesos(r.aplicados) + " de " + pesos(r.totalBeneficios)],
      ["Base gravable", pesos(r.base) + " · " + nf2.format(r.baseUVT) + " UVT", "sub"],
      ["Tabla del art. 383 ET", tr],
      ["Retención del mes", pesos(r.retencion), "total"]
    ]);
  }
  // Intereses de mora
  function calcMora() {
    var mes = $("#mo-mes").value, tasa = D.moratorio[mes];
    var r = S.interesesMora(num($("#mo-cap")), $("#mo-venc").value, $("#mo-pago").value, tasa);
    var r45 = S.interesesMora(num($("#mo-cap")), $("#mo-venc").value, $("#mo-pago").value, 4.5);
    $("#mo-res").innerHTML = rows([
      ["Días de mora", nf.format(r.dias)],
      ["Tasa de interés moratorio (" + mes.split("-").reverse().join("/") + ")", nf2.format(tasa) + " % E.A."],
      ["Fórmula", "capital × tasa ÷ " + r.base + " × días"],
      ["Intereses de mora", pesos(r.interes), "sub"],
      ["Valor a pagar (redondeado a mil)", pesos(r.redondeado), "total"],
      ["Con la tasa del 4,5 % del Decreto 1419 (si aplicas, hasta el 19 nov 2026)", pesos(r45.redondeado)]
    ]);
  }
  // Sanción por extemporaneidad
  function calcSan() {
    var r = S.sancionExtemporaneidad(num($("#sa-imp")), $("#sa-venc").value, $("#sa-pres").value, 2026);
    $("#sa-res").innerHTML = rows([
      ["Meses o fracción de retraso", nf.format(r.meses)],
      ["5 % del impuesto por cada mes (tope 100 %)", pesos(r.calculada)],
      ["Sanción mínima 2026 (10 UVT)", pesos(r.minima)],
      ["Sanción a pagar" + (r.aplicaMinima ? " · aplica la mínima" : ""), pesos(r.sancion), "total"],
      ["Con la reducción al 15 % del Decreto 1419 (omisos al 10 ago 2026)", pesos(Math.max(S.redMil(r.calculada * 0.15), r.minima))]
    ]);
  }
  // Prestaciones
  function calcPre() {
    var r = S.prestaciones(num($("#pr-sal")), $("#pr-ini").value, $("#pr-fin").value, $("#pr-aux").checked);
    $("#pr-res").innerHTML = rows([
      ["Días trabajados (año de 360 días)", nf.format(r.dias)],
      ["Auxilio de transporte incluido", r.aux ? pesos(r.aux) : "No aplica (salario > 2 SMMLV)"],
      ["Cesantías", pesos(r.cesantias)],
      ["Intereses sobre cesantías (12 % anual)", pesos(r.intereses)],
      ["Prima de servicios del semestre (" + r.diasPrima + " días)", pesos(r.prima)],
      ["Vacaciones (15 días hábiles por año)", pesos(r.vacaciones)],
      ["Total estimado", pesos(r.total), "total"]
    ]);
  }
  var calcs = { "f-uvt": calcUVT, "f-dd": calcDeclarar, "f-rt": calcRet, "f-mo": calcMora, "f-sa": calcSan, "f-pr": calcPre };
  Object.keys(calcs).forEach(function (id) {
    var f = document.getElementById(id);
    if (!f) return;
    f.addEventListener("input", calcs[id]);
    f.addEventListener("change", calcs[id]);
    f.addEventListener("submit", function (e) { e.preventDefault(); calcs[id](); });
    calcs[id]();
  });
})();
