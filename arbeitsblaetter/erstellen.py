#!/usr/bin/env python3
"""Erzeugt die Silben-Arbeitsblätter (HTML) für die 1. Klasse.
Aufruf: python3 erstellen.py  -> silben-arbeitsblaetter.html  (PDF: node pdf.js)
Silbentrennung mit "-", Farben wie in der App (blau/rot, Selbstlaute gelb)."""
import random, re, html
from pathlib import Path

random.seed(7)
VOW = re.compile(r'(äu|au|ei|eu|ie|[aeiouäöü])', re.I)

def vow(s):  # Selbstlaute gelb hinterlegen
    return VOW.sub(lambda m: f'<span class="v">{m.group(0)}</span>', html.escape(s))

def word(h, arcs=True, colors=True, vowels=True, start=0):
    parts = h.split('-')
    cls = ' '.join(c for c, on in [('arcs', arcs), ('colors', colors), ('vowels', vowels)] if on)
    inner = ''.join(f'<span class="syl c{(i + start) % 2}">{vow(p) if vowels else html.escape(p)}</span>'
                    for i, p in enumerate(parts))
    return f'<span class="word {cls}">{inner}</span>'

def sentence(text):  # Wörter mit Leerzeichen, Silben mit "-"
    return ' '.join(word(w) for w in text.split())

def page(title, task, body, icon):
    return f'''<section class="page">
  <header><div class="name">Name: <span class="ln"></span></div><div class="name">Datum: <span class="ln short"></span></div></header>
  <h1><span class="ico">{icon}</span>{title}</h1>
  <p class="task">{task}</p>
  {body}
</section>'''

pages = []

# 1 Silben schwingen: nur Bilder, Bögen selbst malen
items = [('🐭', 1), ('☀️', 2), ('🍌', 3), ('🥚', 1), ('🚗', 2), ('🍅', 3),
         ('🐶', 1), ('🌹', 2), ('🚀', 3), ('🐟', 1), ('🦔', 2), ('🍈', 3)]
random.shuffle(items)
cells = ''.join(f'<div class="cell"><div class="pic">{e}</div><div class="arcbox"></div></div>' for e, _ in items)
pages.append(page('Silben schwingen',
    'Sprich das Wort laut. Schwinge und klatsche die Silben. Male für jede Silbe einen Bogen ◡ in das Kästchen.',
    f'''<div class="example"><div class="pic sm">🦁</div><div>Lö – we&nbsp; 👏👏&nbsp; → </div>
    <svg width="120" height="34"><path d="M8 6 Q30 34 52 6" class="a0"/><path d="M66 6 Q88 34 110 6" class="a1"/></svg></div>
    <div class="grid g3">{cells}</div>''', '👏'))

# 2 Wie viele Silben?
items = [('🌙', 'Mond', 1), ('🏠', 'Haus', 1), ('👃', 'Na-se', 2), ('👖', 'Ho-se', 2),
         ('🦁', 'Lö-we', 2), ('🐯', 'Ti-ger', 2), ('🍍', 'A-na-nas', 3), ('🐊', 'Kro-ko-dil', 3),
         ('🐘', 'E-le-fant', 3), ('⚽', 'Ball', 1), ('🛋️', 'So-fa', 2), ('👵', 'O-ma', 2)]
random.shuffle(items)
cells = ''.join(f'''<div class="cell row"><div class="pic">{e}</div>
  <div class="count"><span>1</span><span>2</span><span>3</span></div></div>''' for e, _, _ in items)
pages.append(page('Wie viele Silben?',
    'Sprich das Wort und klatsche. Wie viele Silben hörst du? Kreise die richtige Zahl ein.',
    f'<div class="grid g2">{cells}</div>', '🔢'))
sol_count = ', '.join(f'{h.replace("-", "")} {n}' for _, h, n in items)

# 3 Silbenteppich
cons = ['M', 'L', 'S', 'N', 'R', 'T', 'H', 'F']
vs = ['a', 'e', 'i', 'o', 'u']
rows = ''.join('<tr>' + ''.join(f'<td>{word(c + v, arcs=False, start=(r + i))}</td>' for i, v in enumerate(vs)) + '</tr>'
               for r, c in enumerate(cons))
pages.append(page('Silbenteppich',
    'Lies jede Silbe laut. Male das Feld danach mit einem Buntstift leicht an. Lies erst quer ➡, dann von oben nach unten ⬇.',
    f'<table class="teppich">{rows}</table>', '📖'))

