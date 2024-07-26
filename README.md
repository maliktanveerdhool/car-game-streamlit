# car-game-streamlit

Stylized Car Racing Game
This is a simple, stylized car racing game built with Python, utilizing Streamlit for the web interface and Pygame for game mechanics and rendering.
Technologies and Tools Used

Python: The core programming language used for the game logic and interface.
Streamlit: A powerful web app framework for Python, used to create the interactive user interface.
Pygame: A set of Python modules designed for writing video games, used for game rendering and mechanics.
Pillow (PIL): Python Imaging Library, used for image processing and conversion between Pygame surfaces and Streamlit-compatible images.
NumPy: Used for efficient array operations, particularly in image processing.

Game Description
This Stylized Car Racing Game is a simple yet engaging web-based game where players control a car, trying to avoid obstacles while increasing their speed and score.
Key Features:

Simple Controls: Players can move left or right, accelerate, and brake using on-screen buttons.
Obstacle Avoidance: The main challenge is to avoid other cars on the road.
Speed Mechanics: Players can increase or decrease their speed, affecting both score accumulation and game difficulty.
Score System: The game keeps track of the current score and high score.
Stylized Graphics: Instead of complex sprites, the game uses simple, geometric shapes for a clean, modern look.
Responsive Design: The game adapts to different screen sizes thanks to Streamlit's responsive layout.

How to Play:

Use the "Left" and "Right" buttons to move the car horizontally.
Press "Accelerate" to increase speed and "Brake" to slow down.
Avoid colliding with other cars on the road.
Try to survive as long as possible to increase your score.
If you collide with an obstacle, the game ends.
Press "Restart" to begin a new game.

Technical Implementation:

The game loop runs within a Streamlit app, updating the game state on each iteration.
Pygame is used to render the game graphics, which are then converted to a format that Streamlit can display.
The illusion of movement is created by scrolling the road markings and moving obstacles based on the player's speed.
Game state is managed using Streamlit's session state, allowing for persistent data between reruns.

This game demonstrates the integration of a real-time game engine (Pygame) within a web application framework (Streamlit), showcasing how traditional game development techniques can be adapted for web-based deployments.
