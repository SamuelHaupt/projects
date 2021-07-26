**Janggi Korean Chess** is a chess game not that different from western chess. See the [wiki page](https://en.wikipedia.org/wiki/Janggi) for more information on game play and rules. I built a **backend system** in Python to index game piece objects, simulate 1000s of moves, and determine winner by scanning for checkmate condition. It takes user input from two players to play the game.

I built an accompanying program to run modulated tests to ensure integrity of game during development. The unit testing helped to keep previous development under control and to monitor integration bugs.

**Design Wishes**: Although not required, I could have designed the project differently. I originally designed JanggiGame object to simulate moves for all GamePieces. However, I could have passed the Board object to each GamePiece object in order to simulate moves. I chose the former method, because I wanted to keep 'game rules' within one object. I could have easily been pursuaded the other direction if I had built the game with a team and another team member had requested the latter method.

**Game Board Representation**:

```
[red_chariot_1, red_elephant_1, red_horse_1, red_guard_1, '____e1_____', red_guard_2, red_elephant_2, red_horse_2, red_chariot_2]
        
['____a2_____', '____b2_____', '____c2_____', '____d2_____', red_general, '____f2_____', '____g2_____', '____h2_____', '____i2_____']

['____a3_____', red_cannon_1, '____c3_____', '____d3_____', '____e3_____', '____f3_____', '____g3_____', red_cannon_2, '____i3_____']

[red_soldier_1, '____b4_____', red_soldier_2, '____d4_____', red_soldier_3, '____f4_____', red_soldier_4, '____h4_____', red_soldier_5]

['____a5_____', '____b5_____', '____c5_____', '____d5_____', '____e5_____', '____f5_____', '____g5_____', '____h5_____', '____i5_____']

['____a6_____', '____b6_____', '____c6_____', '____d6_____', '____e6_____', '____f6_____', '____g6_____', '____h6_____', '____i6_____']

[blue_soldier_1, '____b7_____', blue_soldier_2, '____d7_____', blue_soldier_3, '____f7_____', blue_soldier_4, '____h7_____', blue_soldier_5]

['____a8_____', blue_cannon_1, '____c8_____', '____d8_____', '____e8_____', '____f8_____', '____g8_____', blue_cannon_2, '____i8_____']

['____a9_____', '____b9_____', '____c9_____', '____d9_____', blue_general, '____f9_____', '____g9_____', '____h9_____', '____i9_____']

[blue_chariot_1, blue_elephant_1, blue_horse_1, blue_guard_1, '____e10_____', blue_guard_2, blue_elephant_2, blue_horse_2, blue_chariot_2]
```