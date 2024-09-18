"""
Jolie Ganzell
CSCI 3725
M3: A Markov Distinction
17 Sept 2024

Learning Objectives:
- Create a coding project that uses a Markov chain to generate visual art
- Apply your git/GitHub skills to track your changes as you go
- Explain how your personal coding project works

SCUBA diving simulator that shows various fish swimming by based on the last fish that was seen.

Dependencies: random, matplotlib, PIL
"""

import random
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation
from PIL import Image


FISH_IMAGES = {
    "Angelfish" : Image.open("/Users/jolieganzell/Library/CloudStorage/OneDrive-BowdoinCollege/semester7_fall2024/Computational Creativity/M3 Mock Dive/M3_Markov_Distinction/assets/angelfish.png"),
    "Eagle Ray" : Image.open("/Users/jolieganzell/Library/CloudStorage/OneDrive-BowdoinCollege/semester7_fall2024/Computational Creativity/M3 Mock Dive/M3_Markov_Distinction/assets/eagleray.png"),
    "Barracuda" : Image.open("/Users/jolieganzell/Library/CloudStorage/OneDrive-BowdoinCollege/semester7_fall2024/Computational Creativity/M3 Mock Dive/M3_Markov_Distinction/assets/barracuda.png"),
    "Nurse Shark" : Image.open("/Users/jolieganzell/Library/CloudStorage/OneDrive-BowdoinCollege/semester7_fall2024/Computational Creativity/M3 Mock Dive/M3_Markov_Distinction/assets/nurseshark.png"),
    "Grouper" : Image.open("/Users/jolieganzell/Library/CloudStorage/OneDrive-BowdoinCollege/semester7_fall2024/Computational Creativity/M3 Mock Dive/M3_Markov_Distinction/assets/grouper.png")
}

BACKGROUND_IMAGE = Image.open("/Users/jolieganzell/Library/CloudStorage/OneDrive-BowdoinCollege/semester7_fall2024/Computational Creativity/M3 Mock Dive/M3_Markov_Distinction/assets/reef.JPG")


class MockDive:
    def __init__(self, transition_matrix, current_fish):
        """
        Simulates the fish that you may encounter while diving that relies on a simple Markov chain.
        Args:
        - transition_matrix (dict): transition probabilities
        - current_fish (str): the current fish that you see
        """
        self.transition_matrix = transition_matrix
        self.notes = list(transition_matrix.keys())
        self.current_fish = current_fish
    
    def get_next_fish(self):
        """
        Decides which fish you will see next based on the current fish.
        """
        next_fish = random.choices(list(self.transition_matrix.keys()), weights=list(self.transition_matrix[self.current_fish].values()))
        return next_fish[0]
    
    def generate_several_fish(self, num_fish=5):
        """
        Generates a sequence of fish.
        Args:
        num_fish (int): how many fish you will see during the dive
        """
        fish_sequence = []
        while len(fish_sequence) < num_fish:
            next_fish = self.get_next_fish()
            fish_sequence.append(next_fish)
            #current_move = next_fish
        return fish_sequence
    
    def show_fish_line(self, sequence):
        """
        Prints out photos of a line of fish.
        Args:
        sequence (list): a list of strings containing the names of fish
        """
        fig, bg = plt.subplots()
        bg.axis('off')
        bg.imshow(BACKGROUND_IMAGE, extent=(0,1.5,0,1))
        i = 0.25
        for fish in sequence:
            fish_image = OffsetImage(FISH_IMAGES[fish], zoom=0.04)
            fish_bbox = AnnotationBbox(fish_image, (i, 0.5), frameon=False)
            i += 0.11
            bg.add_artist(fish_bbox)
        plt.show()

    def show_fish_video(self, sequence):
        """
        Creates a video showing a sequence of fish one fish at a time.
        Args:
        sequence (list): a list of strings containing the names of fish
        """
        fig, bg = plt.subplots()
        bg.axis('off')
        bg.imshow(BACKGROUND_IMAGE, extent=[0, 1.5, 0, 1])
        overlay_display = bg.imshow(FISH_IMAGES[self.current_fish], extent=[0.45, 1.05, 0.3, 0.7])
        def update(frame):
            overlay_display.set_data(FISH_IMAGES[frame])
            return overlay_display,
        ani = FuncAnimation(fig, update, frames=sequence, repeat=True, interval=1000)
        bg.imshow(BACKGROUND_IMAGE, extent=[0, 1.5, 0, 1], alpha=0)
        plt.show()


def main():
    dive_simulator = MockDive({
        "Angelfish": {"Angelfish": 0.3, "Barracuda": 0.2, "Grouper": 0.1, "Nurse Shark": 0.2, "Eagle Ray": 0.2},
        "Barracuda": {"Angelfish": 0.2, "Barracuda": 0.2, "Grouper": 0.2, "Nurse Shark": 0.3, "Eagle Ray": 0.1},
        "Grouper": {"Angelfish": 0.3, "Barracuda": 0.1, "Grouper": 0.3, "Nurse Shark": 0.2, "Eagle Ray": 0.1},
        "Nurse Shark": {"Angelfish": 0.2, "Barracuda": 0.2, "Grouper": 0.2, "Nurse Shark": 0.1, "Eagle Ray": 0.3},
        "Eagle Ray": {"Angelfish": 0.3, "Barracuda": 0.1, "Grouper": 0.3, "Nurse Shark": 0.2, "Eagle Ray": 0.1}
    }, current_fish = "Angelfish")
    
    new_dive = dive_simulator.generate_several_fish(num_fish=10)
    dive_simulator.show_fish_video(new_dive)

if __name__ == "__main__":
    main()