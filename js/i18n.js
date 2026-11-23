/* Apheloria — selección de idioma, español/inglés/árabe kuwaití. */
(() => {
  const PARAMS = ['es', 'en', 'ar'];
  const translations = {
    en: {
      'Inicio':'Home','Proyectos':'Projects','Productos':'Products','Catálogo':'Catalogue','Contacto':'Contact','Realizados':'Completed','Interiores':'Indoor','Exteriores':'Outdoor','Industriales':'Industrial','Decorativas':'Decorative','Emergencia':'Emergency','Hospitalarias':'Healthcare','Bombillas y Accesorios':'Bulbs & Accessories','Fuentes de Alimentación':'Power Supplies','Sobre Nosotros':'About us','Nuestros Productos':'Our Products','Nuestros Proyectos':'Our Projects','Aviso legal':'Legal notice','Política de privacidad':'Privacy policy','Política de cookies':'Cookie policy','Abrir menú':'Open menu','Todo':'All','Todos':'All','Edificios':'Buildings','Industria':'Industry','Retail':'Retail','Portafolio':'Portfolio','Portfolio':'Portfolio','Proyectos Realizados':'Completed Projects','Galería':'Gallery','Proyectos:':'Projects','Descripción':'Description','Fichas técnicas':'Technical sheets','Ficha técnica':'Technical sheet','Ficha técnica original':'Original technical sheet','Producto':'Product','Medidas':'Dimensions','Ambiente':'Application','Curva fotométrica':'Photometric curve','Pulsa una miniatura para verla en grande':'Select a thumbnail to view it larger','Esta ficha no trae tabla de características.':'This sheet has no specification table.','Próximamente':'Coming soon','Disponible próximamente':'Available soon','Referencias':'References','Años':'Years','Categorías':'Categories','Cuéntanos tu proyecto,':'Tell us about your project','te asesoramos sin compromiso':'we will advise you with no obligation','Nombre':'Name','Email':'Email','Asunto':'Subject','Cuéntanos en qué podemos ayudarte':'Tell us how we can help','He leído y acepto la':'I have read and accept the','Enviar mensaje':'Send message','Enviando…':'Sending…','Hablamos':'Talk','cuando quieras':'whenever you want','Asesoramiento cercano y especializado para instaladores, ingenierías, arquitectos y promotores.':'Personal, specialist advice for installers, engineers, architects and developers.','Teléfono':'Telephone','Horario':'Opening hours','Lunes a viernes · 9:00 – 18:00':'Monday to Friday · 9:00–18:00','Mensaje enviado. Te responderemos lo antes posible.':'Message sent. We will reply as soon as possible.','No se ha podido enviar. Escríbenos a info@apheloria.es.':'Could not send. Email us at info@apheloria.es.','Más de 20 años<br>al servicio de<br>la luz':'More than 20 years<br>serving<br>light','Algunas Aphelorias brillan en la oscuridad.':'Some Aphelorias shine in the dark.','En Apheloria Solutions trabajamos para que':'At Apheloria Solutions, we work to ensure','cada proyecto también lo haga.':'that every project does too.','Más de 20 años colaborando con instaladores, ingenierías, arquitectos y promotores en proyectos de cualquier escala':'More than 20 years supporting installers, engineers, architects and developers on projects of every scale','Acercamos la mejor iluminación técnica a instaladores, ingenieros, arquitectos y promotores, con asesoramiento cercano y especializado en cada proyecto.':'We bring the best technical lighting to installers, engineers, architects and developers, with personal, specialist advice for every project.','Calidad · Servicio · Innovación · Confianza':'Quality · Service · Innovation · Trust','Más de 20 años':'More than 20 years','al servicio de':'serving','la luz':'light','Sobre Nosotros ↓':'About us ↓','Nuestros Productos →':'Our Products →','Nuestros Proyectos →':'Our Projects →','Ver imagen 1':'View image 1','Ver imagen 2':'View image 2','Ver imagen 3':'View image 3','Ver imagen 4':'View image 4','Ver imagen 5':'View image 5','Legal':'Legal','Todo nuestro catálogo,':'Our complete catalogue,','en un solo documento':'in a single document','Estamos preparando el catálogo general en PDF, con todas las familias y referencias en un solo documento. Mientras tanto, cada producto tiene su ficha técnica disponible en la sección Productos.':'We are preparing the general catalogue as a PDF, with every family and reference in one document. In the meantime, each product’s technical sheet is available in Products.','¿Lo necesitas ya? Escríbenos y te lo enviamos por email.':'Need it now? Email us and we will send it to you.',
      'Aviso Legal':'Legal Notice','Política de Privacidad':'Privacy Policy','Política de Cookies':'Cookie Policy','Última actualización: octubre de 2026':'Last updated: October 2026','1. Datos identificativos':'1. Identification details','2. Objeto y ámbito de aplicación':'2. Purpose and scope','3. Condiciones de acceso y uso':'3. Access and use','4. Propiedad intelectual e industrial':'4. Intellectual and industrial property','5. Exclusión de responsabilidad':'5. Disclaimer','6. Protección de datos personales':'6. Personal data protection','7. Legislación aplicable y jurisdicción':'7. Applicable law and jurisdiction','8. Modificaciones':'8. Amendments','Esa dirección ya no existe.':'This address no longer exists.','Volver a Productos':'Back to Products','secciones':'sections','sección':'section','producto':'product','productos':'products','referencias':'references','Ref.':'Ref.'
    },
    ar: {
      'Inicio':'الرئيسية','Proyectos':'المشاريع','Productos':'المنتجات','Catálogo':'الكتالوج','Contacto':'اتصل بنا','Realizados':'المنفذة','Interiores':'الديكور الداخلي','Exteriores':'الديكور الخارجي','Industriales':'الصناعية','Decorativas':'الديكورية','Emergencia':'الطوارئ','Hospitalarias':'المستشفيات','Bombillas y Accesorios':'المصابيح والإكسسوارات','Fuentes de Alimentación':'مصادر التغذية','Sobre Nosotros':'من نحن','Nuestros Productos':'منتجاتنا','Nuestros Proyectos':'مشاريعنا','Aviso legal':'الإشعار القانوني','Política de privacidad':'سياسة الخصوصية','Política de cookies':'سياسة ملفات الارتباط','Abrir menú':'فتح القائمة','Todo':'الكل','Todos':'الكل','Edificios':'المباني','Industria':'الصناعة','Retail':'التجزئة','Portafolio':'معرض الأعمال','Portfolio':'معرض الأعمال','Proyectos Realizados':'المشاريع المنفذة','Galería':'معرض الصور','Proyectos:':'المشاريع','Descripción':'الوصف','Fichas técnicas':'البطاقات الفنية','Ficha técnica':'بطاقة فنية','Ficha técnica original':'البطاقة الفنية الأصلية','Producto':'المنتج','Medidas':'الأبعاد','Ambiente':'بيئة التطبيق','Curva fotométrica':'المنحنى الضوئي','Pulsa una miniatura para verla en grande':'اضغط على الصورة المصغرة لعرضها بحجم أكبر','Esta ficha no trae tabla de características.':'هذه البطاقة لا تتضمن جدول المواصفات.','Próximamente':'قريبًا','Disponible próximamente':'سيتوفر قريبًا','Referencias':'المراجع','Años':'سنوات','Categorías':'الفئات','Cuéntanos tu proyecto,':'احك لنا عن مشروعك،','te asesoramos sin compromiso':'ونقدم لك الاستشارة من دون التزام','Nombre':'الاسم','Email':'البريد الإلكتروني','Asunto':'الموضوع','Cuéntanos en qué podemos ayudarte':'أخبرنا كيف يمكننا مساعدتك','He leído y acepto la':'قرأت وأوافق على','Enviar mensaje':'إرسال الرسالة','Enviando…':'جارٍ الإرسال…','Hablamos':'نتواصل','cuando quieras':'في أي وقت يناسبك','Asesoramiento cercano y especializado para instaladores, ingenierías, arquitectos y promotores.':'استشارات شخصية ومتخصصة للمقاولين والمهندسين والمعماريين والمطورين العقاريين.','Teléfono':'الهاتف','Horario':'ساعات العمل','Lunes a viernes · 9:00 – 18:00':'من الاثنين إلى الجمعة · 9:00 – 18:00','Mensaje enviado. Te responderemos lo antes posible.':'تم إرسال رسالتك. سنرد عليك في أقرب وقت ممكن.','No se ha podido enviar. Escríbenos a info@apheloria.es.':'تعذّر الإرسال. راسلونا على info@apheloria.es.','Más de 20 años<br>al servicio de<br>la luz':'أكثر من 20 عامًا<br>في خدمة<br>الضوء','Algunas Aphelorias brillan en la oscuridad.':'بعض الأجسام المعروفة باسم «آفيلوريا» تتوهج في الظلام.','En Apheloria Solutions trabajamos para que':'في Apheloria Solutions نعمل ليكون','cada proyecto también lo haga.':'كل مشروع قادرًا على الوهج أيضًا.','Más de 20 años colaborando con instaladores, ingenierías, arquitectos y promotores en proyectos de cualquier escala':'أكثر من 20 عامًا من التعاون مع المقاولين والمهندسين المعماريين والمطورين في مشاريع بمختلف الأحجام','Acercamos la mejor iluminación técnica a instaladores, ingenieros, arquitectos y promotores, con asesoramiento cercano y especializado en cada proyecto.':'نوفر أفضل حلول الإضاءة الفنية للمقاولين والمهندسين والمعماريين والمطورين، مع استشارات شخصية ومتخصصة لكل مشروع.','Calidad · Servicio · Innovación · Confianza':'الجودة · الخدمة · الابتكار · الثقة','Más de 20 años':'أكثر من 20 عامًا','al servicio de':'في خدمة','la luz':'الضوء','Sobre Nosotros ↓':'من نحن ↓','Nuestros Productos →':'منتجاتنا →','Nuestros Proyectos →':'مشاريعنا →','Ver imagen 1':'عرض الصورة 1','Ver imagen 2':'عرض الصورة 2','Ver imagen 3':'عرض الصورة 3','Ver imagen 4':'عرض الصورة 4','Ver imagen 5':'عرض الصورة 5','Legal':'قانوني','Todo nuestro catálogo,':'كتالوجنا الكامل،','en un solo documento':'في مستند واحد','Estamos preparando el catálogo general en PDF, con todas las familias y referencias en un solo documento. Mientras tanto, cada producto tiene su ficha técnica disponible en la sección Productos.':'نجهّز الكتالوج العام بصيغة PDF ويضم جميع الفئات والمراجع في مستند واحد. وحتى ذلك الحين، تتوفر البطاقة الفنية لكل منتج في قسم المنتجات.','¿Lo necesitas ya? Escríbenos y te lo enviamos por email.':'تحتاجه الآن؟ راسلنا وسنرسله إلى بريدك الإلكتروني.'
    }
  };

  translations.ar['Esa dirección ya no existe.'] = 'هذا الرابط غير موجود.';
  translations.ar['Volver a Productos'] = 'العودة إلى المنتجات';

  const projectTranslations = {
    en: {
      'proj-tienda-1': ['Retail','Tienda 1','Lighting for retail, combining two systems. Linear luminaires provide general light and uniformity throughout the sales area, while track spotlights illuminate the perimeter shelving, giving the products their own accent.'],
      'proj-tienda-2': ['Retail','Tienda 2','Lighting with track spotlights for accent lighting on products. Their zoom adjusts beam angles from 6° to 60°, so the same fixture can provide broad washes or tight accents, and output is controlled through a 0–10V dimmer.'],
      'proj-tienda-3': ['Retail','Tienda 3','Lighting with track spotlights for accent lighting on products. Their zoom adjusts beam angles from 6° to 60°, so the same fixture can provide broad washes or tight accents, and output is controlled through a 0–10V dimmer.'],
      'proj-tienda-4': ['Retail','Tienda 4','A combined lighting solution: linear luminaires provide general light, while adjustable recessed downlights direct the beam wherever needed. It is ideal for shops with limited ceiling height, where relying only on overhead light is not sufficient and the product must receive targeted light.'],
      'proj-tienda-5': ['Retail','Tienda 5','Lighting with spotlights adjustable in both output and beam angle. This dual adjustment allows one fixture model to cover the different areas of the shop, from the window display to the product zones, simplifying maintenance and spare parts.'],
      'proj-avenida-america-atex': ['Industry · Interchange','Avenida de América — ATEX','ATEX lighting project at the Avenida de América interchange. We used specialist luminaires for explosive atmospheres, classified for zones 2.22, across platforms, vehicle lanes, ramps and tunnels. We replaced 920 existing luminaires with 565, reducing both the number of light points and electricity consumption simply by changing the technology. DALI-dimmable luminaires with different optics and outputs were used throughout, achieving uniformity and illuminance levels above the applicable standards. Tunnel calculations follow the specific tunnel standard, with three distinct zones and therefore different illuminance levels for the carriageway and platforms. The installation required armoured cables with a metallic mesh, specially designed for ATEX-classified areas and difficult to handle. This was a highly complex project because of the different zones, their separate regulations and the demanding luminaires required to achieve the specified levels. Special thanks to the interchange management for trusting our team: a genuine challenge.'],
      'proj-avenida-america-interior': ['Industry · Interchange','Avenida de América — Interior','In this project we preserved the original luminaires by hollowing out their interiors, cleaning the lenses and fitting an internal tray with integrated LEDs and drivers. We converted luminaires originally fitted with two T5 tubes into DALI-dimmable LED luminaires. The intervention covered more than 1,200 units while retaining the interchange’s original appearance in the island area across three floors and access routes—a significant challenge.'],
      'proj-plaza-castilla': ['Industry · Interchange','Plaza Castilla Interchange','Lighting for the advertising banners at the Plaza Castilla interchange. The aim is to illuminate the printed surface so the message remains legible at night from the street. Linear lights run around the perimeter of each banner and point towards it, producing an even wash from one end to the other while keeping the equipment as inconspicuous as possible.'],
      'proj-bandalux': ['Buildings · Corporate headquarters','Bandalux','A building with very different spaces, where lighting enhances the character and particular features of each area. It ranges from the offices, with linear lighting, to exhibition areas combining linear luminaires and spotlights. The zones are separated by a planted area illuminated with LED strips and lateral and overhead lighting.'],
      'proj-ciudad-justicia': ['Buildings · Madrid','Ciudad de la Justicia','A 19-storey building for which we created a custom luminaires, with bespoke dimensions and technical requirements and excellent low-UGR visual comfort for offices, meeting rooms and courtrooms, integrated in a soft, elegant way. Each luminaire hangs approximately five centimetres below the ceiling and is surrounded by a thermoformed diffuser that conceals its base, creating a clean and pleasant appearance. Corridors and emergency stairways use vertical LED strips. The nursery features recessed spotlights arranged as constellations, with small 2W spots representing the stars. On the top floor, a celebratory hall includes two large interlocking circular luminaires with up-and-down light, creating the effect of interlocked rings. Overall, the lighting is efficient, elegant and meaningful.'],
      'proj-edificio-fontan': ['Buildings','Edificio Fontán','A contemporary building with different illuminated areas. We highlight the offices, fitted with an elegant circular suspended luminaire using a microprismatic diffuser and designed for visual comfort. The auditorium is resolved with track spotlights and LED strips.'],
      'proj-fachada-santalucia': ['Buildings · Corporate façade','Fachada Santalucía','The building is illuminated with LED strips that highlight its architectural facade elements, creating an elegant, imposing and harmonious ensemble. An integrated control system creates scenes and changes colour using intelligent RGB+CCT LED strips.'],
      'proj-plaza-eliptica': ['Buildings · Madrid','Plaza Elíptica','Conversion of the old luminaires beneath the dome to LED light engines, preserving the original aesthetic and architectural character. The project achieves energy savings of more than 65%, supported by twilight sensors. We also replaced all interior luminaires in the remaining areas, including the island and restaurant, improving uniformity and light levels.'],
      'proj-principe-pio': ['Buildings · Madrid','Príncipe Pío','An exterior linear-lighting project designed to wash the façade and highlight advertising with uniform light. IP65 luminaires equipped with special optics distribute light evenly across the whole surface. The system is controllable by RF remote to adjust the lighting intensity easily.']
    },
    ar: {
      'proj-tienda-1': ['التجزئة','متجر 1','إضاءة للتجزئة جمعنا فيها بين نظامين. وحدات الإضاءة الخطية توفّر الإضاءة العامة وتوزيعًا متجانسًا في قاعة البيع، بينما تعالج أجهزة الإنارة على السكك الإضاءة المحيطة بالأرفف، وتعطي للمنتج تسليطًا ضوئيًا واضحًا.'],
      'proj-tienda-2': ['التجزئة','متجر 2','إضاءة عاكسات مثبتة على السكك لإبراز المنتجات بشكل مميز. خاصية التكبير توفّر درجات فتحة شعاع من 6 إلى 60 درجة، وتخلي نفس الكشاف مناسب لإضاءة واسعة أو تسليط ضوئي ضيق، وشدة الإضاءة قابلة للتحكم بمتحكم 0–10 فولت.'],
      'proj-tienda-3': ['التجزئة','متجر 3','إضاءة عاكسات مثبتة على السكك لإبراز المنتجات بشكل مميز. خاصية التكبير توفّر درجات فتحة شعاع من 6 إلى 60 درجة، وتخلي نفس الكشاف مناسب لإضاءة واسعة أو تسليط ضوئي ضيق، وشدة الإضاءة قابلة للتحكم بمتحكم 0–10 فولت.'],
      'proj-tienda-4': ['التجزئة','متجر 4','حل إضاءة يجمع بين وحدات خطية للإضاءة العامة ووحدات غاطسة قابلة للتوجيه، تقدر توجه الشعاع إلى المكان المطلوب بأي وقت. هذا الحل مناسب للمحلات اللي ما فيها ارتفاع كافي بالسقف، عشان ما نعتمد بس على الإضاءة العلوية ولازم نور المنتج يكون مضبوط.'],
      'proj-tienda-5': ['التجزئة','متجر 5','إضاءة بعاكسات قابلة لضبط القدرة وزاوية الانفتاح معًا. هالتنظيم المزدوج يخلي موديل واحد يغطي احتياجات مناطق المحل، من واجهة العرض إلى مناطق المنتج، ويسهّل الصيانة واستبدال القطع.'],
      'proj-avenida-america-atex': ['الصناعة · محطة نقل','أفينيدا دي أميركا — ATEX','مشروع إضاءة ATEX في محطة نقل أفينيدا دي أميركا، استخدمنا فيه وحدات إضاءة خاصة للأجواء القابلة للانفجار وتصنيف Zones 2.22، في الأرصفة وممرات الحركة والمنحدرات والأنفاق. استبدلنا 920 وحدة قديمة بـ565 وحدة، وهذا قلّل عدد نقاط الإضاءة واستهلاك الكهرباء بسبب تحديث التقنية. استخدمنا وحدات قابلة للتحكم بنظام DALI وبعدسات وقدرات مختلفة لتغطية كل المناطق، ووصلنا لمستويات توزيع نور أعلى من اشتراطات الكودات. حسابات الأنفاق مبنية على اشتراطات الأنفاق الخاصة، وكلت لنا ثلاث مناطق بمستويات نور مختلفة إلى ممر الحركة والأرصفة. طلبت التركيبة كابلات مدرعة بشبكة معدنية، مخصصة للأماكن المصنفة ATEX ومثل هالنوعيات صعب التعامل وياها. المشروع كان معقدًا لكثرة اختلاف المناطق وكل منطقة لها اشتراطات مختلفة، وكمان الجودة المطلوبة للوحات الإضاءة عشان نوصل للمستويات المحددة. نشكر إدارة المحطة على ثقتهم بفريقنا؛ كان تحدّي حقيقي.'],
      'proj-avenida-america-interior': ['الصناعة · محطة نقل','أفينيدا دي أميركا — داخلي','في هالمشروع حافظنا على وحدات الإضاءة الأصلية، وفكينا داخلها ونظفنا البلورات وحطينا صينية داخلية فيها ليادات وإمدادات متكاملة. حوّلنا وحدات فيها أنابيب T5 إلى وحدات LED قابلة للتحكم بنظام DALI. نفذنا التدخل لأكثر من 1200 وحدة مع الحفاظ على الشكل الأصلي لمحطة النقل في منطقة الجزيرة بجميع أدوارها ومسارات الوصول، وكان التحدي حلو وصعب.'],
      'proj-plaza-castilla': ['الصناعة · محطة نقل','محطة بلازا كاستيا','إضاءة للوحات الإعلانية في محطة نقل بلازا كاستيا. الشغل إننا نوزع نور على السطح المطبوع عشان الرسالة تبقى واضحة بالليل من الشارع. حطينا خطوط إضاءة حول محيط كل لوحة وموجهة عليها، عشان الإضاءة تكون متجانسة من طرف للطرف، ووحدة الإضاءة تكون أقل ما يمكن ظاهرة.'],
      'proj-bandalux': ['المباني · مقر الشركة','باندالوكس','مبنى فيه مساحات كثيرة ومختلفة، والإضاءة فيها تعطي كل مساحة شخصيتها وتبرز ما يميزها. تبدأ الإضاءة الخطية بمناطق المكاتب، ثم مناطق العرض اللي تجمع الإضاءة الخطية بعواكس الإنارة. ومساحة خضراء تفصل بين هالمناطق ومضاءة بأشرطة LED وإضاءة جانبية وسقفية.'],
      'proj-ciudad-justicia': ['المباني · مدريد','مدينة العدالة','مبنى من 19 دور، صممنا له وحدة إضاءة جديدة بمقاسات واشتراطات تقنية خاصة وراحة بصرية منخفضة التوهج UGR، لتغطية المكاتب وغرف الاجتماعات والمحاكم بإضاءة ناعمة وأنيقة. الوحدة تكون هابطة حوالي خمس سنتيمترات عن السقف ومغطاة بعاكس حراري ما يخلّي قاعدة الوحدة ظاهرين، وناسي عليه شكل نظيف ومريح. الممرات وسلالم الطوارئ مضاءة بأشرطة LED عمودية. في الحضانة استخدمنا عواكس غاطسة مرصوصة بشكل نجوم، وبقع صغيرة بقدرة 2W تشبه نجوم السماء. وفي آخر دور فيه قاعة احتفالات حطينا وحدتين دائريتين كبيرتين متداخلتين بالإضاءة للأعلى ولأسفل، يشبهان خواتم متداخلة، وهذا عطى للمكان معنى جميل. بشكل عام الإضاءة عالية الجودة، موفرة، راقية، وفيها إحساس وفكرة واضحة.'],
      'proj-edificio-fontan': ['المباني','مبنى فونتان','مبنى معاصر فيه عدة مساحات مضاءة، نبرز فيها المكاتب بوحدة إضاءة دائرية معلقة مع ناشر ميكروبريزما، أنيقة ومصممة لراحة النظر. أما قاعة المحاضرات فقد حليناها بعواكس على سكك وأشرطة LED.'],
      'proj-fachada-santalucia': ['المباني · واجهة شركات','واجهة سانتالوسيا','المبنى مضاء بأشرطة LED تبرز عناصر واجهته المعمارية، وتعطي إحساسًا جميلًا بتسليط الضوء على التفاصيل. يتكوّن منظر راقي ومتكامل وواضح. وفي النظام تحكم متكامل لإنشاء مشاهد وتغيير الألوان من خلال شرائط LED ذكية تدعم RGB+CCT.'],
      'proj-plaza-eliptica': ['المباني · مدريد','بلازا إلِيبتكا','تحويل وحدات الإضاءة القديمة الخاصة بقبة المبنى إلى وحدات LED تحافظ على الطابع والشكل المعماري الأصلي بدون التأثير على شخصيته. حققنا توفيرًا بأكثر من 65٪ بفضل المحولات وأيضًا حساسات الإضاءة المحيطة. وحوّلنا أيضًا كل وحدات الإضاءة الداخلية لباقي المبنى في منطقة الجزيرة والمطاعم، وصارت الإضاءة أكثر تجانسًا وبمستوى نور أعلى.'],
      'proj-principe-pio': ['المباني · مدريد','برينسيبي بيو','مشروع إضاءة خطية خارجية مصمم لإضاءة واجهة المبنى وإبراز الإعلانات بنور متجانس. استخدمنا وحدات بدرجة حماية IP65 ومناسبة للخارج، ومجهزة بعدسات خاصة توزع الضوء بصورة متجانسة على كامل السطح. والنظام قابل للتحكم عن بُعد بتقنية RF، عشان يقدرون يظبطون شدة الإضاءة بسهولة.']
    }
  };

  const catalogTranslations = {
    en: {
      'Productos':'Products','Interiores':'Indoor','Exteriores':'Outdoor','Decorativas':'Decorative','Industriales':'Industrial','Hospitalarias - Salas Blancas':'Healthcare - Cleanrooms','Emergencia':'Emergency','Bombillas y Accesorios':'Bulbs & Accessories','Fuentes de Alimentación':'Power Supplies','Downlights Empotrados':'Recessed Downlights','Downlights de Superficie':'Surface Downlights','Lineales':'Linear','Retro Gold':'Retro Gold','Tiras y Perfiles LED':'LED Strips & Profiles','Proyectores de Carril':'Track Spotlights','Apliques':'Wall Lights','Balizas':'Bollards','Jardín - Estacas':'Garden - Stakes','Plafones':'Ceiling Panels','Empotrados':'Recessed','Lámparas Colgantes':'Pendant Lights','Superficie':'Surface','Campanas':'High-bay Luminaires','Estancas':'Watertight','Paneles':'Panels','Proyectores':'Spotlights','Farolas':'Streetlights','Salas Blancas':'Cleanrooms','Fuentes de 24V':'24V Drivers','Fuentes de 12V':'12V Drivers','sección':'section','secciones':'sections','producto':'product','productos':'products','referencias':'references','Ref.':'Ref.','Descripción':'Description','Fichas técnicas':'Technical sheets','Ficha técnica':'Technical sheet','Medida':'Dimension','Medidas':'Dimensions','Producto':'Product','Ambiente':'Application','Curva fotométrica':'Photometric curve','Pulsa una miniatura para verla en grande':'Select a thumbnail to view it larger','Esta ficha no trae tabla de características.':'This sheet has no specification table.'
    },
    ar: {
      'Productos':'المنتجات','Interiores':'الداخلية','Exteriores':'الخارجية','Decorativas':'الديكورية','Industriales':'الصناعية','Hospitalarias - Salas Blancas':'المستشفيات - غرف نظيفة','Emergencia':'الطوارئ','Bombillas y Accesorios':'المصابيح والإكسسوارات','Fuentes de Alimentación':'مصادر التغذية','Downlights Empotrados':'دونلايت غاطس','Downlights de Superficie':'دونلايت سطحي','Lineales':'إضاءة خطية','Retro Gold':'ريترو جولد','Tiras y Perfiles LED':'شرائط LED وبروفيلات','Proyectores de Carril':'عواكس سكك','Apliques':'إنارة جدارية','Balizas':'بالايز','Jardín - Estacas':'حدائق - أوتاد','Plafones':'لوحات سقفية','Empotrados':'غاطس','Lámparas Colgantes':'لمبات معلقة','Superficie':'سطحي','Campanas':'ثريات صناعية','Estancas':'محكم ضد الماء','Paneles':'بانلات','Proyectores':'عواكس','Farolas':'فوانيس الشوارع','Salas Blancas':'غرف نظيفة','Fuentes de 24V':'محولات 24 فولت','Fuentes de 12V':'محولات 12 فولت','sección':'قسم','secciones':'أقسام','producto':'منتج','productos':'منتجات','referencias':'مراجع','Ref.':'مرجع','Descripción':'الوصف','Fichas técnicas':'البطاقات الفنية','Ficha técnica':'بطاقة فنية','Medida':'المقاس','Medidas':'المقاسات','Producto':'المنتج','Ambiente':'بيئة التطبيق','Curva fotométrica':'المنحنى الضوئي','Pulsa una miniatura para verla en grande':'اضغط على الصورة المصغرة لعرضها بحجم أكبر','Esta ficha no trae tabla de características.':'هذه البطاقة ما فيها جدول مواصفات.'
    }
  };

  const tableLabelsManual = {
    en: {
      'Potencia total luminaria':'Total luminaire power','Potencia total':'Total power','Potencia Máxima':'Maximum power','Potencia W/mt.':'Power W/m','Lúmenes reales':'Actual luminous flux','Lumenes reales':'Actual luminous flux','Lúmenes':'Lumens','Lúmenes reales: Rollo 5mt.':'Actual luminous flux: 5 m roll','Lúmenes reales: Rollo 10mt.':'Actual luminous flux: 10 m roll','Lúmenes reales: Rollo 50mt.':'Actual luminous flux: 50 m roll','Lm / W reales':'Real efficacy','Temperatura de color':'Correlated colour temperature','Temperatura de color: A elegir':'Correlated colour temperature: selectable','Temperatura de color correlacionada':'Correlated colour temperature','Temperatura de color correlacionada (CCT)':'Correlated colour temperature (CCT)','Temperatura de color correlacionada (3CCT)':'Correlated colour temperature (3CCT)','Ángulo Ópticas / Reflector':'Beam angle / reflector','Acabado estructura':'Structure finish','Acabado difusor':'Diffuser finish','Acabado':'Finish','Acabados':'Finishes','Material de la estructura':'Structure material','Material del difusor':'Diffuser material','Clase de aislamiento':'Insulation class','Voltaje / Frecuencia':'Voltage / frequency','Tensión de entrada':'Input voltage','Protocolo de regulación':'Dimming protocol','Opcional regulación':'Optional dimming','Factor de potencia':'Power factor','Vida útil':'Rated lifetime','Garantía':'Warranty','Medida':'Dimensions','Medidas de corte':'Cut-out dimensions','Marca Driver':'Driver brand','Material':'Material','Temperatura de trabajo':'Operating temperature','Temperatura De Trabajo':'Operating temperature','Tiempo de carga':'Charging time','Tiempo De Carga':'Charging time','Tiempo De Uso':'Runtime','Autonomia':'Runtime','Autonomía':'Runtime','Bateria':'Battery','Batería':'Battery','Protecciones':'Protections','Salida':'Output','Tipo LED':'LED type','CRI':'CRI','IP':'IP','IK':'IK','UGR':'UGR','Lúmenes x metro (lm/mt)':'Lumens per metre (lm/m)','Máx. Enlazable':'Maximum linked length','Distancia De Detección':'Detection distance','Modo funcionamiento':'Operating mode','Tecnología batería':'Battery technology','Autotest':'Self-test','Rango de frecuencia':'Frequency range','Driver':'Driver','Flujo total':'Total luminous flux','Riesgo fotobiologico (GR)':'Photobiological risk (RG)','Protección Contra Cortocircuito':'Short-circuit protection','Protección De Sobrecarga':'Overload protection'
    },
    ar: {
      'Potencia total luminaria':'إجمالي قدرة وحدة الإضاءة','Potencia total':'القدرة الإجمالية','Potencia Máxima':'القدرة القصوى','Potencia W/mt.':'القدرة واط/متر','Lúmenes reales':'التدفق الضوئي الفعلي','Lumenes reales':'التدفق الضوئي الفعلي','Lúmenes':'اللومن','Lm / W reales':'الكفاءة الفعلية لم/واط','Temperatura de color':'درجة حرارة اللون','Temperatura de color: A elegir':'درجة حرارة اللون: قابلة للاختيار','Temperatura de color correlacionada':'درجة حرارة اللون المرتبط','Temperatura de color correlacionada (CCT)':'درجة حرارة اللون المرتبط (CCT)','Temperatura de color correlacionada (3CCT)':'درجة حرارة اللون المرتبط (3CCT)','Ángulo Ópticas / Reflector':'زاوية الشعاع / العاكس','Acabado estructura':'تشطيب الهيكل','Acabado difusor':'تشطيب الناشر','Acabado':'التشطيب','Acabados':'التشطيبات','Material de la estructura':'مادة الهيكل','Material del difusor':'مادة الناشر','Clase de aislamiento':'فئة العزل','Voltaje / Frecuencia':'الجهد / التردد','Tensión de entrada':'جهد الإدخال','Protocolo de regulación':'نظام التحكّم بالإضاءة','Opcional regulación':'تحكّم اختياري','Factor de potencia':'معامل القدرة','Vida útil':'العمر التشغيلي','Garantía':'الضمان','Medida':'الأبعاد','Medidas de corte':'أبعاد الفتحة','Marca Driver':'علامة موزع الطاقة','Material':'المادة','Temperatura de trabajo':'درجة حرارة التشغيل','Temperatura De Trabajo':'درجة حرارة التشغيل','Tiempo de carga':'وقت الشحن','Tiempo De Carga':'وقت الشحن','Tiempo De Uso':'مدة التشغيل','Autonomia':'مدة التشغيل','Autونومía':'مدة التشغيل','Bateria':'البطارية','Batería':'البطارية','Protecciones':'الحمايات','Salida':'المخرج','Tipo LED':'نوع LED','CRI':'CRI','IP':'IP','IK':'IK','UGR':'UGR','Lúmenes x metro (lm/mt)':'اللومن لكل متر (lm/m)','Máx. Enlazable':'الحد الأقصى للتوصيل المتسلسل','Distancia De Detección':'مسافة الكشف','Modo funcionamiento':'نظام التشغيل','Tecnología batería':'تقنية البطارية','Autotest':'اختبار ذاتي','Rango de frecuencia':'نطاق التردد','Driver':'مزود طاقة','Flujo total':'التدفق الضوئي الإجمالي','Riesgo fotobiologico (GR)':'المخاطر الضوئية الحيوية (RG)','Protección Contra Cortocircuito':'حماية ضد القصر','Protección De Sobrecarga':'حماية ضد الحمل الزائد'
    }
  };

  const tableValuesManual = {
    en: {'Aluminio':'Aluminium','Acero inoxidable':'Stainless steel','Cristal':'Glass','PMMA':'PMMA','Blanco':'White','Negro':'Black','Negro o blanco':'Black or white','Negro o Blanco':'Black or white','Transparente':'Transparent','OPAL':'Opal','Sí':'Yes','Si':'Yes','No':'No','ON-OFF':'ON-OFF','DALI':'DALI','TRIAC':'TRIAC','CASAMBI':'CASAMBI','Integrado':'Integrated','Integrada':'Integrated','Anodizado':'Anodised','Gris':'Grey','Plateado':'Silver','Niquel':'Nickel','Sensible a presencia':'Presence sensing','Inclinación':'Tilting','Basculante':'Adjustable','Fijo':'Fixed','Orientable':'Adjustable','IP20':'IP20','IP54':'IP54','IP65':'IP65','IP66':'IP66','IP67':'IP67','IK05':'IK05','IK08':'IK08','I':'I','II':'II','III':'III'},
    ar: {'Aluminio':'ألمنيوم','Acero inoxidable':'فولاذ مقاوم للصدأ','Cristal':'زجاج','PMMA':'PMMA','Blanco':'أبيض','Negro':'أسود','Negro o blanco':'أسود أو أبيض','Negro o Blanco':'أسود أو أبيض','Transparente':'شفاف','OPAL':'أوبال','Sí':'نعم','Si':'نعم','No':'لا','ON-OFF':'تشغيل-إطفاء','DALI':'DALI','TRIAC':'TRIAC','CASAMBI':'CASAMBI','Integrado':'مدمج','Integrada':'مدمجة','Anodizado':'أنوديزد','Gris':'رمادي','Plateado':'فضي','Niquel':'نيكل','Sensible a presencia':'حساس للحركة','Inclinación':'ميل','Basculante':'قابل للإمالة','Fijo':'ثابت','Orientable':'قابل للتوجيه','IP20':'IP20','IP54':'IP54','IP65':'IP65','IP66':'IP66','IP67':'IP67','IK05':'IK05','IK08':'IK08','I':'I','II':'II','III':'III'}
  };

  // Los diccionarios del catálogo van en js/i18n-datos-{en,ar}.js (los genera
  // scripts/empaquetar_traducciones.py). Se cargan con <script> y no con fetch()
  // para que funcionen también al abrir las páginas con doble clic (file://).
  let descriptionTranslations = null;
  let catalogSummaryTranslations = null;
  let tableLabelTranslations = null;
  let tableValueTranslations = null;
  let loadingTranslations = null;

  function loadCompleteTranslations() {
    if (lang === 'es') return Promise.resolve();
    if (!loadingTranslations) {
      loadingTranslations = new Promise(resolve => {
        const script = document.createElement('script');
        script.src = `js/i18n-datos-${lang}.js`;
        script.onload = script.onerror = () => {
          const datos = window.APHE_I18N_DATOS || {};
          descriptionTranslations = datos.textos || {};
          catalogSummaryTranslations = datos.resumenes || {};
          tableLabelTranslations = datos.etiquetas || {};
          tableValueTranslations = datos.valores || {};
          resolve();
        };
        document.head.appendChild(script);
      });
    }
    return loadingTranslations;
  }

  const saved = localStorage.getItem('apheloria-language');
  const lang = saved && PARAMS.includes(saved) ? saved : 'es';
  window.APHE_LANGUAGE = lang;

  function tr(text) {
    if (lang === 'es' || !text) return text;
    const clean = text.replace(/\s+/g, ' ').trim();
    const dict = translations[lang] || {};
    if (dict[clean]) return dict[clean];
    if (dict[text]) return dict[text];
    return text;
  }

  function translateNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const value = node.textContent;
      const translated = tr(value);
      if (translated !== value) node.textContent = translated;
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      if (node.matches('[data-i18n-ignore]')) return;
      if (node.hasAttribute('placeholder')) {
        const key = node.getAttribute('placeholder');
        node.setAttribute('placeholder', tr(key));
        node.setAttribute('aria-label', tr(node.getAttribute('aria-label') || key));
      }
      if (node.hasAttribute('aria-label') && node.tagName !== 'INPUT') {
        const key = node.getAttribute('aria-label');
        node.setAttribute('aria-label', tr(key));
      }
      if (node.tagName === 'TITLE') node.textContent = tr(node.textContent);
      Array.from(node.childNodes).forEach(translateNode);
    }
  }

  function applyProjects() {
    const projects = projectTranslations[lang];
    if (!projects) return;
    document.querySelectorAll('.project-detail-view').forEach(panel => {
      const text = projects[panel.id];
      if (!text) return;
      panel.querySelectorAll('.project-detail-eyebrow').forEach(el => { el.textContent = text[0]; });
      panel.querySelectorAll('.project-detail-title, .pdb-current').forEach(el => { el.textContent = text[1]; });
      panel.querySelectorAll('.project-detail-text').forEach(el => { el.textContent = text[2]; });
    });

    document.querySelectorAll('.project-card').forEach(card => {
      const panelId = card.getAttribute('data-open');
      const text = projects[panelId];
      if (!text) return;
      card.querySelectorAll('.project-card-name').forEach(el => { el.textContent = text[1]; });
      card.querySelectorAll('.project-card-meta').forEach(el => { el.textContent = text[0]; });
    });
  }

  function applyCatalog() {
    if (lang === 'es' || !window.CATALOGO) return;
    const map = catalogTranslations[lang];
    if (!map) return;

    function translateCatalogNode(node) {
      if (typeof node.nombre === 'string' && map[node.nombre]) node.nombre = map[node.nombre];
      if (typeof node.texto === 'string' && node.texto) node.texto = tr(node.texto);
      if (Array.isArray(node.descripcion)) node.descripcion = node.descripcion.map(text => tr(text));
      if (typeof node.resumen === 'string') node.resumen = tr(node.resumen);
      (node.hijos || []).forEach(translateCatalogNode);
      (node.productos || []).forEach(producto => {
        if (typeof producto.nombre === 'string' && map[producto.nombre]) producto.nombre = map[producto.nombre];
        if (typeof producto.resumen === 'string') producto.resumen = tr(producto.resumen);
        if (Array.isArray(producto.descripcion)) producto.descripcion = producto.descripcion.map(text => tr(text));
        if (Array.isArray(producto.notas)) producto.notas = producto.notas.map(text => tr(text));
        if (Array.isArray(producto.tabla)) producto.tabla = producto.tabla.map(([label, value]) => [tr(label), value]);
      });
    }

    translateCatalogNode(window.CATALOGO);
  }

  async function applyCatalogDynamic() {
    if (lang === 'es' || !window.CATALOGO) return;
    await loadCompleteTranslations();
    window.dispatchEvent(new Event('apheloria-i18n-ready'));
  }

  function applyCatalogLabels() {
    if (lang === 'es') return;
    const map = catalogTranslations[lang];
    document.querySelectorAll('.cat-hero-titulo, .cat-hero-eyebrow, .cat-card-nombre, .cat-ruta a, .cat-ruta-actual, .ficha-titulo, img[alt], .ficha-mini[title]').forEach(el => {
      const attribute = el.matches('img[alt]') ? 'alt' : el.matches('.ficha-mini[title]') ? 'title' : null;
      const source = (attribute ? el.getAttribute(attribute) : el.textContent).trim();
      const translation = source.split(/( · )/).map(part => part === ' · ' ? part : map?.[part.trim()] || translateProductName(part)).join('');
      if (translation !== source) {
        if (attribute) el.setAttribute(attribute, translation);
        else el.textContent = translation;
      }
      if (el.matches('.ficha-mini')) {
        const label = translateProductName(el.getAttribute('aria-label') || '');
        if (label) el.setAttribute('aria-label', label);
      }
    });
    document.querySelectorAll('.cat-apartado, .cat-card-meta, .cat-vacio, .ficha-rotulo, .ficha-mini-pie, .ficha-refs, details summary').forEach(el => {
      let text = el.textContent;
      const summary = catalogSummaryTranslations?.[text.trim()];
      if (summary) {
        text = summary;
      } else {
        const words = lang === 'ar'
          ? { secciones: 'أقسام', sección: 'قسم', productos: 'منتجات', producto: 'منتج', referencias: 'مراجع' }
          : { secciones: 'sections', sección: 'section', productos: 'products', producto: 'product', referencias: 'references' };
        text = text.replace(/\b(secciones|sección|productos|producto|referencias)\b/gi, word => words[word.toLowerCase()] || word);
      }
      // Solo si cambia: cada escritura avisa al MutationObserver, que vuelve a llamar aquí.
      if (text !== el.textContent) el.textContent = text;
    });
  }

  const productNameWords = {
    en: {
      'downlights':'downlights','downlight':'downlight','luminarias':'luminaires','luminaria':'luminaire',
      'proyectores':'spotlights','proyector':'spotlight','farolas':'street lights','farola':'street light',
      'pantallas':'luminaires','pantalla':'luminaire','perfiles':'profiles','perfil':'profile',
      'tiras':'strips','tira':'strip','campanas':'high-bay luminaires','campana':'high-bay luminaire',
      'estancas':'sealed battens','estanca':'sealed batten','balizas':'bollards','baliza':'bollard',
      'apliques':'wall lights','aplique':'wall light','emergencia':'emergency','hospitalaria':'healthcare',
      'hospitalarias':'healthcare','exteriores':'outdoor','exterior':'outdoor','interiores':'indoor','interior':'indoor',
      'empotrable':'recessed','empotrable':'recessed','empotrados':'recessed','empotradas':'recessed','empotrado':'recessed',
      'empotrar':'recess','superficie':'surface-mounted','superficial':'surface-mounted','suspender':'suspend',
      'suspendida':'suspended','suspendido':'suspended','colgante':'pendant','orientable':'adjustable','orientables':'adjustable',
      'circular':'circular','cuadrado':'square','cuadrada':'square','rectangular':'rectangular','lineal':'linear',
      'flexible':'flexible','pared':'wall','techo':'ceiling','blanco':'white','blanca':'white','negro':'black',
      'negra':'black','doble':'double','triple':'triple','tipo':'type','modelo':'model','mod.':'model',
      'de':'of','del':'of the','la':'the','el':'the','y':'and','o':'or','en':'in','para':'for','con':'with','aluminio':'aluminium','acero':'steel','inoxidable':'stainless steel',
      'accesorios':'accessories','accesorio':'accessory','fuentes':'power supplies','fuente':'power supply',
      'alimentación':'power','regulador':'controller','controlador':'controller','monocolor':'single-colour',
      'cubo':'cube','bolardo':'bollard','pincho':'spike','montaje':'mounting','integrado':'integrated',
      'integrada':'integrated','calle':'street','calles':'streets','luz':'light','indirecta':'indirect','grandes':'high',
      'alturas':'bay','paso':'step','farol':'lantern','acabado':'finish','pintado':'painted','libre':'clearance',
      'corte':'cut-out','cuerpo':'body','tubo':'tube','capi':'CAPI','solar':'solar',
      'panel':'panel','paneles':'panels','led':'LED','smd':'SMD','lampara':'lamp','lámpara':'lamp',
      'supender':'suspend','emergrncia':'emergency','alimentacion':'power','jardin':'garden','jardín':'garden',
      'alto':'height','alta':'high','fondo':'depth','hueco':'cut-out','ancho':'width','largo':'length'
    },
    ar: {
      'downlights':'داون لايت','downlight':'داون لايت','luminarias':'وحدات إنارة','luminaria':'وحدة إنارة',
      'proyectores':'كشافات','proyector':'كشاف','farolas':'أعمدة إنارة','farola':'عمود إنارة',
      'pantallas':'وحدات إنارة','pantalla':'وحدة إنارة','perfiles':'بروفايلات','perfil':'بروفايل',
      'tiras':'شرائط','tira':'شريط','campanas':'وحدات هاي باي','campana':'وحدة هاي باي',
      'estancas':'وحدات محكمة الإغلاق','estanca':'وحدة محكمة الإغلاق','balizas':'إنارة أرضية','baliza':'إنارة أرضية',
      'apliques':'إنارة جدارية','aplique':'إنارة جدارية','emergencia':'طوارئ','hospitalaria':'للمستشفيات',
      'hospitalarias':'للمستشفيات','exteriores':'خارجية','exterior':'خارجي','interiores':'داخلية','interior':'داخلي',
      'empotrable':'غاطس','empotrables':'غاطسة','empotrados':'غاطسة','empotradas':'غاطسة','empotrado':'غاطس',
      'empotrar':'للتركيب الغاطس','superficie':'سطحي','superficial':'سطحي','suspender':'للتعليق',
      'suspendida':'معلقة','suspendido':'معلق','colgante':'معلق','orientable':'قابل للتوجيه','orientables':'قابلة للتوجيه',
      'circular':'دائري','cuadrado':'مربع','cuadrada':'مربعة','rectangular':'مستطيل','lineal':'خطي',
      'flexible':'مرن','pared':'الجدار','techo':'السقف','blanco':'أبيض','blanca':'بيضاء','negro':'أسود',
      'negra':'سوداء','doble':'مزدوج','triple':'ثلاثي','tipo':'نوع','modelo':'موديل','mod.':'موديل',
      'de':'من','del':'من الـ','la':'الـ','el':'الـ','y':'و','o':'أو','en':'في','para':'لـ','con':'مع','aluminio':'ألمنيوم','acero':'فولاذ','inoxidable':'مقاوم للصدأ',
      'accesorios':'إكسسوارات','accesorio':'إكسسوار','fuentes':'مزودات طاقة','fuente':'مزود طاقة',
      'alimentación':'طاقة','regulador':'متحكم','controlador':'متحكم','monocolor':'أحادي اللون',
      'cubo':'مكعب','bolardo':'بولارد','pincho':'وتد','montaje':'تركيب','integrado':'مدمج',
      'integrada':'مدمجة','calle':'شارع','calles':'شوارع','luz':'ضوء','indirecta':'غير مباشر','grandes':'عالية',
      'alturas':'الارتفاعات','paso':'ممر','farol':'فانوس','acabado':'تشطيب','pintado':'مطلي','libre':'متاح',
      'corte':'فتحة','cuerpo':'هيكل','tubo':'أنبوب','capi':'CAPI','solar':'شمسي',
      'panel':'بانل','paneles':'بانلات','led':'LED','smd':'SMD','lampara':'مصباح','lámpara':'مصباح',
      'supender':'معلق','emergrncia':'طوارئ','alimentacion':'طاقة','jardin':'حديقة','jardín':'حديقة',
      'alto':'ارتفاع','alta':'عالية','fondo':'عمق','hueco':'فتحة','ancho':'عرض','largo':'طول'
    }
  };

  function translateProductName(source) {
    const words = productNameWords[lang];
    if (!words || !source) return source;
    const boundary = '(^|[^A-Za-zÀ-ÖØ-öø-ÿ0-9])';
    const end = '(?=$|[^A-Za-zÀ-ÖØ-öø-ÿ0-9])';
    let result = source;
    Object.entries(words).sort(([a],[b]) => b.length-a.length).forEach(([word, replacement]) => {
      const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      result = result.replace(new RegExp(boundary + escaped + end, 'giu'), (_, prefix) => prefix + replacement);
    });
    return result;
  }

  function applyLanguage() {
    applyCatalogDynamic();
    applyCompleteCatalogTranslations();
    document.documentElement.lang = lang === 'ar' ? 'ar-KW' : lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.body.classList.toggle('lang-ar', lang === 'ar');
    document.body.classList.toggle('lang-en', lang === 'en');
    document.querySelectorAll('main, footer, nav, title').forEach(translateNode);
    applyCatalogLabels();
    applyProjects();
    document.querySelectorAll('.nav-links a, .nav-dropdown a, .nav-contact-btn').forEach(a => {
      const key = a.textContent.trim();
      if (translations[lang]?.[key]) a.textContent = translations[lang][key];
    });
    document.querySelectorAll('meta[name="description"], meta[property="og:title"], meta[property="og:description"]').forEach(meta => {
      meta.content = tr(meta.content);
    });
  }

  function buildSwitcher() {
    const navRight = document.querySelector('.nav-right');
    if (!navRight || document.querySelector('.language-switcher')) return;
    const box = document.createElement('div');
    box.className = 'language-switcher';
    box.setAttribute('aria-label', lang === 'ar' ? 'اختيار اللغة' : lang === 'en' ? 'Language' : 'Idioma');
    const names = { es: 'ES', en: 'EN', ar: 'ع' };
    PARAMS.forEach(code => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = names[code];
      button.lang = code === 'ar' ? 'ar-KW' : code;
      button.classList.toggle('active', code === lang);
      button.setAttribute('aria-label', code === 'es' ? 'Español' : code === 'en' ? 'English' : 'العربية الكويتية');
      button.addEventListener('click', () => {
        localStorage.setItem('apheloria-language', code);
        location.reload();
      });
      box.appendChild(button);
    });
    navRight.insertBefore(box, navRight.firstChild);
  }

  function observeDynamicContent() {
    const target = document.body;
    if (!target) return;
    const observer = new MutationObserver(records => {
      records.forEach(record => record.addedNodes.forEach(node => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          translateNode(node);
          applyCompleteCatalogTranslations();
        }
      }));
    });
    observer.observe(target, { childList: true, subtree: true });
  }

  async function applyCompleteCatalogTranslations() {
    await loadCompleteTranslations();
    applyCatalogLabels();

    document.querySelectorAll('.ficha-desc p, .ficha-notas li, .cat-hero-texto, .cat-card-meta').forEach(el => {
      const original = el.textContent.trim();
      if (catalogSummaryTranslations?.[original]) el.textContent = catalogSummaryTranslations[original];
      else if (descriptionTranslations?.[original]) el.textContent = descriptionTranslations[original];
    });

    document.querySelectorAll('.ficha-tabla th').forEach(el => {
      const original = el.textContent.trim();
      if (tableLabelsManual[lang]?.[original]) el.textContent = tableLabelsManual[lang][original];
      else if (tableLabelTranslations?.[original]) el.textContent = tableLabelTranslations[original];
    });

    document.querySelectorAll('.ficha-tabla td').forEach(el => {
      const original = el.textContent.trim();
      if (tableValuesManual[lang]?.[original]) el.textContent = tableValuesManual[lang][original];
      else if (tableValueTranslations?.[original]) el.textContent = tableValueTranslations[original];
    });

    document.querySelectorAll('.ficha-descarga').forEach(link => {
      const label = lang === 'ar' ? 'بطاقة فنية' : 'Technical sheet';
      const textNode = [...link.childNodes].find(node => node.nodeType === Node.TEXT_NODE);
      if (textNode) textNode.textContent = textNode.textContent.replace(/^\s*Ficha técnica/, ` ${label}`);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      buildSwitcher();
      applyLanguage();
      observeDynamicContent();
    });
  } else {
    buildSwitcher();
    applyLanguage();
    observeDynamicContent();
  }

  window.APHELORIA_TRANSLATE_COMPLETE = applyCompleteCatalogTranslations;
})();
