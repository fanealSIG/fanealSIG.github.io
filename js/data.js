// ═══════════════════════════════════════════════════════════
//  DATA.JS — Edit this file to update all portfolio content
// ═══════════════════════════════════════════════════════════

const NAV_LABELS = {
  en: ['Skills', 'Experience', 'Education', 'Certifications', 'Awards', 'Contact'],
  es: ['Habilidades', 'Experiencia', 'Educación', 'Certificados', 'Reconocimientos', 'Contacto']
};

const NAV_HREFS = ['#skills', '#experience', '#education', '#certifications', '#awards', '#contact'];

// ── SKILLS ──────────────────────────────────────────────────
const SKILLS = [
  {
    icon: '🗺️',
    en: { name: 'ESRI Platform', desc: 'Administration, configuration, and support of federated ArcGIS environments.' },
    es: { name: 'Plataforma ESRI', desc: 'Administración, configuración y soporte de entornos ArcGIS federados.' },
    tags: ['ArcGIS Enterprise', 'ArcGIS Pro', 'ArcGIS Online', 'ArcGIS Server']
  },
  {
    icon: '⚙️',
    en: { name: 'Automation & Dev', desc: 'Python-driven workflows for service publishing, data management, and toolbox development.' },
    es: { name: 'Automatización y Desarrollo', desc: 'Flujos Python para publicación de servicios, gestión de datos y desarrollo de toolboxes.' },
    tags: ['Python', 'ArcPy', 'Python Toolboxes', 'REST API']
  },
  {
    icon: '🌐',
    en: { name: 'Open Source GIS', desc: 'Full open source stack for spatial data publishing and web mapping.' },
    es: { name: 'SIG Open Source', desc: 'Stack open source completo para publicación de datos espaciales y mapeo web.' },
    tags: ['QGIS', 'GeoServer', 'PostGIS', 'Leaflet']
  },
  {
    icon: '☁️',
    en: { name: 'Cloud & Interoperability', desc: 'Cloud-hosted GIS services and OGC-compliant data sharing.' },
    es: { name: 'Nube e Interoperabilidad', desc: 'Servicios SIG en la nube y compartición de datos conforme a OGC.' },
    tags: ['ArcGIS Online', 'WMS / WFS', 'OAuth2', 'REST']
  },
  {
    icon: '🛰️',
    en: { name: 'Remote Sensing', desc: 'SAR and optical satellite imagery processing for environmental and territorial analysis.' },
    es: { name: 'Teledetección', desc: 'Procesamiento de imágenes SAR y ópticas para análisis ambiental y territorial.' },
    tags: ['Sentinel-1 SAR', 'Google Earth Engine', 'SNAP']
  },
  {
    icon: '🤖',
    en: { name: 'AI in GIS', desc: 'Integration of AI agents and LLMs into geospatial workflows using Claude and Google AI.' },
    es: { name: 'IA en SIG', desc: 'Integración de agentes IA y LLMs en flujos geoespaciales con Claude y Google AI.' },
    tags: ['Claude (Anthropic)', 'Google Gemini', 'AI Agents', 'LLM']
  },
  {
    icon: '🗄️',
    en: { name: 'Spatial Databases', desc: 'Multi-user geodatabase administration, versioning, and data integrity.' },
    es: { name: 'Bases de Datos Espaciales', desc: 'Administración de geodatabases multiusuario, versionamiento e integridad de datos.' },
    tags: ['Enterprise Geodatabase', 'Branch Versioning', 'Replication', 'SQL']
  },
  {
    icon: '👥',
    en: { name: 'Leadership & Training', desc: 'Team management, instructional design, and technical knowledge transfer.' },
    es: { name: 'Liderazgo y Capacitación', desc: 'Gestión de equipos, diseño instruccional y transferencia de conocimiento técnico.' },
    tags: ['Scrum / Agile', 'Curriculum Design', 'UNIR Certified', 'Mentoring']
  }
];

