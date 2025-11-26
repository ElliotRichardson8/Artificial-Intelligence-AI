import initial, fitness, selection, crossover, mutation
import pose_generator, plot_spider_pose

import os, cv2

import numpy as np
import matplotlib.pyplot as plt

IMAGE_FOLDER = "gait/"

DEFAULT_POPULATION_SIZE = 50
DEFAULT_MUTATION_RATE = 0.005
DEFAULT_GENERATIONS_PER_FRAME = 100

class GaitGenerator:
    def __init__(
        self,
        population_size=DEFAULT_POPULATION_SIZE,
        mutation_rate=DEFAULT_MUTATION_RATE,
        generations_per_frame=DEFAULT_GENERATIONS_PER_FRAME
    ):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations_per_frame = generations_per_frame

        self.population = initial.initial_population(population_size)
        assert len(self.population) == self.population_size

        self.pose_generator = pose_generator.PoseGenerator(
            population_size=population_size,
            mutation_rate=mutation_rate
        )
        self.frames = np.zeros((300, 8, 3))
        self.frame = 0

    def set_current_frame(self, chromosome):
        assert np.shape(chromosome) == (8,3)
        self.frames[self.frame] = chromosome

    def save_frame(self):
        plot_spider_pose.save_spider_pose(
            self.frames[self.frame],
            f"gait/frame_{self.frame}"
        )

    def next_frame(self):
        self.pose_generator.perform_generations(self.generations_per_frame)
        chromosome, fitness = self.pose_generator.get_fittest()
        self.set_current_frame(chromosome)
        self.save_frame()
        self.pose_generator = pose_generator.PoseGeneratorDynamic(
            chromosome,
            self.population_size,
            self.mutation_rate
        )
        self.frame += 1

    def generate_frames(self, n):
        for i in range(n):
            self.next_frame()

# copied a lot of this off stackoverflow
def export_video(video_name):
    video_name += ".avi"

    images = [img for img in os.listdir(IMAGE_FOLDER)
     if img.startswith("frame_") and img.endswith(".png")]

    images.sort()

    frame = cv2.imread(os.path.join(IMAGE_FOLDER, images[0]))
    height,width,layers = frame.shape

    video = cv2.VideoWriter(
        os.path.join(IMAGE_FOLDER, video_name) ,
         0, 
         1, 
         (width, height)
    )

    for image in images:
        video.write(cv2.imread(os.path.join(IMAGE_FOLDER, image)))

    cv2.destroyAllWindows()
    video.release()

gg = GaitGenerator()
print("Frame 0")
gg.next_frame()
print("Frame 1")
gg.next_frame()