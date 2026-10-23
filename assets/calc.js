/* Cálculos puros. Sin dependencias. Se prueban con node. */
var SCF = (function (D) {
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function iso(y, m, d) { return y + "-" + pad(m) + "-" + pad(d); }
  function parseISO(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function idxDigit(d) { return d === 0 ? 9 : d - 1; } // orden DIAN 1..9,0

  // ---------- Calendario ----------
  // opts: { dos: "34", tipo: "pn"|"pj"|"gc", iva: ""|"bim"|"cuat", ret: bool, rst: bool }
  function vencimientos(opts) {
    var dos = String(opts.dos || "").replace(/\D/g, "");
    if (dos.length < 2) return [];
    dos = dos.slice(-2);
    var n2 = parseInt(dos, 10);        // 0..99
    var d1 = n2 % 10;                  // último dígito
    var i = idxDigit(d1);
    var out = [];
    var C = D.cal;
    function addMes(item, tipo, detalle) {
      var p = item.mes.split("-");
      out.push({ fecha: iso(+p[0], +p[1], item.dias[i]), tipo: tipo, detalle: detalle });
    }
    if (opts.rst) {
      C.rst_anticipo.forEach(function (it) { addMes(it, "Régimen Simple", "Anticipo bimestral " + it.periodo); });
      var pairIdx = Math.floor(i / 2);
      out.push({ fecha: iso(2026, 4, C.rst_anual.dias[pairIdx]), tipo: "Régimen Simple", detalle: "Declaración anual consolidada (año 2025)" });
      if (opts.iva) out.push({ fecha: iso(2026, 2, C.rst_iva_anual.dias[pairIdx]), tipo: "IVA (Régimen Simple)", detalle: "Declaración anual consolidada de IVA (año 2025)" });
    } else {
      if (opts.tipo === "pn") {
        var k = n2 === 0 ? 49 : Math.ceil(n2 / 2) - 1; // 01-02 → 0 … 99-00 → 49
        out.push({ fecha: C.renta_pn[k], tipo: "Renta personas naturales", detalle: "Declaración y pago (año gravable 2025)" });
      } else if (opts.tipo === "pj") {
        C.renta_pj.forEach(function (it) { addMes(it, it.tipo, it.detalle + " (año gravable 2025)"); });
      } else if (opts.tipo === "gc") {
        C.renta_gc.forEach(function (it) { addMes(it, it.tipo, it.detalle + " (año gravable 2025)"); });
      }
      if (opts.iva === "bim") C.iva_bim.forEach(function (it) { addMes(it, "IVA bimestral", "Período " + it.periodo); });
      if (opts.iva === "cuat") C.iva_cuat.forEach(function (it) { addMes(it, "IVA cuatrimestral", "Período " + it.periodo); });
    }
    if (opts.ret) C.retencion.forEach(function (it) { addMes(it, "Retención en la fuente", "Período " + it.periodo); });
    out.sort(function (a, b) { return a.fecha < b.fecha ? -1 : a.fecha > b.fecha ? 1 : 0; });
    return out;
  }

  // ---------- Utilidades ----------
  function redMil(v) { return Math.round(v / 1000) * 1000; }
  function diasEntre(a, b) { return Math.round((parseISO(b) - parseISO(a)) / 86400000); }
  function esUltimoDeFeb(dt) { var n = new Date(dt.getFullYear(), dt.getMonth(), dt.getDate() + 1); return dt.getMonth() === 1 && n.getMonth() === 2; }
  // Días comerciales 360, inclusivo (convención laboral colombiana)
  function dias360(a, b) {
    var A = parseISO(a), B = parseISO(b);
    if (B < A) return 0;
    var d1 = Math.min(A.getDate(), 30), d2 = Math.min(B.getDate(), 30);
    if (esUltimoDeFeb(B)) d2 = 30;
    if (esUltimoDeFeb(A)) d1 = 30;
    return (B.getFullYear() - A.getFullYear()) * 360 + (B.getMonth() - A.getMonth()) * 30 + (d2 - d1) + 1;
  }
  function mesesOFraccion(venc, pres) {
    var A = parseISO(venc), B = parseISO(pres);
    if (B <= A) return 0;
    var m = (B.getFullYear() - A.getFullYear()) * 12 + (B.getMonth() - A.getMonth());
    if (B.getDate() > A.getDate()) m += 1;
    return Math.max(m, 1);
  }

  // ---------- ¿Debo declarar renta? (art. 592, 593, 594-3 ET) ----------
  function debeDeclarar(ag, v) {
    var u = D.uvt[ag];
    var topes = [
      { k: "patrimonio", txt: "Patrimonio bruto al 31 de diciembre", uvt: 4500, val: v.patrimonio, regla: "mayor" },
      { k: "ingresos", txt: "Ingresos brutos del año", uvt: 1400, val: v.ingresos, regla: "mayorigual" },
      { k: "tarjeta", txt: "Consumos con tarjeta de crédito", uvt: 1400, val: v.tarjeta, regla: "mayor" },
      { k: "compras", txt: "Compras y consumos totales", uvt: 1400, val: v.compras, regla: "mayor" },
      { k: "consignaciones", txt: "Consignaciones, depósitos o inversiones", uvt: 1400, val: v.consignaciones, regla: "mayor" }
    ];
    var motivos = [];
    topes.forEach(function (t) {
      t.pesos = t.uvt * u;
      var x = +t.val || 0;
      t.supera = t.regla === "mayor" ? x > t.pesos : x >= t.pesos;
      if (t.supera) motivos.push(t.txt);
    });
    if (v.iva) motivos.push("Es responsable de IVA");
    return { uvt: u, topes: topes, debe: motivos.length > 0, motivos: motivos };
  }

  // ---------- Retención en la fuente por salarios, procedimiento 1 (arts. 383, 387, 388 ET) ----------
  var TABLA383 = [
    { desde: 0, hasta: 95, tarifa: 0, base: 0, mas: 0 },
    { desde: 95, hasta: 150, tarifa: 0.19, base: 95, mas: 0 },
    { desde: 150, hasta: 360, tarifa: 0.28, base: 150, mas: 10 },
    { desde: 360, hasta: 640, tarifa: 0.33, base: 360, mas: 69 },
    { desde: 640, hasta: 945, tarifa: 0.35, base: 640, mas: 162 },
    { desde: 945, hasta: 2300, tarifa: 0.37, base: 945, mas: 268 },
    { desde: 2300, hasta: Infinity, tarifa: 0.39, base: 2300, mas: 770 }
  ];
  function tabla383(baseUVT) {
    for (var j = 0; j < TABLA383.length; j++) {
      var r = TABLA383[j];
      if (baseUVT > r.desde && baseUVT <= r.hasta) return { rango: r, uvt: (baseUVT - r.base) * r.tarifa + r.mas };
    }
    return { rango: TABLA383[0], uvt: 0 };
  }
  function fsp(ibc) {
    var s = D.smmlv, x = ibc / s;
    if (x < 4) return 0;
    if (x < 16) return 0.01;
    if (x < 17) return 0.012;
    if (x < 18) return 0.014;
    if (x < 19) return 0.016;
    if (x < 20) return 0.018;
    return 0.02;
  }
  // v: { salario, otros, depend, vivienda, prepagada, voluntarios }
  function retencionSalarios(v) {
    var U = D.uvt[2026];
    var ingresos = (+v.salario || 0) + (+v.otros || 0);
    var ibc = Math.min(ingresos, 25 * D.smmlv);
    var salud = ibc * 0.04, pension = ibc * 0.04, solidaridad = ibc * fsp(ibc);
    var incr = salud + pension + solidaridad;
    var neto = ingresos - incr;
    var dDep = v.depend ? Math.min(ingresos * 0.10, 32 * U) : 0;
    var dViv = Math.min(+v.vivienda || 0, 100 * U);
    var dPre = Math.min(+v.prepagada || 0, 16 * U);
    var deducciones = dDep + dViv + dPre;
    var vol = Math.min(+v.voluntarios || 0, ingresos * 0.30, 3800 * U / 12);
    var sub = Math.max(neto - deducciones - vol, 0);
    var exenta25 = Math.min(sub * 0.25, 790 * U / 12);
    var totalBeneficios = deducciones + vol + exenta25;
    var limite = Math.min(neto * 0.40, 1340 * U / 12);
    var aplicados = Math.min(totalBeneficios, limite);
    var base = Math.max(neto - aplicados, 0);
    var baseUVT = base / U;
    var t = tabla383(baseUVT);
    var ret = t.uvt * U;
    return {
      ingresos: ingresos, salud: salud, pension: pension, solidaridad: solidaridad, incr: incr, neto: neto,
      dDep: dDep, dViv: dViv, dPre: dPre, vol: vol, exenta25: exenta25, totalBeneficios: totalBeneficios,
      limite: limite, aplicados: aplicados, base: base, baseUVT: baseUVT, rango: t.rango, retUVT: t.uvt, retencion: ret
    };
  }

  // ---------- Intereses de mora (arts. 634 y 635 ET) ----------
  function interesesMora(capital, venc, pago, tasaEA) {
    var dias = Math.max(diasEntre(venc, pago), 0);
    var anio = parseISO(pago).getFullYear();
    var base = (anio % 4 === 0 && (anio % 100 !== 0 || anio % 400 === 0)) ? 366 : 365;
    var interes = (+capital || 0) * (tasaEA / 100) / base * dias;
    return { dias: dias, base: base, interes: interes, redondeado: redMil(interes) };
  }

  // ---------- Sanción por extemporaneidad antes de emplazamiento (art. 641 ET) ----------
  function sancionExtemporaneidad(impuesto, venc, pres, anioSancionMinima) {
    var meses = mesesOFraccion(venc, pres);
    var imp = +impuesto || 0;
    var calculada = Math.min(imp * 0.05 * meses, imp);
    var minima = D.sancionMinima[anioSancionMinima || 2026];
    var sancion = Math.max(calculada, minima);
    return { meses: meses, calculada: calculada, minima: minima, sancion: redMil(sancion), aplicaMinima: calculada < minima };
  }

  // ---------- Prestaciones sociales (CST arts. 249, 306, 186; Ley 52 de 1975) ----------
  function prestaciones(salario, desde, hasta, conAux) {
    var sal = +salario || 0;
    var aux = conAux && sal <= 2 * D.smmlv ? D.auxTransporte : 0;
    var base = sal + aux;
    var dias = dias360(desde, hasta);
    var H = parseISO(hasta);
    var semIni = H.getMonth() < 6 ? iso(H.getFullYear(), 1, 1) : iso(H.getFullYear(), 7, 1);
    var desdePrima = desde > semIni ? desde : semIni;
    var diasPrima = dias360(desdePrima, hasta);
    var cesantias = base * dias / 360;
    var intereses = cesantias * dias * 0.12 / 360;
    var prima = base * diasPrima / 360;
    var vacaciones = sal * dias / 720;
    return { aux: aux, base: base, dias: dias, diasPrima: diasPrima, cesantias: cesantias, intereses: intereses, prima: prima, vacaciones: vacaciones, total: cesantias + intereses + prima + vacaciones };
  }

  return {
    vencimientos: vencimientos, debeDeclarar: debeDeclarar, retencionSalarios: retencionSalarios,
    interesesMora: interesesMora, sancionExtemporaneidad: sancionExtemporaneidad, prestaciones: prestaciones,
    dias360: dias360, mesesOFraccion: mesesOFraccion, diasEntre: diasEntre, redMil: redMil, tabla383: tabla383, TABLA383: TABLA383
  };
})(typeof SCF_DATA !== "undefined" ? SCF_DATA : require("./data.js"));
if (typeof module !== "undefined") module.exports = SCF;
