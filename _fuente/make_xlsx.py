#!/usr/bin/env python3
"""Plantillas Excel con fórmulas para el portal."""
import json, re, datetime as dt
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).parent
OUT = ROOT / "site/formatos"; OUT.mkdir(parents=True, exist_ok=True)
NAVY, GOLD, CREAM = "1B3562", "C9AD69", "F8F6F0"
H = Font(name="Calibri", size=16, bold=True, color=NAVY)
B = Font(name="Calibri", size=11, bold=True, color=NAVY)
W = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
SMALL = Font(name="Calibri", size=9, color="5A6273")
FILL_H = PatternFill("solid", fgColor=NAVY)
FILL_IN = PatternFill("solid", fgColor="FFF6DD")
FILL_C = PatternFill("solid", fgColor=CREAM)
thin = Side(style="thin", color="E2DDCF")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
PESOS = '"$"#,##0'
FOOT = "Plantilla de Solución Contable y Fiscal · recursos.solucioncontableyfiscal.com · WhatsApp 300 507 4934. Información de referencia; no reemplaza la asesoría profesional."

# Datos del calendario desde data.js
def load_cal():
    # Ejecuta data.js con node para obtener el objeto exacto
    import subprocess
    out = subprocess.check_output(["node", "-e", "const D=require('./src/data.js');console.log(JSON.stringify(D))"], cwd=ROOT)
    return json.loads(out)
D = load_cal()
C = D["cal"]

def d(mes, dia):
    y, m = map(int, mes.split("-")); return dt.date(y, m, dia)

def widths(ws, ws_w):
    for col, w in ws_w.items(): ws.column_dimensions[col].width = w