# 4 Silbenbögen malen
ws = [('Ma-ma', '👩'), ('O-ma', '👵'), ('O-pa', '👴'), ('Ro-se', '🌹'), ('Na-se', '👃'), ('Ho-se', '👖'),
      ('So-fa', '🛋️'), ('Lu-pe', '🔍'), ('Au-to', '🚗'), ('I-gel', '🦔'), ('To-ma-te', '🍅'), ('Ba-na-ne', '🍌')]
cells = ''.join(f'''<div class="cell row"><div class="pic sm">{e}</div>
  <div class="plain">{h.replace("-", "")}</div></div>''' for h, e in ws[1:])
pages.append(page('Silbenbögen malen',
    'Lies das Wort und schwinge mit. Male die Silbenbögen unter das Wort. Male dann den 1. Bogen blau und den 2. Bogen rot.',
    f'''<div class="example"><div class="pic sm">👩</div><div class="big">{word("Ma-ma", vowels=False)}</div><div class="hint">So geht es!</div></div>
    <div class="grid g2 tall">{cells}</div>''', '✏️'))

# 5 Silbe + Silbe = Wort, mit Bild verbinden
ws = [('Ro-se', '🌹'), ('O-ma', '👵'), ('Lu-pe', '🔍'), ('So-fa', '🛋️'), ('Au-to', '🚗'), ('Ti-ger', '🐯'), ('Na-se', '👃')]
pics = ws[:]; random.shuffle(pics)
rows = ''.join(f'''<div class="link">
  <div class="sum">{word(h.split("-")[0], arcs=True)} <b>+</b> {word(h.split("-")[1], arcs=True, start=1)} <b>=</b></div>
  <div class="wline"></div><div class="dot">●</div><div class="gap"></div><div class="dot">●</div><div class="pic sm">{p[1]}</div></div>'''
  for (h, _), p in zip(ws, pics))
pages.append(page('Silbe + Silbe = Wort',
    'Lies beide Silben. Schwinge sie zusammen. Schreibe das Wort auf die Linie. Verbinde es mit dem passenden Bild.',
    f'<div class="links">{rows}</div>', '➕'))

# 6 Welche Silbe fehlt?
ws = [('Ro-se', '🌹', 1), ('O-ma', '👵', 1), ('Au-to', '🚗', 1), ('So-fa', '🛋️', 1),
      ('Na-se', '👃', 0), ('I-gel', '🦔', 1), ('Ti-ger', '🐯', 0), ('Me-lo-ne', '🍈', 2)]
bank = sorted({h.split('-')[m] for h, _, m in ws}, key=str.lower)
def gapword(h, m):
    out = []
    for i, s in enumerate(h.split('-')):
        out.append(f'<span class="slot c{i % 2}"></span>' if i == m else word(s, start=i))
    return ' '.join(out)
cells = ''.join(f'<div class="cell row"><div class="pic sm">{e}</div><div class="gw">{gapword(h, m)}</div></div>' for h, e, m in ws)
pages.append(page('Welche Silbe fehlt?',
    'Schau das Bild an und sprich das Wort. Welche Silbe fehlt? Schreibe sie in das Kästchen. Jede Silbe aus dem Kasten passt einmal.',
    f'''<div class="bank">{" ".join(word(b, arcs=False) for b in bank)}</div>
    <div class="grid g2 tall">{cells}</div>''', '🧩'))

# 7 Silben-Puzzle zum Ausschneiden
ws = [('Lö-we', '🦁'), ('Ho-se', '👖'), ('Ba-na-ne', '🍌'), ('Ra-ke-te', '🚀'), ('Ma-ma', '👩'), ('To-ma-te', '🍅')]
rows = ''.join(f'''<div class="cell row puz"><div class="pic sm">{e}</div>
  <div class="slots">{"".join(f'<span class="pslot c{i % 2}"></span>' for i in range(len(h.split("-"))))}</div></div>''' for h, e in ws)
cards = [(s, i) for h, _ in ws for i, s in enumerate(h.split('-'))]
random.shuffle(cards)
cardhtml = ''.join(f'<div class="card">{word(s, arcs=False, start=i)}</div>' for s, i in cards)
pages.append(page('Silben-Puzzle',
    'Schneide die Silbenkarten unten aus. Lege sie zu den Bildern. Lies das Wort. Stimmt es? Dann klebe die Karten auf.',
    f'''<div class="grid g2 puzz">{rows}</div>
    <div class="cut">✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -</div>
    <div class="cards">{cardhtml}</div>''', '✂️'))

