# CS3050_Frogger
***NOTICE - this uses firebase thus requires a credentials.json. The game should run, just will not be able to update leaderboard
In order to run the file one must install arcade. (pip install arcade)
If using an IDE to run the file, make sure that firebase-admin is installed in the python interpreter it is using. 
For example, if using pycharm, do file>>settings>>project Name>>Python interpreter, click the + button in the left corner, search for firebase-admin and install if it needed. 

To run the game, run game_view.py. This will create the game window and open the instruction view screen.

## Instructions To Play
- Move the frog using the arrow keys or w, a, s, and d. Try to move the frog across the screen and make it into each of the homes. If you fill all 5 homes you advance to the next level where the obstacles speed up.
- There are 3 lives, once all 3 are used the game is over. If you don't make it across within the time limit you lose a life.
- Avoid the cars, if hit them you will lose a life.
- Ride the logs and turtles to cross the river, falling in will result in losing a life.
- A fly will occassionally spawn in unfilled homes and gives bonus points if collected.
- After losing all lives, the user can enter a name for the highscore leaderboard. Highscores are maintained in a Firebase Firestore and the top 5 scores are shown in the leaderboard view screen.
