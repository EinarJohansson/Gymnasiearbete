# Gymnasiearbete 🤠
Robot för automatisering av lagerarbete m.m 🤖

### Skaffa koden
- Ladda ner [git](https://git-scm.com/downloads)
- Clone:a projektet
  - Öppna en terminal/kommandotolk.
  - Navigera till ett lämpligt direktiv, ex. Dokument eller Skrivbordet.
  - Copy-paste:a ```git clone https://github.com/EinarJohansson/Gymnasiearbete.git```
  - Klart!🍺
  
### Initialisera projektet
 - Navigera till mappen Gymnasiearbete.
 - Gör en virtuell miljö:
   - ```python3 -m venv venv ```
   - ```source venv/bin/activate```
   - ```pip install -r requirements.txt```
 - När inte längre vill använda den virtuella miljön
   - ```deactivate```

### Göra ändringar i robotens kod
- Ladda ner [Arduino IDE](https://www.arduino.cc/en/Main/Software)
- Öppna upp ```.ino``` filen i Arduino IDE
- Gå in i inställningar och lägg till ```https://arduino.esp8266.com/stable/package_esp8266com_index.json``` i fältet **Additional Boards manager URLs**
- Välj kortet ```Generic ESP8266 Module``` under fliken verktyg
- Kompilera projektet genom att klicka på ✅ symbolen
- Om du får errors
  - gör om gör rätt noob
- Om inga errors
  - Gör en pull request
  noob

### Göra ändringar i koden för visualering:
 - Innan virtuella miljön avaktiveras
   - Navigera till Gymnasiearbete
   - ```pip freeze > requirements.txt```
   - ```deactivate```
