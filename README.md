# Luminara Schüler-KI-Plattform

## Beschreibung

Die Schüler-KI-Plattform ist eine webbasierte Anwendung, die es Schülern ermöglicht, sich anzumelden und mit verschiedenen Künstlichen Intelligenzen (KI) zu interagieren. Die Plattform kombiniert die Nutzung der ChatGPT-API mit unbegrenzten lokalen KI-Modellen wie Ollama, die auf dem Schulserver betrieben werden. Ziel ist es, den Schülern vielseitige Unterstützung beim Lernen und bei der Bearbeitung von Aufgaben zu bieten.

## Funktionen

- **Programmierbot**: Unterstützung beim Programmieren durch Beantwortung von Fragen und Bereitstellung von Codebeispielen.
- **OCR (Bild zu Mitschrift)**: Konvertierung von Bildern in Text, um handschriftliche Notizen oder gedruckte Dokumente digital verfügbar zu machen.
- **Allgemeiner Chatbot**: Ein angepasster Chatbot mit einem speziellen System-Prompt für allgemeine Anfragen und Konversationen.
- **Bilderkennung**: Analyse und Lösung von Aufgaben anhand von hochgeladenen Bildern.
- **Mathe-Bot**: Unterstützung bei mathematischen Problemen und Aufgabenlösungen.
- **Chatten mit API**: Integration von ChatGPT und Claude AI mit Token-Limitierungen für erweiterte Konversationsmöglichkeiten.
- **Testvorbereitung**: Generierung von Fragen zur Vorbereitung auf Tests, eventuell mit einem Karteikartensystem zur effektiven Wiederholung.

## Konto-Modell

Die Plattform verwendet ein differenziertes Kontomodell, das den Zugang zu den KI-Diensten basierend auf verschiedenen Benutzerrollen und Token-Beschränkungen steuert:

- **Student-Accounts**: Jeder Schüler erhält pro Monat eine bestimmte Anzahl an Premium-Token, die zum Promten der leistungsstarken KI-Modelle wie ChatGPT und Claude AI verwendet werden können. Nicht genutzte Token werden auf den nächsten Monat übertragen, sodass Schüler ihre Ressourcen effizient planen können.
  
- **Admin- und Dev-Accounts**: Diese Konten besitzen unbegrenzte Token, um umfassende Verwaltungs- und Entwicklungsaufgaben zu unterstützen. Admins haben zusätzliche Rechte zur Verwaltung von Benutzerkonten, Token-Verteilungen und Systemkonfigurationen.

- **Student+ Accounts**: Diese erweiterten Schülerkonten bieten eine größere Menge an Token, um intensivere Nutzung der KI-Dienste zu ermöglichen. Um einen Student+ Account zu erhalten, müssen Schüler einen Antrag stellen, der von den Website-Admins geprüft und genehmigt werden muss. Dies ermöglicht eine kontrollierte Verteilung der erweiterten Ressourcen und stellt sicher, dass nur berechtigte Schüler von den zusätzlichen Token profitieren.

Dieses Kontomodell stellt sicher, dass alle Benutzergruppen entsprechend ihrer Bedürfnisse und Verantwortlichkeiten ausgestattet sind, während gleichzeitig eine faire und nachhaltige Nutzung der KI-Ressourcen gewährleistet wird.


## Technologie-Stack

- **Frontend**: Vue.js
- **Backend**: (Falls zutreffend, z.B. Node.js, Express)
- **KI-Modelle**:
  - ChatGPT API
  - Ollama (lokale KI-Modelle)
  - Claude AI
- **Weitere Technologien**:
  - OCR-Tools (z.B. Tesseract)
  - Bildverarbeitungslibraries (z.B. TensorFlow, OpenCV)
  - Datenbank (z.B. MongoDB, PostgreSQL)

## Nutzung

1. **Registrierung und Anmeldung**

   Schüler können sich registrieren und anmelden, um Zugriff auf die verschiedenen KI-Tools zu erhalten.

2. **Auswahl der gewünschten Funktion**

   Nach der Anmeldung können Schüler aus den verschiedenen Funktionen wie Programmierbot, OCR, allgemeiner Chatbot, Bilderkennung, Mathe-Bot und Testvorbereitung wählen.

3. **Interaktion mit der KI**

   Je nach gewählter Funktion können Schüler Fragen stellen, Aufgaben hochladen oder interaktive Lernmaterialien nutzen.


## Lizenz

Dieses Projekt ist unter der [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) lizenziert.

## Kontakt

Bei Fragen oder Anregungen kannst du dich gerne an mich wenden:

- **E-Mail**: luna.schaetzle.website@gmail.com
- **GitHub**: [Luna-Schaetzle](https://github.com/Luna-Schaetzle)