// ── EXPERIENCE ───────────────────────────────────────────────
const EXPERIENCE = [
  {
    date: '2025 – PRESENT',
    en: {
      role: 'GIS Instructor — University Level',
      bullets: [
        'Design and deliver the GIS for Public Administration course at Politécnico Jaime Isaza Cadavid, integrating open source tools and cloud platforms for territorial management.',
        'Develop curriculum materials combining QGIS, ArcGIS Online, and Google Earth Engine for non-technical student profiles.',
        'Completing a Diploma in University Teaching — certified to design organizational learning plans and structured training programs.'
      ]
    },
    es: {
      role: 'Profesor de Cátedra SIG — Nivel Universitario',
      bullets: [
        'Diseño y dicto el curso de SIG para Administración Pública en el Politécnico Jaime Isaza Cadavid, integrando herramientas open source y plataformas en la nube para gestión territorial.',
        'Desarrollo materiales curriculares combinando QGIS, ArcGIS Online y Google Earth Engine para estudiantes sin perfil técnico.',
        'Cursando el Diplomado en Docencia Universitaria — habilitado para diseñar planes de aprendizaje y programas de capacitación en organizaciones.'
      ]
    },
    company: 'Politécnico Jaime Isaza Cadavid · Medellín, Colombia'
  },
  {
    date: '2021 – PRESENT',
    en: {
      role: 'GIS Infrastructure & Support Specialist',
      bullets: [
        'Work at HYG Consultores S.A.S., a GIS consulting firm, providing transversal GIS support across projects for public and private sector clients including Municipio de Envigado, Municipio de Itagüí, Cornare, BanCO2, Corantioquia, Metro de Medellín, ISA, and ISAGEN.',
        'Currently dedicated full-time to Geosura — a national geospatial platform — administering its federated ArcGIS Enterprise 11.x environment and ensuring continuous availability of web GIS services across 3+ business units.',
        'Automated the full service publishing lifecycle with Python Toolboxes (ArcPy), cutting deployment time by ~60% and eliminating manual errors.',
        'Diagnose and resolve incidents in corporate GIS infrastructure, coordinating with IT teams to maintain service continuity and data integrity.',
        'Implemented OAuth2 Client Credentials flow for a public-facing geoportal, managing token lifecycle and service-sharing strategies.',
        'Provide Level 2 technical support to GIS users across ArcGIS Pro, ArcGIS Online, and QGIS — configuration, service access, symbology, and performance.',
        'Designed a corporate Web GIS methodology based on OGC standards (WMS/WFS/REST), integrating ESRI and open source platforms.'
      ]
    },
    es: {
      role: 'Especialista SIG — Soporte e Infraestructura',
      bullets: [
        'Trabajo en HYG Consultores S.A.S., firma consultora GIS, brindando soporte SIG transversal en proyectos para clientes públicos y privados: Municipio de Envigado, Municipio de Itagüí, Cornare, BanCO2, Corantioquia, Metro de Medellín, ISA e ISAGEN.',
        'Actualmente dedicado de lleno a Geosura — plataforma geoespacial nacional — administrando su entorno ArcGIS Enterprise 11.x federado y garantizando la disponibilidad continua de servicios Web SIG en más de 3 unidades de negocio.',
        'Automaticé el ciclo completo de publicación de servicios con Python Toolboxes (ArcPy), reduciendo el tiempo de despliegue en ~60% y eliminando errores manuales.',
        'Diagnostico y resuelvo incidentes en la infraestructura SIG corporativa, coordinando con equipos TI para mantener la continuidad del servicio e integridad de los datos.',
        'Implementé el flujo OAuth2 Client Credentials para un geoportal público, gestionando el ciclo de vida de tokens y estrategias de compartición de servicios.',
        'Brindo soporte técnico nivel 2 a usuarios SIG en ArcGIS Pro, ArcGIS Online y QGIS — configuración, acceso a servicios, simbología y rendimiento.',
        'Diseñé una metodología Web GIS corporativa basada en estándares OGC (WMS/WFS/REST), integrando plataformas ESRI y open source.'
      ]
    },
    company: 'HYG Consultores S.A.S. · Medellín, Colombia'
  },
  {
    date: '2019 – 2021',
    en: {
      role: 'Engineering Support Intern — GIS & Infrastructure',
      bullets: [
        'Processed geographic databases for water and sewage infrastructure systems, supporting data loading and validation on the HydroCaz platform.',
        'Handled topographic data and raster layers (DTMs, orthophotographs) for environmental and hydraulic infrastructure projects.',
        'Created, reprojected, and converted vector elements in GIS environments, ensuring geometric and attribute data consistency.'
      ]
    },
    es: {
      role: 'Auxiliar de Ingeniería — SIG e Infraestructura',
      bullets: [
        'Procesé y gestioné bases de datos geográficas para sistemas de acueducto y alcantarillado, apoyando la carga y validación en la plataforma HydroCaz.',
        'Manejé datos topográficos y capas ráster (MDT, ortofotografías) para proyectos de infraestructura ambiental e hídrica.',
        'Creé, reproyecté y convertí elementos vectoriales en entornos SIG, asegurando la consistencia geométrica y de atributos.'
      ]
    },
    company: 'LINTEK S.A.S. · Colombia'
  },
];

