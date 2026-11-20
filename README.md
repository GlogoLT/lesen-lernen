# Lesen lernen

Tablet-App zum **Silbenlesen** und **Wörterbauen** mit Spracheingabe. Läuft komplett auf dem Tablet:
kein PC, kein Internet und kein Server nötig, sobald sie einmal installiert ist. Die Spracherkennung
(Vosk, deutsches Modell, 46 MB) läuft im Browser. Aufnahmen verlassen das Tablet nicht.

## Einmalig aufs Tablet bringen

Der Browser muss die App einmal über eine „sichere“ Adresse öffnen (https oder localhost), sonst gibt es
kein Mikrofon und keine Installation. Danach ist alles auf dem Tablet gespeichert.

### Weg A: per USB-Kabel (ohne Internet, nur Android)

1. Am Tablet: Einstellungen → Über das Tablet → 7× auf „Build-Nummer“ tippen → Entwickleroptionen →
   **USB-Debugging** einschalten.
2. Tablet per USB an den PC, Nachfrage „USB-Debugging zulassen?“ am Tablet bestätigen.
3. Am PC:
   ```bash
   ~/lesen-app/start.sh
   ```
   und in einem zweiten Terminal:
   ```bash
   adb reverse tcp:8790 tcp:8790
   ```
4. Am Tablet in Chrome oder Brave `http://localhost:8790/` öffnen und warten, bis „Spracherkennung
   wird geladen“ verschwindet.
5. Browser-Menü (⋮) → **App installieren** bzw. **Zum Startbildschirm hinzufügen**.
6. Fertig. Kabel ab, Server am PC mit Strg+C beenden. USB-Debugging kann wieder aus.

### Weg B: über einen Link (GitHub Pages)

**https://glogolt.github.io/lesen-lernen/**

Am Tablet den Link in Chrome oder Brave einmal öffnen, warten, bis „Spracherkennung wird geladen“
verschwindet, dann im Browser-Menü (⋮) **App installieren** bzw. **Zum Startbildschirm hinzufügen**.
Danach läuft die App offline. Änderungen landen per `git push` automatisch online, und das Tablet holt
sie, sobald es online ist (Versionsnummer in `sw.js` erhöhen).

## Bereiche

**📖 Silben lesen:** Das Kind liest Silbe für Silbe vor (Bögen, blau/rot, Selbstlaute gelb) und
schwingt die Silben dann zum Wort zusammen. Erst danach erscheint das Bild.

**🧩 Wörter bauen:** Das Bild zeigt das Ziel. Das Kind tippt die passenden Silben in der richtigen
Reihenfolge an, eine oder zwei falsche Silben sind beigemischt. Danach liest das Kind das Wort vor.

Die App sagt nichts von selbst vor. „💡 Tipp“ erscheint erst, nachdem falsch gelesen (oder beim
Bauen eine falsche Silbe gelegt) wurde, und ist bei jeder neuen Silbe bzw. jedem neuen Wort wieder
weg. Er hilft zuerst ohne Ton, erst beim zweiten Tippen mit Vorlesen. **Zum nächsten Wort geht es nur, wenn die Spracherkennung das ganze Wort richtig gehört hat.**
Es gibt keinen Bestätigungs- und keinen Überspringen-Knopf. Das gilt in beiden Bereichen.
Hängt ein Wort fest, weil die Erkennung es nicht versteht, hilft der zweite Tipp (Vorlesen zum
Nachsprechen). Notfalls können Erwachsene über die Stufen-Auswahl oder den anderen Bereich ein neues Wort holen.

## Spracherkennung

- Die Erkennung kennt nur die Silben und Wörter der App (Wortliste). Das macht sie schnell und genau.
- 11 Silben fehlen im Wortschatz des Modells und werden über gleich klingende Wörter erkannt
  (z. B. „lam“ als „lamm“, `SYL_ALIAS` in `index.html`). „gur“, „kro“ und „schmet“ lassen sich
  nicht prüfen. Dort zählt jedes Vorlesen, geprüft wird dann beim ganzen Wort.
- Einzelne Silben sind schwieriger als ganze Wörter. Nach zwei nicht erkannten Versuchen wechselt die App
  zum ganzen Wort. Das muss dann richtig erkannt werden.

## Ändern

- Wörter: `LEVELS` oben in `public/index.html`, Silben mit `-` getrennt, z. B. `['Ba-na-ne','🍌']`.
  Neue Silben, die das Modell nicht kennt, in `SYL_ALIAS` eintragen.
  Neue Wörter dürfen nicht ähnlich klingen wie vorhandene, sonst verwechselt die Erkennung sie
  (deshalb fehlen z. B. Biene wegen Birne, Affe wegen Giraffe/Koffer, Torte wegen Karotte).
- Nach jeder Änderung in `public/sw.js` die Versionsnummer (`lesen-v4`) erhöhen, damit installierte
  Tablets die neue Fassung holen.
- `build/` (nicht im Repository) enthält Rohdaten (Modell, Bibliothek) und die alte PC-Version mit
  Whisper (`build/alt-pc-whisper`).

## Lizenzen

- Spracherkennung: [vosk-browser](https://github.com/ccoreilly/vosk-browser) 0.0.8, Apache-2.0
- Sprachmodell: [vosk-model-small-de-0.15](https://alphacephei.com/vosk/models) von Alpha Cephei,
  Apache-2.0 (`public/vosk/LICENSE-model.txt`)
