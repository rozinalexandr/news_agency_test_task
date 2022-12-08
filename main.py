from article_scraper import ArticleScraper

companies_list = ["Ginkgo Bioworks", "GlaxoSmithKline", "Canopy Growth", "Evolv Technology", "Aziyo Biologics",
                  "Bausch Health", "Evofem Biosciences", "Essity", "DermTech", "Cutera", "Arcadia Biosciences",
                  "Avita Medical", "Dare Bioscience", "Cerus", "Dermira", "Avicanna", "Collegium Pharmaceutical",
                  "Appili Therapeutics", "Charlotte's Web", "Aytu BioScience", "CNA Insurance Company", "Amryt Pharma",
                  "DSM", "BBI Life Sciences", "Arecor", "Dixie Brands", "Achieve Life Science",
                  "Acerus Pharmaceuticals", "Eton Pharmaceuticals", "Bloomage BioTechnology", "Botanix Pharmaceuticals",
                  "Dermata Therapeutics", "Apricus Biosciences", "Ergomed", "Excel Crop Care", "Bone Biologics",
                  "Encision", "AgraFlora", "Endymed", "Elite Pharmaceuticals", "Beauty&Health",
                  "Elanix Biotechnologies", "Beiersdorf", "Biorem Inc.", "Blueberries Medical Co.", "ASIT biotech",
                  "Forte Biosciences", "Baiyu", "+3S", "Crystal Beads Tibetan Medicine Group", "Allium Medical",
                  "Charioteer", "EXMceuticals", "Eagle Pharmaceuticals", "Clinuvel Pharmaceuticals", "Arjo",
                  "Decipher Labs", "Coloplast Denmark", "Alliance Pharmaceuticals", "Clearwater Paper",
                  "Easton Pharmaceuticals", "Biokangtai", "CARiNG Pharmacy", "Arctic Bioscience",
                  "Beijing Tiantan Biological Products", "AMDL", "Albaad", "Empowered Products Inc", "Anpario plc",
                  "Animalcare Group Plc", "Agape Atp Corp", "Enseval", "China Medical System Holdings Limited",
                  "AXIM Biotechnologies", "BioSyent", "Dashenlin", "Bespoke Extracts", "Arterra Bioscience",
                  "Glow LifeTech", "Cronos Australia", "GTG Wellness", "Cian Healthcare", "Getein Biotech",
                  "Brawn Biotech", "Apex Biotechnology", "C-Rad", "Beijing Bohui Innovation Biotechnology",
                  "China YCT International Group", "China Medicine Corporation", "Desh Rakshak Aushdhalaya Ltd",
                  "CanaQuest", "Engro Polymer & Chemicals", "Balaxi Ventures Lt", "Farmaceutica Remedia",
                  "Auro Laboratories", "CR Phrama Comm", "Baotou Dongbao Bio-Tech",
                  "Anhui Sunhere Pharmaceutical Excipients", "Dhruv Wellness", "Biosino Bio-Technology & Science"]


scraper = ArticleScraper(companies_list)
scraper.get_all_links()
