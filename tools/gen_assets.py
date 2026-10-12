# Генератор иллюстраций курса. Запуск: python3 tools/gen_assets.py assets
import sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]
FONT = "Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, Menlo, monospace"

def svg(w, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#4a5568"/>
  </marker>
</defs>
<rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="#ffffff"/>
<g font-family="{FONT}">
{body}
</g>
</svg>
'''

def text(x, y, s, size=13, color="#2d3748", weight="normal", anchor="start", family=None, style=""):
    fam = f' font-family="{family}"' if family else ""
    st = f' font-style="{style}"' if style else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}"{fam}{st}>{esc(s)}</text>'

def rect(x, y, w, h, fill, stroke="none", rx=10, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

def line(x1, y1, x2, y2, color="#4a5568", sw=1.6, arrow=True, dash=None):
    m = ' marker-end="url(#arr)"' if arrow else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{m}{d}/>'

def pill(x, y, w, abbr, name, color):
    s = rect(x, y, w, 28, "#ffffff", color, rx=14, sw=1.3)
    if abbr:
        s += f'<text x="{x+12}" y="{y+19}" font-size="12.5"><tspan font-weight="700" fill="{color}">{esc(abbr)}</tspan><tspan fill="#2d3748" dx="6">{esc(name)}</tspan></text>'
    else:
        s += text(x + w/2, y+19, name, 12.5, "#2d3748", anchor="middle")
    return s

# ---------------------------------------------------------------- 1. process map
def process_map():
    W, H = 1200, 520
    b = []
    b.append(text(30, 42, "Сквозной процесс SAP TM", 24, "#1a202c", "700"))
    b.append(text(30, 66, "От спроса до денег: шесть шагов и документы на каждом шаге", 14, "#4a5568"))
    stages = [
        ("Спрос", "#2b6cb0", "#ebf4ff", ["Заказ SD, поставка", "или заказ экспедитору"],
         [("OTR", "из заказа"), ("DTR", "из поставки"), ("FWO", "заказ клиента"), ("FWQ", "предложение")], "/SCMTMS/TRQ"),
        ("Единицы фрахта", "#2f855a", "#e6f6ec", ["Спрос режется", "по правилу FUBR"],
         [("FU", "единица фрахта")], "/SCMTMS/TOR"),
        ("Планирование", "#c05621", "#fff3e6", ["Cockpit планировщика,", "оптимизатор VSR"],
         [("FO", "фрахтовый заказ"), ("FB", "бронирование"), ("TU", "трейлер, вагон")], "/SCMTMS/TOR"),
        ("Перевозчик", "#b7791f", "#fefbea", ["Ручной выбор,", "автовыбор, тендер"],
         [(None, "Carrier selection"), (None, "Tendering")], "BP: перевозчик"),
        ("Исполнение", "#6b46c1", "#f3edff", ["Факты рейса", "и документы"],
         [(None, "События исполнения"), (None, "Печать и вывод (PPF)"), (None, "Отслеживание")], "узел EXECUTION"),
        ("Деньги", "#c53030", "#fdecec", ["Ставки: FA для закупки,", "FWA для продажи"],
         [(None, "Расчёт стоимости"), ("FSD", "→ MM"), ("FWSD", "→ SD")], "SFIR · CFIR"),
    ]
    x0, cw, gap = 30, 175, 20
    for i, (title, c, light, cap, pills, bo) in enumerate(stages):
        x = x0 + i * (cw + gap)
        b.append(rect(x, 146, cw, 242, light, c, rx=10, sw=1.2))
        b.append(rect(x, 90, cw, 56, c, rx=10))
        b.append(f'<rect x="{x}" y="130" width="{cw}" height="16" fill="{c}"/>')
        b.append(f'<circle cx="{x+24}" cy="118" r="13" fill="#ffffff"/>')
        b.append(text(x+24, 123, str(i+1), 14, c, "700", "middle"))
        b.append(text(x+46, 124, title, 14, "#ffffff", "700"))
        b.append(text(x+12, 172, cap[0], 12, "#4a5568"))
        b.append(text(x+12, 188, cap[1], 12, "#4a5568"))
        py = 202
        for abbr, name in pills:
            b.append(pill(x+12, py, cw-24, abbr, name, c))
            py += 36
        if title == "Единицы фрахта":
            for k, s in enumerate(["Неделимая единица:", "не разрывается", "между машинами"]):
                b.append(text(x+12, 260 + k*17, s, 12, "#2f855a", style="italic"))
        if title == "Перевозчик":
            b.append(text(x+12, 292, "Работают с FO и FB", 12, "#b7791f", style="italic"))
        b.append(rect(x+12, 352, cw-24, 26, "#ffffff", "#a0aec0", rx=6, sw=1))
        b.append(text(x+cw/2, 369, bo, 12, "#2d3748", "600", "middle", MONO))
        if i < len(stages) - 1:
            ax = x + cw + 2
            b.append(f'<path d="M{ax},108 L{ax+15},118 L{ax},128 z" fill="#a0aec0"/>')
    b.append(rect(30, 410, 1140, 40, "#f7fafc", "#cbd5e0", rx=8, sw=1))
    b.append(f'<text x="46" y="435" font-size="13.5"><tspan font-weight="700" fill="#1a202c">Мастер-данные</tspan><tspan fill="#2d3748" dx="12">Location · Transportation Zone · Transportation Lane · Means of Transport · Resource · Business Partner · соглашения FA и FWA</tspan></text>')
    b.append(rect(30, 460, 1140, 40, "#f7fafc", "#cbd5e0", rx=8, sw=1))
    b.append(f'<text x="46" y="485" font-size="13.5"><tspan font-weight="700" fill="#1a202c">Настройка (SPRO)</tspan><tspan fill="#2d3748" dx="12">тип каждого документа задаёт его поведение: тип FU, тип FO, тип FWO, профили планирования, условия</tspan></text>')
    return svg(W, H, "\n".join(b), "Сквозной процесс SAP TM")

# ---------------------------------------------------------------- 2. BOPF anatomy
def bopf_anatomy():
    W, H = 1200, 600
    b = []
    b.append(text(30, 42, "Анатомия бизнес-объекта BOPF", 24, "#1a202c", "700"))
    b.append(text(30, 66, "Вы описываете модель и пишете маленькие обработчики. Буфер, транзакции и вызовы берёт на себя фреймворк", 14, "#4a5568"))
    # consumers
    b.append(text(30, 104, "ПОТРЕБИТЕЛИ", 12, "#718096", "700"))
    cons = ["UI: FPM / FBI, Fiori", "Отчёты, фоновые задания", "Интерфейсы: SOA, IDoc", "Другие бизнес-объекты"]
    for k, s in enumerate(cons):
        y = 118 + k*66
        b.append(rect(30, y, 200, 50, "#f7fafc", "#a0aec0", rx=8, sw=1.2))
        b.append(text(130, y+30, s, 13, "#2d3748", "600", "middle"))
        b.append(line(232, y+25, 266, y+25))
    # service manager
    b.append(rect(270, 112, 130, 266, "#2b6cb0", rx=10))
    b.append(text(335, 150, "Service", 16, "#ffffff", "700", "middle"))
    b.append(text(335, 170, "Manager", 16, "#ffffff", "700", "middle"))
    b.append(text(335, 190, "фасад BO", 12, "#d6e6f8", anchor="middle", style="italic"))
    for k, s in enumerate(["query", "retrieve", "retrieve_by_assoc", "modify", "do_action"]):
        b.append(text(335, 228 + k*28, s, 11, "#ffffff", anchor="middle", family=MONO))
    b.append(line(402, 245, 426, 245))
    # BO container
    b.append(rect(430, 96, 740, 300, "#f7fafc", "#2d3748", rx=12, sw=1.4, dash="6 4"))
    b.append(f'<text x="450" y="122" font-size="15"><tspan font-weight="700" fill="#1a202c">Бизнес-объект</tspan><tspan dx="8" fill="#2d3748" font-family="{MONO}">/SCMTMS/TOR</tspan><tspan dx="8" fill="#718096" font-style="italic">модель</tspan></text>')
    # node tree
    b.append(rect(450, 138, 290, 58, "#ffffff", "#2b6cb0", rx=8, sw=1.6))
    b.append(text(464, 162, "ROOT", 15, "#2b6cb0", "700", family=MONO))
    b.append(text(464, 184, "KEY · PARENT_KEY · ROOT_KEY + поля", 12, "#4a5568"))
    kids = [("ITEM_TR", "позиции"), ("STOP", "точки маршрута"), ("EXECUTION", "события")]
    for k, (n, d) in enumerate(kids):
        y = 212 + k*54
        b.append(f'<path d="M474,196 L474,{y+22} L506,{y+22}" fill="none" stroke="#2b6cb0" stroke-width="1.4"/>')
        b.append(rect(508, y, 232, 44, "#ffffff", "#2b6cb0", rx=8, sw=1.2))
        b.append(f'<text x="522" y="{y+27}" font-size="13"><tspan font-weight="700" fill="#2b6cb0" font-family="{MONO}">{n}</tspan><tspan dx="8" fill="#4a5568">{esc(d)}</tspan></text>')
    b.append(text(482, 386, "линии: ассоциации между узлами", 11.5, "#718096", style="italic"))
    # handlers
    b.append(text(770, 150, "НАВЕШАНО НА УЗЛЫ", 12, "#718096", "700"))
    hs = [
        ("D", "Determination", "вычисляет и меняет данные", "#2f855a"),
        ("V", "Validation", "проверяет, может запретить", "#c53030"),
        ("A", "Action", "операция, вызывается извне", "#c05621"),
        ("Q", "Query", "поиск, возвращает ключи", "#6b46c1"),
        ("K", "Alternative key", "номер документа → GUID", "#b7791f"),
    ]
    for k, (ic, n, d, c) in enumerate(hs):
        y = 162 + k*45
        b.append(rect(770, y, 380, 38, "#ffffff", c, rx=8, sw=1.2))
        b.append(f'<circle cx="790" cy="{y+19}" r="11" fill="{c}"/>')
        b.append(text(790, y+24, ic, 12, "#ffffff", "700", "middle"))
        b.append(f'<text x="810" y="{y+24}" font-size="13"><tspan font-weight="700" fill="{c}">{esc(n)}</tspan><tspan dx="8" fill="#4a5568">{esc(d)}</tspan></text>')
    b.append(f'<path d="M760,170 L752,170 L752,375 L760,375" fill="none" stroke="#a0aec0" stroke-width="1.4"/>')
    b.append(line(752, 272, 744, 272, "#a0aec0", 1.4))
    # runtime row
    b.append(text(30, 432, "РАНТАЙМ", 12, "#718096", "700"))
    b.append(rect(30, 444, 330, 62, "#edf2f7", "#4a5568", rx=10, sw=1.2))
    b.append(text(195, 470, "Transaction Manager", 15, "#1a202c", "700", "middle"))
    b.append(text(195, 492, "SAVE  ·  CLEANUP", 12.5, "#2d3748", anchor="middle", family=MONO))
    b.append(rect(430, 444, 330, 62, "#fffbea", "#b7791f", rx=10, sw=1.2))
    b.append(text(595, 470, "Буфер BO", 15, "#1a202c", "700", "middle"))
    b.append(text(595, 492, "изменения в памяти до сохранения", 12.5, "#4a5568", anchor="middle"))
    b.append(line(362, 475, 426, 475))
    b.append(line(595, 398, 595, 440))
    b.append(text(603, 424, "MODIFY пишет сюда", 11.5, "#718096", style="italic"))
    # db cylinder
    cx, cy, cw = 905, 448, 260
    b.append(f'<path d="M{cx},{cy+10} a{cw/2},10 0 0,0 {cw},0 v44 a{cw/2},10 0 0,1 {-cw},0 z" fill="#edf2f7" stroke="#4a5568" stroke-width="1.2"/>')
    b.append(f'<ellipse cx="{cx+cw/2}" cy="{cy+10}" rx="{cw/2}" ry="10" fill="#f7fafc" stroke="#4a5568" stroke-width="1.2"/>')
    b.append(text(cx+cw/2, cy+40, "Таблицы БД", 14, "#1a202c", "700", "middle"))
    b.append(text(cx+cw/2, cy+58, "/SCMTMS/D_TOR*", 12, "#2d3748", anchor="middle", family=MONO))
    b.append(line(762, 475, 900, 475))
    b.append(text(830, 467, "при SAVE", 11.5, "#718096", anchor="middle", style="italic"))
    # constants strip
    b.append(rect(30, 534, 1140, 40, "#ebf4ff", "#2b6cb0", rx=8, sw=1))
    b.append(f'<text x="46" y="559" font-size="13.5"><tspan font-weight="700" fill="#1a202c">Интерфейс констант</tspan><tspan dx="10" fill="#2d3748" font-family="{MONO}">/SCMTMS/IF_TOR_C</tspan><tspan dx="10" fill="#2d3748">переводит имена узлов, связей, действий и запросов в GUID. Без него код BOPF не пишется</tspan></text>')
    return svg(W, H, "\n".join(b), "Анатомия бизнес-объекта BOPF")

# ---------------------------------------------------------------- 3. TOR family
def tor_family():
    W, H = 1200, 480
    b = []
    b.append(text(30, 42, "Семейства бизнес-объектов TM", 24, "#1a202c", "700"))
    b.append(text(30, 66, "Двенадцать документов укладываются в четыре основных бизнес-объекта", 14, "#4a5568"))

    def group(x, w, c, light, bo, sub):
        b.append(rect(x, 90, w, 300, light, c, rx=12, sw=1.5))
        b.append(text(x+18, 120, bo, 17, c, "700", family=MONO))
        b.append(text(x+18, 142, sub, 13, "#4a5568", style="italic"))

    def card(x, y, w, abbr, name, c):
        b.append(rect(x, y, w, 40, "#ffffff", c, rx=8, sw=1.2))
        b.append(f'<text x="{x+14}" y="{y+25}" font-size="13.5"><tspan font-weight="700" fill="{c}">{esc(abbr)}</tspan><tspan dx="10" fill="#2d3748">{esc(name)}</tspan></text>')

    c1, l1 = "#2b6cb0", "#ebf4ff"
    group(30, 330, c1, l1, "/SCMTMS/TRQ", "Спрос: что везти")
    for k, (a, n) in enumerate([("FWQ", "предложение клиенту"), ("FWO", "заказ клиента экспедитору"), ("OTR", "из заказа SD или MM"), ("DTR", "из поставки")]):
        card(48, 158 + k*48, 294, a, n, c1)
    b.append(text(48, 372, "Различаются категорией и типом TRQ", 12, c1, style="italic"))

    c2, l2 = "#c05621", "#fff3e6"
    group(430, 400, c2, l2, "/SCMTMS/TOR", "Исполнение: как везти")
    for k, (a, n) in enumerate([("FU", "единица фрахта"), ("FO", "фрахтовый заказ"), ("FB", "бронирование"), ("TU", "трейлер, вагон")]):
        card(448 + (k % 2)*186, 158 + (k // 2)*48, 178, a, n, c2)
    b.append(rect(448, 262, 364, 82, "#ffffff", "#a0aec0", rx=8, sw=1, dash="4 3"))
    b.append(text(462, 284, "Одна модель, общие узлы:", 12.5, "#1a202c", "700"))
    b.append(text(462, 304, "ROOT · ITEM_TR · STOP · EXECUTION", 12, "#2d3748", family=MONO))
    b.append(text(462, 324, "+ стоимость (делегированный узел)", 12, "#2d3748"))
    b.append(text(448, 372, "Различаются полями TOR_CAT и TOR_TYPE", 12, c2, "700", style="italic"))

    c3, l3 = "#c53030", "#fdecec"
    group(900, 270, c3, l3, "Расчёты", "Деньги")
    b.append(rect(918, 158, 234, 64, "#ffffff", c3, rx=8, sw=1.2))
    b.append(text(932, 182, "/SCMTMS/SFIR", 13, c3, "700", family=MONO))
    b.append(text(932, 204, "FSD: перевозчику, → MM", 12.5, "#2d3748"))
    b.append(rect(918, 236, 234, 64, "#ffffff", c3, rx=8, sw=1.2))
    b.append(text(932, 260, "/SCMTMS/CFIR", 13, c3, "700", family=MONO))
    b.append(text(932, 282, "FWSD: клиенту, → SD", 12.5, "#2d3748"))

    b.append(line(362, 200, 426, 200, "#4a5568", 2))
    b.append(text(394, 190, "FUBR", 11.5, "#4a5568", "700", "middle"))
    b.append(line(832, 190, 896, 190, "#4a5568", 2))
    b.append(text(864, 180, "FO, FB", 11.5, "#4a5568", "700", "middle"))
    b.append(f'<path d="M195,392 L195,440 L1035,440 L1035,398" fill="none" stroke="#4a5568" stroke-width="2" marker-end="url(#arr)"/>')
    b.append(rect(520, 428, 260, 24, "#ffffff", rx=6))
    b.append(text(650, 445, "FWO → FWSD: счёт клиенту экспедитора", 12, "#4a5568", "700", "middle"))
    return svg(W, H, "\n".join(b), "Семейства бизнес-объектов TM")

open(f"{OUT}/tm-process-map.svg", "w").write(process_map())
open(f"{OUT}/bopf-anatomy.svg", "w").write(bopf_anatomy())
open(f"{OUT}/tor-family.svg", "w").write(tor_family())
print("ok")
