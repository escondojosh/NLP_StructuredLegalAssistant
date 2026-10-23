# ground_truth.py
# Each entry has:
#   "query"    — the Taglish test question
#   "relevant" — list of TXT filenames that contain the correct answer

GROUND_TRUTH = [

    # ── ORDINANCE NO. 8092 — Traffic Management Code ─────────────────────────

    # Sec. 93 — Truck ban hours (6am-9am, 4pm-9pm)
    {"query": "Anong oras bawal ang malalaking truck sa city streets ng Manila?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # Sec. 54 — Overnight parking hours (10pm to 5am)
    {"query": "Hanggang anong oras lang pwedeng mag-overnight parking sa kalsada?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # Sec. 4 — Emergency vehicle exemptions
    {"query": "Pwede bang lumabag sa traffic signal ang ambulance o fire truck?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # Sec. 136 — Color coding / number coding scheme
    {"query": "Araw-araw ba ang number coding sa Manila o may exemption sa weekend?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # Sec. 46 — Parking in front of residential/commercial establishment
    {"query": "May bayad ba kung mag-park sa harap ng sarili mong bahay o negosyo sa Manila?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # Sec. 115 — Safety helmets for motorcyclists
    {"query": "Kailangan bang magsuot ng helmet ang motorcyclist sa Manila?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # Sec. 97(e) — No driving in slippers or sleeveless
    {"query": "Pwede bang magmaneho ng sasakyan habang naka-tsinelas?",
     "relevant": ["ORDINANCE-NO-8092.txt"]},

    # ── ORDINANCE NO. 8327 — Traffic Code Amendment ───────────────────────────

    # Fine for driving over yellow box
    {"query": "Magkano ang multa pag nasakay ka sa yellow box intersection?",
     "relevant": ["ORDINANCE-NO-8327.txt"]},

    # Jaywalking fines
    {"query": "Ano ang penalty ng jaywalking sa Manila?",
     "relevant": ["ORDINANCE-NO-8327.txt"]},

    # Smoke belching fines
    {"query": "Magkano ang multa ng sasakyan na smoke belching sa Manila?",
     "relevant": ["ORDINANCE-NO-8327.txt"]},

    # ── ORDINANCE NO. 8331 — Omnibus Revenue Code ────────────────────────────

    # Sec. 13 — Real property tax exemptions (churches, gov property, cooperatives)
    {"query": "Sino ang hindi kailangang magbayad ng real property tax sa Manila?",
     "relevant": ["ORDINANCE-NO-8331.txt"]},

    # Sec. 7 — Basic real property tax rates (residential 1.5%, commercial 2%)
    {"query": "Magkano ang real property tax rate para sa residential at commercial na lote sa Manila?",
     "relevant": ["ORDINANCE-NO-8331.txt"]},

    # Sec. 16 — Tax discount for advance/prompt payment (20% if paid before Jan 31)
    {"query": "May diskwento ba kung magbayad ng real property tax bago mag-January 31?",
     "relevant": ["ORDINANCE-NO-8331.txt"]},

    # Sec. 15 — Real property tax payment in installments (4 equal installments)
    {"query": "Pwede bang hulugin sa apat na installment ang real property tax sa Manila?",
     "relevant": ["ORDINANCE-NO-8331.txt"]},

    # Sec. 101 — Business tax for manufacturers based on gross sales
    {"query": "Paano kinukuwenta ang business tax ng manufacturer o assembler sa Manila?",
     "relevant": ["ORDINANCE-NO-8331.txt"]},

    # ── ORDINANCE NO. 8355 — Anti-Dengue Ordinance ───────────────────────────

    # Sec. 11 — Prohibited breeding sites (uncovered containers, old tires, clogged gutters)
    {"query": "Anong mga bagay sa bahay ang bawal dahil breeding site ng lamok?",
     "relevant": ["ORDINANCE-NO-8355.txt"]},

    # Sec. 12 — Penalties: 1st offense warning, 2nd P2000, 3rd P4000 or 6 months
    {"query": "Magkano ang multa ng pangalawang pagkakataon na may mosquito breeding site sa property mo?",
     "relevant": ["ORDINANCE-NO-8355.txt"]},

    # Sec. 8 — Barangay Watch Team responsibilities (source reduction, clean-up campaigns)
    {"query": "Ano ang tungkulin ng Barangay Watch Team sa paglaban sa dengue?",
     "relevant": ["ORDINANCE-NO-8355.txt"]},

    # Sec. 10 — Community responsibility (seek medical treatment if fever >2 days)
    {"query": "Kailan dapat dalhin sa ospital ang pasyente na may lagnat para sa dengue?",
     "relevant": ["ORDINANCE-NO-8355.txt"]},

    # Sec. 9 — School Dengue Task Force (principal as chairman, grade 4-5 pupils as members)
    {"query": "Sino ang dapat mag-lead ng dengue task force sa paaralan?",
     "relevant": ["ORDINANCE-NO-8355.txt"]},

    # ── ORDINANCE NO. 8371 — Environmental Code ──────────────────────────────

    # Art. V Sec. 9 — Incineration or open burning of solid waste is prohibited
    {"query": "Bawal ba ang magsunog ng basura sa bakuran o labas ng bahay sa Manila?",
     "relevant": ["ORDINANCE-NO-8371.txt"]},

    # Art. II Sec. 5 — Noise pollution penalties (1st: P300, 2nd: P400, 3rd: P600)
    {"query": "Magkano ang multa kung ang kalapit-bahay ay nagreklamo sa ingay ng iyong negosyo?",
     "relevant": ["ORDINANCE-NO-8371.txt"]},

    # Art. II Sec. 4 — Dry sandblasting is strictly prohibited (Clean Air Act)
    {"query": "Bawal ba ang dry sandblasting sa mga shipyard o shop sa Manila?",
     "relevant": ["ORDINANCE-NO-8371.txt"]},

    # Art. V Sec. 5 — Solid waste segregation required (biodegradable vs non-biodegradable)
    {"query": "Paano dapat i-separate ang basura ng mga residente sa Manila?",
     "relevant": ["ORDINANCE-NO-8371.txt"]},

    # ── ORDINANCE NO. 9107 — 4Ps Cash Card Protection ────────────────────────

    # Sec. 7 — Penalty for lenders: 1st offense P2000 fine + imprisonment 2 months
    {"query": "Ano ang parusa ng loan shark na kumukuha ng 4Ps cash card bilang collateral?",
     "relevant": ["ORDINANCE-NO-9107.txt"]},

    # ── ORDINANCE NO. 9170 — New Market Code of Manila ───────────────────────

    # Sec. 21(e) — Sub-leasing of stalls is prohibited
    {"query": "Pwede bang ipagawa sa ibang tao ang stall na inarkila mo sa palengke ng Manila?",
     "relevant": ["ORDINANCE-NO-9170.txt"]},

    # Sec. 11 — Stall rental rates (Class A: P18/sqm for wet section)
    {"query": "Magkano ang bayad sa araw-araw na rental ng stall sa Class A na palengke sa Manila?",
     "relevant": ["ORDINANCE-NO-9170.txt"]},

    # Sec. 20 — Qualifications to apply for stall (Filipino, 18+, Manila resident 6 months)
    {"query": "Ano ang mga kailangan para makapag-apply ng market stall sa Manila?",
     "relevant": ["ORDINANCE-NO-9170.txt"]},

    # Sec. 21(b) — Lease cancellation after 60 days non-payment
    {"query": "Mawawala ba ang stall mo sa palengke kung hindi ka magbabayad ng rental ng dalawang buwan?",
     "relevant": ["ORDINANCE-NO-9170.txt"]},

    # Sec. 36 — Injection of water in meat/dressed chicken strictly prohibited
    {"query": "Bawal ba ang mag-inject ng tubig sa karne o manok na ibinebenta sa palengke?",
     "relevant": ["ORDINANCE-NO-9170.txt"]},

]