# 8 Silben-Detektiv
targets = [('Ma', ['Ma', 'Mo', 'Na', 'Ma', 'Mi', 'Ma', 'La', 'Mu', 'Ma', 'Am']),
           ('Lo', ['Lo', 'Lu', 'Ol', 'Lo', 'Li', 'Ro', 'Lo', 'Le', 'Lo', 'Lo']),
           ('Si', ['Su', 'Si', 'Sa', 'Is', 'Si', 'Si', 'Se', 'Ni', 'Si', 'So']),
           ('Ne', ['Ne', 'Me', 'Na', 'Ne', 'En', 'Ne', 'Nu', 'Re', 'Ne', 'Ni']),
           ('Ru', ['Ra', 'Ru', 'Ur', 'Ru', 'Lu', 'Ru', 'Re', 'Ru', 'Ro', 'Ru'])]
rows = ''.join(f'''<div class="det"><div class="tgt">{word(t, arcs=False)}</div>
  <div class="seq">{"".join(f'<span>{word(s, arcs=False, colors=False, vowels=False)}</span>' for s in seq)}</div></div>''' for t, seq in targets)
pages.append(page('Silben-Detektiv',
    'Lies die Silbe vorne im Kasten. Finde sie in der Reihe. Kreise jedes Mal ein, wenn du sie findest. Wie oft? Schreibe die Zahl ans Ende.',
    f'<div class="dets">{rows}</div>', '🔍'))
sol_det = ', '.join(f'{t} {seq.count(t)}×' for t, seq in targets)

# 9 Lesen und malen
ss = ['Ei-ne Ro-se', 'Ein Au-to', 'Ei-ne Ba-na-ne', 'Ei-ne Son-ne', 'Ein I-gel', 'Ei-ne To-ma-te']
cells = ''.join(f'<div class="draw"><div class="sent">{sentence(s)}</div><div class="frame"></div></div>' for s in ss)
pages.append(page('Lesen und malen',
    'Lies Silbe für Silbe. Schwinge mit. Male ein Bild dazu.',
    f'<div class="grid g2">{cells}</div>', '🎨'))

# 10 Hinweise + Lösungen
pages.append(f'''<section class="page info">
  <h1><span class="ico">💡</span>Hinweise für Erwachsene</h1>
  <ul>
    <li><b>Reihenfolge:</b> Die Blätter werden langsam schwerer: erst nur hören und klatschen (1–2), dann Silben lesen (3), dann Wörter (4–7), dann kleine Sätze (9). Ein bis zwei Blätter am Tag reichen.</li>
    <li><b>Silben schwingen:</b> Wort laut sprechen und bei jeder Silbe mit dem Arm einen Bogen machen oder einen Schritt gehen. Das hilft mehr als nur Klatschen.</li>
    <li><b>Farben:</b> 1. Silbe blau, 2. Silbe rot, 3. Silbe wieder blau – wie in der App. Die Selbstlaute (a, e, i, o, u, au, ei) sind gelb hinterlegt: Jede Silbe hat einen.</li>
    <li><b>Buchstaben:</b> Die Wörter nutzen vor allem M, L, S, N, R, T, O, A, I, E, U. Kennt Ihr Kind einen Buchstaben noch nicht, lesen Sie ihn vor – das ist kein Fehler.</li>
    <li><b>Lob statt Druck:</b> Lieber langsam und richtig. Gesprochene Laute ziehen („Mmmm-aaaa“ → „Ma“) hilft beim Zusammenschleifen.</li>
  </ul>
  <h2>Lösungen</h2>
  <p><b>Blatt 1 (Bögen):</b> Maus 1, Ei 1, Hund 1, Fisch 1 · Sonne 2, Auto 2, Rose 2, Igel 2 · Banane 3, Tomate 3, Rakete 3, Melone 3</p>
  <p><b>Blatt 2 (Zahl):</b> {sol_count}</p>
  <p><b>Blatt 6 (fehlende Silbe):</b> Ro-<u>se</u>, O-<u>ma</u>, Au-<u>to</u>, So-<u>fa</u>, <u>Na</u>-se, I-<u>gel</u>, <u>Ti</u>-ger, Me-lo-<u>ne</u></p>
  <p><b>Blatt 8 (Detektiv):</b> {sol_det}</p>
</section>''')

css = Path(__file__).with_name('stil.css').read_text()
out = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Silben-Arbeitsblätter</title>
<link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{"".join(pages)}</body></html>'''
Path(__file__).with_name('silben-arbeitsblaetter.html').write_text(out)
print('ok', len(pages), 'Seiten')
