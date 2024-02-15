# BETH - Badminton Equipment for Training and Health

## Projektbeschreibung
Das Elektronikprojekt konzentriert sich auf verschiedene Aspekte der Elektrotechnik, darunter die Programmierung von Mikrocontrollern, die Analyse und Umsetzung der Energieversorgung kleinerer Geräte sowie die Implementierung von Sensoren, optischen und akustischen Bausteinen. Das Hauptziel besteht darin, ein System zu entwickeln, das sowohl im sportlichen Bereich als auch im Freizeitbereich Anwendung findet. BETH (Badminton Equipment for Training and Health) wurde entwickelt, um Spielern die Möglichkeit zu geben, ihre Reaktionsfähigkeit, Bewegungskoordination und Ausdauer zu verbessern, indem es eine dynamische und unterhaltsame Umgebung schafft.

## Funktionen und Technologien
- Programmierung von ESP32 Mikrocontrollern und eines Raspberry Pi's
- Analyse des Energiekonsums und Umsetzung der Energieversorgung kleinerer Geräte
- Integration von Sensoren, Licht- und Tonbausteinen für innovative und interaktive Systeme

---

### Audio
#### Eingliederung in das Projekt
Die Umsetzung einer effektiven Audiowiedergabe erfordert präzise Signalverarbeitung und Kontrolle. Im Fokus steht die Audiowiedergabe, bei der mehrere Schaltungselemente kombiniert wurden, um optimale Klangqualität und Steuerbarkeit zu gewährleisten. Die Grundlage bildet ein Audioplayer-Modul, dem im Verlauf der Realisierung verschiedene Elemente hinzugefügt wurden.

##### Funktionsweise
1. **DF Player**
   - Ein DF Player bzw. ein Audioplayer-Modul von DFRobot wird verwendet.
   - Speziell für die Wiedergabe von Audiodateien mit einem einfachen Steuerungsprotokoll konzipiert.
   - Unterstützt Funktionen wie Abspielen, Pausieren, Stoppen, Vor- und Zurückspulen von Audiotracks.
   - Über eine serielle Schnittstelle (UART) vom Mikrocontroller (ESP32S) gesteuert.

2. **Addierer und Rekonstruktionsfilter**
   - Verwendung einer Schaltung mit einem Operationsverstärker (OPV), um rechte und linke Stereosignale zu kombinieren.
   - Ein Rekonstruktions-Tiefpassfilter minimiert Aliasing-Effekte und glättet das digitale Signal.

3. **Audio Verstärker**
   - Der LM386 Audioverstärkerchip ermöglicht eine effektive Verstärkung von Audiosignalen.
   - Die Schaltung umfasst verschiedene Bauteile, die in ihrer Kombination eine qualitativ hochwertige Audiowiedergabe gewährleisten.

4. **DC/DC Wandler**
   - Ein DC/DC-Wandler wird eingesetzt, um die Batteriespannung von +5V auf +12V umzuwandeln.
   - Ein Filterkondensator minimiert Eingangs- und Ausgangswelligkeit.
   - Eine Elektromagnetische Verträglichkeit (EMC) Schaltung gewährleistet störungsfreies Arbeiten in elektromagnetisch sensiblen Umgebungen.

##### Anleitung zur Nutzung
1. Lade Audiofiles auf die micro SD-Karte.
2. Verbinde die serielle Schnittstelle des DF Players mit der Steuerungseinheit.
3. Steuere die Audiowiedergabe über UART-Befehle.

##### Hinweise
- Beachte die Platzbeschränkungen bei der Implementierung der Audiofunktionen.
- Stelle sicher, dass die Spannungsversorgung und EMC-Richtlinien eingehalten werden.

---

### LED-Beleuchtung im Projekt
#### Eingliederung in das Projekt
Die Integration der LED-Beleuchtung in das Projekt bietet eine ästhetische Komponente und erweitert die Funktionalität. Die Wahl der RGB-LEDs WS2812B ermöglicht die flexible Ansteuerung jeder einzelnen LED, was eine vielfältige Gestaltung der Beleuchtung und die Umsetzung verschiedener Spielmodi ermöglicht. Die LEDs dienen auch zur Anzeige von Statusinformationen wie dem Verbindungsstatus und dem Batteriezustand.

#### Funktionsweise
Die Platine für die LED-Beleuchtung wurde so gestaltet, dass sie neben den RGB-LEDs WS2812B auch alle notwendigen Komponenten enthält, um eine nahtlose Integration in das Gesamtsystem zu gewährleisten. Die Anordnung der LEDs in einem Ring ermöglicht die Erzeugung kreativer Lichteffekte, die das Spielerlebnis intensivieren.

Die WS2812B RGB-LEDs haben vier Pins: Versorgungsspannung, Masse, Eingangssignal und Ausgangssignal. Die Verbindung zwischen den LEDs erfolgt durch Verknüpfung des Ausgangssignal-Pins einer LED mit dem Eingangssignal-Pin der nächsten LED. Die Status-LED auf der Seite des Gehäuses kommuniziert über verschiedene Farben und Blinkmuster wichtige Informationen, wie den Verbindungsstatus mit anderen Satelliten oder den Batteriezustand.

#### Schaltplan
Aufgrund des begrenzten Platzes im Gehäuse wurden 16 LEDs auf die Hauptplatine des Moduls gesetzt. Die LEDs sind mit dem Mikrocontroller verbunden, um das Eingangssignal, die Spannungsversorgung und die Masse zu erhalten, und leiten das Signal an die Status-LED und den LED-Streifen weiter.

