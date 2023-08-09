# AR-PONG: Augmented Reality Pong Game

AR-PONG is an interactive game where players control the paddle using hand gestures captured by a webcam. The game ball bounces between the paddle and the top wall, and players earn points by keeping the ball in play. This game is designed to be run using Docker to ensure consistent dependencies and a seamless execution experience.

## Getting Started
Follow these steps to get AR-PONG up and running on your machine:
1. Clone this repository to your local machine.
2. Ensure you have Docker installed.
3. Open a terminal and navigate to the cloned repository's root directory.
4. Run the run.sh script with appropriate arguments (see Usage).


## Usage
To run AR-PONG using Docker, execute the following command in the terminal:
```./run.sh <docker-image-name> <camera-source-value>```
Replace <docker-image-name> with the name of the Docker image you want to use and <camera-source-value> with the value of the camera source you want to use (e.g., 0 for the default camera). This script will start the Docker container with the appropriate configurations.

## License
This project is licensed under the MIT License.

---

Have fun playing AR-PONG and enjoy the unique experience of controlling the game with your hands in augmented reality!




