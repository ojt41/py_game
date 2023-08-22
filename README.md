# Collecting Game

This is a simple game created using the Pygame library. The objective of the game is to control a robot to collect coins while avoiding monsters. The robot can move using the arrow keys and must collect coins scattered around the screen. If the robot collides with a monster, the player loses 2 coins and is knocked back to prevent continuous collisions. The game continues until the player either collects all the coins (50 or more) or runs out of coins (0 or fewer).

## How to Play

1. Make sure you have Python and the Pygame library installed.
2. Download the game assets: `robot.png`, `coin.png`, and `monster.png`.
3. Save the downloaded images in the same directory as the game script.
4. Run the script 

## Instructions

- Use the arrow keys to control the robot's movement.
- The objective is to collect coins while avoiding monsters.
- Colliding with a monster deducts 2 coins and knocks the robot away.
- The robot is invincible for the first 3 seconds.
- The game ends when you either collect all the coins (50 or more) or run out of coins (0 or fewer).
- If you lose or win, press 'R' to restart the game or 'Q' to quit.

## Gameplay

1. Run the script to start the game.
2. Follow the instructions displayed on the screen.
3. Control the robot's movement using the arrow keys.
4. Collect coins and avoid monsters.
5. Check the "Collected Coins" count at the top-left corner.
6. If you run out of coins, the game is over.
7. Press 'R' to restart or 'Q' to quit.
8. If you collect 50 or more coins, you win!
9. Press 'R' to restart or 'Q' to quit.

## Customization

Feel free to adjust the game constants in the script to modify the game's difficulty and behavior. You can change values like `constant_width`, `constant_height`, `robot_velocity`, `number_of_monsters`, and `knock_distance` to experiment with different settings.
