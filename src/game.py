import cv2 as cv
import numpy as np
from typing import List
from handDetection import HandDetector
import utils as utils

class Game:
    def __init__(self) -> None:
        """
        Initialize the Game class.

        This constructor initializes the video capture, hand detector, game assets,
        and game state variables.

        Args:
            None

        Returns:
            None
        """
        self.cap: cv.VideoCapture = cv.VideoCapture(2)
        self.hd: HandDetector = HandDetector(detectionCon=0.7)

        self.width: int = 640
        self.height: int = 480
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)

        self.load_assets()
        self.initialize_game_state()

    def load_assets(self) -> None:
        """
        Load game assets.

        Load and resize game images (ball, plataform, game over screen).

        Args:
            None

        Returns:
            None
        """
        self.ball: np.ndarray = cv.resize(cv.imread('assets/ball.png', cv.IMREAD_UNCHANGED), (40, 40))
        self.plataform: np.ndarray = cv.resize(cv.imread('assets/plataform.png', cv.IMREAD_UNCHANGED), (120, 26))
        self.gameover: np.ndarray = cv.resize(cv.imread('assets/gameover.png', cv.IMREAD_UNCHANGED), (self.width, self.height))

    def initialize_game_state(self) -> None:
        """
        Initialize game state variables.

        Set the initial values for position, speed, and score.

        Args:
            None

        Returns:
            None
        """
        self.position: List[int] = [50, 50]
        self.speedx: int = 15
        self.speedy: int = 15
        self.score: int = 0

    def process_hands(self, hands: List[dict]) -> None:
        """
        Process hand gestures.

        Analyze hand gestures to determine plataform movement and update the game state accordingly.

        Args:
            hands (List[dict]): List of hand information dictionaries

        Returns:
            None
        """
        if hands:
            bbox: dict = hands[0]['bbox']
            x, y, w, h = bbox
            h1, w1, c = self.plataform.shape
            x1: int = x - h1 // 2
            x1 = np.clip(x1, 5, 510)
            self.image = utils.overlayPNG(self.image, self.plataform, [x1, 447])

            if self.position[1] < 50:
                self.speedy = -self.speedy
                self.position[0] -= 10

            if x1 - 10 < self.position[0] < x1 + w1 and 380 < self.position[1] < 380 + h1:
                self.speedy = -self.speedy
                self.position[0] += 30
                self.score += 1

    def update_position(self) -> None:
        """
        Update ball position and check game over condition.

        Update ball position based on speed and direction, and handle game over condition.

        Args:
            None

        Returns:
            None
        """
        if self.position[1] > 400:
            self.image = self.gameover
            # Display game over message and instructions
            utils.putTextRect(self.gameover, f'Final score {self.score}', [300, 190], 1.9, 2, colorR=(0, 0, 0))
            utils.putTextRect(self.gameover, 'Press R to restart', [290, 305], 1.82, 2, colorR=(0, 0, 0))
            utils.putTextRect(self.gameover, 'Press Esc to quit', [290, 345], 1.82, 2, colorR=(0, 0, 0))
        else:
            if self.position[0] >= 560 or self.position[0] <= 20:
                self.speedx = -self.speedx
            self.position[0] += self.speedx
            self.position[1] += self.speedy

    def run(self) -> None:
        """
        Main game loop.

        Run the game loop that processes user input, updates game state, and displays the game frame.

        Args:
            None

        Returns:
            None
        """
        while True:
            ret, self.image = self.cap.read()
            self.image = cv.flip(self.image, 1)

            cv.rectangle(self.image, (0, self.height), (self.width, 0), (0, 0, 255), 8)
            cv.rectangle(self.image, (0, self.height - 40), (self.width, self.height), (0, 255, 255), 6)

            hands, self.image = self.hd.findHands(self.image, flipType=True)
            self.process_hands(hands)
            self.update_position()

            utils.putTextRect(self.image, f'Score {self.score}', [270, 30], 1.5)
            try:
                self.image = utils.overlayPNG(self.image, self.ball, self.position)
                cv.imshow('frame', self.image)
                key = cv.waitKey(1)
            except:
                break

            if key in [ord('r'), ord('R')]:
                self.initialize_game_state()  # Reset game state
                self.load_assets()            # Reload game assets
            elif key == 27:  # 27 is the ASCII code for the 'Esc' key
                break

if __name__ == "__main__":
    game = Game()
    game.run()