// ── EDUCATION ────────────────────────────────────────────────
const EDUCATION = [
  {
    year: { en: '2024 – Jun 2025', es: '2024 – Jun 2025' },
    en: { degree: 'GIS Specialization (Posgrado)', note: 'Advanced spatial analysis, Python automation, satellite imagery processing. ArcGIS Pro, QGIS, SNAP, Google Earth Engine. Thesis: SAR technology (Sentinel-1) for automated waterbody detection in coastal zones.' },
    es: { degree: 'Especialización en Sistemas de Información Geográfica', note: 'Análisis espacial avanzado, automatización con Python, procesamiento de imágenes satelitales. ArcGIS Pro, QGIS, SNAP, Google Earth Engine. Trabajo de grado: SAR (Sentinel-1) para identificación de cuerpos de agua en zonas costeras.' },
    institution: 'Universidad de Manizales'
  },
  {
    year: { en: 'Mar 2021', es: 'Mar 2021' },
    en: { degree: 'Environmental Engineering (B.Sc.)', note: 'Complementary studies in modelling, geomatics, risk management, water resource planning, and environmental auditing.' },
    es: { degree: 'Ingeniería Ambiental', note: 'Estudios complementarios en modelación, geomática, gestión del riesgo, planificación de recursos hídricos y auditoría ambiental.' },
    institution: 'Universidad de Antioquia'
  },
];

