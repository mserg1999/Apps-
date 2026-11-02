"""Builds Claims_Outside_Counsel_Operations.xlsx (template). Run: python build_workbook.py"""
import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

OUT = "Claims_Outside_Counsel_Operations.xlsx"
FIRST, LAST = 5, 1004          # data rows on Directory / Tracker
FONT = "Arial"

# ---------- palette (pastel) ----------
LAV, LAV_D = "E8E0F7", "4B3B70"
BLUE, MINT, PEACH, PINK, BUTTER = "D9E8F7", "D7F2E6", "FDE5D6", "F9DDE8", "FFF6CC"
GRID = "D0CCE0"
fill = lambda c: PatternFill("solid", start_color=c, end_color=c)
thin = Side(style="thin", color=GRID)
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

def f(size=10, bold=False, color="333333", italic=False, underline=None):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic, underline=underline)

# ---------- cyber statuses & colours ----------
CYBER = [  # label, fill, font colour
    ("Completed", "C6EFCE", "1E5631"),
    ("Pending with Firm", "CFE2F3", "1F4E79"),
    ("Pending OneTrust with GEICO", "E1D5F0", "4B2C7A"),
    ("Under Review", "FCD9B6", "7F4012"),
    ("Rejected", "9C0006", "FFFFFF"),
    ("Firm Declined Assessment", "FFC7CE", "9C0006"),
    ("No Assessment on File", "E3E3E3", "404040"),
]
IN_PROCESS = ["Pending with Firm", "Pending OneTrust with GEICO", "Under Review"]
ONBOARD = ["Not Started", "In Progress", "Onboarding Complete", "On Hold", "Inactive / Terminated"]
FIRM_TYPES = ["Defense Panel", "Coverage Counsel", "Subrogation", "Fraud / SIU", "Appellate",
              "Monitoring Counsel", "Extra-Contractual", "Other"]
RISK = ["Low", "Moderate", "High", "Critical"]
SUFFIXES = [" llp", " pllc", " llc", " lllp", " lp", " pc", " pa", " plc", " ltd", " inc", " co",
            " law firm", " law group", " law offices", " attorneys at law", " attorneys", " esq"]
