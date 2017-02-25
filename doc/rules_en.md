### Rule of Blokus(CUW-edition)：  


## Definitions  

* The entire board is defined as "B".  
* The board B has cells, and there exist B\[i,j] (0 <= i, j < 12).  
* First player commences the game from B[2, 2], and the second from B[9, 9]  
* The area where the player has placed carpet is defined as a "player-region".  

## Rules  

* The red plays the first placement, followed by the blue.  
* Both the players have 60 carpets.  
* A single turn is completed when both the players execute placements. When a player no longer has  
a playable placement, the player stops playing and the another plays till the end of the game.  
* One "placement" is an extension of the existing player region, which can be executed provided the following:  
  + The extension region must be "connected"; for any provided cell in the extension region,  
there must be another extension cell next to it(Manhattan distance[1] is 1).  
  + For the first placement, player has to include his or her starting cell.  
  + From the second placement onwards, the player has to include at least one cell such that it is on a corner of the existing player cell.  
  + However, the player must not extend to a cell whose Manhattan distance to the existing player region equals one.  
* Both the players can extend the region 10 times with 3 carpets, 5 times with 4 and 2 times with 5 carpets.  
* The game is terminated when both the players no longer have any possible placement.  
* The winner of the game is who has gained wider player-region. However, the blue wins when both have the same area of player-regions.  
* Annotations
  - [1]: [https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%B3%E3%83%8F%E3%83%83%E3%82%BF%E3%83%B3%E8%B7%9D%E9%9B%A2](https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%B3%E3%83%8F%E3%83%83%E3%82%BF%E3%83%B3%E8%B7%9D%E9%9B%A2)
