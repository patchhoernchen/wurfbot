wurfbot is a simple telegram bot to let you roll a dice.

available as @wurfbot on telegram.

TODO:
* pylinting
* pnp-diceparsing:
    * `/roll 3w6` -> `1 + 3 + 3 = 7`
    * `/roll 4w6 drop lowest` -> `(1) + 5 + 5 + 4 = 14 (15)`
    * `/roll 4w6 > 4` -> `1, 4, 6, 3 = 1`
