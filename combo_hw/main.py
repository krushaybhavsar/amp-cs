import random
from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile


def create_hexagon(position, radius=50, flat_top=False, id=0) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, color=(0, 0, 0), id=id)


def get_random_color(min_=150, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB color with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))


def init_hexagons(num_x=20, num_y=20, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=(-50, -50), flat_top=flat_top, id=0)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top, id=0)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(
                position,
                flat_top=flat_top,
                id=int((position[0] + position[1]) // 10),
            )
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((0, 0, 0))
    for hexagon in hexagons:
        hexagon.render(screen)

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    # colliding_hexagons = [
    #     hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    # ]

    # check for user click and set is_selected to True for all colliding hexagons

    for hexagon in hexagons:
        # for neighbour in hexagon.compute_neighbours(hexagons):
        #     neighbour.render_highlight(screen, border_color=(255, 255, 255))
        if hexagon.selected:
            hexagon.set_color((100, 100, 0))
        else:
            hexagon.set_color((0, 0, 0))
        hexagon.render_highlight(screen, border_color=(255, 255, 255))
    pygame.display.flip()


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=True)
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for hexagon in hexagons:
                    if hexagon.collide_with_point(event.pos):
                        hexagon.set_selected(not hexagon.get_selected())

        for hexagon in hexagons:
            hexagon.update()

        render(screen, hexagons)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
