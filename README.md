#Christmas Cannon Challenge

Use your Christmas Cannon to deliver gifts by shooting them into chimneys. This challenge focuses on calculating the trajectory of a projectile over time. The provided code handles rotation/aiming the cannon and chimney-gift collisions.


Github repo: https://github.com/reddit-pygame/christmas-cannon-challenge

#How It Works

Run main.py to launch the game.

###Collisions

Because of the high speed of gifts, it's possible for a gift to pass through a chimney cap without a collision being detected. To handle this, a rect that covers the area between
 the gift's last and current positions is also checked for collision with the chimney cap.

###Controls

*Mouse Position* Aim Cannon

*Mouse Click* Shoot Gift

*F* Toggle Fullscreen

*ESC* Exit

#Challenge

Calculate the trajectory of Gift objects launched from the Christmas Cannon using the following formulas:

x = initial_x_position + (initial_x_velocity * time_elapsed)
y = initial_y_position - (initial_y_velocity * time_elapsed) - (.5 * GRAVITY * time_elapsed**2)

Note that the distance travelled on the y-axis is subtracted from the initial y-position because the screen's y-axis is inverted.

Hint: You can use angles.project to find the initial x and y velocities

Suggested values (or what I used, at least):

GRAVITY = 9.8 (this is the actual acceleration of gravity in meters/second^2, however, it is positive due to the inverted y-axis)

Cannon.firing_speed = 125 

time_elapsed = time since firing in milliseconds / 100 (dividing by 100 keeps the gift from moving too fast on the screen)

#Achievements

*Trigger Happy Jack Frost* Implement a cooldown period after firing the cannon and restrict the cannon to firing on left-clicks only.

*More (Or Less) Into the Breech, My Friend* Display the cannon's firing speed attribute onscreen and allow the player to adjust it.

*Gift Exchange* The player should start each level with a certain number of gifts. Successfully delivering a gift to a house which hasn't received one
 should give the player a number of additional gifts to fire. Award the player points based on how many gifts they have left after completing the level.
 
*Failure Is An Option* Implement level failure if the player runs out of gifts before delivering a gift to each house. Add a new GameState that alerts the
 player of their failure and allows them to restart the level.