#### PCB
Die Leiterplatte (PCB) wurde entsprechend dem Schaltplan erstellt. Die LEDs wurden in einem Kreis angeordnet, und auf der anderen Seite der Platine wurden der große Kondensator und der Widerstand platziert.

#### Programmierung
Für die Steuerung der LEDs wurde die Neopixel-Bibliothek von Adafruit Industries verwendet. Die Programmierung ermöglicht eine flexible und anpassbare visuelle Gestaltung, um das LEDmintons-Erlebnis zu verbessern. Die Integration dieser Programmierfunktionalitäten erlaubt die Steuerung der Beleuchtungseffekte in Echtzeit während des Spielbetriebs.

---

### Sensorik im Projekt
#### Eingliederung in das Projekt
Im Sensorik-Kapitel wird die Integration der im Projekt verwendeten Sensoren beschrieben. Sensoren sind in der Lage, Informationen von der Umgebung aufzunehmen und elektrische Signale zu erzeugen. Im Projekt wurden Sensoren ausgewählt, die spezifische Anforderungen erfüllen sollten, darunter die Detektion des Badmintonschlägers auf unterschiedlichen Distanzen und die schnelle Reaktion auf Bewegungen.

#### Anforderungen
Die Auswahl der Sensoren erfolgte unter Berücksichtigung von Anforderungen wie der Reaktionsgeschwindigkeit und der Fähigkeit, Bewegungen auf kurze und lange Distanzen zu detektieren. Es wurden TOF-Sensoren (Time of Flight) ausgewählt, um die Entfernungen zuverlässig zu messen, sowie der eingebaute Touchsensor des ESP32 für die Detektion von Berührungen.

#### Funktionsweise
**TOF Sensoren**
Die Entfernungsmessung wird von TOF-Sensoren übernommen. Diese Sensoren wurden aufgrund ihrer Zuverlässigkeit, schnellen Reaktion und geringen Größe ausgewählt. Sie sind in der Lage, Entfernungen von 40 mm bis 4 m mit einer Genauigkeit von ±5 % zu messen. Die Messung basiert auf der Laufzeitmessung von Licht, das zum Zielobjekt geschossen wird und reflektiert zurückkehrt.

**Touch Sensor**
Der Touchsensor basiert auf den Touchpins des ESP32. Die Berührung einer Metallplatte, die mit einem Pin verbunden ist, sendet ein elektrisches Signal an den ESP32. Schutzmaßnahmen, wie eine Supressordiode und ein Widerstand, wurden implementiert, um Überladungen zu verhindern.

**Programmierung und Interrupts**
Um eine schnelle Reaktion der TOF-Sensoren zu gewährleisten, wurden Interrupts in der Programmierung verwendet. Diese ermöglichen eine zuverlässige Detektion von Umweltveränderungen und eine unmittelbare Weiterleitung an den ESP32.

---

### Kommunikation
#### Eingliederung in das Projekt
Dieser Abschnitt beschäftigt sich mit der technischen Implementierung und Realisierung der Kommunikation zwischen den Satelliten (ESP32) und der Basisstation (Raspberry Pi). Die Kommunikation spielt eine entscheidende Rolle, da sämtliche Benutzerinteraktionen über die Basisstation erfolgen.

#### Kommunikationsmethoden
Zur Gestaltung des Projekts wurden zwei Kommunikationsmethoden in Betracht gezogen: Bluetooth und drahtlose Verbindung (WLAN). Nach sorgfältiger Überlegung wurde WLAN als die bessere Option gewählt, da es die spezifizierten Anforderungen besser erfüllt. Als Kommunikationsprotokoll wurde TCP (Transmission Control Protocol) ausgewählt, um eine stabile und zuverlässige Verbindung zu ermöglichen.

#### Anforderungen
Die formulierten Anforderungen umfassen unter anderem die gleichzeitige Verbindung aller Satelliten mit der Basisstation, eine stabile Verbindung, schnelle Erkennung von Unterbrechungen, minimaler Paketverlust, automatische Wiederherstellung der Verbindung nach Unterbrechungen und unabhängige Verbindungen zwischen der Basisstation und den Satelliten.

#### Implementierung
Die Kommunikation erfolgt über WLAN unter Verwendung von TCP. Die Basisstation (Raspberry Pi) erstellt einen drahtlosen Hotspot, und die Satelliten (ESP32) stellen eine TCP-Verbindung her. Die Kommunikation erfolgt in JSON-Format für die Übertragung von Nachrichten.

##### Raspberry Pi Programmierung
Die Basisstations-Software wurde in Python (Version 3.12) implementiert. Sie erstellt einen kabellosen Hotspot, verwaltet die Kommunikation und bietet eine grafische Benutzeroberfläche (GUI) für Benutzerinteraktionen.

##### ESP-32 Programmierung
Die Satelliten-Software wurde in C++ mit Hilfe von Espressifs Wifi-Bibliothek und ArduinoJson implementiert. Die Satelliten senden regelmäßig Nachrichten, die die Satellite-ID und den Batteriestand enthalten.

##### Test der Kommunikation
Verschiedene Testfälle wurden durchgeführt, darunter der reibungslose Betrieb paralleler Verbindungen und die erfolgreiche Erkennung von Verbindungsunterbrechungen. Die Kommunikation wurde über mehrere Stunden ohne Unterbrechungen getestet.

## Installation und Nutzung
1. Klone das Repository: `git@github.com:ToTo279/BETH.git`
2. Folge den Anweisungen in der Installationsanleitung, um das System einzurichten.
3. Erkunde die verschiedenen Funktionen und Anwendungsbereiche im Projekt.

