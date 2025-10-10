import pygame
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from PIL import Image
import yaml
from f110_gym.envs.collision_models import get_vertices

ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1 / ZOOM_IN_FACTOR
CAR_LENGTH = 0.58
CAR_WIDTH = 0.31


class EnvRenderer:
    """Pygame + PyOpenGL renderer for F1TENTH"""

    def __init__(self, width=1280, height=720):
        pygame.init()
        pygame.display.set_caption("F1TENTH Gym Renderer")
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL | RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        glClearColor(9 / 255, 32 / 255, 87 / 255, 1.0)
        glEnable(GL_DEPTH_TEST)

        self.left = -width / 2
        self.right = width / 2
        self.bottom = -height / 2
        self.top = height / 2
        self.zoom_level = 1.2
        self.zoomed_width = width
        self.zoomed_height = height

        self.map_points = None
        self.poses = None
        self.cars = []
        self.font = pygame.font.SysFont("Arial", 24)

    # ---------------------------------------------------------------------
    def update_map(self, map_path, map_ext):
        with open(map_path + ".yaml", "r") as yaml_stream:
            map_metadata = yaml.safe_load(yaml_stream)
            res = map_metadata["resolution"]
            origin = map_metadata["origin"]
            origin_x, origin_y = origin[:2]

        img = np.array(Image.open(map_path + map_ext).transpose(Image.FLIP_TOP_BOTTOM))
        h, w = img.shape[0], img.shape[1]

        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        map_x = (map_x * res + origin_x).flatten()
        map_y = (map_y * res + origin_y).flatten()
        map_z = np.zeros_like(map_y)
        mask = (img == 0).flatten()
        self.map_points = 50.0 * np.vstack((map_x[mask], map_y[mask], map_z[mask])).T

    # ---------------------------------------------------------------------
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.VIDEORESIZE:
                w, h = e.w, e.h
                pygame.display.set_mode((w, h), DOUBLEBUF | OPENGL | RESIZABLE)
                glViewport(0, 0, w, h)
            elif e.type == pygame.MOUSEWHEEL:
                f = ZOOM_IN_FACTOR if e.y > 0 else ZOOM_OUT_FACTOR
                self.zoom_level *= f
                self.left *= f
                self.right *= f
                self.bottom *= f
                self.top *= f

    # ---------------------------------------------------------------------
    def update_obs(self, obs):
        self.ego_idx = obs["ego_idx"]
        poses_x, poses_y, poses_theta = (
            obs["poses_x"],
            obs["poses_y"],
            obs["poses_theta"],
        )
        poses = np.stack((poses_x, poses_y, poses_theta)).T
        self.poses = poses

    # ---------------------------------------------------------------------
    def draw_map(self):
        if self.map_points is None:
            return
        glBegin(GL_POINTS)
        glColor3f(0.7, 0.75, 0.9)
        for x, y, z in self.map_points:
            glVertex3f(x, y, z)
        glEnd()

    # ---------------------------------------------------------------------
    def draw_cars(self):
        if self.poses is None:
            return
        for j, pose in enumerate(self.poses):
            verts = 50.0 * get_vertices(pose, CAR_LENGTH, CAR_WIDTH)
            (
                glColor3f(0.67, 0.38, 0.72)
                if j == self.ego_idx
                else glColor3f(0.4, 0.2, 0.4)
            )
            glBegin(GL_QUADS)
            for v in verts:
                glVertex2f(v[0], v[1])
            glEnd()

    # ---------------------------------------------------------------------
    def render(self, laptime=0.0, count=0):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.left, self.right, self.bottom, self.top, 1, -1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.draw_map()
        self.draw_cars()

        # Overlay FPS + Lap info
        fps_text = f"Lap Time: {laptime:.2f}, Lap Count: {count:.0f}, FPS: {self.clock.get_fps():.1f}"
        text_surface = self.font.render(fps_text, True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glWindowPos2d(10, 10)
        glDrawPixels(
            text_surface.get_width(),
            text_surface.get_height(),
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            text_data,
        )

        pygame.display.flip()
        self.clock.tick(60)

    # ---------------------------------------------------------------------
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
        pygame.quit()
