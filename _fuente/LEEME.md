# Fuente del portal (no se publica: GitHub Pages ignora carpetas que empiezan por "_")

- `src/data.js`: datos (UVT, SMMLV, auxilio, usura, moratorio mensual, sanción mínima, calendario DIAN 2026).
- `src/calc.js`: cálculos (vencimientos, retención art. 383, mora, sanción art. 641, prestaciones, UVT).
- `src/ui.js`, `src/site.css`: interfaz y estilos.
- `build.py`: genera el sitio en `site/` (y `preview/`). Formulario de descargas: `FORM_FORMATOS=https://forms.gle/CyQ64XtjGx3GynNW8 python3 build.py`.
- `make_xlsx.py`: genera los 3 Excel en `site/formatos/` (requiere node y openpyxl).
- Publicar: copiar el contenido de `site/` a la raíz del repo, commit y push a `main`.
- Actualización mensual: tasa de usura (Superfinanciera) e interés moratorio DIAN (usura − 2) en `src/data.js` (`usura`, `moratorio`, `moratorioVigente`).
