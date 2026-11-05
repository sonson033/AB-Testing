# Headline-CTR-A/B-Test — Sprechzettel (Deutsch, Kurzversion ~5 Min)

*Zum wörtlichen Vorlesen gedacht. Drei Folien, je ca. 1,5 Minuten.*

---

## Folie 1 — Was wir getestet haben und warum

Wir haben einen A/B-Test zum Headline-Stil gemacht, weil unsere CTR stagniert, und wollten wissen, ob schon die Formulierung etwas bewirkt.

Getestet haben wir drei Varianten: A, unser aktueller neutraler, faktischer Stil; B, emotionale, neugierde-getriebene Headlines; und C, KI-generierte Headlines. Unsere Hypothese: Wenn wir die Neugierlücke öffnen, steigt der wahrgenommene Reward eines Klicks, also sollte B bei der CTR gewinnen — aber wir haben eine mögliche "Clickbait-Tax" befürchtet: Wenn die Headline zu viel verspricht, klicken Leser, springen aber sofort wieder ab. Deshalb haben wir nicht nur Klicks gemessen, sondern auch Scroll-Tiefe, Verweildauer und Bounce-Rate.

Wir haben 1.500 Impressionen über zwei Wochen gesammelt, aufgeteilt 45/35/20 auf A, B und C, und Stichprobengröße sowie Stopping-Regel vorab festgelegt, bevor wir Ergebnisse angeschaut haben.

---

## Folie 2 — Was wir herausgefunden haben

Beobachtete CTR: 3,4 % für A, 5,3 % für B, 4,0 % für C. B sieht wie der klare Gewinner aus. Ein Zwei-Proportionen-z-Test zeigt aber: Der Unterschied A gegen B ist nicht signifikant, p liegt bei etwa 0,10 — weil wir mit 300 bis 675 Impressionen pro Arm weit unter den rund 10.300 liegen, die ein sauber gepowerter Test bräuchte. Die Bayesianische Analyse liefert die nützlichere Zahl: 95 % Wahrscheinlichkeit, dass B tatsächlich besser ist als A. Es gibt also ein echtes Signal, nur eben noch kein bestätigtes.

Wir können auch zeigen, warum Geduld hier wichtig ist: Spielen wir die Daten wie ein Live-Dashboard durch, ist die "führende" Variante allein in den ersten 300 Impressionen sechsmal umgesprungen. Ein früher Stopp hätte wahrscheinlich die falsche Variante gekürt.

Der erwartete Trade-off zeigt sich derweil genau wie vorhergesagt: Klicks auf B springen in 43 % der Fälle sofort ab, bei A nur 13 %. Sie scrollen nur 37 % des Artikels, bei A 67 %. Und sie bleiben 85 statt 164 Sekunden auf der Seite. B gewinnt den Klick, verliert aber den Leser.

---

## Folie 3 — Empfehlung

Unsere Empfehlung: iterieren — weder ausrollen noch verwerfen. Das 95-%-Bayes-Signal ist vielversprechend, aber statistisch noch nicht bestätigt, und es kostet echtes Engagement.

Konkret: den Test auf die benötigten rund 10.300 Impressionen pro Arm verlängern und nicht wegen Zwischenständen vorzeitig stoppen — wir haben gerade gezeigt, dass die sich drehen und in die Irre führen können. Ein früher Stopp ist nur gerechtfertigt, wenn eine Guardrail-Metrik wie die Bounce-Rate klar ausschlägt. Parallel dazu: den Artikelinhalt von Variante B so anpassen, dass er die versprochene Neugier auch einlöst, um die Bounce-Strafe zu senken, ohne den CTR-Gewinn zu verlieren. Und künftig bei jedem Headline-Test Scroll-Tiefe, Verweildauer und Bounce-Rate mitverfolgen — die CTR allein hätte uns dazu gebracht, etwas auszurollen, das leise das Vertrauen unserer Leser untergräbt.
