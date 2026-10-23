/* Datos oficiales. Actualizado: 22 de octubre de 2026.
   Fuentes: Calendario Tributario 2026 DIAN (versión 1-jul-2026, Decreto 2229 de 2023),
   Res. DIAN 000238/2025 (UVT 2026), Res. DIAN 000193/2024 (UVT 2025),
   Decretos 1469 y 1470 de 2025 (SMMLV y auxilio de transporte 2026),
   Res. SFC 1472/2026 (usura octubre 2026), art. 635 ET. */
var SCF_DATA = {
  actualizado: "22 de octubre de 2026",
  uvt: { 2025: 49799, 2026: 52374 },
  smmlv: 1750905,
  auxTransporte: 249095,
  usura: { mes: "octubre de 2026", ea: 28.59, ibc: 19.06 },
  // Interés moratorio tributario (usura consumo y ordinario − 2 puntos), vigente al momento del pago
  moratorio: {
    "2026-01": 22.36, "2026-02": 23.23, "2026-03": 23.52, "2026-04": 24.76,
    "2026-05": 26.17, "2026-06": 26.79, "2026-07": 26.79, "2026-08": 27.66,
    "2026-09": 27.24, "2026-10": 26.59
  },
  moratorioVigente: "2026-10",
  sancionMinima: { 2026: 524000 },
  // Dígitos en orden 1,2,3,4,5,6,7,8,9,0 → índice 0..9
  cal: {
    renta_gc: [
      { tipo: "Renta grandes contribuyentes", detalle: "Pago 1.ª cuota", mes: "2026-02", dias: [10,11,12,13,16,17,18,19,20,23] },
      { tipo: "Renta grandes contribuyentes", detalle: "Declaración y pago 2.ª cuota", mes: "2026-04", dias: [13,14,15,16,20,21,22,23,24,27] },
      { tipo: "Renta grandes contribuyentes", detalle: "Pago 3.ª cuota", mes: "2026-06", dias: [10,11,12,16,17,18,19,22,23,24] }
    ],
    renta_pj: [
      { tipo: "Renta personas jurídicas", detalle: "Declaración y pago 1.ª cuota", mes: "2026-05", dias: [12,13,14,15,19,20,21,22,25,26] },
      { tipo: "Renta personas jurídicas", detalle: "Pago 2.ª cuota", mes: "2026-07", dias: [9,10,14,15,16,17,21,22,23,24] }
    ],
    // Personas naturales: pares de los dos últimos dígitos (01-02 … 99-00) → fecha
    renta_pn: [
      "2026-08-12","2026-08-13","2026-08-14","2026-08-18","2026-08-19","2026-08-20","2026-08-21","2026-08-24","2026-08-25","2026-08-26",
      "2026-08-27","2026-08-28","2026-08-31",
      "2026-09-01","2026-09-02","2026-09-03","2026-09-04","2026-09-07","2026-09-08","2026-09-09","2026-09-10","2026-09-11","2026-09-14",
      "2026-09-15","2026-09-16","2026-09-17","2026-09-18","2026-09-21","2026-09-22","2026-09-23","2026-09-24","2026-09-25","2026-09-28",
      "2026-10-01","2026-10-02","2026-10-05","2026-10-06","2026-10-07","2026-10-08","2026-10-09","2026-10-13","2026-10-14","2026-10-15",
      "2026-10-16","2026-10-19","2026-10-20","2026-10-21","2026-10-22","2026-10-23","2026-10-26"
    ],
    iva_bim: [
      { periodo: "enero–febrero", mes: "2026-03", dias: [10,11,12,13,16,17,18,19,20,24] },
      { periodo: "marzo–abril", mes: "2026-05", dias: [12,13,14,15,19,20,21,22,25,26] },
      { periodo: "mayo–junio", mes: "2026-07", dias: [9,10,14,15,16,17,21,22,23,24] },
      { periodo: "julio–agosto", mes: "2026-09", dias: [9,10,11,14,15,16,17,18,21,22] },
      { periodo: "septiembre–octubre", mes: "2026-11", dias: [11,12,13,17,18,19,20,23,24,25] },
      { periodo: "noviembre–diciembre", mes: "2027-01", dias: [13,14,15,18,19,20,21,22,25,26] }
    ],
    iva_cuat: [
      { periodo: "enero–abril", mes: "2026-05", dias: [12,13,14,15,19,20,21,22,25,26] },
      { periodo: "mayo–agosto", mes: "2026-09", dias: [9,10,11,14,15,16,17,18,21,22] },
      { periodo: "septiembre–diciembre", mes: "2027-01", dias: [13,14,15,18,19,20,21,22,25,26] }
    ],
    retencion: [
      { periodo: "enero", mes: "2026-02", dias: [10,11,12,13,16,17,18,19,20,23] },
      { periodo: "febrero", mes: "2026-03", dias: [10,11,12,13,16,17,18,19,20,24] },
      { periodo: "marzo", mes: "2026-04", dias: [13,14,15,16,20,21,22,23,24,27] },
      { periodo: "abril", mes: "2026-05", dias: [12,13,14,15,19,20,21,22,25,26] },
      { periodo: "mayo", mes: "2026-06", dias: [10,11,12,16,17,18,19,22,23,24] },
      { periodo: "junio", mes: "2026-07", dias: [9,10,14,15,16,17,21,22,23,24] },
      { periodo: "julio", mes: "2026-08", dias: [12,13,14,18,19,20,21,24,25,26] },
      { periodo: "agosto", mes: "2026-09", dias: [9,10,11,14,15,16,17,18,21,22] },
      { periodo: "septiembre", mes: "2026-10", dias: [9,13,14,15,16,19,20,21,22,23] },
      { periodo: "octubre", mes: "2026-11", dias: [11,12,13,17,18,19,20,23,24,25] },
      { periodo: "noviembre", mes: "2026-12", dias: [10,11,14,15,16,17,18,21,22,23] },
      { periodo: "diciembre", mes: "2027-01", dias: [13,14,15,18,19,20,21,22,25,26] }
    ],
    rst_anticipo: [
      { periodo: "enero–febrero", mes: "2026-05", dias: [12,13,14,15,19,20,21,22,25,26] },
      { periodo: "marzo–abril", mes: "2026-06", dias: [10,11,12,16,17,18,19,22,23,24] },
      { periodo: "mayo–junio", mes: "2026-07", dias: [9,10,14,15,16,17,21,22,23,24] },
      { periodo: "julio–agosto", mes: "2026-09", dias: [9,10,11,14,15,16,17,18,21,22] },
      { periodo: "septiembre–octubre", mes: "2026-11", dias: [11,12,13,17,18,19,20,23,24,25] },
      { periodo: "noviembre–diciembre", mes: "2027-01", dias: [13,14,15,18,19,20,21,22,25,26] }
    ],
    // RST declaración anual: abril, por pares de último dígito 1-2,3-4,5-6,7-8,9-0
    rst_anual: { mes: "2026-04", dias: [20,21,22,23,24] },
    rst_iva_anual: { mes: "2026-02", dias: [16,17,18,19,20] }
  }
};
if (typeof module !== "undefined") module.exports = SCF_DATA;
