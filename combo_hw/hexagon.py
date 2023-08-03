from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple

import pygame


@dataclass
class HexagonTile:
    """Hexagon class"""

    radius: float
    position: Tuple[float, float]
    color: Tuple[int, ...]
    highlight_offset: int = 3
    max_highlight_ticks: int = 15
    selected: bool = False
    id: int = 0

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0
        self.font = pygame.font.SysFont("Arial", 13)
        self.text = self.font.render(str(self.id), True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.centre)

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]

    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        # could cache results for performance
        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, self.highlight_color, self.vertices)
        # draw id in centre of hexagon
        screen.blit(self.text, self.text_rect)

    def render_highlight(self, screen, border_color) -> None:
        """Draws a border around the hexagon with the specified color"""
        self.highlight_tick = self.max_highlight_ticks
        # pygame.draw.polygon(screen, self.highlight_color, self.vertices)
        pygame.draw.aalines(screen, border_color, closed=True, points=self.vertices)

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_color(self) -> Tuple[int, ...]:
        """color of the hexagon tile when rendering highlight"""
        # offset = self.highlight_offset * self.highlight_tick
        # brighten = lambda x, y: x + y if x + y < 255 else 255
        # return tuple(brighten(x, offset) for x in self.color)
        return self.color

    def set_selected(self, selected: bool) -> None:
        """Sets the selected attribute to the specified value"""
        self.selected = selected

    def get_selected(self) -> bool:
        """Returns the selected attribute"""
        return self.selected

    def set_color(self, color: Tuple[int, ...]) -> None:
        """Sets the color attribute to the specified value"""
        self.color = color

    def get_color(self) -> Tuple[int, ...]:
        """Returns the color attribute"""
        return self.color

    def set_id(self, id: int) -> None:
        """Sets the id attribute to the specified value"""
        self.id = id

    def get_id(self) -> int:
        """Returns the id attribute"""
        return self.id


class FlatTopHexagonTile(HexagonTile):
    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x + self.radius / 2, y + self.minimal_radius)
