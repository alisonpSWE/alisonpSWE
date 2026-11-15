# gera o dark_mode.svg e o light_mode.svg do readme
# a action roda isso todo dia pra atualizar o uptime, mas da pra rodar local:
#   python card.py

import datetime
import os
from xml.sax.saxutils import escape

HOST = "alison@github"
BIRTHDAY = datetime.date(2004, 6, 5)

COLS = 80     # tamanho de cada linha em caracteres
CHAR_W = 9.6  # 16px * 0.6
LINE_H = 20

themes = {
    "dark_mode.svg": {
        "bg": "#161b22", "border": "#30363d", "text": "#c9d1d9", "key": "#ffa657",
        "value": "#a5d6ff", "cc": "#616e7f", "prompt": "#7ee787",
    },
    "light_mode.svg": {
        "bg": "#f6f8fa", "border": "#d0d7de", "text": "#24292f", "key": "#953800",
        "value": "#0a3069", "cc": "#c2cfde", "prompt": "#116329",
    },
}


def card():
    return [
        prompt("neofetch --off"),
        title(HOST),
        line("OS", "Windows 11, Arch Linux, Debian"),
        line("Uptime", age(BIRTHDAY)),
        line("Host", "Federal University of Ceará (UFC)"),
        line("Kernel", "Computer Science, final year"),
        line("BIOS", "Computer Networks Technician (EEEP)"),
        dot(),
        line("Languages.Programming", "C#, TypeScript, Python, C, Rust, Java"),
        line("Languages.Real", "Portuguese (native), English (advanced)"),
        line("Stack.Web", "ASP.NET Core, React, Next.js, Node.js"),
        line("Stack.Tools", "PostgreSQL, Bruno, Docker, Git, Wireshark"),
        dot(),
        line("Interests", "Open source, AI agents & LLMs, Data Science, Networking"),
        line("Hobbies.Software", "Game modding, Game dev, Language learning"),
        line("Hobbies.Hardware", "Networks, Arduino projects (ESP32)"),
        [],
        title("Highlights", "- "),
        line("Award", "1st place, UFC Crateús Hackathon 2023"),
        line("Volunteer", "FIT (Fórum de Inovação e Tecnologia), 2024-2026"),
        [],
        title("Contact", "- "),
        line("Email.Personal", "alisonp.dev@gmail.com"),
        line("Email.Academic", "alisonps@alu.ufc.br"),
        line("LinkedIn", "in/alisondev"),
        [],
        prompt("", cursor=True),
    ]


# ". Chave.Sub: ........ valor" sempre com o mesmo tamanho
def line(key, value):
    parts = [(". ", "cc")]
    for i, k in enumerate(key.split(".")):
        if i > 0:
            parts.append((".", None))
        parts.append((k, "key"))
    parts.append((":", None))

    used = sum(len(t) for t, _ in parts) + len(value)
    dots = COLS - used - 2
    if dots < 1:
        raise ValueError(f"linha muito grande: {key}")
    return parts + [(" " + "." * dots + " ", "cc"), (value, "value")]


def title(name, lead=""):
    return [(lead + name, None), (" -" + "—" * (COLS - len(lead + name) - 5) + "-—-", None)]


def dot():
    return [(". ", "cc")]


def prompt(cmd, cursor=False):
    parts = [(HOST, "prompt"), (":", None), ("~", "value"), ("$ " + cmd, None)]
    if cursor:
        parts.append(("█", "cursor"))
    return parts


def age(since):
    today = datetime.date.today()
    y = today.year - since.year
    m = today.month - since.month
    d = today.day - since.day
    if d < 0:
        m -= 1
        d += (today.replace(day=1) - datetime.timedelta(days=1)).day
    if m < 0:
        y -= 1
        m += 12
    s = lambda n: "" if n == 1 else "s"
    return f"{y} year{s(y)}, {m} month{s(m)}, {d} day{s(d)}"


def svg(rows, c):
    w = round(48 + COLS * CHAR_W)
    h = 34 + (len(rows) - 1) * LINE_H + 20
    out = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        "font-family=\"MonoFit, Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', monospace\" "
        'font-size="16px" xml:space="preserve">',
        "<style>",
        # consolas e mais estreita que as outras fontes mono, isso deixa todas do mesmo tamanho
        "@font-face { font-family: 'MonoFit'; src: local('Consolas'); size-adjust: 109%; }",
        f"text {{ fill: {c['text']}; white-space: pre; }}",
        *[f".{k} {{ fill: {c[k]}; }}" for k in ("key", "value", "cc", "prompt")],
        f".cursor {{ fill: {c['text']}; animation: blink 1.1s steps(1) infinite; }}",
        "@keyframes blink { 50% { opacity: 0; } }",
        "</style>",
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
    ]
    for i, row in enumerate(rows):
        if row:
            spans = "".join(escape(t) if cls is None else f'<tspan class="{cls}">{escape(t)}</tspan>'
                            for t, cls in row)
            out.append(f'<text x="24" y="{34 + i * LINE_H}">{spans}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    rows = card()
    folder = os.path.dirname(os.path.abspath(__file__))
    for name, colors in themes.items():
        with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(rows, colors))
