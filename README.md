Klar – hier ist eine **README.md** für deinen „Lustiger Kleiner Bot“ in Markdown-Format:

````markdown
# Lustiger Kleiner Bot (LKB)

Ein mächtiger, lokal gehosteter Discord-Admin-Bot mit Slash-Commands.  
Alle Admin-Funktionen sind unter der Haupt-Command-Gruppe `/lkb` erreichbar.  
**Achtung:** Viele Befehle sind destruktiv – nutze sie mit Bedacht.

---

## 📦 Installation

1. **Bot in Discord Developer Portal erstellen**
   - Gehe zu [https://discord.com/developers/applications](https://discord.com/developers/applications)
   - Erstelle eine neue Application → Bot hinzufügen
   - Token **kopieren** (wird später als Umgebungsvariable `DISCORD_TOKEN` benötigt)
   - Unter **Privileged Gateway Intents**:
     - `Server Members Intent` aktivieren
     - `Message Content Intent` optional aktivieren (nicht zwingend)
   - Bot einladen mit **Admin-Rechten** (OAuth2 → URL Generator → Bot + Administrator)

2. **Python-Umgebung vorbereiten**
   ```bash
   pip install -U discord.py
````

3. **Bot-Token als Umgebungsvariable setzen**

   * Windows (PowerShell):

     ```powershell
     setx DISCORD_TOKEN "DEIN_BOT_TOKEN"
     ```
   * Linux/Mac:

     ```bash
     export DISCORD_TOKEN="DEIN_BOT_TOKEN"
     ```

4. **Bot starten**

   ```bash
   python bot.py
   ```

---

## ⚙️ Befehlsübersicht

### `/ping`

**Beschreibung:** Schneller Healthcheck – antwortet mit „Pong! ✅“.
**Berechtigungen:** Keine (jeder kann ausführen).

---

### `/lkb channel delete`

**Beschreibung:** Löscht Kanäle per Namen.
**Parameter:**

* `name` → Exakter Kanalname oder `*` für ALLE Kanäle
  **Berechtigungen:** `Kanäle verwalten`

---

### `/lkb channel rename_all`

**Beschreibung:** Bennennt alle Kanäle nach einem Namensmuster um.
**Parameter:**

* `base` → Basisname (z. B. `channel`)
* `start` → Startindex (Standard: 1)
* `include_categories` → Kategorien ebenfalls umbenennen
  **Berechtigungen:** `Kanäle verwalten`

---

### `/lkb members kick_all`

**Beschreibung:** Kickt (fast) alle Mitglieder eines Servers.
**Parameter:**

* `reason` → Grund (für Audit Log)
* `include_admins` → Admins/Owner ebenfalls kicken? *(nicht empfohlen)*
* `include_bots` → Bots ebenfalls kicken
* `confirm` → Sicherheitsabfrage – **muss genau `YES` sein**
  **Berechtigungen:** `Administrator`

---

### `/lkb roles delete_all`

**Beschreibung:** Löscht Rollen (geschützt: @everyone, höhere Rollen, managed Roles).
**Parameter:**

* `include_managed` → Auch gemanagte Rollen löschen versuchen
* `confirm` → **muss genau `YES` sein**
  **Berechtigungen:** `Server verwalten` oder `Administrator`

---

### `/lkb server`

**Beschreibung:** Zeigt eine Übersicht des Servers (Name, ID, Owner, Mitgliederzahl, Kanäle, Rollen, Erstellungsdatum).
**Berechtigungen:** Keine (jeder kann ausführen).

---

### `/lkb resync`

**Beschreibung:** Registriert Slash-Commands neu (falls Änderungen nicht angezeigt werden).
**Berechtigungen:** `Administrator`

---

## 🛡️ Sicherheitshinweise

* Nutze diesen Bot nur auf Servern, auf denen du **volle Admin-Rechte** hast.
* Viele Befehle können **nicht rückgängig gemacht** werden (z. B. Kick, Delete).
* Überprüfe vor Ausführung immer die Parameter (`confirm`-Abfrage schützt dich).

---

## 📜 Lizenz

Frei nutzbar, aber Nutzung auf eigenes Risiko.

```

---

Wenn du willst, kann ich dir auch noch **Beispielscreenshots der Commands** für die README einfügen – das macht es visuell klarer, vor allem bei `/lkb channel delete` und `/lkb members kick_all`.  
Möchtest du, dass ich das noch einbaue?
```
