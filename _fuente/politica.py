"""Política de Tratamiento de Datos Personales (versión web).
Fuente única del texto publicado en /politica-de-datos.html. Si cambia, actualizar también el Word."""

SLUG = "politica-de-datos"
TITLE = "Política de Tratamiento de Datos Personales"
DESC = ("Política de Tratamiento de Datos Personales de SOLUCION CONTABLE Y FISCAL S.A.S. (Ley 1581 de 2012): "
        "qué datos tratamos, para qué, tus derechos y cómo ejercerlos.")
VERSION = "Versión 1.0 · Vigente desde el 24 de octubre de 2026"


def tbl(head, rows, stack=False):
    th = "".join(f"<th>{h}</th>" for h in head) if head else ""
    thead = f"<thead><tr>{th}</tr></thead>" if head else ""
    lab = (lambda i: f' data-label="{head[i]}"') if (stack and head) else (lambda i: "")
    trs = "".join("<tr>" + "".join(f"<td{lab(i)}>{c}</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    cls = "tbl stack" if stack else "tbl"
    return f'<div class="{cls}"><table>{thead}<tbody>{trs}</tbody></table></div>'


SECTIONS = [
 ("responsable", "1. Responsable del tratamiento", tbl(None, [
   ["<b>Razón social</b>", "SOLUCION CONTABLE Y FISCAL S.A.S."],
   ["<b>Nombre comercial</b>", "Solución Contable y Fiscal (SOLUCONFIS)"],
   ["<b>NIT</b>", '<span class="num">902.118.737-1</span>'],
   ["<b>Domicilio</b>", "Barranquilla, Atlántico, Colombia"],
   ["<b>Dirección</b>", "Vía 40 #73-290, Edificio Mix, Oficina 612, Barranquilla"],
   ["<b>Correo electrónico</b>", "solucontfisc@gmail.com"],
   ["<b>Teléfono y WhatsApp</b>", '<span class="num">+57 300 507 4934</span>'],
   ["<b>Sitios web</b>", "solucioncontableyfiscal.com y recursos.solucioncontableyfiscal.com"],
 ])),

 ("marco-legal", "2. Marco legal", """<ul>
<li>Constitución Política, artículos 15 y 20.</li>
<li>Ley Estatutaria 1581 de 2012, régimen general de protección de datos personales.</li>
<li>Decreto 1377 de 2013 y Decreto 886 de 2014, compilados en el Decreto Único Reglamentario 1074 de 2015 (Libro 2, Parte 2, Título 2, capítulos 25 y 26).</li>
<li>Circular Única de la Superintendencia de Industria y Comercio (SIC), Título V.</li>
<li>Ley 2300 de 2023, sobre canales, horarios y periodicidad de los contactos comerciales y publicitarios.</li>
<li>Ley 43 de 1990, sobre la reserva profesional del contador público.</li>
<li>Ley 527 de 1999, sobre la validez de los mensajes de datos, que permite otorgar la autorización por medios electrónicos.</li>
</ul>"""),

 ("ambito", "3. Ámbito de aplicación", """<p>Esta política aplica a todas las bases de datos y archivos, físicos o digitales, que contengan datos personales y que SOLUCONFIS trate como responsable. También aplica, en lo que no contradiga las instrucciones del cliente, a los datos que SOLUCONFIS trate como encargado por cuenta de sus clientes (numeral 8).</p>
<p>Es de obligatorio cumplimiento para los socios, empleados, contratistas y demás personas que traten datos por cuenta de SOLUCONFIS. No aplica a la información de personas jurídicas, salvo los datos de sus representantes, socios, empleados y contactos, que sí son datos personales.</p>"""),

 ("definiciones", "4. Definiciones", "<p>Para efectos de esta política se usan las definiciones de la Ley 1581 de 2012 y del Decreto 1377 de 2013:</p>" + tbl(["Término", "Significado"], [
   ["Autorización", "Consentimiento previo, expreso e informado del titular para que se traten sus datos personales."],
   ["Aviso de privacidad", "Comunicación verbal o escrita que informa al titular que existe esta política, cómo acceder a ella y para qué se usarán sus datos."],
   ["Base de datos", "Conjunto organizado de datos personales que es objeto de tratamiento."],
   ["Dato personal", "Cualquier información vinculada o que pueda asociarse a una o varias personas naturales determinadas o determinables."],
   ["Dato público", "El que no es semiprivado, privado ni sensible; por ejemplo, el estado civil, la profesión u oficio, la calidad de comerciante y los datos contenidos en registros públicos."],
   ["Dato semiprivado", "El que no es íntimo, reservado ni público y cuyo conocimiento interesa a su titular y a cierto sector o grupo, como los datos financieros y crediticios."],
   ["Dato privado", "El que por su naturaleza íntima o reservada solo es relevante para su titular."],
   ["Dato sensible", "El que afecta la intimidad del titular o cuyo uso indebido puede generar discriminación, como el origen racial o étnico, la orientación política, las convicciones religiosas o filosóficas, la afiliación sindical, los datos de salud, de vida sexual y los biométricos."],
   ["Encargado del tratamiento", "Persona que trata datos personales por cuenta del responsable."],
   ["Responsable del tratamiento", "Persona que decide sobre la base de datos y sobre el tratamiento de los datos."],
   ["Titular", "Persona natural cuyos datos personales son objeto de tratamiento."],
   ["Tratamiento", "Cualquier operación sobre datos personales, como recolectarlos, almacenarlos, usarlos, hacerlos circular o suprimirlos."],
   ["Transferencia", "Envío de datos personales a un receptor, dentro o fuera del país, que a su vez es responsable del tratamiento."],
   ["Transmisión", "Comunicación de datos personales, dentro o fuera del país, para que un encargado los trate por cuenta del responsable."],
   ["Cookies", "Pequeños archivos que un sitio web guarda en el navegador del visitante para recordar información sobre su visita."],
 ])),

 ("principios", "5. Principios", """<p>SOLUCONFIS aplica los principios del artículo 4 de la Ley 1581 de 2012:</p>
<ul>
<li><b>Legalidad:</b> el tratamiento se sujeta a lo que dispone la ley.</li>
<li><b>Finalidad:</b> los datos se tratan para fines legítimos que se informan al titular.</li>
<li><b>Libertad:</b> el tratamiento solo se realiza con el consentimiento previo, expreso e informado del titular, salvo mandato legal o judicial.</li>
<li><b>Veracidad o calidad:</b> la información debe ser veraz, completa, exacta, actualizada, comprobable y comprensible.</li>
<li><b>Transparencia:</b> el titular puede obtener información sobre sus datos en cualquier momento y sin restricciones.</li>
<li><b>Acceso y circulación restringida:</b> los datos solo los conocen las personas autorizadas y no se publican en internet, salvo que sean públicos o el acceso pueda controlarse.</li>
<li><b>Seguridad:</b> los datos se protegen con medidas técnicas, humanas y administrativas.</li>
<li><b>Confidencialidad:</b> quienes intervienen en el tratamiento guardan reserva, incluso después de terminada su relación con SOLUCONFIS. Este deber se suma a la reserva profesional del contador público (Ley 43 de 1990).</li>
</ul>"""),

 ("datos", "6. Datos que tratamos y cómo los obtenemos", tbl(["Titulares", "Datos", "Cómo los obtenemos"], stack=True, rows=[
   ["Visitantes de los sitios web", "Datos de navegación: páginas visitadas, duración de la visita, tipo de dispositivo y navegador, ubicación aproximada y origen de la visita.", 'Cookies de Google Analytics en solucioncontableyfiscal.com (<a href="#cookies">numeral 14</a>).'],
   ["Interesados en nuestros servicios", "Nombre completo, celular o WhatsApp, correo electrónico, ciudad, si es persona natural o empresa, servicio que necesita, modalidad de atención preferida y descripción de la solicitud.", "Formulario «Solicita tu asesoría», WhatsApp, correo, redes sociales, llamadas y atención presencial."],
   ["Personas que descargan formatos", "Nombre completo, celular o WhatsApp, correo electrónico (opcional) y perfil (persona natural, empresa o emprendedor, contador o auxiliar contable).", "Formulario de descargas de este portal."],
   ["Personas que agendan citas", "Nombre, correo electrónico, fecha y hora de la cita y la información que agreguen al reservar.", "Agenda de citas en línea (Google Calendar)."],
   ["Clientes personas naturales, y representantes, socios y contactos de clientes empresas", "Identificación (tipo y número de documento, NIT, RUT), datos de contacto e información tributaria, contable, financiera y patrimonial: ingresos, bienes, deudas, cuentas, declaraciones, facturas electrónicas, certificados y extractos. Datos de dependientes económicos cuando se necesitan para depurar la renta o la retención.", "Directamente del cliente, de los documentos que entrega y de las plataformas de las autoridades a las que el cliente nos da acceso."],
   ["Trabajadores, contratistas y beneficiarios de nuestros clientes", "Identificación, datos laborales y salariales, afiliaciones a seguridad social, novedades de nómina (incapacidades, licencias, vacaciones), datos bancarios para el pago y beneficiarios.", 'Los entrega el cliente empleador, que es el responsable de esos datos (<a href="#encargado">numeral 8</a>).'],
   ["Proveedores y contratistas de SOLUCONFIS", "Identificación, RUT, datos de contacto, datos bancarios y documentos del contrato.", "Directamente del proveedor o contratista."],
   ["Candidatos y colaboradores de SOLUCONFIS", "Hoja de vida, formación, experiencia, referencias, afiliaciones a seguridad social y los demás datos que exige la ley laboral.", "Directamente del candidato o colaborador."],
 ]) + '<p><b>Calendario tributario por NIT.</b> La herramienta de este portal solo usa los dos últimos dígitos del NIT y hace el cálculo en el navegador del visitante. SOLUCONFIS no recibe ni guarda ese dato.</p>'),

 ("finalidades", "7. Finalidades del tratamiento", """<h3>7.1 Para todos los titulares</h3>
<ul>
<li>Atender peticiones, consultas, quejas y reclamos.</li>
<li>Cumplir las obligaciones legales, contables y tributarias de SOLUCONFIS y responder los requerimientos de las autoridades.</li>
<li>Conservar prueba de la autorización y de las comunicaciones con el titular.</li>
<li>Proteger la seguridad de los sistemas y defender los derechos de SOLUCONFIS en procesos judiciales o administrativos.</li>
</ul>
<h3>7.2 Interesados, visitantes y personas que descargan formatos</h3>
<ul>
<li>Responder la solicitud y contactar al titular por el canal que eligió.</li>
<li>Enviar los formatos descargables solicitados.</li>
<li>Agendar, confirmar y recordar citas.</li>
<li>Con autorización expresa, enviar información sobre servicios, vencimientos tributarios, novedades normativas, boletines y eventos de SOLUCONFIS.</li>
<li>Medir de forma estadística el uso de los sitios web para mejorar sus contenidos.</li>
</ul>
<h3>7.3 Clientes</h3>
<ul>
<li>Prestar los servicios contratados: contabilidad, asesoría tributaria, preparación y presentación de declaraciones, revisoría fiscal y auditoría, nómina electrónica y trámites ante la DIAN y otras entidades.</li>
<li>Celebrar, ejecutar y documentar el contrato, facturar y gestionar los pagos.</li>
<li>Enviar recordatorios de vencimientos y solicitar la información necesaria para el servicio.</li>
<li>Elaborar y conservar los papeles de trabajo que exigen las normas profesionales.</li>
<li>Medir la satisfacción con el servicio.</li>
<li>Cumplir los deberes de prevención de lavado de activos y de reporte que la ley imponga a SOLUCONFIS.</li>
</ul>
<h3>7.4 Proveedores, contratistas, candidatos y colaboradores</h3>
<ul>
<li>Seleccionar, contratar, pagar y evaluar a proveedores y contratistas, y cumplir las obligaciones tributarias derivadas, como retenciones e información exógena.</li>
<li>Adelantar procesos de selección y gestionar la relación laboral o contractual: nómina, seguridad social, bienestar y demás obligaciones legales.</li>
</ul>"""),

 ("encargado", "8. SOLUCONFIS como encargado del tratamiento", """<p>Cuando llevamos la contabilidad, la nómina electrónica o los impuestos de una empresa, tratamos datos de sus trabajadores, clientes, proveedores y otros terceros por cuenta de ella. En esos casos la empresa cliente es la responsable del tratamiento: le corresponde obtener la autorización de los titulares y atender sus solicitudes. SOLUCONFIS actúa como encargado y se obliga a:</p>
<ul>
<li>Tratar los datos solo para prestar el servicio contratado y según las instrucciones del cliente.</li>
<li>Guardar reserva y no usar los datos para fines propios.</li>
<li>Aplicar las medidas de seguridad de esta política.</li>
<li>Trasladar al cliente, dentro de los dos (2) días hábiles siguientes, las consultas o reclamos que reciba sobre esos datos, e informar de ello al titular.</li>
<li>Devolver o suprimir los datos al terminar el servicio, salvo los que deba conservar por obligación legal o como papeles de trabajo.</li>
</ul>"""),

 ("sensibles", "9. Datos sensibles y datos de niñas, niños y adolescentes", """<h3>9.1 Datos sensibles</h3>
<p>SOLUCONFIS solo trata datos sensibles cuando son necesarios para un servicio o para cumplir una obligación legal; por ejemplo, las incapacidades y licencias que se registran en la nómina electrónica, o la afiliación sindical que se refleja en los descuentos de nómina. Se tratan con autorización explícita del titular, salvo en los casos que permite el artículo 6 de la Ley 1581 de 2012. Al pedirlos, SOLUCONFIS informa:</p>
<ol type="a">
<li>que el titular no está obligado a entregarlos ni a responder preguntas sobre ellos;</li>
<li>cuáles de los datos solicitados son sensibles y para qué se usarán.</li>
</ol>
<p>Ninguna actividad se condiciona a que el titular entregue datos sensibles.</p>
<h3>9.2 Datos de niñas, niños y adolescentes</h3>
<p>SOLUCONFIS solo trata datos de menores de edad cuando es necesario para el servicio, por ejemplo, hijos registrados como dependientes económicos o como beneficiarios de seguridad social. El tratamiento responde y respeta el interés superior del menor y asegura el respeto de sus derechos fundamentales. La autorización la otorga su representante legal, previo ejercicio del derecho del menor a ser escuchado según su madurez. Estos datos nunca se usan con fines comerciales.</p>"""),

 ("autorizacion", "10. Autorización del titular", """<p>SOLUCONFIS pide la autorización a más tardar al momento de recolectar los datos. Puede otorgarse por escrito, por medios electrónicos (como la casilla de los formularios), de forma oral grabada o mediante conductas inequívocas que permitan concluir razonablemente que se otorgó. Por ejemplo, quien escribe por WhatsApp para pedir información autoriza que usemos su número y su mensaje para responderle. El silencio nunca se entiende como autorización.</p>
<p>La autorización para recibir información comercial se pide de forma explícita y el titular puede retirarla en cualquier momento. SOLUCONFIS conserva prueba de cada autorización, como el registro del formulario, el mensaje o el documento firmado.</p>
<p>No se requiere autorización, según el artículo 10 de la Ley 1581 de 2012, cuando se trate de:</p>
<ol type="a">
<li>información requerida por una entidad pública o administrativa en ejercicio de sus funciones legales, o por orden judicial;</li>
<li>datos de naturaleza pública;</li>
<li>casos de urgencia médica o sanitaria;</li>
<li>tratamiento autorizado por la ley para fines históricos, estadísticos o científicos;</li>
<li>datos relacionados con el Registro Civil de las Personas.</li>
</ol>"""),

 ("derechos", "11. Derechos de los titulares", """<p>De acuerdo con el artículo 8 de la Ley 1581 de 2012, el titular tiene derecho a:</p>
<ol type="a">
<li>conocer, actualizar y rectificar sus datos personales, incluso frente a datos parciales, inexactos, incompletos, fraccionados o que induzcan a error;</li>
<li>solicitar prueba de la autorización otorgada, salvo cuando no se requiera;</li>
<li>ser informado, previa solicitud, del uso que se ha dado a sus datos;</li>
<li>presentar quejas ante la Superintendencia de Industria y Comercio por infracciones a la ley, después de agotar el trámite ante SOLUCONFIS (<a href="#consultas">numeral 12</a>);</li>
<li>revocar la autorización y solicitar la supresión de sus datos cuando no se respeten los principios, derechos y garantías constitucionales y legales;</li>
<li>acceder en forma gratuita a sus datos personales.</li>
</ol>
<p>El acceso es gratuito al menos una vez cada mes calendario y cada vez que esta política cambie de forma sustancial. La revocatoria y la supresión no proceden cuando el titular tiene un deber legal o contractual de permanecer en la base de datos; por ejemplo, los soportes contables y tributarios que la ley obliga a conservar.</p>
<p>Pueden ejercer estos derechos el titular, acreditando su identidad; sus causahabientes, acreditando esa calidad; su representante o apoderado, acreditando la representación; y quien se haya estipulado a favor de otro o para otro. Los derechos de los menores los ejercen sus representantes legales.</p>"""),

 ("consultas", "12. Atención de consultas y reclamos", """<h3>12.1 Área responsable y canales</h3>
<p>El <b>Representante Legal</b> de SOLUCONFIS es el responsable de atender las peticiones, consultas y reclamos sobre datos personales. Se reciben por estos canales:</p>
""" + tbl(None, [
   ["<b>Correo electrónico</b>", "solucontfisc@gmail.com, con el asunto «Protección de datos personales»"],
   ["<b>WhatsApp</b>", '<span class="num">+57 300 507 4934</span>'],
   ["<b>Por escrito</b>", "Vía 40 #73-290, Edificio Mix, Oficina 612, Barranquilla"],
 ]) + """
<p>La solicitud debe incluir: nombre e identificación del titular (y del representante, con prueba de la representación), descripción clara de lo que pide, dirección física o electrónica para la respuesta y los documentos que quiera hacer valer.</p>
<h3>12.2 Consultas</h3>
<p>Las consultas se atienden en un máximo de <b>diez (10) días hábiles</b> contados desde su recibo. Si no es posible hacerlo en ese plazo, SOLUCONFIS informará los motivos y la fecha de respuesta, que no podrá superar <b>cinco (5) días hábiles</b> adicionales (artículo 14 de la Ley 1581 de 2012).</p>
<h3>12.3 Reclamos</h3>
<p>Quien considere que sus datos deben corregirse, actualizarse o suprimirse, o que se incumplió la ley o esta política, puede presentar un reclamo, que se tramita así (artículo 15 de la Ley 1581 de 2012):</p>
<ol type="a">
<li>Si el reclamo está incompleto, SOLUCONFIS pedirá al interesado, dentro de los cinco (5) días siguientes a su recibo, que lo complete. Si pasan dos (2) meses desde ese requerimiento sin que entregue la información, se entenderá que desistió.</li>
<li>Si SOLUCONFIS no es competente para resolverlo, lo trasladará a quien corresponda en un máximo de dos (2) días hábiles e informará al interesado.</li>
<li>Recibido el reclamo completo, en un máximo de dos (2) días hábiles se marcará en la base de datos con la leyenda «reclamo en trámite» y su motivo, hasta que se decida.</li>
<li>El reclamo se resuelve en un máximo de <b>quince (15) días hábiles</b> contados desde el día siguiente a su recibo. Si no es posible, se informarán los motivos y la nueva fecha, que no podrá superar <b>ocho (8) días hábiles</b> adicionales.</li>
</ol>
<h3>12.4 Queja ante la Superintendencia de Industria y Comercio</h3>
<p>El titular solo puede presentar una queja ante la SIC después de haber agotado este trámite de consulta o reclamo ante SOLUCONFIS (artículo 16 de la Ley 1581 de 2012).</p>"""),

 ("deberes", "13. Deberes de SOLUCONFIS", """<p>Como responsable del tratamiento, SOLUCONFIS cumple los deberes del artículo 17 de la Ley 1581 de 2012, entre ellos:</p>
<ul>
<li>Garantizar al titular el pleno y efectivo ejercicio del derecho de hábeas data.</li>
<li>Conservar copia de la autorización otorgada por el titular.</li>
<li>Informar al titular la finalidad de la recolección y los derechos que le asisten.</li>
<li>Conservar la información con las condiciones de seguridad necesarias para impedir su adulteración, pérdida, consulta, uso o acceso no autorizado o fraudulento.</li>
<li>Mantener la información veraz y actualizada, y rectificarla cuando sea incorrecta.</li>
<li>Tramitar las consultas y reclamos en los plazos de ley.</li>
<li>Informar a la SIC cuando se presenten violaciones a los códigos de seguridad y existan riesgos en la administración de la información de los titulares.</li>
<li>Cumplir las instrucciones y requerimientos de la SIC.</li>
</ul>"""),

 ("cookies", "14. Cookies y medición de los sitios web", """<p>El sitio solucioncontableyfiscal.com usa <b>Google Analytics</b>, de Google LLC, para saber cuántas personas lo visitan, qué páginas consultan y desde qué tipo de dispositivo. Esta información se usa de forma estadística y SOLUCONFIS no la usa para identificar a los visitantes. Al ingresar, el sitio muestra un aviso de cookies.</p>
<p>El visitante puede rechazar o borrar las cookies desde la configuración de su navegador, o instalar el <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">complemento de inhabilitación de Google Analytics</a>. Si las bloquea, el sitio sigue funcionando.</p>"""),

 ("comunicaciones", "15. Comunicaciones comerciales", """<p>SOLUCONFIS solo envía información comercial o publicitaria a quien la haya autorizado y por los canales que autorizó. Conforme a la Ley 2300 de 2023:</p>
<ul>
<li>Los mensajes y llamadas se hacen de lunes a viernes de 7:00 a. m. a 7:00 p. m. y los sábados de 8:00 a. m. a 3:00 p. m. Nunca los domingos ni festivos.</li>
<li>No se contacta al titular más de una vez en el mismo día ni por varios canales en la misma semana.</li>
<li>El titular puede dejar de recibir estos mensajes cuando quiera: respondiendo «NO» por WhatsApp, escribiendo al correo de SOLUCONFIS o usando el enlace para cancelar la suscripción que traen los boletines.</li>
</ul>
<p>Estos límites no impiden responder lo que el titular haya pedido, ni enviar a los clientes la información estrictamente relacionada con el servicio contratado, como recordatorios de vencimientos o solicitudes de documentos.</p>"""),

 ("transmision", "16. Transmisión y transferencia de datos", """<p>SOLUCONFIS no vende, alquila ni cede datos personales a terceros para fines comerciales de estos.</p>
<p>Para operar, SOLUCONFIS usa proveedores tecnológicos que tratan datos por su cuenta como encargados, entre ellos: Google (formularios, hojas de cálculo, correo, almacenamiento, agenda y Google Analytics), Meta (WhatsApp), Canva (alojamiento del sitio principal), GitHub (alojamiento de este portal) y los programas de contabilidad y nómina electrónica con los que presta sus servicios. SOLUCONFIS usa estos servicios bajo condiciones contractuales que obligan al proveedor a tratar los datos solo para prestar el servicio y a protegerlos.</p>
<p>Algunos de estos proveedores guardan la información en servidores fuera de Colombia, principalmente en Estados Unidos, país que la SIC reconoce con un nivel adecuado de protección de datos (Circular Externa 005 de 2017, incorporada a la Circular Única).</p>
<p>SOLUCONFIS entrega datos a autoridades como la DIAN, la UGPP, las secretarías de hacienda, las superintendencias y los jueces cuando la ley lo exige o cuando el servicio contratado lo requiere, por ejemplo, al presentar declaraciones o transmitir la nómina electrónica. Cualquier otra transferencia solo se hará con autorización expresa del titular o en los casos que permite el artículo 26 de la Ley 1581 de 2012.</p>"""),

 ("seguridad", "17. Seguridad de la información", """<p>SOLUCONFIS adopta, entre otras, las siguientes medidas:</p>
<ul>
<li>Acceso a los datos solo para las personas que los necesitan para su trabajo, con cuentas protegidas por contraseñas robustas y verificación en dos pasos cuando el servicio lo permite.</li>
<li>Archivos compartidos con permisos restringidos, nunca mediante enlaces públicos.</li>
<li>Copias de seguridad de la información.</li>
<li>Acuerdos de confidencialidad con colaboradores y contratistas.</li>
<li>Las claves de acceso a plataformas que un cliente entregue para un trámite se usan solo para ese trámite, no se comparten y se recomienda al cliente cambiarlas al terminar el encargo.</li>
<li>En videos, capturas o materiales de capacitación no se muestran datos de clientes: se usan datos ficticios o se ocultan.</li>
<li>Ante un incidente de seguridad, SOLUCONFIS toma medidas para contenerlo, informa a los titulares afectados cuando corresponda y lo reporta a la SIC.</li>
</ul>"""),

 ("conservacion", "18. Conservación de los datos y vigencia de las bases de datos", "<p>Los datos se conservan durante el tiempo necesario para la finalidad para la que se recogieron y por los plazos que exige la ley:</p>" + tbl(["Datos", "Plazo"], [
   ["Interesados y personas que descargan formatos", "Hasta dos (2) años después del último contacto, salvo que el titular pida antes su supresión."],
   ["Clientes: libros y papeles de comercio", "Diez (10) años desde la fecha del último asiento, documento o comprobante (artículo 28 de la Ley 962 de 2005)."],
   ["Clientes: soportes tributarios", "Como mínimo, durante el término de firmeza de la declaración correspondiente (artículo 632 del Estatuto Tributario)."],
   ["Papeles de trabajo", "Por el plazo que exijan las normas de aseguramiento y de la profesión contable."],
   ["Candidatos no seleccionados", "Hasta un (1) año, salvo que el candidato pida antes su supresión."],
   ["Datos de navegación", "Según el plazo de conservación configurado en Google Analytics."],
 ]) + "<p>Cumplido el plazo, los datos se suprimen o se anonimizan de forma segura. Las bases de datos de SOLUCONFIS estarán vigentes mientras la empresa desarrolle su objeto social, sin perjuicio de los plazos anteriores.</p>"),

 ("rnbd", "19. Registro Nacional de Bases de Datos", "<p>SOLUCONFIS inscribirá sus bases de datos en el Registro Nacional de Bases de Datos de la SIC cuando esté obligada a hacerlo, es decir, cuando sus activos totales superen 100.000 UVT (Decreto 090 de 2018, compilado en el Decreto 1074 de 2015).</p>"),

 ("vigencia", "20. Vigencia y modificaciones", "<p>Esta política rige desde el 24 de octubre de 2026 y se publica en los sitios web de SOLUCONFIS. Cualquier cambio sustancial se comunicará a los titulares antes de aplicarlo, por los sitios web o por los canales de contacto registrados.</p>" + tbl(["Versión", "Fecha", "Cambio", "Aprobó"], [
   ["1.0", "24 de octubre de 2026", "Emisión inicial", "Representante Legal"],
 ])),
]


def body_html():
    intro = """<p>SOLUCION CONTABLE Y FISCAL S.A.S. (en adelante, <b>SOLUCONFIS</b>) adopta esta política para cumplir la Ley Estatutaria 1581 de 2012 y sus decretos reglamentarios, y para garantizar el derecho de toda persona a conocer, actualizar y rectificar la información que se haya recogido sobre ella (artículo 15 de la Constitución Política).</p>
<p>Aplica a los datos personales que recibimos por nuestros sitios web, formularios, agenda de citas, WhatsApp, correo electrónico, redes sociales, atención presencial y en la prestación de nuestros servicios de contabilidad, impuestos, revisoría fiscal y auditoría, y nómina electrónica.</p>"""
    toc = '<nav class="toc" aria-label="Contenido"><b>Contenido</b><ol>' + "".join(
        f'<li><a href="#{sid}">{t.split(". ", 1)[1]}</a></li>' for sid, t, _ in SECTIONS) + "</ol></nav>"
    secs = "".join(f'<section id="{sid}"><h2>{t}</h2>{c}</section>' for sid, t, c in SECTIONS)
    return intro + toc + secs
