# Headline-CTR-A/B-Test — Sprechzettel (Deutsch, zur eigenen Vorbereitung)

*Zum wörtlichen Vorlesen gedacht. Drei Folien.*

---

## Folie 1 — Was wir getestet haben und warum

Wir haben einen A/B-Test zum Headline-Stil unserer Artikel durchgeführt, weil unsere Click-Through-Rate stagniert und wir wissen wollten, ob schon die Art, wie wir eine Headline formulieren — nicht der Inhalt selbst — daran etwas ändern kann.

Getestet haben wir drei Varianten. Variante A ist unser aktueller Stil: neutrale, faktische Headlines. Variante B ersetzt das durch emotionale, neugierde-getriebene Headlines — also solche, die eine "Neugierlücke" öffnen, statt den Fakt direkt zu nennen. Variante C ist eine KI-generierte Headline, mit der wir prüfen wollten, ob ein Sprachmodell ohne zusätzliche Steuerung mit unserer Redaktion mithalten oder sie sogar übertreffen kann.

Unsere Hypothese war: Wenn wir diese Neugierlücke öffnen, steigt der wahrgenommene Reward eines Klicks, also sollte Variante B bei der CTR gewinnen. Genauso wichtig war uns aber der mögliche Trade-off: Wenn eine Headline zu viel verspricht, klicken Leser zwar, verlassen die Seite danach aber sofort wieder, weil der Artikel das Versprechen nicht einlöst. Wir nennen das die "Clickbait-Tax", und unsere Analyse ist gezielt so aufgebaut, dass wir genau das erkennen können — nicht nur die Klicks isoliert zu betrachten.

Wir haben 1.500 Impressionen über zwei Wochen gesammelt, aufgeteilt in etwa 45 % A, 35 % B und 20 % C, und dabei nicht nur die Klicks gemessen, sondern auch, was danach passiert: Scroll-Tiefe, Verweildauer und Bounce-Rate.

Bevor wir uns überhaupt Ergebnisse angeschaut haben, haben wir außerdem zwei Dinge vorab festgelegt. Erstens die Stichprobengröße: Bei einer Baseline-CTR von 4 % und einem gewünschten relativen Mindesteffekt von 20 % braucht ein sauber gepowerter Test rund 10.300 Impressionen pro Arm — das war unser Zielwert. Zweitens die Stopping-Regel: Wir haben uns vorgenommen, vor Erreichen dieses Zielwerts keinen Gewinner auszurufen, und einen Test nur dann vorzeitig zu stoppen, wenn er nachweislich schadet, etwa durch eine stark erhöhte Bounce-Rate. Beide Entscheidungen sind wichtig, um die nächste Folie richtig einzuordnen.

---

## Folie 2 — Was wir herausgefunden haben

Zuerst die Kernzahl: Die beobachtete Click-Through-Rate lag bei 3,4 % für A, 5,3 % für B und 4,0 % für C. Auf den ersten Blick gewinnt also klar Variante B — die emotionale, neugierde-getriebene Variante — genau wie in unserer Hypothese.

Als wir aber einen klassischen statistischen Signifikanztest gerechnet haben — einen Zwei-Proportionen-z-Test — war der Unterschied zwischen A und B *nicht* statistisch signifikant, mit einem p-Wert von etwa 0,10. Dasselbe gilt für den Vergleich A gegen C. Auf Deutsch: Bei der Menge an Traffic, die wir hatten, können wir noch nicht ausschließen, dass der Unterschied reiner Zufall ist.

Zusätzlich haben wir eine Bayesianische Analyse gerechnet, die für Entscheidungen die eigentlich relevantere Frage beantwortet: Wie wahrscheinlich ist es angesichts der Daten, dass B tatsächlich besser ist als A? Die Antwort: 95 %. Es gibt also ein starkes Signal, auch wenn es die klassische Signifikanzschwelle noch nicht reißt — was auch Sinn ergibt, denn wir liegen ja erst bei 300 bis 675 Impressionen pro Arm, bei einem Zielwert von 10.300. Der Test ist also richtungsweisend vielversprechend, aber unterpowert.

Und genau in dieser unterpowerten Phase werden vorschnelle Schlüsse gefährlich — das können wir sogar konkret zeigen: Wir haben die Analyse noch einmal so durchgerechnet, als hätten wir ab der ersten Impression live auf ein Dashboard geschaut. Allein in den ersten 300 Impressionen ist die "führende" Variante nach kumulativer CTR sechsmal umgesprungen — erst C vorne, dann A, dann B, hin und her — bevor sich das Bild in das heutige Muster eingependelt hat. Hätten wir an irgendeinem dieser frühen Zeitpunkte gestoppt und dem Zwischenstand vertraut, hätten wir leicht die falsche Variante ausgerollt. Genau deshalb haben wir Stichprobengröße und Stopping-Regel vorab festgelegt, bevor wir überhaupt gestartet sind.

Und hier zeigt sich der Trade-off, den wir erwartet hatten: Variante B hat zwar bei den Klicks gewonnen, aber bei allem, was danach kommt, deutlich verloren. Leser, die auf B geklickt haben, sind in 43 % der Fälle sofort wieder abgesprungen, bei A waren es nur 13 %. Sie haben im Schnitt nur 37 % des Artikels gescrollt, bei A waren es 67 %. Und sie waren nur 85 Sekunden auf der Seite, bei A 164 Sekunden. Das ist die Clickbait-Tax, und sie zeigt sich genau dort, wo wir sie erwartet haben.

---

## Folie 3 — Empfehlung

Unsere Empfehlung: Variante B nicht einfach so ausrollen — aber auch nicht verwerfen. Der CTR-Anstieg sieht real aus — laut unserer Bayesianischen Schätzung mit 95 % Wahrscheinlichkeit tatsächlich besser als A — aber statistisch ist er noch nicht abgesichert, und er kommt mit einem echten Preis beim Reader Engagement.

Konkret schlagen wir drei Dinge vor. Erstens: den Test verlängern, bis wir die rund 10.300 Impressionen pro Arm erreichen, die für ein belastbares Ergebnis nötig wären — und der Versuchung widerstehen, ihn vorher zu beenden. Wir haben gerade gezeigt, dass die scheinbar führende Variante in den ersten paar hundert Impressionen mehrfach wechseln kann, ein Zwischenblick ist also kein Entscheidungspunkt. Ein vorzeitiger Stopp ist nur gerechtfertigt, wenn eine Guardrail-Metrik eindeutig kippt, etwa eine Bounce-Rate, die weit über die Baseline schießt. Zweitens: parallel an Variante B weiterarbeiten, damit das Versprechen der Headline vom Artikel auch eingelöst wird — das Ziel ist, den neugierde-getriebenen Ansatz beizubehalten, aber ohne die Bounce-Strafe, nicht ihn aufzugeben. Drittens: künftig bei jedem Headline-Test Scroll-Tiefe, Verweildauer und Bounce-Rate als Guardrail-Metriken mitverfolgen, nicht nur die CTR — denn die CTR allein hätte uns dazu gebracht, einen Headline-Stil auszurollen, der leise das Vertrauen und Engagement unserer Leser beschädigt.
