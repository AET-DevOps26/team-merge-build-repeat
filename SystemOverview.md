# System Overview

## Project Statment

Sudoku learners often struggle to understand why a specific move is correct or incorrect.
Existing Sudoku platforms usually provide simple hints or mark errors,
but they often fail to explain the reasoning behind a move or teach the solving techniques needed to improve over time.

This project addresses that problem by developing a Sudoku platform with integrated Generative AI.
The platform supports users while solving Sudoku puzzles by providing contextual help,
explaining mistakes, and teaching relevant solving strategies.
Instead of only giving the next answer, the system aims to guide users through the logical reasoning process,
helping them learn Sudoku techniques and improve their problem-solving skills.

## Authentication

- Supabase Auth (JWT, Postgress)

## Engine Service

(stateless)

Alogrithmic solver for sudoku

- Sprint Boot REST API

## Game Store Service

Store Games of a user. Past and active games.

- Spring Boot REST API
- Postgress Database

## Frontend

- React (Type Script)

## GenAI Service

### Kleinen Hint geben

- nur Region nennen
- keine Zahl verraten
- keine Zielzelle verraten

### Hint stufenweise aufdecken

- mehr Details auf Nachfrage
- gleicher Hint bleibt konsistent
- von „Schau in diesen Block“ bis „Setze R4C7 = 9“

### Nächsten logischen Schritt erklären

- warum ein Zug korrekt ist
- welche Sudoku-Technik verwendet wird
- welche Kandidaten ausgeschlossen werden

### Sokratischer Coach

- stellt Fragen statt Lösung zu verraten
- führt den User Schritt für Schritt
- korrigiert Denkfehler sanft

### Fehleranalyse

- erklärt offensichtliche Regelkonflikte
- erklärt, warum ein Zug falsch ist
- unterscheidet zwischen Regelverstoß, falscher Lösung und nicht-logischem Guess

### Delayed Error Handling

- Fehler nicht sofort aggressiv anzeigen
- erst erklären, wenn User weitergeht oder Hint anfordert
- Tippfehler/Verklicker nicht unnötig bestrafen

### Timeline-basierte Fehleraufarbeitung

- ersten Fehler in der Timeline finden
- Fehler erklären
- Optionen anbieten:
- alles behalten
- nur Fehler löschen
- ab Fehler zurücksetzen

### Smart-Recovery

- fehlerhafte Zelle entfernen
- spätere Moves replayen
- nur logisch herleitbare Moves behalten
- Preview zeigen, was gelöscht/ behalten wird

### Technik-basierte Recovery

- User wählt erlaubte Techniken
- z. B. nur Naked Single / Hidden Single
- Recovery behält nur Moves, die mit diesen Techniken beweisbar sind
- Kandidaten erklären
- mögliche Zahlen für eine Zelle nennen
- erklären, warum eine Zahl ausgeschlossen ist
  Kandidatenlogik anhand des Boards zeigen

### Sudoku-Techniken erklären

- Naked Single
- Hidden Single
- Locked Candidate
- Naked Pair
- später X-Wing, Swordfish usw.

### Training / Challenge-Modus

- kleine Aufgaben aus aktuellem Board erzeugen
- User antworten lassen
- Antwort prüfen und Feedback geben

### Stil anpassen

Anfänger-Erklärung
Expertenmodus
kurze Antwort
ausführliche Tutor-Erklärung
motivierender Coach
UI steuern
relevante Region markieren
Zelle markieren
Kandidaten hervorheben
Konflikte anzeigen
Markierungen passend zum Hint setzen
Board-Zustand prüfen
gültig / ungültig
lösbar / unlösbar
eindeutige Lösung vorhanden
mehrere Lösungen erkennen
Freie Fragen beantworten
„Warum kann hier keine 7 stehen?“
„Welche Technik brauche ich gerade?“
„Was habe ich übersehen?“
„Gib mir weniger Spoiler.“

- LangChain (Python)
- FastAPI (REST)

## Prometheus

- Store service logs

## Grafana

- Visualise logs
- Alerts
