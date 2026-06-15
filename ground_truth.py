# ground_truth.py
# This is your evaluation dataset.
# Each entry has:
#   "query"    — the Taglish test question
#   "relevant" — list of PDF filenames that contain the correct answer
# Add or update entries as you manually verify which ordinance answers each question.

GROUND_TRUTH = [
    # Environmental Code (8371)
    {"query": "Pwede bang magsunugan ng basura sa bakuran?",              "relevant": ["ORDINANCE-NO.-8371.pdf"]},
    {"query": "Ano ang parusa pag nagtapon ng basura sa ilog?",           "relevant": ["ORDINANCE-NO.-8371.pdf"]},
    {"query": "Bawal ba ang maingay na makinarya sa residential area?",   "relevant": ["ORDINANCE-NO.-8371.pdf"]},
    {"query": "Hanggang anong oras pwede ang malakas na sound system?",   "relevant": ["ORDINANCE-NO.-8371.pdf"]},
    {"query": "Sino ang responsible sa pag-segregate ng basura?",         "relevant": ["ORDINANCE-NO.-8371.pdf"]},

    # Traffic (8092 + 8327)
    {"query": "Magkano ang multa pag naka-park sa no parking zone?",      "relevant": ["ORDINANCE-NO.-8092.pdf", "ORDINANCE-NO.-8327.pdf"]},
    {"query": "Pwede bang mag-counterflow sa one-way street pag emergency?","relevant": ["ORDINANCE-NO.-8092.pdf"]},
    {"query": "Anong oras bawal ang trucks sa main roads ng Manila?",      "relevant": ["ORDINANCE-NO.-8092.pdf"]},
    {"query": "Ano ang penalty kapag walang driver's license tapos nahuli?","relevant": ["ORDINANCE-NO.-8092.pdf", "ORDINANCE-NO.-8327.pdf"]},
    {"query": "Puwede bang mag-park sa tapat ng bahay ko kahit walang sign?","relevant": ["ORDINANCE-NO.-8092.pdf"]},

    # Revenue Code (8331)
    {"query": "Magkano ang bayad para makakuha ng business permit sa Manila?","relevant": ["ORDINANCE-NO.-8331.pdf"]},
    {"query": "Kailangan pa bang mag-renew ng permit kahit hindi nag-operate?","relevant": ["ORDINANCE-NO.-8331.pdf"]},
    {"query": "Ano ang penalties pag late ang pagbabayad ng local business tax?","relevant": ["ORDINANCE-NO.-8331.pdf"]},
    {"query": "May diskwento ba para sa small business sa permit fees?",    "relevant": ["ORDINANCE-NO.-8331.pdf"]},
    {"query": "Sino ang exempt sa pagbabayad ng real property tax sa Manila?","relevant": ["ORDINANCE-NO.-8331.pdf"]},

    # Anti-Dengue (8355)
    {"query": "Ano ang gagawin ng barangay kapag may mosquito breeding site sa bahay?","relevant": ["ORDINANCE-NO.-8355.pdf"]},
    {"query": "Magkano ang multa pag may natuklasang standing water sa property?","relevant": ["ORDINANCE-NO.-8355.pdf"]},
    {"query": "Ilang beses pwedeng mag-inspect ang barangay official ng bahay para sa dengue?","relevant": ["ORDINANCE-NO.-8355.pdf"]},
    {"query": "Sino ang may responsibilidad na mag-abate ng mosquito sa apartment?","relevant": ["ORDINANCE-NO.-8355.pdf"]},
    {"query": "Ano ang kailangan gawin ng may-ari ng bakanteng lote para sa dengue?","relevant": ["ORDINANCE-NO.-8355.pdf"]},

    # Market Code (9170)
    {"query": "Hanggang anong oras pwede mag-operate ang vendors sa public market?","relevant": ["ORDINANCE-NO.-9170.pdf"]},
    {"query": "Ano ang kailangan para makapag-apply ng stall sa palengke ng Manila?","relevant": ["ORDINANCE-NO.-9170.pdf"]},
    {"query": "Bawal ba ang ibang tao na mag-sublet ng stall sa public market?","relevant": ["ORDINANCE-NO.-9170.pdf"]},
    {"query": "Ano ang karapatan ng vendor kapag pinagbayad ng hindi authorized na fee?","relevant": ["ORDINANCE-NO.-9170.pdf"]},

    # 4Ps (9107)
    {"query": "Ano ang mangyayari sa loan shark na kumuha ng 4Ps card ng benepisyaryo?","relevant": ["ORDINANCE-No.-9107.pdf"]},
]
