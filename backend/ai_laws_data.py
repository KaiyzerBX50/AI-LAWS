"""
Curated, real-world dataset of AI-related laws, acts, regulations and governance
frameworks from around the world.

Status values: "Enacted", "Proposed", "Draft", "Superseded"
Regions: Europe, North America, South America, Asia, Middle East, Africa, Oceania

`geo_names` are the country names as they appear in the world-atlas (Natural Earth)
countries-110m topojson, used to color the interactive world map. Supra-national
laws (EU) are spread across all member states via EU_MEMBER_GEO_NAMES in server.py.
"""

# ISO-A3 codes and geo names help match the map + comparison views.

AI_LAWS = [
    # ---------------- EUROPEAN UNION ----------------
    {
        "id": "eu-ai-act-2024",
        "country": "European Union",
        "iso_a3": "EUU",
        "geo_names": ["__EU__"],
        "region": "Europe",
        "title": "EU Artificial Intelligence Act (Regulation 2024/1689)",
        "status": "Enacted",
        "category": "Comprehensive",
        "year": 2024,
        "date": "2024-08-01",
        "authority": "European Parliament & Council of the EU",
        "summary": "The world's first comprehensive, horizontal AI law. It follows a risk-based approach, classifying AI systems into unacceptable, high, limited and minimal risk, with obligations scaling accordingly. It entered into force on 1 August 2024 with a phased application through 2027.",
        "key_provisions": [
            "Bans 'unacceptable risk' uses such as social scoring and untargeted facial scraping.",
            "High-risk AI systems must meet requirements for risk management, data governance, transparency and human oversight.",
            "Dedicated rules and transparency duties for general-purpose AI (GPAI) / foundation models.",
            "Fines up to EUR 35 million or 7% of global annual turnover for prohibited-practice breaches.",
        ],
        "sources": [
            {"title": "EUR-Lex: Regulation (EU) 2024/1689", "url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"},
            {"title": "European Commission - AI Act", "url": "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"},
        ],
    },
    {
        "id": "eu-gdpr-2016",
        "country": "European Union",
        "iso_a3": "EUU",
        "geo_names": ["__EU__"],
        "region": "Europe",
        "title": "General Data Protection Regulation (GDPR) - Automated Decisions",
        "status": "Enacted",
        "category": "Data Privacy",
        "year": 2016,
        "date": "2018-05-25",
        "authority": "European Parliament & Council of the EU",
        "summary": "The GDPR governs personal data processing and is foundational to AI systems handling EU personal data. Article 22 grants individuals rights regarding solely automated decision-making, including profiling.",
        "key_provisions": [
            "Right not to be subject to solely automated decisions with legal/significant effects (Art. 22).",
            "Rights to information, access, and meaningful explanation of automated processing logic.",
            "Data minimisation and purpose limitation constrain AI training data use.",
            "Fines up to EUR 20 million or 4% of global annual turnover.",
        ],
        "sources": [
            {"title": "EUR-Lex: Regulation (EU) 2016/679", "url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj"},
        ],
    },

    # ---------------- UNITED STATES ----------------
    {
        "id": "us-eo-14179-2025",
        "country": "United States of America",
        "iso_a3": "USA",
        "geo_names": ["United States of America"],
        "region": "North America",
        "title": "Executive Order 14179 - Removing Barriers to American Leadership in AI",
        "status": "Enacted",
        "category": "Executive Policy",
        "year": 2025,
        "date": "2025-01-23",
        "authority": "The White House",
        "summary": "Signed in January 2025, this executive order revoked prior AI directives and set a policy of sustaining U.S. AI dominance by reducing regulatory barriers. It directs agencies to develop an AI action plan prioritising innovation and national competitiveness.",
        "key_provisions": [
            "Revokes Executive Order 14110 and related guidance seen as barriers to innovation.",
            "Directs development of a national AI Action Plan within 180 days.",
            "Emphasises free-market AI development and reduced compliance burden.",
        ],
        "sources": [
            {"title": "Federal Register - EO 14179", "url": "https://www.federalregister.gov/documents/2025/01/31/2025-02172/removing-barriers-to-american-leadership-in-artificial-intelligence"},
        ],
    },
    {
        "id": "us-eo-14110-2023",
        "country": "United States of America",
        "iso_a3": "USA",
        "geo_names": ["United States of America"],
        "region": "North America",
        "title": "Executive Order 14110 - Safe, Secure, and Trustworthy AI",
        "status": "Superseded",
        "category": "Executive Policy",
        "year": 2023,
        "date": "2023-10-30",
        "authority": "The White House",
        "summary": "The Biden administration's landmark 2023 order directed sweeping federal action on AI safety, security and civil rights. It was revoked in January 2025 by Executive Order 14179.",
        "key_provisions": [
            "Required developers of powerful models to share safety-test results under the Defense Production Act.",
            "Directed NIST to develop AI red-teaming and safety standards.",
            "Addressed privacy, equity, consumer protection and workforce impacts.",
        ],
        "sources": [
            {"title": "Federal Register - EO 14110", "url": "https://www.federalregister.gov/documents/2023/11/01/2023-24283/safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence"},
        ],
    },
    {
        "id": "us-nist-airmf-2023",
        "country": "United States of America",
        "iso_a3": "USA",
        "geo_names": ["United States of America"],
        "region": "North America",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0)",
        "status": "Enacted",
        "category": "Voluntary Framework",
        "year": 2023,
        "date": "2023-01-26",
        "authority": "National Institute of Standards and Technology",
        "summary": "A voluntary framework to help organisations manage AI risks across the lifecycle. Widely referenced by industry and increasingly embedded in procurement and state rules.",
        "key_provisions": [
            "Four core functions: Govern, Map, Measure, Manage.",
            "Defines characteristics of trustworthy AI (valid, safe, secure, accountable, transparent, fair).",
            "Companion Generative AI Profile released in 2024.",
        ],
        "sources": [
            {"title": "NIST AI RMF", "url": "https://www.nist.gov/itl/ai-risk-management-framework"},
        ],
    },
    {
        "id": "us-colorado-ai-act-2024",
        "country": "United States of America",
        "iso_a3": "USA",
        "geo_names": ["United States of America"],
        "region": "North America",
        "title": "Colorado AI Act (SB 24-205)",
        "status": "Enacted",
        "category": "Comprehensive",
        "year": 2024,
        "date": "2024-05-17",
        "authority": "State of Colorado",
        "summary": "The first comprehensive U.S. state AI law targeting algorithmic discrimination by developers and deployers of 'high-risk' AI systems used in consequential decisions. Effective date has been delayed to 2026.",
        "key_provisions": [
            "Duty of reasonable care to protect consumers from algorithmic discrimination.",
            "Impact assessments and disclosures for high-risk AI systems.",
            "Consumer right to notice when AI is used in consequential decisions.",
        ],
        "sources": [
            {"title": "Colorado SB 24-205", "url": "https://leg.colorado.gov/bills/sb24-205"},
        ],
    },
    {
        "id": "us-ca-transparency-2024",
        "country": "United States of America",
        "iso_a3": "USA",
        "geo_names": ["United States of America"],
        "region": "North America",
        "title": "California AI Transparency Act (SB 942) & Training Data Disclosure (AB 2013)",
        "status": "Enacted",
        "category": "Transparency",
        "year": 2024,
        "date": "2024-09-19",
        "authority": "State of California",
        "summary": "A package of California laws requiring transparency around generative AI, including detection tools and provenance disclosures (SB 942) and disclosure of training data documentation (AB 2013).",
        "key_provisions": [
            "Large GenAI providers must offer AI-content detection tools and provenance disclosures.",
            "Developers must publish documentation about datasets used to train GenAI systems.",
            "Applies to systems made available to Californians.",
        ],
        "sources": [
            {"title": "California SB 942", "url": "https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB942"},
        ],
    },

    # ---------------- CHINA ----------------
    {
        "id": "cn-genai-2023",
        "country": "China",
        "iso_a3": "CHN",
        "geo_names": ["China"],
        "region": "Asia",
        "title": "Interim Measures for the Management of Generative AI Services",
        "status": "Enacted",
        "category": "Generative AI",
        "year": 2023,
        "date": "2023-08-15",
        "authority": "Cyberspace Administration of China (CAC) + 6 agencies",
        "summary": "China's core regulation for public-facing generative AI services. Providers must ensure content aligns with core socialist values, complete security assessments, and label AI-generated content.",
        "key_provisions": [
            "Content must uphold 'core socialist values'; illegal content prohibited.",
            "Security assessment and algorithm filing with the CAC required.",
            "Labelling of AI-generated content and protection of personal data.",
        ],
        "sources": [
            {"title": "CAC Interim Measures (official)", "url": "http://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm"},
        ],
    },
    {
        "id": "cn-deep-synthesis-2022",
        "country": "China",
        "iso_a3": "CHN",
        "geo_names": ["China"],
        "region": "Asia",
        "title": "Provisions on Deep Synthesis Internet Information Services",
        "status": "Enacted",
        "category": "Deepfakes",
        "year": 2022,
        "date": "2023-01-10",
        "authority": "Cyberspace Administration of China (CAC)",
        "summary": "Rules governing 'deep synthesis' technologies (deepfakes), requiring conspicuous labelling of synthetically generated or altered content and consent for use of personal likeness.",
        "key_provisions": [
            "Mandatory labelling of deep-synthesis (deepfake) content.",
            "Consent required before editing biometric information such as faces/voices.",
            "Real-identity verification of users.",
        ],
        "sources": [
            {"title": "CAC Deep Synthesis Provisions", "url": "http://www.cac.gov.cn/2022-12/11/c_1672221949318230.htm"},
        ],
    },
    {
        "id": "cn-algo-recommendation-2022",
        "country": "China",
        "iso_a3": "CHN",
        "geo_names": ["China"],
        "region": "Asia",
        "title": "Provisions on the Management of Algorithmic Recommendations",
        "status": "Enacted",
        "category": "Algorithms",
        "year": 2022,
        "date": "2022-03-01",
        "authority": "Cyberspace Administration of China (CAC)",
        "summary": "One of the world's first binding rules on recommendation algorithms, requiring transparency, user opt-outs and protections against price discrimination and addictive design.",
        "key_provisions": [
            "Users can turn off algorithmic recommendation services.",
            "Prohibits unfair price discrimination based on user profiling.",
            "Algorithm filing requirement for services with public-opinion influence.",
        ],
        "sources": [
            {"title": "CAC Algorithm Provisions", "url": "http://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm"},
        ],
    },

    # ---------------- UNITED KINGDOM ----------------
    {
        "id": "uk-ai-whitepaper-2023",
        "country": "United Kingdom",
        "iso_a3": "GBR",
        "geo_names": ["United Kingdom"],
        "region": "Europe",
        "title": "A pro-innovation approach to AI regulation (White Paper)",
        "status": "Proposed",
        "category": "Framework",
        "year": 2023,
        "date": "2023-03-29",
        "authority": "UK Government (DSIT)",
        "summary": "The UK's principles-based, sector-led approach that empowers existing regulators rather than creating a single AI law. The UK also established the AI Safety Institute (2023) to evaluate frontier models.",
        "key_provisions": [
            "Five cross-sector principles: safety, transparency, fairness, accountability, contestability.",
            "Relies on existing regulators (ICO, CMA, FCA) rather than a new AI regulator.",
            "AI Safety Institute conducts frontier-model evaluations.",
        ],
        "sources": [
            {"title": "UK AI Regulation White Paper", "url": "https://www.gov.uk/government/publications/ai-regulation-a-pro-innovation-approach"},
        ],
    },

    # ---------------- CANADA ----------------
    {
        "id": "ca-aida-2022",
        "country": "Canada",
        "iso_a3": "CAN",
        "geo_names": ["Canada"],
        "region": "North America",
        "title": "Artificial Intelligence and Data Act (AIDA) - Bill C-27",
        "status": "Draft",
        "category": "Comprehensive",
        "year": 2022,
        "date": "2022-06-16",
        "authority": "Parliament of Canada",
        "summary": "Proposed federal AI law within Bill C-27 to regulate 'high-impact' AI systems. The bill did not pass before Parliament was prorogued in early 2025 and lapsed, leaving Canada without a dedicated AI statute.",
        "key_provisions": [
            "Obligations for 'high-impact' AI systems including risk assessment and mitigation.",
            "Would create an AI and Data Commissioner for enforcement.",
            "Transparency and record-keeping requirements for regulated systems.",
        ],
        "sources": [
            {"title": "Bill C-27 (Parliament of Canada)", "url": "https://www.parl.ca/legisinfo/en/bill/44-1/c-27"},
        ],
    },

    # ---------------- BRAZIL ----------------
    {
        "id": "br-pl2338-2023",
        "country": "Brazil",
        "iso_a3": "BRA",
        "geo_names": ["Brazil"],
        "region": "South America",
        "title": "Brazil AI Bill (PL 2338/2023)",
        "status": "Proposed",
        "category": "Comprehensive",
        "year": 2023,
        "date": "2024-12-10",
        "authority": "National Congress of Brazil",
        "summary": "A comprehensive, rights- and risk-based AI framework. The Federal Senate approved the bill in December 2024; it advanced to the Chamber of Deputies for further consideration.",
        "key_provisions": [
            "Risk-based classification with banned 'excessive risk' uses.",
            "Rights for people affected by AI decisions, including explanation and contestation.",
            "Governance and oversight by a coordinating authority.",
        ],
        "sources": [
            {"title": "Senado Federal - PL 2338/2023", "url": "https://www25.senado.leg.br/web/atividade/materias/-/materia/157233"},
        ],
    },

    # ---------------- SOUTH KOREA ----------------
    {
        "id": "kr-ai-basic-act-2024",
        "country": "South Korea",
        "iso_a3": "KOR",
        "geo_names": ["South Korea"],
        "region": "Asia",
        "title": "AI Basic Act (Framework Act on AI Development and Trust)",
        "status": "Enacted",
        "category": "Comprehensive",
        "year": 2024,
        "date": "2025-01-21",
        "authority": "National Assembly of the Republic of Korea",
        "summary": "Asia's first comprehensive AI framework law, promulgated in early 2025 and set to take effect in January 2026. It balances promotion of the AI industry with trust and safety obligations for high-impact AI.",
        "key_provisions": [
            "Obligations for 'high-impact' and generative AI, including risk management and labelling.",
            "Transparency notice when users interact with AI systems.",
            "Government support for AI R&D, data and infrastructure.",
        ],
        "sources": [
            {"title": "Korea AI Basic Act coverage", "url": "https://www.koreaherald.com/view.php?ud=20241226050514"},
        ],
    },

    # ---------------- JAPAN ----------------
    {
        "id": "jp-ai-promotion-2025",
        "country": "Japan",
        "iso_a3": "JPN",
        "geo_names": ["Japan"],
        "region": "Asia",
        "title": "Act on Promotion of Research, Development and Utilisation of AI",
        "status": "Enacted",
        "category": "Innovation / Soft-law",
        "year": 2025,
        "date": "2025-05-28",
        "authority": "National Diet of Japan",
        "summary": "Japan's first AI-specific law, enacted in 2025. It takes a light-touch, innovation-first approach, establishing a national AI strategy headquarters and cooperation duties rather than hard penalties.",
        "key_provisions": [
            "Establishes an AI Strategy Headquarters led by the Prime Minister.",
            "Promotes R&D and adoption while relying on guidance over penalties.",
            "Government may investigate and publicise serious AI-related harms.",
        ],
        "sources": [
            {"title": "Japan AI Promotion Act coverage", "url": "https://www.japantimes.co.jp/news/2025/05/28/japan/politics/ai-bill-passed/"},
        ],
    },
    {
        "id": "jp-social-principles-2019",
        "country": "Japan",
        "iso_a3": "JPN",
        "geo_names": ["Japan"],
        "region": "Asia",
        "title": "Social Principles of Human-Centric AI",
        "status": "Enacted",
        "category": "Voluntary Framework",
        "year": 2019,
        "date": "2019-03-29",
        "authority": "Cabinet Office of Japan",
        "summary": "A foundational set of human-centric AI principles guiding Japan's AI governance and later 'AI Guidelines for Business' (2024).",
        "key_provisions": [
            "Human-centric, education, privacy, security, fair competition, accountability principles.",
            "Basis for the 2024 AI Guidelines for Business.",
        ],
        "sources": [
            {"title": "Social Principles of Human-Centric AI", "url": "https://www.cas.go.jp/jp/seisaku/jinkouchinou/pdf/humancentricai.pdf"},
        ],
    },

    # ---------------- INDIA ----------------
    {
        "id": "in-dpdp-2023",
        "country": "India",
        "iso_a3": "IND",
        "geo_names": ["India"],
        "region": "Asia",
        "title": "Digital Personal Data Protection Act, 2023",
        "status": "Enacted",
        "category": "Data Privacy",
        "year": 2023,
        "date": "2023-08-11",
        "authority": "Parliament of India",
        "summary": "India's first comprehensive data-protection law, foundational for AI systems processing personal data. India currently regulates AI through this and sectoral advisories rather than a dedicated AI act.",
        "key_provisions": [
            "Consent-based processing of digital personal data with defined data-principal rights.",
            "Obligations on data fiduciaries including security safeguards and breach notice.",
            "Establishes a Data Protection Board of India.",
        ],
        "sources": [
            {"title": "DPDP Act 2023 (MeitY)", "url": "https://www.meity.gov.in/data-protection-framework"},
        ],
    },
    {
        "id": "in-ai-advisory-2024",
        "country": "India",
        "iso_a3": "IND",
        "geo_names": ["India"],
        "region": "Asia",
        "title": "MeitY Advisory on AI / Generative AI Intermediaries",
        "status": "Proposed",
        "category": "Advisory",
        "year": 2024,
        "date": "2024-03-15",
        "authority": "Ministry of Electronics and IT (MeitY)",
        "summary": "Government advisories urging platforms to label AI-generated content and prevent unlawful or biased outputs, signalling India's evolving, guidance-led approach ahead of any dedicated AI law.",
        "key_provisions": [
            "Labelling of synthetically generated content and deepfakes.",
            "Due-diligence expectations for AI intermediaries under IT Rules.",
            "Measures to curb bias and unlawful content.",
        ],
        "sources": [
            {"title": "MeitY advisory coverage", "url": "https://www.meity.gov.in/"},
        ],
    },

    # ---------------- AUSTRALIA ----------------
    {
        "id": "au-safety-standard-2024",
        "country": "Australia",
        "iso_a3": "AUS",
        "geo_names": ["Australia"],
        "region": "Oceania",
        "title": "Voluntary AI Safety Standard & Proposed Mandatory Guardrails",
        "status": "Proposed",
        "category": "Framework",
        "year": 2024,
        "date": "2024-09-05",
        "authority": "Australian Government (DISR)",
        "summary": "Australia published a Voluntary AI Safety Standard (10 guardrails) in 2024 and consulted on mandatory guardrails for high-risk AI, moving toward a risk-based regulatory model.",
        "key_provisions": [
            "Ten voluntary guardrails covering accountability, testing, transparency and human oversight.",
            "Proposed mandatory guardrails for 'high-risk' AI settings.",
            "Emphasis on human oversight and record-keeping.",
        ],
        "sources": [
            {"title": "Australia Voluntary AI Safety Standard", "url": "https://www.industry.gov.au/publications/voluntary-ai-safety-standard"},
        ],
    },

    # ---------------- SINGAPORE ----------------
    {
        "id": "sg-model-framework-2024",
        "country": "Singapore",
        "iso_a3": "SGP",
        "geo_names": ["Singapore"],
        "region": "Asia",
        "title": "Model AI Governance Framework (incl. Generative AI)",
        "status": "Enacted",
        "category": "Voluntary Framework",
        "year": 2024,
        "date": "2024-05-30",
        "authority": "IMDA / PDPC Singapore",
        "summary": "Singapore's influential voluntary governance framework, updated in 2024 with a dedicated Model AI Governance Framework for Generative AI. Supported by the AI Verify testing toolkit.",
        "key_provisions": [
            "Nine dimensions including accountability, data, testing, incident reporting and content provenance.",
            "AI Verify: an open-source testing framework and toolkit.",
            "Practical, industry-friendly guidance rather than binding law.",
        ],
        "sources": [
            {"title": "Singapore Model AI Governance Framework for GenAI", "url": "https://aiverifyfoundation.sg/downloads/Model_AI_Governance_Framework_for_Generative_AI_May_2024.pdf"},
        ],
    },

    # ---------------- UAE ----------------
    {
        "id": "ae-ai-strategy-2031",
        "country": "United Arab Emirates",
        "iso_a3": "ARE",
        "geo_names": ["United Arab Emirates"],
        "region": "Middle East",
        "title": "UAE National Strategy for AI 2031",
        "status": "Enacted",
        "category": "National Strategy",
        "year": 2018,
        "date": "2018-10-17",
        "authority": "UAE Government",
        "summary": "The UAE was the first country to appoint a Minister of State for AI (2017) and adopted a national AI strategy to embed AI across government and the economy by 2031, complemented by AI ethics guidelines.",
        "key_provisions": [
            "Whole-of-government AI adoption targets across sectors.",
            "AI ethics principles and guidelines issued by regulators.",
            "Focus on talent, infrastructure and public-sector AI deployment.",
        ],
        "sources": [
            {"title": "UAE National AI Strategy 2031", "url": "https://ai.gov.ae/strategy/"},
        ],
    },

    # ---------------- SAUDI ARABIA ----------------
    {
        "id": "sa-ai-ethics-2023",
        "country": "Saudi Arabia",
        "iso_a3": "SAU",
        "geo_names": ["Saudi Arabia"],
        "region": "Middle East",
        "title": "AI Ethics Principles (SDAIA)",
        "status": "Enacted",
        "category": "Voluntary Framework",
        "year": 2023,
        "date": "2023-09-01",
        "authority": "Saudi Data & AI Authority (SDAIA)",
        "summary": "Saudi Arabia's national AI ethics principles, issued by SDAIA, provide risk-based guidance for the responsible development and use of AI, aligned with the National Strategy for Data & AI.",
        "key_provisions": [
            "Principles: fairness, privacy, humanity, reliability, transparency and accountability.",
            "Risk-based assessment approach for AI systems.",
            "Guidance tied to the National Strategy for Data & AI.",
        ],
        "sources": [
            {"title": "SDAIA AI Ethics Principles", "url": "https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf"},
        ],
    },

    # ---------------- ISRAEL ----------------
    {
        "id": "il-ai-policy-2023",
        "country": "Israel",
        "iso_a3": "ISR",
        "geo_names": ["Israel"],
        "region": "Middle East",
        "title": "Policy on AI Regulation and Ethics",
        "status": "Proposed",
        "category": "Framework",
        "year": 2023,
        "date": "2023-12-17",
        "authority": "Israel Ministry of Innovation, Science and Technology",
        "summary": "Israel's soft, sector-based and principles-led approach to AI, favouring existing regulators and voluntary standards over comprehensive legislation to preserve innovation.",
        "key_provisions": [
            "Responsible-innovation principles aligned with OECD.",
            "Sector-specific regulation via existing bodies.",
            "Risk-based and non-binding guidance.",
        ],
        "sources": [
            {"title": "Israel AI Policy", "url": "https://www.gov.il/en/departments/news/most-news20231218"},
        ],
    },

    # ---------------- FRANCE (national addition beyond EU) ----------------
    {
        "id": "fr-cnil-ai-2023",
        "country": "France",
        "iso_a3": "FRA",
        "geo_names": ["France"],
        "region": "Europe",
        "title": "CNIL AI Action Plan & Guidance",
        "status": "Enacted",
        "category": "Data Privacy / Guidance",
        "year": 2023,
        "date": "2023-05-16",
        "authority": "Commission Nationale de l'Informatique et des Libertés (CNIL)",
        "summary": "France's data protection authority launched an AI action plan and issued practical guidance on developing AI systems in compliance with the GDPR, complementing the EU AI Act.",
        "key_provisions": [
            "Guidance on lawful basis and datasets for AI training.",
            "Support and audits for AI systems processing personal data.",
            "How-to sheets for GDPR-compliant AI development.",
        ],
        "sources": [
            {"title": "CNIL AI Action Plan", "url": "https://www.cnil.fr/en/artificial-intelligence-action-plan-cnil"},
        ],
    },

    # ---------------- CHILE ----------------
    {
        "id": "cl-ai-bill-2024",
        "country": "Chile",
        "iso_a3": "CHL",
        "geo_names": ["Chile"],
        "region": "South America",
        "title": "AI Systems Regulation Bill",
        "status": "Proposed",
        "category": "Comprehensive",
        "year": 2024,
        "date": "2024-05-07",
        "authority": "National Congress of Chile",
        "summary": "Chile introduced a risk-based AI bill inspired by the EU model, alongside an updated National AI Policy, positioning it among Latin America's AI-regulation frontrunners.",
        "key_provisions": [
            "Risk-based classification of AI systems (unacceptable, high, limited, no risk).",
            "Obligations for high-risk systems and oversight authority.",
            "Aligned with an updated National AI Policy.",
        ],
        "sources": [
            {"title": "Chile AI bill coverage", "url": "https://www.camara.cl/legislacion/ProyectosDeLey/proyectos_ley.aspx"},
        ],
    },

    # ---------------- COUNCIL OF EUROPE (treaty) ----------------
    {
        "id": "coe-ai-convention-2024",
        "country": "Council of Europe",
        "iso_a3": "COE",
        "geo_names": ["__COE__"],
        "region": "Europe",
        "title": "Framework Convention on AI, Human Rights, Democracy & the Rule of Law",
        "status": "Enacted",
        "category": "International Treaty",
        "year": 2024,
        "date": "2024-09-05",
        "authority": "Council of Europe",
        "summary": "The first legally binding international treaty on AI, opened for signature in September 2024. Signatories including the EU, UK, US and others commit to ensuring AI respects human rights, democracy and the rule of law.",
        "key_provisions": [
            "Binding principles: human dignity, transparency, accountability, equality and privacy.",
            "Applies across the AI lifecycle in public (and, per each party, private) sectors.",
            "Remedies and procedural safeguards for affected persons.",
        ],
        "sources": [
            {"title": "Council of Europe AI Treaty", "url": "https://www.coe.int/en/web/artificial-intelligence/the-framework-convention-on-artificial-intelligence"},
        ],
    },
]


# EU-27 member state geo names (Natural Earth / world-atlas naming) used to color the
# map for supra-national EU laws.
EU_MEMBER_GEO_NAMES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden",
]

# Council of Europe treaty coloring: apply to a broad set of European signatories
# plus notable non-European signatories.
COE_SIGNATORY_GEO_NAMES = EU_MEMBER_GEO_NAMES + [
    "United Kingdom", "Norway", "Iceland", "Switzerland", "Ukraine",
    "Moldova", "Serbia", "Albania", "Georgia", "United States of America",
]
