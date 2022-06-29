# Maze_generator

Algorithm generating and solving a maze on triangular grid.

Step 1:

Generates triangular grid by creating instances of class Triangle containing informations such as coordinates and radius of the circumscribed circle centre direction of the triangle (facing upwards or downwards) and indices on a grid.


![triangular_grid](https://user-images.githubusercontent.com/67229687/176331693-317eced0-1fe2-4402-ba1c-76c4fc9fa33e.png)

Step 2:

Carves a labyrinth on the grid by traversing it and erasing the walls standing on our way.

![carved_lab](https://user-images.githubusercontent.com/67229687/176331812-a73a7675-1b88-4383-8e3a-b8867f07afc5.png)

Step 3:

Chooses random entrance end exit point and erases two walls accordingly.

![entrances_lab](https://user-images.githubusercontent.com/67229687/176332045-97f703cd-7996-4ce3-9b5e-dc329ced57cd.png)


Step 4:

Using A* algorithm implementation solves the maze and draws the solution.

![maze](https://user-images.githubusercontent.com/67229687/176332257-bf17bb8b-6d25-4a16-be59-958460e9dabd.png)