US = [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA","California"),
 ("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("DC","District of Columbia"),("FL","Florida"),
 ("GA","Georgia"),("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),
 ("KS","Kansas"),("KY","Kentucky"),("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),
 ("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),("MS","Mississippi"),("MO","Missouri"),
 ("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),("NJ","New Jersey"),
 ("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
 ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),
 ("SD","South Dakota"),("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),
 ("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),("WI","Wisconsin"),("WY","Wyoming"),
 ("AS","American Samoa"),("GU","Guam"),("MP","Northern Mariana Islands"),("PR","Puerto Rico"),
 ("VI","U.S. Virgin Islands")]
CA = [("AB","Alberta"),("BC","British Columbia"),("MB","Manitoba"),("NB","New Brunswick"),
 ("NL","Newfoundland and Labrador"),("NS","Nova Scotia"),("NT","Northwest Territories"),
 ("NU","Nunavut"),("ON","Ontario"),("PE","Prince Edward Island"),("QC","Quebec"),
 ("SK","Saskatchewan"),("YT","Yukon")]

wb = Workbook()
ws_s = wb.active; ws_s.title = "Firm Search"
ws_m = wb.create_sheet("Metrics Dashboard")
ws_d = wb.create_sheet("Firm Directory")
ws_t = wb.create_sheet("Cyber Assessment Tracker")
ws_h = wb.create_sheet("How To Use")
ws_l = wb.create_sheet("Lists")
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
ws_s.sheet_properties.tabColor = "B9A6E0"; ws_m.sheet_properties.tabColor = "A8D5BA"
ws_d.sheet_properties.tabColor = "9EC5E8"; ws_t.sheet_properties.tabColor = "F5B98E"
ws_h.sheet_properties.tabColor = "F3B6CB"; ws_l.sheet_properties.tabColor = "CCCCCC"

def banner(ws, rng, title, sub=None, color=LAV):
    first = rng.split(":")[0]
    ws.merge_cells(rng)
    c = ws[first]; c.value = title; c.font = f(18, True, LAV_D); c.fill = fill(color)
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[c.row].height = 36
    for row in ws[rng]:
        for x in row: x.fill = fill(color)
    if sub:
        col = first.rstrip("0123456789")
        s = ws[f"{col}{c.row+1}"]; s.value = sub; s.font = f(10, italic=True, color="6B6385")

def cyber_cf(ws, rng):
    for label, bg, fg in CYBER:
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{label}"'],
            fill=fill(bg), font=Font(name=FONT, color=fg, bold=True)))

# =====================================================================
# Lists
# =====================================================================
ws_l["A1"] = "State / Province"; ws_l["B1"] = "Name"; ws_l["C1"] = "Country"
r = 2
for ab, nm in US: ws_l.append([ab, nm, "USA"]); r += 1
ca_start = r
for ab, nm in CA: ws_l.append([ab, nm, "Canada"]); r += 1
st_last = r - 1
STATE_RNG = f"Lists!$A$2:$A${st_last}"
CA_RNG = f"Lists!$A${ca_start}:$A${st_last}"
lists = {"E": ("Cyber Assessment Status", [c[0] for c in CYBER]),
         "F": ("Onboarding Status", ONBOARD), "G": ("Firm Type", FIRM_TYPES),
         "H": ("Yes / No", ["Yes", "No"]), "I": ("Cyber Risk Rating", RISK),
         "J": ("Entity Suffixes (ignored by search)", SUFFIXES)}
RNG = {}
for col, (hdr, vals) in lists.items():
    ws_l[f"{col}1"] = hdr
    for i, v in enumerate(vals, start=2): ws_l[f"{col}{i}"] = v
    RNG[col] = f"Lists!${col}$2:${col}${len(vals)+1}"
for c in ws_l[1]:
    c.font = f(10, True, LAV_D); c.fill = fill(LAV); c.border = BOX
for row in ws_l.iter_rows(min_row=2, max_row=ws_l.max_row):
    for c in row:
        c.font = f(10)
        if c.value is not None: c.border = BOX
for col, w in zip("ABCDEFGHIJ", [16, 28, 10, 3, 30, 24, 22, 10, 18, 32]):
    ws_l.column_dimensions[col].width = w
for i, (lab, bg, fg) in enumerate(CYBER, start=2):
    ws_l[f"E{i}"].fill = fill(bg); ws_l[f"E{i}"].font = Font(name=FONT, color=fg, bold=True)
ws_l["L1"] = "Admin tab – edit these lists to change the dropdown choices. Do not insert rows above row 2."
ws_l["L1"].font = f(9, italic=True, color="6B6385")
ws_l.freeze_panes = "A2"

# =====================================================================
# Firm Directory
# =====================================================================
DIR_COLS = [  # header, width, kind
    ("Firm ID", 12, "in"), ("Firm Name", 32, "in"), ("Also Known As / Prior Names", 28, "in"),
    ("Firm Type", 18, "in"), ("Practice Areas / Lines", 26, "in"), ("Tax ID (TIN)", 14, "txt"),
    ("Vendor / Payee #", 14, "txt"), ("Street Address", 28, "in"), ("City", 16, "in"),
    ("State / Prov", 10, "in"), ("ZIP / Postal Code", 12, "txt"), ("Country", 10, "calc"),
    ("Jurisdictions Covered", 20, "in"), ("Main Phone", 15, "txt"), ("Website", 24, "in"),
    ("Relationship Partner", 20, "in"), ("Partner Email", 26, "in"), ("Partner Phone", 15, "txt"),
    ("Billing Contact", 18, "in"), ("Billing Email", 26, "in"), ("Internal Relationship Owner", 20, "in"),
    ("Onboarding Status", 20, "in"), ("Engagement Letter Date", 14, "date"),
    ("Billing Guidelines Ack.", 12, "in"), ("E-Billing Set Up", 11, "in"),
    ("Partner Rate ($/hr)", 12, "money"), ("Associate Rate ($/hr)", 12, "money"),
    ("Paralegal Rate ($/hr)", 12, "money"), ("Onboarding Complete Date", 14, "date"),
    ("Cyber Assessment Status", 26, "calc"), ("Cyber Completed Date", 14, "calcdate"),
    ("Fully Onboarded (incl. Cyber)", 14, "calc"), ("Fully Onboarded Date", 14, "calcdate"),
    ("Notes", 36, "in"), ("Search Key (auto)", 10, "calc"), ("Match # (auto)", 8, "calc"),
]
DC = {h: L(i) for i, (h, _, _) in enumerate(DIR_COLS, start=1)}
nd = len(DIR_COLS)
banner(ws_d, f"A1:{L(nd-2)}1", "Firm Directory",
       "One row per firm. Yellow headers = you type; mint headers = auto-calculated (don't type over). Firm ID is required and must be unique.")
HDR = 4
ws_d.row_dimensions[HDR].height = 42
for i, (h, w, kind) in enumerate(DIR_COLS, start=1):
    c = ws_d.cell(HDR, i, h)
    c.font = f(10, True, LAV_D); c.border = BOX
    c.fill = fill(MINT if kind.startswith("calc") else BUTTER)
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws_d.column_dimensions[L(i)].width = w

def dref(name, r): return f"${DC[name]}{r}"
def drng(name): return f"'Firm Directory'!${DC[name]}${FIRST}:${DC[name]}${LAST}"

def norm_formula(expr):
    """lower-case, punctuation -> space/blank, drop ' and ', drop spaces"""
    x = f'LOWER(" "&{expr}&" ")'
    for a, b in [("&", " "), ("-", " "), ("/", " "), (".", ""), (",", ""), ("'", ""),
                 ("’", ""), ("(", ""), (")", ""), (";", " ")]:
        x = f'SUBSTITUTE({x},"{a}","{b}")'
    x = f'SUBSTITUTE(SUBSTITUTE({x}," and "," ")," and "," ")'
    return f'SUBSTITUTE({x}," ","")'

KEY_FIELDS = ["Firm ID", "Firm Name", "Also Known As / Prior Names", "Firm Type", "Practice Areas / Lines",
              "Tax ID (TIN)", "Vendor / Payee #", "City", "State / Prov", "ZIP / Postal Code",
              "Relationship Partner", "Partner Email", "Billing Contact", "Billing Email",
              "Internal Relationship Owner", "Main Phone"]
T_A = f"'Cyber Assessment Tracker'!$A${FIRST}:$A${LAST}"
T_D = f"'Cyber Assessment Tracker'!$D${FIRST}:$D${LAST}"
T_I = f"'Cyber Assessment Tracker'!$I${FIRST}:$I${LAST}"

for r in range(FIRST, LAST + 1):
    B, A = dref("Firm Name", r), dref("Firm ID", r)
    ws_d[f"{DC['Country']}{r}"] = (f'=IF({dref("State / Prov", r)}="","",IF(ISNUMBER(MATCH('
                                   f'{dref("State / Prov", r)},{CA_RNG},0)),"Canada","USA"))')
    ws_d[f"{DC['Cyber Assessment Status']}{r}"] = (
        f'=IF({B}="","",IF({A}="","No Assessment on File",IFERROR(IF(INDEX({T_D},MATCH({A},{T_A},0))="",'
        f'"No Assessment on File",INDEX({T_D},MATCH({A},{T_A},0))),"No Assessment on File")))')
    ws_d[f"{DC['Cyber Completed Date']}{r}"] = (
        f'=IF(OR({B}="",{A}=""),"",IFERROR(IF(INDEX({T_I},MATCH({A},{T_A},0))="","",'
        f'IF({dref("Cyber Assessment Status", r)}="Completed",INDEX({T_I},MATCH({A},{T_A},0)),"")),""))')
    ws_d[f"{DC['Fully Onboarded (incl. Cyber)']}{r}"] = (
        f'=IF({B}="","",IF(AND({dref("Onboarding Status", r)}="Onboarding Complete",'
        f'{dref("Cyber Assessment Status", r)}="Completed"),"Yes","No"))')
    oc, cc = dref("Onboarding Complete Date", r), dref("Cyber Completed Date", r)
    ws_d[f"{DC['Fully Onboarded Date']}{r}"] = (
        f'=IF({dref("Fully Onboarded (incl. Cyber)", r)}<>"Yes","",IF(OR({oc}="",{cc}=""),"",MAX({oc},{cc})))')
    concat = '&" | "&'.join(dref(k, r) for k in KEY_FIELDS)
    ws_d[f"{DC['Search Key (auto)']}{r}"] = f'=IF({B}="","",{norm_formula(concat)})'
    mc = DC["Match # (auto)"]
    ws_d[f"{mc}{r}"] = (f"=IF(OR('Firm Search'!$Z$3=\"\",{B}=\"\"),\"\",IF(ISNUMBER(FIND('Firm Search'!$Z$3,"
                        f"{dref('Search Key (auto)', r)})),MAX(${mc}${HDR}:{mc}{r-1})+1,\"\"))")
    for i, (h, w, kind) in enumerate(DIR_COLS, start=1):
        c = ws_d.cell(r, i); c.font = f(10); c.border = BOX
        if kind in ("date", "calcdate"): c.number_format = "mm/dd/yyyy"
        elif kind == "money": c.number_format = '$#,##0.00'
        elif kind == "txt": c.number_format = "@"
        if kind.startswith("calc"): c.fill = fill("F4FBF7")
        elif r % 2 == 0: c.fill = fill("FBF9FE")

# example row
ex = {"Firm ID": "EX-0001", "Firm Name": "Sample & Associates, LLP",
      "Also Known As / Prior Names": "Sample Associates; Sample Law Group", "Firm Type": "Defense Panel",
      "Practice Areas / Lines": "Auto BI, PIP, Coverage", "Tax ID (TIN)": "12-3456789",
      "Vendor / Payee #": "V-100245", "Street Address": "123 Main St, Suite 400", "City": "Richmond",
      "State / Prov": "VA", "ZIP / Postal Code": "23219", "Jurisdictions Covered": "VA, MD, DC",
      "Main Phone": "(804) 555-0100", "Website": "www.samplelaw.example",
      "Relationship Partner": "Jane Doe", "Partner Email": "jdoe@samplelaw.example",
      "Partner Phone": "(804) 555-0101", "Billing Contact": "John Roe",
      "Billing Email": "billing@samplelaw.example", "Internal Relationship Owner": "Your Name",
      "Onboarding Status": "Onboarding Complete", "Engagement Letter Date": dt.date(2026, 3, 2),
      "Billing Guidelines Ack.": "Yes", "E-Billing Set Up": "Yes", "Partner Rate ($/hr)": 250,
      "Associate Rate ($/hr)": 185, "Paralegal Rate ($/hr)": 95,
      "Onboarding Complete Date": dt.date(2026, 3, 15),
      "Notes": "EXAMPLE ROW – shows the expected format. Delete this row (and its tracker row) before use."}
for k, v in ex.items():
    ws_d[f"{DC[k]}{FIRST}"] = v
ws_d[f"{DC['Notes']}{FIRST}"].font = f(10, italic=True, color="9C0006")

# validations
def dv_list(ws, src, rng, prompt=None, strict=True):
    dv = DataValidation(type="list", formula1=f"={src}" if not src.startswith('"') else src,
                        allow_blank=True, showDropDown=False)
    dv.error = "Please pick a value from the dropdown list."; dv.errorTitle = "Invalid entry"
    dv.errorStyle = "stop" if strict else "warning"
    if prompt: dv.prompt = prompt; dv.showInputMessage = True
    ws.add_data_validation(dv); dv.add(rng)
def col_rng(name): return f"{DC[name]}{FIRST}:{DC[name]}{LAST}"
dv_list(ws_d, STATE_RNG, col_rng("State / Prov"))
dv_list(ws_d, RNG["F"], col_rng("Onboarding Status"))
dv_list(ws_d, RNG["G"], col_rng("Firm Type"), strict=False)
dv_list(ws_d, RNG["H"], col_rng("Billing Guidelines Ack."))
dv_list(ws_d, RNG["H"], col_rng("E-Billing Set Up"))
uniq = DataValidation(type="custom", formula1=f"=COUNTIF($A${FIRST}:$A${LAST},A{FIRST})=1", allow_blank=True)
uniq.error = "This Firm ID is already used. Firm IDs must be unique."; uniq.errorTitle = "Duplicate Firm ID"
ws_d.add_data_validation(uniq); uniq.add(col_rng("Firm ID"))
for nm in ("Engagement Letter Date", "Onboarding Complete Date"):
    dvd = DataValidation(type="date", operator="greaterThan", formula1="DATE(1990,1,1)", allow_blank=True)
    dvd.error = "Enter a date, e.g. 03/15/2026."; ws_d.add_data_validation(dvd); dvd.add(col_rng(nm))

cyber_cf(ws_d, col_rng("Cyber Assessment Status"))
ws_d.conditional_formatting.add(col_rng("Fully Onboarded (incl. Cyber)"),
    CellIsRule(operator="equal", formula=['"Yes"'], fill=fill("C6EFCE"), font=Font(name=FONT, color="1E5631", bold=True)))
ws_d.freeze_panes = ws_d[f"C{FIRST}"]
ws_d.auto_filter.ref = f"A{HDR}:{L(nd-2)}{LAST}"
for h in ("Search Key (auto)", "Match # (auto)"):
    ws_d.column_dimensions[DC[h]].hidden = True
ws_d[f"{DC['Fully Onboarded (incl. Cyber)']}{HDR}"].comment = Comment(
    "Yes only when Onboarding Status = 'Onboarding Complete' AND Cyber Assessment Status = 'Completed'.", "Template")
ws_d[f"{DC['Fully Onboarded Date']}{HDR}"].comment = Comment(
    "Later of Onboarding Complete Date and Cyber Completed Date – the date the firm became fully onboarded.", "Template")
ws_d[f"{DC['Cyber Assessment Status']}{HDR}"].comment = Comment(
    "Pulled automatically from the Cyber Assessment Tracker by Firm ID. Firms with no tracker row show 'No Assessment on File'.", "Template")

# =====================================================================
# Cyber Assessment Tracker
# =====================================================================
TR_COLS = [("Firm ID", 12, "in"), ("Firm Name (auto)", 32, "calc"), ("State / Prov (auto)", 11, "calc"),
           ("Cyber Assessment Status", 28, "in"), ("Assessment Sent Date", 13, "date"),
           ("Firm Response Received", 13, "date"), ("Submitted to OneTrust", 13, "date"),
           ("Review Start Date", 13, "date"), ("Completed / Decision Date", 14, "date"),
           ("Risk Rating", 11, "in"), ("Next Reassessment Due (auto)", 14, "calcdate"),
           ("Days Open (auto)", 10, "calcnum"), ("Assigned Reviewer", 18, "in"),
           ("OneTrust Ref #", 14, "txt"), ("Notes / Last Update", 40, "in")]
banner(ws_t, "A1:O1", "Cyber Assessment Tracker",
       "One row per firm (keep it current – re-use the row for reassessments). Enter the Firm ID exactly as in the Firm Directory; pick the status from the dropdown.",
       color=PEACH)
ws_t.row_dimensions[HDR].height = 42
for i, (h, w, kind) in enumerate(TR_COLS, start=1):
    c = ws_t.cell(HDR, i, h); c.font = f(10, True, LAV_D); c.border = BOX
    c.fill = fill(MINT if kind.startswith("calc") else BUTTER)
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws_t.column_dimensions[L(i)].width = w
D_A, D_B, D_J = drng("Firm ID"), drng("Firm Name"), drng("State / Prov")
for r in range(FIRST, LAST + 1):
    ws_t[f"B{r}"] = f'=IF($A{r}="","",IFERROR(INDEX({D_B},MATCH($A{r},{D_A},0)),"⚠ Firm ID not in Directory"))'
    ws_t[f"C{r}"] = f'=IF($A{r}="","",IFERROR(IF(INDEX({D_J},MATCH($A{r},{D_A},0))="","",INDEX({D_J},MATCH($A{r},{D_A},0))),""))'
    ws_t[f"K{r}"] = f'=IF(AND($D{r}="Completed",ISNUMBER($I{r})),EDATE($I{r},12),"")'
    ws_t[f"L{r}"] = f'=IF(NOT(ISNUMBER($E{r})),"",IF(ISNUMBER($I{r}),$I{r}-$E{r},TODAY()-$E{r}))'
    for i, (h, w, kind) in enumerate(TR_COLS, start=1):
        c = ws_t.cell(r, i); c.font = f(10); c.border = BOX
        if kind in ("date", "calcdate"): c.number_format = "mm/dd/yyyy"
        elif kind == "calcnum": c.number_format = "0"
        elif kind == "txt": c.number_format = "@"
        if kind.startswith("calc"): c.fill = fill("F4FBF7")
        elif r % 2 == 0: c.fill = fill("FFFBF8")
ex_t = ["EX-0001", None, None, "Completed", dt.date(2026, 2, 2), dt.date(2026, 2, 16), dt.date(2026, 2, 20),
        dt.date(2026, 2, 23), dt.date(2026, 3, 10), "Low", None, None, "Your Name", "OT-000123",
        "EXAMPLE ROW – delete before use."]
for i, v in enumerate(ex_t, start=1):
    if v is not None: ws_t.cell(FIRST, i, v)
ws_t[f"O{FIRST}"].font = f(10, italic=True, color="9C0006")
dv_list(ws_t, RNG["E"], f"D{FIRST}:D{LAST}", prompt="Pick the current cyber assessment status.")
dv_list(ws_t, RNG["I"], f"J{FIRST}:J{LAST}")
dv_list(ws_t, f"'Firm Directory'!$A${FIRST}:$A${LAST}", f"A{FIRST}:A{LAST}", strict=False)
uniq_t = DataValidation(type="custom", formula1=f"=COUNTIF($A${FIRST}:$A${LAST},A{FIRST})=1", allow_blank=True)
uniq_t.error = "This firm already has a tracker row – update that row instead."; uniq_t.errorTitle = "Duplicate firm"
ws_t.add_data_validation(uniq_t); uniq_t.add(f"A{FIRST}:A{LAST}")
cyber_cf(ws_t, f"D{FIRST}:D{LAST}")
ws_t.conditional_formatting.add(f"B{FIRST}:B{LAST}", CellIsRule(operator="equal",
    formula=['"⚠ Firm ID not in Directory"'], font=Font(name=FONT, color="9C0006", bold=True)))
# legend
ws_t["Q4"] = "Status Colour Key"; ws_t["Q4"].font = f(10, True, LAV_D); ws_t["Q4"].fill = fill(LAV)
ws_t.column_dimensions["P"].width = 3; ws_t.column_dimensions["Q"].width = 30
for i, (lab, bg, fg) in enumerate(CYBER, start=5):
    c = ws_t[f"Q{i}"]; c.value = lab; c.fill = fill(bg); c.font = Font(name=FONT, color=fg, bold=True); c.border = BOX
ws_t.freeze_panes = ws_t[f"C{FIRST}"]
ws_t.auto_filter.ref = f"A{HDR}:O{LAST}"

# =====================================================================
# Firm Search
# =====================================================================
s = ws_s
for col, w in {"A": 2, "B": 9, "C": 12, "D": 34, "E": 15, "F": 8, "G": 20, "H": 27, "I": 3,
               "J": 28, "K": 44, "L": 3}.items():
    s.column_dimensions[col].width = w
banner(s, "B2:K2", "🔍  Claims Outside Counsel – Firm Search",
       "Type ANY part of a firm's name or details – any format works: “Smith & Jones LLP”, “smith and jones”, “Smith-Jones”, a Firm ID, Tax ID (with or without dash), city, state, partner or email.")
s["B5"] = "Search"; s["B5"].font = f(12, True, LAV_D); s["B5"].alignment = Alignment(vertical="center")
s.merge_cells("C5:H5")
s["C5"].fill = fill(BUTTER); s["C5"].font = f(14, True, "333333")
s["C5"].alignment = Alignment(vertical="center", indent=1)
for col in "CDEFGH":
    s[f"{col}5"].border = Border(left=Side("medium", "B9A6E0") if col == "C" else None,
                                 right=Side("medium", "B9A6E0") if col == "H" else None,
                                 top=Side("medium", "B9A6E0"), bottom=Side("medium", "B9A6E0"))
s.row_dimensions[5].height = 30
s["C5"].comment = Comment("Type here and press Enter. Delete the text to clear the search.", "Template")
s["J5"] = "Firms found"; s["J5"].font = f(11, True, LAV_D); s["J5"].fill = fill(PINK)
s["J5"].alignment = Alignment(horizontal="right", vertical="center", indent=1)
s["K5"] = f"=IF($Z$3=\"\",0,MAX({drng('Match # (auto)')}))"
s["K5"].font = f(14, True, LAV_D); s["K5"].fill = fill(PINK); s["K5"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
s["C6"] = "Tip: fewer words = more results. Entity suffixes (LLP, LLC, PC, PA…), “the”, “&/and” and punctuation are ignored. Click a firm name to jump to its Directory row."
s["C6"].font = f(9, italic=True, color="6B6385")

# hidden helper cells (column Z)
inp = 'LOWER($C$5)'
for a, b in [("&", " and "), ("-", " "), ("/", " "), (";", " "), (".", ""), (",", ""), ("'", ""),
             ("’", ""), ("(", ""), (")", "")]:
    inp = f'SUBSTITUTE({inp},"{a}","{b}")'
s["Y1"] = "cleaned input"; s["Z1"] = f'=TRIM({inp})'
s["Y2"] = "suffix/'the' stripped"
s["Z2"] = (f'=IF(LEFT(TRIM(LEFT($Z$1,LEN($Z$1)-SUMPRODUCT(MAX((RIGHT($Z$1,LEN({RNG["J"]}))={RNG["J"]})*LEN({RNG["J"]}))))),4)="the ",'
           f'MID(TRIM(LEFT($Z$1,LEN($Z$1)-SUMPRODUCT(MAX((RIGHT($Z$1,LEN({RNG["J"]}))={RNG["J"]})*LEN({RNG["J"]}))))),5,500),'
           f'TRIM(LEFT($Z$1,LEN($Z$1)-SUMPRODUCT(MAX((RIGHT($Z$1,LEN({RNG["J"]}))={RNG["J"]})*LEN({RNG["J"]}))))))')
s["Y3"] = "normalised search"; s["Z3"] = '=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(" "&$Z$2&" "," and "," ")," and "," ")," ","")'
s["Y4"] = "selected row"; s["Z4"] = f"=IFERROR(MATCH($K$9,{drng('Match # (auto)')},0),\"\")"
s.column_dimensions["Y"].hidden = True; s.column_dimensions["Z"].hidden = True

# match list
s.merge_cells("B8:H8"); s["B8"] = "Matching Firms"; s["B8"].font = f(12, True, LAV_D)
for col in "BCDEFGH": s[f"{col}8"].fill = fill(BLUE)
heads = ["#", "Firm ID", "Firm Name (click to open)", "City", "State", "Onboarding Status", "Cyber Status"]
srcs = [None, "Firm ID", "Firm Name", "City", "State / Prov", "Onboarding Status", "Cyber Assessment Status"]
for col, h in zip("BCDEFGH", heads):
    c = s[f"{col}9"]; c.value = h; c.font = f(10, True, LAV_D); c.fill = fill(LAV); c.border = BOX
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
NLIST = 20
for i in range(1, NLIST + 1):
    r = 9 + i
    s[f"B{r}"] = f'=IF({i}<=$K$5,{i},"")'
    s[f"Y{r}"] = f"=IF($B{r}=\"\",\"\",IFERROR(MATCH($B{r},{drng('Match # (auto)')},0),\"\"))"
    for col, src in zip("CDEFGH", srcs[1:]):
        rngx = drng(src)
        val = f'IF(INDEX({rngx},$Y{r})&""="","",INDEX({rngx},$Y{r}))'
        if src == "Firm Name":
            s[f"{col}{r}"] = f"=IF($Y{r}=\"\",\"\",HYPERLINK(\"#'Firm Directory'!B\"&($Y{r}+{FIRST-1}),{val}))"
        else:
            s[f"{col}{r}"] = f'=IF($Y{r}="","",{val})'
    for col in "BCDEFGH":
        c = s[f"{col}{r}"]; c.border = BOX; c.font = f(10)
        c.fill = fill("FFFFFF" if i % 2 else "F7F4FC")
        if col in "BF": c.alignment = Alignment(horizontal="center")
    s[f"D{r}"].font = f(10, color="5B3FA0", underline="single")
cyber_cf(s, f"H10:H{9+NLIST}")
s.merge_cells(f"B{10+NLIST}:H{10+NLIST}")
s[f"B{10+NLIST}"] = (f'=IF($C$5="","Type in the yellow search box above to find a firm.",IF($K$5=0,'
                     f'"No matches – try fewer words or a different spelling.",IF($K$5>{NLIST},'
                     f'"Showing the first {NLIST} of "&$K$5&" matches – add more words to narrow it down.",'
                     f'"Pick a result # on the right to see the firm\'s full profile.")))')
s[f"B{10+NLIST}"].font = f(10, italic=True, color="6B6385")

# detail card
s.merge_cells("J8:K8"); s["J8"] = "Firm Profile"; s["J8"].font = f(12, True, LAV_D)
s["J8"].fill = fill(MINT); s["K8"].fill = fill(MINT)
s["J9"] = "Show result #  ▶"; s["J9"].font = f(10, True, LAV_D); s["J9"].fill = fill(PINK); s["J9"].border = BOX
s["J9"].alignment = Alignment(horizontal="right", indent=1)
s["K9"] = 1; s["K9"].font = f(12, True); s["K9"].fill = fill(BUTTER); s["K9"].border = BOX
s["K9"].alignment = Alignment(horizontal="left", indent=1)
dvn = DataValidation(type="whole", operator="between", formula1="1", formula2="100000", allow_blank=False)
dvn.error = "Enter the # of a result from the Matching Firms list."; s.add_data_validation(dvn); dvn.add("K9")
s["K9"].comment = Comment("Enter the # of the firm in the Matching Firms list to see its full profile.", "Template")
detail = [h for h, _, _ in DIR_COLS if h not in ("Search Key (auto)", "Match # (auto)")]
kinds = {h: k for h, _, k in DIR_COLS}
for i, h in enumerate(detail):
    r = 10 + i
    lab = s[f"J{r}"]; lab.value = h; lab.font = f(10, True, "5A5470"); lab.border = BOX
    lab.fill = fill("F3EFFA"); lab.alignment = Alignment(horizontal="right", indent=1)
    rngx = drng(h)
    v = s[f"K{r}"]
    v.value = f'=IF($Z$4="","",IF(INDEX({rngx},$Z$4)&""="","",INDEX({rngx},$Z$4)))'
    v.font = f(10, h == "Firm Name"); v.border = BOX; v.alignment = Alignment(horizontal="left", indent=1, wrap_text=True)
    if kinds[h] in ("date", "calcdate"): v.number_format = "mm/dd/yyyy"
    elif kinds[h] == "money": v.number_format = '$#,##0.00'
    if h == "Cyber Assessment Status": cyber_cf(s, f"K{r}")
    if h == "Fully Onboarded (incl. Cyber)":
        s.conditional_formatting.add(f"K{r}", CellIsRule(operator="equal", formula=['"Yes"'],
            fill=fill("C6EFCE"), font=Font(name=FONT, color="1E5631", bold=True)))
s.freeze_panes = "A7"

# =====================================================================
# Metrics Dashboard
# =====================================================================
m = ws_m
for col, w in {"A": 2, "B": 30, "C": 14, "D": 12, "E": 3, "F": 30, "G": 14, "H": 12, "I": 3}.items():
    m.column_dimensions[col].width = w
banner(m, "B2:H2", "📊  Outside Counsel Metrics Dashboard",
       "All numbers update automatically from the Firm Directory and Cyber Assessment Tracker. Only the yellow date cells are edited here.",
       color=MINT)
m["B5"] = "Reporting start date (since)"; m["C5"] = dt.date(2026, 1, 1)
m["B6"] = "Reporting end date (blank = no end)"; m["C6"] = None
for rr in (5, 6):
    m[f"B{rr}"].font = f(10, True, LAV_D); m[f"B{rr}"].fill = fill(LAV); m[f"B{rr}"].border = BOX
    m[f"C{rr}"].fill = fill(BUTTER); m[f"C{rr}"].border = BOX; m[f"C{rr}"].number_format = "mm/dd/yyyy"
    m[f"C{rr}"].font = f(11, True)
m["C5"].comment = Comment("Change this date to count firms fully onboarded on or after it.", "Template")
m["D5"] = '=IF(ISNUMBER($C$5),"","⚠ enter a date")'; m["D5"].font = f(9, True, "9C0006")
m["X5"] = '=IF(ISNUMBER($C$6),$C$6,DATE(2099,12,31))'; m.column_dimensions["X"].hidden = True
dvd = DataValidation(type="date", operator="greaterThan", formula1="DATE(1990,1,1)", allow_blank=True)
dvd.error = "Enter a date, e.g. 01/01/2026."; m.add_data_validation(dvd); dvd.add("C5:C6")

FN, FO, FOD = drng("Firm Name"), drng("Fully Onboarded (incl. Cyber)"), drng("Fully Onboarded Date")
CS, OS = drng("Cyber Assessment Status"), drng("Onboarding Status")
in_proc = "+".join(f'COUNTIF({CS},"{x}")' for x in IN_PROCESS)
cards = [
    ("B8", "Total Firms in Directory", f'=COUNTIF({FN},"?*")', LAV,
     "Every firm row with a Firm Name."),
    ("F8", "Fully Onboarded Since Start Date (incl. Cyber)",
     f'=COUNTIFS({FO},"Yes",{FOD},">="&$C$5,{FOD},"<="&$X$5)', "C6EFCE",
     "Onboarding Complete + Cyber Completed, with Fully Onboarded Date in the reporting window."),
    ("B13", "Firms Currently in Cyber Process", f"={in_proc}", "CFE2F3",
     "Pending with Firm + Pending OneTrust with GEICO + Under Review."),
    ("F13", "Firms Still Needing Cyber Assessment", f'=COUNTIF({CS},"No Assessment on File")', "E3E3E3",
     "No tracker row, or tracker status = No Assessment on File."),
    ("B18", "Fully Onboarded – All Time (incl. Cyber)", f'=COUNTIF({FO},"Yes")', "D7F2E6",
     "Ignores the date window."),
    ("F18", "Needs Follow-Up (Rejected / Declined)",
     f'=COUNTIF({CS},"Rejected")+COUNTIF({CS},"Firm Declined Assessment")', "FFC7CE",
     "Not counted in 'Still Needing Cyber' – these firms need a decision or re-assessment."),
]
for anchor, title, formula, color, note in cards:
    col = anchor[0]; r0 = int(anchor[1:]); col2 = chr(ord(col) + 2)
    m.merge_cells(f"{col}{r0}:{col2}{r0}"); m.merge_cells(f"{col}{r0+1}:{col2}{r0+2}"); m.merge_cells(f"{col}{r0+3}:{col2}{r0+3}")
    m[f"{col}{r0}"] = title; m[f"{col}{r0}"].font = f(11, True, LAV_D)
    m[f"{col}{r0+1}"] = formula; m[f"{col}{r0+1}"].font = f(28, True, LAV_D); m[f"{col}{r0+1}"].number_format = "#,##0"
    m[f"{col}{r0+3}"] = note; m[f"{col}{r0+3}"].font = f(8, italic=True, color="5A5470")
    for rr in range(r0, r0 + 4):
        for cc in (col, chr(ord(col) + 1), col2):
            m[f"{cc}{rr}"].fill = fill(color)
        m[f"{col}{rr}"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    m.row_dimensions[r0 + 3].height = 24
m["F9"].value  # keep
m.merge_cells("F12:H12")
m["F12"] = '="Window: "&TEXT($C$5,"mm/dd/yyyy")&" – "&IF(ISNUMBER($C$6),TEXT($C$6,"mm/dd/yyyy"),"present")'
m["F12"].font = f(8, italic=True, color="5A5470"); m["F12"].alignment = Alignment(horizontal="center")

# breakdown tables
def table(top, left, title, labels, count_rng, color):
    lc, cc, pc = left, chr(ord(left) + 1), chr(ord(left) + 2)
    m.merge_cells(f"{lc}{top}:{pc}{top}"); m[f"{lc}{top}"] = title; m[f"{lc}{top}"].font = f(12, True, LAV_D)
    for x in (lc, cc, pc): m[f"{x}{top}"].fill = fill(color)
    for x, h in zip((lc, cc, pc), ("Status", "Count", "% of Firms")):
        c = m[f"{x}{top+1}"]; c.value = h; c.font = f(10, True, LAV_D); c.fill = fill(LAV); c.border = BOX
        c.alignment = Alignment(horizontal="center")
    for i, lab in enumerate(labels):
        r = top + 2 + i
        m[f"{lc}{r}"] = lab; m[f"{cc}{r}"] = f'=COUNTIF({count_rng},${lc}{r})'
        m[f"{pc}{r}"] = f'=IF($B$9=0,0,{cc}{r}/$B$9)'; m[f"{pc}{r}"].number_format = "0.0%"
        for x in (lc, cc, pc):
            m[f"{x}{r}"].border = BOX; m[f"{x}{r}"].font = f(10)
        m[f"{cc}{r}"].alignment = Alignment(horizontal="center"); m[f"{pc}{r}"].alignment = Alignment(horizontal="center")
    r = top + 2 + len(labels)
    m[f"{lc}{r}"] = "Total"; m[f"{cc}{r}"] = f"=SUM({cc}{top+2}:{cc}{r-1})"
    m[f"{pc}{r}"] = f'=IF($B$9=0,0,{cc}{r}/$B$9)'; m[f"{pc}{r}"].number_format = "0.0%"
    for x in (lc, cc, pc):
        m[f"{x}{r}"].font = f(10, True, LAV_D); m[f"{x}{r}"].fill = fill(LAV); m[f"{x}{r}"].border = BOX
    m[f"{cc}{r}"].alignment = Alignment(horizontal="center"); m[f"{pc}{r}"].alignment = Alignment(horizontal="center")
    return top + 2, top + 1 + len(labels)

c1, c2 = table(24, "B", "Cyber Assessment Status – Count", [c[0] for c in CYBER], CS, PEACH)
for i, (lab, bg, fg) in enumerate(CYBER):
    m[f"B{c1+i}"].fill = fill(bg); m[f"B{c1+i}"].font = Font(name=FONT, color=fg, bold=True)
o1, o2 = table(24, "F", "Onboarding Status – Count", ONBOARD, OS, BLUE)
blank_r = o2 + 3
m[f"F{blank_r}"] = "Onboarding Status left blank"; m[f"G{blank_r}"] = f'=COUNTIF({FN},"?*")-SUM(G{o1}:G{o2})'
m[f"F{blank_r}"].font = f(9, italic=True, color="6B6385"); m[f"G{blank_r}"].font = f(9, italic=True, color="6B6385")
m[f"G{blank_r}"].alignment = Alignment(horizontal="center")

ch = BarChart(); ch.type = "bar"; ch.style = 2
ch.title = "Firms by Cyber Assessment Status"; ch.y_axis.title = None; ch.x_axis.title = None
ch.add_data(Reference(m, min_col=3, min_row=c1, max_row=c2), titles_from_data=False)
ch.set_categories(Reference(m, min_col=2, min_row=c1, max_row=c2))
ch.legend = None; ch.height = 8; ch.width = 18; ch.gapWidth = 60
ch.x_axis.scaling.orientation = "maxMin"; ch.x_axis.delete = False; ch.y_axis.delete = False
ser = ch.series[0]
for i, (lab, bg, fg) in enumerate(CYBER):
    pt = DataPoint(idx=i); pt.graphicalProperties.solidFill = bg if lab != "Rejected" else "9C0006"
    pt.graphicalProperties.line.solidFill = "8C84A8"; ser.dPt.append(pt)
m.add_chart(ch, f"B{c2+4}")

# =====================================================================
# How To Use
# =====================================================================
h = ws_h
h.column_dimensions["A"].width = 2; h.column_dimensions["B"].width = 30; h.column_dimensions["C"].width = 95
banner(h, "B2:C2", "How To Use This Workbook", color=PINK)
rows = [
    ("Tabs", None),
    ("Firm Search", "Type anything about a firm in the yellow box. Up to 20 matches list on the left; enter a result # in 'Show result #' to see the full profile. Click a firm name to jump to its Directory row."),
    ("Metrics Dashboard", "Read-only counts. Change the yellow Start / End dates to set the 'Fully Onboarded Since' window."),
    ("Firm Directory", "Master list – one row per firm. Fill the yellow-header columns. Mint-header columns calculate themselves."),
    ("Cyber Assessment Tracker", "One row per firm. Enter the Firm ID, pick the status (colour-coded), and fill the dates."),
    ("Lists", "Dropdown sources (states/provinces, statuses, firm types, search suffixes). Edit to change dropdown choices."),
    ("Colour legend", None),
    ("Yellow cell / header", "You type here."),
    ("Mint header / pale-green cell", "Formula – do not type over. If you accidentally do, copy the formula down from the row above."),
    ("Rules & definitions", None),
    ("Firm ID", "Required, unique (e.g. F-0001). It links the Directory and the Cyber Tracker."),
    ("Fully Onboarded (incl. Cyber)", "Yes when Onboarding Status = 'Onboarding Complete' AND Cyber Status = 'Completed'. Fully Onboarded Date = the later of the two completion dates."),
    ("In Cyber Process", "Pending with Firm, Pending OneTrust with GEICO, or Under Review."),
    ("Still Needs Cyber", "Cyber status = No Assessment on File (includes firms with no tracker row). Rejected and Firm Declined are counted separately as 'Needs Follow-Up'."),
    ("Search matching", "Case, punctuation, spaces, '&' vs 'and', a leading 'The', and a trailing entity suffix (LLP, LLC, PC, PA, PLLC, Ltd, Inc, Law Firm, Law Group…) are ignored. Searches Firm ID, name, AKA, type, practice areas, Tax ID, vendor #, city, state, ZIP, phone, partner, billing contact, emails and relationship owner."),
    ("Capacity", f"Formulas are pre-filled for {LAST-FIRST+1} firms (rows {FIRST}–{LAST}). Sort/filter freely using the header filter arrows; don't insert columns."),
    ("Example rows", "Row 5 on the Directory and Tracker (EX-0001) shows the expected format. Delete the contents of both rows before entering real data (they are counted in the metrics while present)."),
]
r = 4
for k, v in rows:
    if v is None:
        h.merge_cells(f"B{r}:C{r}"); h[f"B{r}"] = k; h[f"B{r}"].font = f(12, True, LAV_D)
        h[f"B{r}"].fill = fill(LAV); h[f"C{r}"].fill = fill(LAV)
    else:
        h[f"B{r}"] = k; h[f"C{r}"] = v; h[f"B{r}"].font = f(10, True, "5A5470"); h[f"C{r}"].font = f(10)
        h[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top"); h[f"B{r}"].alignment = Alignment(vertical="top")
        for x in "BC": h[f"{x}{r}"].border = BOX
        if k.startswith("Yellow"): h[f"B{r}"].fill = fill(BUTTER)
        if k.startswith("Mint"): h[f"B{r}"].fill = fill(MINT)
    r += 1

wb.active = 0
wb.save(OUT)
print("saved", OUT)