# ---------- 1. Calendario por NIT ----------
def calendario():
    wb = Workbook(); ws = wb.active; ws.title = "Mis fechas"
    dd = wb.create_sheet("Datos DIAN 2026")
    # Hoja de datos: fila 1 encabezado con dígitos
    dd.append(["Obligación", "Período", "Mes de vencimiento"] + [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    rows = []
    def add(obl, per, mes, dias):
        dd.append([obl, per, mes] + [d(mes, x) for x in dias]); rows.append((obl, per))
    for it in C["renta_gc"]: add(it["tipo"], it["detalle"], it["mes"], it["dias"])
    for it in C["renta_pj"]: add(it["tipo"], it["detalle"], it["mes"], it["dias"])
    for it in C["iva_bim"]: add("IVA bimestral", it["periodo"], it["mes"], it["dias"])
    for it in C["iva_cuat"]: add("IVA cuatrimestral", it["periodo"], it["mes"], it["dias"])
    for it in C["retencion"]: add("Retención en la fuente", it["periodo"], it["mes"], it["dias"])
    for it in C["rst_anticipo"]: add("Régimen Simple · anticipo", it["periodo"], it["mes"], it["dias"])
    an = C["rst_anual"]["dias"]; iv = C["rst_iva_anual"]["dias"]
    add("Régimen Simple · declaración anual", "año 2025", C["rst_anual"]["mes"], [an[0], an[0], an[1], an[1], an[2], an[2], an[3], an[3], an[4], an[4]])
    add("Régimen Simple · IVA anual consolidado", "año 2025", C["rst_iva_anual"]["mes"], [iv[0], iv[0], iv[1], iv[1], iv[2], iv[2], iv[3], iv[3], iv[4], iv[4]])
    n_rows = len(rows)
    for r in dd.iter_rows(min_row=2, min_col=4, max_col=13):
        for c in r: c.number_format = "dd/mm/yyyy"
    for c in dd[1]: c.font = W; c.fill = FILL_H
    # Tabla renta personas naturales por dos dígitos (columnas P:Q)
    dd["P1"] = "Dos últimos dígitos"; dd["Q1"] = "Renta personas naturales"
    dd["P1"].font = W; dd["P1"].fill = FILL_H; dd["Q1"].font = W; dd["Q1"].fill = FILL_H
    for n in range(100):
        k = 49 if n == 0 else (n + 1) // 2 - 1
        y, m, dia = map(int, C["renta_pn"][k].split("-"))
        dd.cell(row=n + 2, column=16, value=n); c = dd.cell(row=n + 2, column=17, value=dt.date(y, m, dia)); c.number_format = "dd/mm/yyyy"
    widths(dd, {"A": 38, "B": 30, "C": 18, "P": 18, "Q": 22})

    ws["A1"] = "Calendario tributario 2026 por NIT"; ws["A1"].font = H
    ws["A2"] = "Escribe los dos últimos dígitos de tu NIT (sin el dígito de verificación) en la celda amarilla."; ws["A2"].font = SMALL
    ws["A4"] = "Dos últimos dígitos del NIT"; ws["A4"].font = B
    ws["B4"] = 34; ws["B4"].fill = FILL_IN; ws["B4"].border = BOX; ws["B4"].font = Font(size=14, bold=True, color=NAVY)
    ws["A5"] = "Último dígito"; ws["B5"] = "=MOD(B4,10)"
    ws["A6"] = "Renta personas naturales (año gravable 2025)"; ws["A6"].font = B
    ws["B6"] = "=VLOOKUP(MOD(B4,100),'Datos DIAN 2026'!$P$2:$Q$101,2,FALSE)"; ws["B6"].number_format = "dd/mm/yyyy"
    ws["A8"] = "Obligación"; ws["B8"] = "Período"; ws["C8"] = "Fecha límite"; ws["D8"] = "Días que faltan"
    for c in ws[8][:4]: c.font = W; c.fill = FILL_H
    for i in range(n_rows):
        r = 9 + i; src = 2 + i
        ws[f"A{r}"] = f"='Datos DIAN 2026'!A{src}"
        ws[f"B{r}"] = f"='Datos DIAN 2026'!B{src}"
        ws[f"C{r}"] = f"=INDEX('Datos DIAN 2026'!$D${src}:$M${src},MATCH($B$5,'Datos DIAN 2026'!$D$1:$M$1,0))"
        ws[f"C{r}"].number_format = "dd/mm/yyyy"
        ws[f"D{r}"] = f'=IF(C{r}-TODAY()<0,"Vencido",C{r}-TODAY())'
        if i % 2:
            for col in "ABCD": ws[f"{col}{r}"].fill = FILL_C
    ws[f"A{9 + n_rows + 1}"] = "Revisa solo las filas que te aplican. Fuente: Calendario Tributario 2026 de la DIAN (versión del 1 de julio de 2026)."; ws[f"A{9 + n_rows + 1}"].font = SMALL
    ws[f"A{9 + n_rows + 2}"] = FOOT; ws[f"A{9 + n_rows + 2}"].font = SMALL
    widths(ws, {"A": 44, "B": 34, "C": 16, "D": 16})
    ws.freeze_panes = "A9"
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="99", showErrorMessage=True, errorTitle="Dígitos", error="Escribe un número de 00 a 99.")
    ws.add_data_validation(dv); dv.add("B4")
    wb.save(OUT / "calendario-tributario-2026-por-nit.xlsx")

# ---------- 2. Retención por salarios ----------
def retencion():
    wb = Workbook(); ws = wb.active; ws.title = "Retención"
    p = wb.create_sheet("Parámetros")
    params = [("UVT 2026", D["uvt"]["2026"]), ("Salario mínimo 2026", D["smmlv"])]
    for i, (k, v) in enumerate(params, 1):
        p.cell(row=i, column=1, value=k); c = p.cell(row=i, column=2, value=v); c.number_format = PESOS
    p["A4"] = "Tabla art. 383 ET"; p["A4"].font = B
    p.append(["Desde (UVT)", "Hasta (UVT)", "Tarifa marginal", "Se resta (UVT)", "Se suma (UVT)"])
    tabla = [(0, 95, 0, 0, 0), (95, 150, .19, 95, 0), (150, 360, .28, 150, 10), (360, 640, .33, 360, 69), (640, 945, .35, 640, 162), (945, 2300, .37, 945, 268), (2300, 999999999, .39, 2300, 770)]
    for t in tabla: p.append(list(t))
    for c in p[5]: c.font = W; c.fill = FILL_H
    widths(p, {"A": 22, "B": 16, "C": 16, "D": 16, "E": 16})
    ws["A1"] = "Retención en la fuente por salarios 2026 · procedimiento 1"; ws["A1"].font = H
    ws["A2"] = "Llena las celdas amarillas. Arts. 383, 387 y 388 del Estatuto Tributario. Topes anuales aplicados en doceavas partes."; ws["A2"].font = SMALL
    inputs = [("Salario del mes", 15000000), ("Otros pagos laborales del mes", 0), ("¿Tiene dependientes? (1 = sí, 0 = no)", 0),
              ("Intereses de vivienda (mensual)", 0), ("Medicina prepagada (mensual)", 0), ("Aportes voluntarios a pensión o AFC del mes", 0)]
    for i, (k, v) in enumerate(inputs):
        r = 4 + i; ws[f"A{r}"] = k; c = ws[f"B{r}"]; c.value = v; c.fill = FILL_IN; c.border = BOX; c.number_format = PESOS if i != 2 else "0"
    U = "Parámetros!$B$1"; S = "Parámetros!$B$2"
    calc = [
        ("Ingresos laborales", "=B4+B5"),
        ("Ingreso base de cotización (tope 25 SMMLV)", f"=MIN(B11,25*{S})"),
        ("(−) Salud 4 %", "=B12*4%"),
        ("(−) Pensión 4 %", "=B12*4%"),
        ("(−) Fondo de solidaridad pensional", f"=B12*IF(B12<4*{S},0,IF(B12<16*{S},1%,IF(B12<17*{S},1.2%,IF(B12<18*{S},1.4%,IF(B12<19*{S},1.6%,IF(B12<20*{S},1.8%,2%))))))"),
        ("Ingreso neto", "=B11-B13-B14-B15"),
        ("(−) Dependientes (10 %, máx. 32 UVT)", f"=IF(B6=1,MIN(B11*10%,32*{U}),0)"),
        ("(−) Intereses de vivienda (máx. 100 UVT)", f"=MIN(B7,100*{U})"),
        ("(−) Medicina prepagada (máx. 16 UVT)", f"=MIN(B8,16*{U})"),
        ("(−) Aportes voluntarios / AFC (máx. 30 % y 3.800 UVT al año)", f"=MIN(B9,B11*30%,3800*{U}/12)"),
        ("Subtotal", "=MAX(B16-B17-B18-B19-B20,0)"),
        ("(−) Renta exenta 25 % (máx. 790 UVT al año)", f"=MIN(B21*25%,790*{U}/12)"),
        ("Total deducciones y rentas exentas", "=B17+B18+B19+B20+B22"),
        ("Límite 40 % y 1.340 UVT al año", f"=MIN(B16*40%,1340*{U}/12)"),
        ("Base gravable", "=MAX(B16-MIN(B23,B24),0)"),
        ("Base gravable en UVT", f"=B25/{U}"),
        ("Retención en UVT", "=IF(B26<=95,0,(B26-VLOOKUP(B26,Parámetros!$A$6:$E$12,4,TRUE))*VLOOKUP(B26,Parámetros!$A$6:$E$12,3,TRUE)+VLOOKUP(B26,Parámetros!$A$6:$E$12,5,TRUE))"),
        ("Retención del mes", f"=B27*{U}"),
    ]
    for i, (k, f) in enumerate(calc):
        r = 11 + i; ws[f"A{r}"] = k; ws[f"B{r}"] = f
        ws[f"B{r}"].number_format = '0.00' if r in (26, 27) else PESOS
    for r in (16, 25, 28): ws[f"A{r}"].font = B; ws[f"B{r}"].font = B
    ws["A30"] = FOOT; ws["A30"].font = SMALL
    widths(ws, {"A": 58, "B": 20})
    wb.save(OUT / "retencion-en-la-fuente-salarios-2026.xlsx")

# ---------- 3. Prestaciones sociales ----------
def prestaciones():
    wb = Workbook(); ws = wb.active; ws.title = "Prestaciones"
    ws["A1"] = "Liquidador de prestaciones sociales 2026"; ws["A1"].font = H
    ws["A2"] = "Llena las celdas amarillas. Año de 360 días. Supone que no se han pagado cesantías ni tomado vacaciones en el período."; ws["A2"].font = SMALL
    ins = [("Salario mensual", D["smmlv"], PESOS), ("Fecha de inicio", dt.date(2026, 1, 1), "dd/mm/yyyy"), ("Fecha de corte", dt.date(2026, 10, 31), "dd/mm/yyyy"),
           ("Salario mínimo 2026", D["smmlv"], PESOS), ("Auxilio de transporte 2026", D["auxTransporte"], PESOS)]
    for i, (k, v, fmt) in enumerate(ins):
        r = 4 + i; ws[f"A{r}"] = k; c = ws[f"B{r}"]; c.value = v; c.number_format = fmt
        if i < 3: c.fill = FILL_IN; c.border = BOX
    calc = [
        ("Auxilio de transporte incluido (salario hasta 2 SMMLV)", "=IF(B4<=2*B7,B8,0)", PESOS),
        ("Base para cesantías y prima", "=B4+B10", PESOS),
        ("Días trabajados", "=DAYS360(B5,B6,TRUE)+1+IF(AND(MONTH(B6+1)=3,DAY(B6+1)=1),30-DAY(B6),0)", "0"),
        ("Inicio del semestre de la prima", "=MAX(B5,IF(MONTH(B6)<=6,DATE(YEAR(B6),1,1),DATE(YEAR(B6),7,1)))", "dd/mm/yyyy"),
        ("Días de prima del semestre", "=DAYS360(B13,B6,TRUE)+1+IF(AND(MONTH(B6+1)=3,DAY(B6+1)=1),30-DAY(B6),0)", "0"),
        ("Cesantías", "=B11*B12/360", PESOS),
        ("Intereses sobre cesantías (12 %)", "=B15*B12*12%/360", PESOS),
        ("Prima de servicios", "=B11*B14/360", PESOS),
        ("Vacaciones (15 días hábiles por año)", "=B4*B12/720", PESOS),
        ("Total", "=B15+B16+B17+B18", PESOS),
    ]
    for i, (k, f, fmt) in enumerate(calc):
        r = 10 + i; ws[f"A{r}"] = k; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = fmt
    ws["A19"].font = B; ws["B19"].font = B
    ws["A21"] = FOOT; ws["A21"].font = SMALL
    widths(ws, {"A": 56, "B": 20})
    wb.save(OUT / "liquidador-prestaciones-sociales-2026.xlsx")

calendario(); retencion(); prestaciones()
print(sorted(p.name for p in OUT.iterdir()))