// ── CERTIFICATIONS ───────────────────────────────────────────
// Organized by category for rendering with group headers
const CERT_GROUPS = [
  {
    en: { group: 'ESRI / ArcGIS Platform' },
    es: { group: 'Plataforma ESRI / ArcGIS' },
    items: [
      {
        icon: '🏅',
        year: { en: 'Oct 2022', es: 'Oct 2022' },
        en: { name: 'ArcGIS Systems Administration Diploma', issuer: 'Esri Colombia · 180 hours', note: 'Full diploma covering Enterprise configuration, branch versioning, geodatabase replication, and multiuser workflows.' },
        es: { name: 'Diplomado en Administración de Sistemas ArcGIS', issuer: 'Esri Colombia · 180 horas', note: 'Diplomado completo sobre configuración Enterprise, versionamiento Branch, replicación de geodatabases y flujos multiusuario.' }
      },
      {
        icon: '⚙️',
        year: { en: 'Apr 2024', es: 'Abr 2024' },
        en: { name: 'ArcGIS Enterprise: Administration Workflows', issuer: 'Esri Colombia · ID 16261', note: 'Advanced enterprise GIS administration workflows, monitoring, and maintenance best practices.' },
        es: { name: 'ArcGIS Enterprise: Administration Workflows', issuer: 'Esri Colombia · ID 16261', note: 'Flujos de trabajo avanzados de administración de Enterprise GIS, monitoreo y mejores prácticas de mantenimiento.' }
      },
      {
        icon: '🖥️',
        year: { en: 'Aug 2022', es: 'Ago 2022' },
        en: { name: 'ArcGIS Enterprise: Configuring a Base Deployment', issuer: 'Esri Colombia · ID 8902', note: 'Configuration of a base ArcGIS Enterprise deployment including Portal, Server, and Data Store.' },
        es: { name: 'ArcGIS Enterprise: Configuring a Base Deployment', issuer: 'Esri Colombia · ID 8902', note: 'Configuración de un despliegue base de ArcGIS Enterprise incluyendo Portal, Server y Data Store.' }
      },
      {
        icon: '🗄️',
        year: { en: 'Aug 2022', es: 'Ago 2022' },
        en: { name: 'Deploying and Maintaining a Multiuser Geodatabase', issuer: 'Esri Colombia · ID 8736', note: 'Deployment, configuration and maintenance of enterprise geodatabases in multiuser environments.' },
        es: { name: 'Deploying and Maintaining a Multiuser Geodatabase', issuer: 'Esri Colombia · ID 8736', note: 'Despliegue, configuración y mantenimiento de geodatabases empresariales en entornos multiusuario.' }
      },
      {
        icon: '📋',
        year: { en: 'Sep 2022', es: 'Sep 2022' },
        en: { name: 'Implementing Versioned Workflows in a Multiuser Geodatabase', issuer: 'Esri Colombia · ID 8752', note: 'Implementation of versioned editing workflows for collaborative GIS data management.' },
        es: { name: 'Implementing Versioned Workflows in a Multiuser Geodatabase', issuer: 'Esri Colombia · ID 8752', note: 'Implementación de flujos de edición versionada para gestión colaborativa de datos SIG.' }
      },
      {
        icon: '🔄',
        year: { en: 'Sep 2022', es: 'Sep 2022' },
        en: { name: 'Distributing Data Using Geodatabase Replication', issuer: 'Esri Colombia · ID 8750', note: 'Strategies and implementation of geodatabase replication for distributed data management.' },
        es: { name: 'Distributing Data Using Geodatabase Replication', issuer: 'Esri Colombia · ID 8750', note: 'Estrategias e implementación de replicación de geodatabases para gestión distribuida de datos.' }
      },
      {
        icon: '📡',
        year: { en: 'Oct 2023', es: 'Oct 2023' },
        en: { name: 'Spatial Data Science: The New Frontier in Analytics', issuer: 'Esri · Signed by Jack Dangermond', note: 'MOOC on advanced spatial statistics, machine learning, and data-driven decision-making using the ArcGIS platform.' },
        es: { name: 'Spatial Data Science: The New Frontier in Analytics', issuer: 'Esri · Firmado por Jack Dangermond', note: 'MOOC sobre estadística espacial avanzada, machine learning y toma de decisiones basada en datos con la plataforma ArcGIS.' }
      },
      {
        icon: '🛰️',
        year: { en: 'Oct 2023', es: 'Oct 2023' },
        en: { name: 'Imagery in Action', issuer: 'Esri · Signed by Jack Dangermond', note: 'MOOC on satellite imagery analysis, remote sensing workflows, and image processing with ArcGIS.' },
        es: { name: 'Imagery in Action', issuer: 'Esri · Firmado por Jack Dangermond', note: 'MOOC sobre análisis de imágenes satelitales, flujos de teledetección y procesamiento de imágenes con ArcGIS.' }
      },
      {
        icon: '📊',
        year: { en: 'Sep 2022', es: 'Sep 2022' },
        en: { name: 'ArcGIS Dashboards: Create Powerful Dashboards', issuer: 'Esri Colombia · ID 8941', note: 'Design and implementation of powerful operational dashboards with ArcGIS for real-time data visualization.' },
        es: { name: 'ArcGIS Dashboard: Cree Potentes Tableros de Control', issuer: 'Esri Colombia · ID 8941', note: 'Diseño e implementación de tableros operacionales con ArcGIS para visualización de datos en tiempo real.' }
      },
      {
        icon: '📂',
        year: { en: 'Aug 2022', es: 'Ago 2022' },
        en: { name: 'Managing Geospatial Data in ArcGIS', issuer: 'Esri Colombia · ID 8739', note: 'Management, organization and quality control of geospatial data within the ArcGIS platform.' },
        es: { name: 'Managing Geospatial Data in ArcGIS', issuer: 'Esri Colombia · ID 8739', note: 'Gestión, organización y control de calidad de datos geoespaciales dentro de la plataforma ArcGIS.' }
      },
      {
        icon: '🔀',
        year: { en: 'Sep 2022', es: 'Sep 2022' },
        en: { name: 'Configuring Branch Versioning in ArcGIS', issuer: 'Esri Colombia · ID 8751', note: 'Configuration and management of branch versioning for collaborative and enterprise GIS data workflows.' },
        es: { name: 'Configuración del Control de Versiones Branch en ArcGIS', issuer: 'Esri Colombia · ID 8751', note: 'Configuración y gestión del versionamiento Branch para flujos de trabajo colaborativos y empresariales en SIG.' }
      },
      {
        icon: '🗺️',
        year: { en: 'May 2017', es: 'May 2017' },
        en: { name: 'Using ArcMap in ArcGIS Desktop 10', issuer: 'Esri', note: 'Foundational ArcGIS Desktop certification covering cartographic production and spatial analysis.' },
        es: { name: 'Using ArcMap in ArcGIS Desktop 10', issuer: 'Esri', note: 'Certificación fundacional de ArcGIS Desktop cubriendo producción cartográfica y análisis espacial.' }
      }
    ]
  },
  {
    en: { group: 'AI & Emerging Technologies' },
    es: { group: 'IA y Tecnologías Emergentes' },
    items: [
      {
        icon: '✨',
        year: { en: 'Jun 2025', es: 'Jun 2025' },
        en: { name: 'Generative AI Diploma', issuer: 'Eidos Global + Microsoft', note: 'Foundations and practical applications of generative artificial intelligence in professional environments.' },
        es: { name: 'Diplomado en Inteligencia Artificial Generativa', issuer: 'Eidos Global + Microsoft', note: 'Fundamentos y aplicaciones prácticas de la inteligencia artificial generativa en entornos profesionales.' }
      },
      {
        icon: '📊',
        year: { en: 'Feb 2026', es: 'Feb 2026' },
        en: { name: 'Advanced Geospatial Data Analytics in Python', issuer: 'LinkedIn Learning', note: 'Advanced spatial data analysis and visualization using Python for GIS workflows.' },
        es: { name: 'Análisis Avanzado de Datos Geoespaciales en Python', issuer: 'LinkedIn Learning', note: 'Análisis avanzado y visualización de datos espaciales con Python para flujos SIG.' }
      },
      {
        icon: '🛰️',
        year: { en: 'Feb 2026', es: 'Feb 2026' },
        en: { name: 'Geospatial Raster Data Analytics in Python', issuer: 'LinkedIn Learning', note: 'Processing and analysing raster satellite data using Python libraries.' },
        es: { name: 'Análisis de Datos Raster Geoespaciales en Python', issuer: 'LinkedIn Learning', note: 'Procesamiento y análisis de datos raster satelitales con librerías Python.' }
      },
      {
        icon: '🔢',
        year: { en: 'Dec 2025', es: 'Dic 2025' },
        en: { name: 'Introduction to Data Science', issuer: 'Cisco', note: 'Foundational data science concepts, data analysis, and machine learning fundamentals.' },
        es: { name: 'Introducción a la Ciencia de Datos', issuer: 'Cisco', note: 'Conceptos fundamentales de ciencia de datos, análisis de datos y fundamentos de machine learning.' }
      },
      {
        icon: '🐍',
        year: { en: 'Sep 2022', es: 'Sep 2022' },
        en: { name: 'Data Science in Python & ArcGIS Pro', issuer: 'Esri Colombia', note: 'Applied data science workflows using Python integrated with ArcGIS Pro for geospatial analysis.' },
        es: { name: 'Ciencia de Datos en Python y ArcGIS Pro', issuer: 'Esri Colombia', note: 'Flujos de trabajo de ciencia de datos con Python integrado a ArcGIS Pro para análisis geoespacial.' }
      }
    ]
  },
  {
    en: { group: 'Environmental GIS & Risk Management' },
    es: { group: 'SIG Ambiental y Gestión de Riesgos' },
    items: [
      {
        icon: '🌊',
        year: { en: 'Apr 2018', es: 'Abr 2018' },
        en: { name: 'Remote Sensing & GIS for Flood Risk Management', issuer: 'Universidad de Antioquia — Faculty of Engineering', note: '32-hour course on satellite remote sensing and GIS applied to flood risk analysis and disaster management. Issued by the Dean of Engineering.' },
        es: { name: 'Sensores Remotos y SIG para Manejo y Gestión de Riesgos en Inundaciones', issuer: 'Universidad de Antioquia — Facultad de Ingeniería', note: 'Curso de 32 horas sobre teledetección satelital y SIG aplicados al análisis de riesgo de inundaciones y gestión de desastres. Emitido por el Decano de Ingeniería.' }
      },
      {
        icon: '🗃️',
        year: { en: 'Dec 2022', es: 'Dic 2022' },
        en: { name: 'Geodatabase (GDB) — ANLA Standards', issuer: 'FG Training Colombia SAS', note: '40-hour course on the geodatabase model required by the Autoridad Nacional de Licencias Ambientales (ANLA) for environmental licensing projects in Colombia.' },
        es: { name: 'Geodatabase (GDB) de la Autoridad Nacional de Licencias Ambientales (ANLA)', issuer: 'FG Training Colombia SAS', note: 'Curso de 40 horas sobre el modelo de geodatabase exigido por la ANLA para proyectos de licenciamiento ambiental en Colombia.' }
      }
    ]
  },
  {
    en: { group: 'Leadership, Teaching & Soft Skills' },
    es: { group: 'Liderazgo, Docencia y Habilidades Blandas' },
    items: [
      {
        icon: '📚',
        year: { en: 'In progress · 2025', es: 'En curso · 2025' },
        en: { name: 'Diploma in University Teaching', issuer: 'In progress', note: 'Certified to design organizational learning plans and structured training programs for technical and non-technical audiences.' },
        es: { name: 'Diplomado en Docencia Universitaria', issuer: 'En curso', note: 'Habilitado para diseñar planes de aprendizaje organizacionales y programas de capacitación para audiencias técnicas y no técnicas.' }
      },
      {
        icon: '👥',
        year: { en: 'Mar 2026', es: 'Mar 2026' },
        en: { name: 'Leadership & Team Management', issuer: 'Universidad Internacional de La Rioja (UNIR)', note: 'Team management, effective communication, decision-making, and leadership in technical and organizational environments. Credential ID: 77202603011143.' },
        es: { name: 'Curso de Liderazgo y Gestión de Equipos', issuer: 'Universidad Internacional de La Rioja (UNIR)', note: 'Gestión de equipos, comunicación efectiva, toma de decisiones y liderazgo en entornos técnicos y organizacionales. ID: 77202603011143.' }
      },
      {
        icon: '🌐',
        year: { en: 'Nov 2019', es: 'Nov 2019' },
        en: { name: 'Plugin Development with PyQGIS', issuer: 'QGIS Colombia', note: 'Development of custom plugins for QGIS using Python, extending GIS tool functionality.' },
        es: { name: 'Desarrollo de Plugins con PyQGIS', issuer: 'QGIS Colombia', note: 'Desarrollo de plugins personalizados para QGIS con Python, extendiendo la funcionalidad de herramientas SIG.' }
      },
      {
        icon: '💻',
        year: { en: 'Aug 2020', es: 'Ago 2020' },
        en: { name: 'Online Teaching & Virtual Education', issuer: 'LinkedIn Learning', note: 'Best practices in online and virtual instruction for technical audiences.' },
        es: { name: 'Enseñanza Online o Virtual', issuer: 'LinkedIn Learning', note: 'Mejores prácticas de instrucción online y virtual para audiencias técnicas.' }
      },
      {
        icon: '🤝',
        year: { en: 'Aug 2020', es: 'Ago 2020' },
        en: { name: 'Leadership & Teamwork', issuer: 'LinkedIn Learning', note: 'Collaborative leadership strategies and effective teamwork methodologies.' },
        es: { name: 'Liderazgo y Trabajo en Equipo', issuer: 'LinkedIn Learning', note: 'Estrategias de liderazgo colaborativo y metodologías efectivas de trabajo en equipo.' }
      },
      {
        icon: '⏱️',
        year: { en: 'Aug 2020', es: 'Ago 2020' },
        en: { name: 'Fundamentals of Time Management', issuer: 'LinkedIn Learning', note: 'Productivity strategies and time management frameworks for knowledge workers.' },
        es: { name: 'Fundamentos de la Gestión del Tiempo', issuer: 'LinkedIn Learning', note: 'Estrategias de productividad y marcos de gestión del tiempo para trabajadores del conocimiento.' }
      }
    ]
  },
  {
    en: { group: 'Languages & English' },
    es: { group: 'Idiomas e Inglés' },
    items: [
      {
        icon: '🇺🇸',
        year: { en: 'Dec 2025', es: 'Dic 2025' },
        en: { name: 'Academic Knowledge in English as a Foreign Language — B1', issuer: 'Institución Universitaria ESUMER', note: 'Certified English B1 proficiency with focus on academic and professional communication.' },
        es: { name: 'Conocimientos Académicos en Inglés como Lengua Extranjera — Nivel B1', issuer: 'Institución Universitaria ESUMER', note: 'Certificación de inglés nivel B1 con enfoque en comunicación académica y profesional.' }
      },
      {
        icon: '💬',
        year: { en: 'Dec 2025', es: 'Dic 2025' },
        en: { name: 'English for IT 2', issuer: 'Cisco', note: 'Advanced technical English for IT professionals: customer support vocabulary and communication.' },
        es: { name: 'English for IT 2', issuer: 'Cisco', note: 'Inglés técnico avanzado para profesionales TI: vocabulario de soporte al cliente y comunicación.' }
      },
      {
        icon: '💬',
        year: { en: 'Dec 2025', es: 'Dic 2025' },
        en: { name: 'English for IT 1', issuer: 'Cisco', note: 'Technical English foundations for IT professionals covering key vocabulary and user experience terminology.' },
        es: { name: 'English for IT 1', issuer: 'Cisco', note: 'Fundamentos de inglés técnico para profesionales TI con vocabulario clave y terminología de experiencia de usuario.' }
      }
    ]
  }
];

