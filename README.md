
# Lustiger Kleiner Bot (LKB) 

Ein leistungsstarker, lokal gehosteter Discord-Bot mit Slash-Commands, Admin-Tools und einem **Console-Mode**, Hauptfokus liegt natürlich auf griefing :D

>  **Achtung:** Ich übernehme **keine** verantwortung für was auch immer mit diesem Bot getan wird ;p

---

## Funktionen

### Basis
- `/ping` → Testet, ob der Bot reagiert ("Pong!").

### Kanalbefehle (`/lkb channel`)
- `delete <name|*>` → Löscht Kanäle mit bestimmtem Namen oder mit `*` alle Kanäle.
- `rename_all` → Bennent alle Kanäle (und optional Kategorien) nach einem Muster um.

### Mitgliederbefehle (`/lkb members`)
- `kick_all` → Kickt (fast) alle Mitglieder, mit Schutz für Owner/Admins/Bots (optional deaktivierbar).

### Rollenbefehle (`/lkb roles`)
- `delete_all` → Löscht Rollen (mit Schutz für Standardrolle, höchste Botrolle und gemanagte Rollen).

### Serverinfos
- `/lkb server` → Zeigt Infos zum aktuellen Server.

### Console-Mode (`/lkb switch console`)
- `on` → Aktiviert die Möglichkeit, **lokal** Befehle an den Bot zu senden, die er auf dem Server ausführt.
- `off` → Deaktiviert den Modus.
- **Unterstützte Befehle in der Konsole:**
  - `say <text>` → Schickt Nachricht in den Zielkanal.
  - `channel delete <name|*>` → Löscht Kanäle.
  - `server info` → Zeigt Serverinformationen.
  
### Commands neu laden
- `/lkb resync` → Synchronisiert die Slash-Commands erneut.

---

## Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/DEINUSERNAME/LKB.git
   cd LKB

2. **Python-Abhängigkeiten installieren**

   ```bash
   pip install -r requirements.txt
   ```

   Mindestanforderungen:

   * `discord.py` 2.x
   * `colorama`

3. **Bot-Token setzen**

   * Erstelle in deinem Discord-Entwicklerportal eine Bot-App.
   * Kopiere den Bot-Token und setze ihn als Umgebungsvariable:

     ```bash
     # Linux / macOS
     export DISCORD_TOKEN="DEIN_TOKEN"

     # Windows (Powershell)
     setx DISCORD_TOKEN "DEIN_TOKEN"
     ```

4. **Bot starten**

   ```bash
   python bot.py
   ```

---

## Console-Mode

Mit `/lkb switch console on` kannst du Befehle über deine **lokale Konsole** an den Bot senden.
Du musst angeben:

* **Dauer** in Minuten (`minutes`).
* **Ziel-Textkanal** für Ausgaben (`target_channel`).

**Beispiel:**

```
say Hallo Welt!
channel delete test-channel
server info
```

Deaktivieren:

```
/lkb switch console state:off
```
### Damit kannst du quasi trotz Bann oder kick weitermachen :D
---

## Sicherheitshinweise

* Verwende diesen Bot **nicht** auf produktiven Servern ohne ausdrückliche Genehmigung. (Muss das sagen, kontrollieren kanns eh keiner :D)
* Befehle wie `kick_all`, `delete_all` oder `channel delete *` sind irreversibel.
* Der **Console-Mode** gibt dir direkten Zugriff über die lokale Konsole – sichere deine Umgebung entsprechend ab.

---

## Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Siehe [LICENSE](LICENSE) für Details.
MIT-Lizenz in Kurzform:
`"Hier ist der Code. Mach damit, was du willst – aber erwähne meinen Namen und verlange nicht, dass ich für Schäden hafte."`
---

## Autor

**Lustiger Kleiner Bot** entwickelt von *Mausi*.

---

### Signatur
# /* ======================================== */
# // Signature
# //
#    01001001 01110000 01000001 01110101 01010110 01000011 01000101
#    01100111 01011010 01000101 01010011 00111000 01001010 00110010
#    01001001 01101110 01010000 01100111 00111101 00111101
# /* ======================================== */
