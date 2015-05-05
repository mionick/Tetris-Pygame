# Tetris-Pygame
##Intro
First time I tried to make something substantial without a tutorial. 

This project was a lot of fun! Gave me a great way to take a break from exams at the end of third year.
Decided to go with Python because of the speed of development and because I was allready familiar with Java and C++. this seemed like a good opportunity to learn something new. 
Also, reading up on game design and architectures it seemed like a common way to write games was to have game logic in a high level language like python and all the detailed optimized code in a lower level language like c.
I was going to try this with this game, but it never seemed like the "easiest" or "right" way to do it. 

The Pygame library(and think Python in general) doesn't have a good way of timing the main game loop, so I don't think writing the game logic here makes sense.
Also Python is inherently single threaded, so using it eliminated the idea of a rendering thread completely which is an important concept in large games. 

Looking back on it, I would probably not use python again for the main game logic, but I've read about using a scripting language for AI behavior. Will have to try that in the next game. 

##The Game
This tetris game comes close to official implementations of the game. 
The scoring system is the same, with the exception of T-spins because detecting them was going to be tedious and wouldn't add much to the game. Not worth it.
Combos work. Clearing more lines gives more points.
The speed increases as the player clears more lines, though I didn't make an effort to match speeds with the official game. 
The distribution of pieces is the same as the official versions. This was surpprising to implement because before trying this game I thought it was a uniform distribution. 
As it turns out, you are guaranteed to get one of each piece every seven pieces, the order is random though.

The graphics are simple squares with borders, so they are all dynamically generated except for the title screen.

The title screen:
![Title screen](https://www.dropbox.com/s/bxl20jnofbzi4zo/TitleScreen.png?raw=1)

The game:
![Playing](https://www.dropbox.com/s/fibl7y2rkg7ytsd/Playing.png?raw=1)

Game Over:
![Game over](https://www.dropbox.com/s/jmryzucnpwwb6vp/GameOver.png?raw=1)

##Issues
Choosing Python brought with it some frustrations. 
The IDLE IDE isn't great for larger projects, and has some small inconvenient behaviors like dissapearing function definitions once you start filling out the parameters.
No threading.
Also, since Python has dynamically typed variables there's no easy way to catch typos. For example:
  variable = 5;
  vraiable = 10;
  
Instead of throwing an error, this runs fine but variable keeps the value of 5. This caused some headaches during development. 