// Flatten for backward compat
const CERTIFICATIONS = CERT_GROUPS.flatMap(g => g.items);

// ── AWARDS ───────────────────────────────────────────────────
const AWARDS = [
  {
    icon: '🌍',
    en: { title: 'USAID Leadership Scholarship — Open Data Mapping', body: 'Awarded by USAID for leadership in open data mapping and community development. Intensive training conducted in South Africa, 2019.' },
    es: { title: 'Beca de Liderazgo USAID — Mapeo con Datos Abiertos', body: 'Otorgada por USAID por liderazgo en mapeo con datos abiertos y desarrollo comunitario. Entrenamiento intensivo realizado en Sudáfrica, 2019.' }
  },
  {
    icon: '🗺️',
    en: { title: 'YouthMappers Leadership Fellow', body: 'YouthMappers · Jan 2019. Recognized for leadership in open data mapping, community development, and geospatial volunteering at an international level.' },
    es: { title: 'YouthMappers Leadership Fellow', body: 'YouthMappers · Ene 2019. Reconocido por liderazgo en mapeo con datos abiertos, desarrollo comunitario y voluntariado geoespacial a nivel internacional.' }
  },
  {
    icon: '🏆',
    en: { title: 'ACRES Foundation Scholarship', body: 'Cámara Colombiana de Infraestructura — full academic merit scholarship recognizing excellence in engineering, 2017–2021.' },
    es: { title: 'Beca Fundación ACRES', body: 'Cámara Colombiana de Infraestructura — beca completa por mérito académico al desempeño sobresaliente en ingeniería, 2017–2021.' }
  },
  {
    icon: '🔬',
    en: { title: 'Lead Member — GeoLab Research Group', body: 'Universidad de Antioquia — leadership in geospatial university research and open innovation, 2017–2021.' },
    es: { title: 'Miembro Líder — Semillero GeoLab', body: 'Universidad de Antioquia — liderazgo en investigación geoespacial universitaria e innovación abierta, 2017–2021.' }
  }
];
