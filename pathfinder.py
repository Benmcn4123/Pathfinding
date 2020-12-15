import pygame, sys
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("A* pathfinding")

draw_state = "wall"

start = (20, 20)
end = (40, 40)

path_nodes = []

walls = []
mouse_down = False

def calc_path(end, start):
    global win, walls

    path_points = []
    dead_points = []
    current_points = [start]

    ended = False

    progenitors = {}

    def get_surrounding_points(point, blocks):
        points = []
        edges = [(point[0] + 1, point[1]), (point[0] - 1, point[1]), (point[0], point[1] + 1), (point[0], point[1] - 1), (point[0] + 1, point[1] - 1), (point[0] + 1, point[1] + 1), (point[0] - 1, point[1] + 1), (point[0] - 1, point[1] - 1)]
        for edge in edges:
            if not edge in blocks:
                points.append(edge)
        return points

    ended = False
    while not ended:
        surrounding_points = []
        new_current_points = current_points[:]

        for current_point in current_points[:]:
            current_points = []
            for surrounding_point in get_surrounding_points(current_point, new_current_points + walls + dead_points):
                new_current_points.append(surrounding_point)
                progenitors[surrounding_point] = current_point
                if end in new_current_points:
                    ended = True
            dead_points.append(current_point)
        current_points = new_current_points[:]

    stop = False
    current_point = end
    while not stop:
        current_point = progenitors[current_point]
        if current_point == start:
            stop = True
        path_points.append(current_point)

    return path_points

while True:
    win.fill((255, 255, 255))

    mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    cell_pos = (round(mouse_pos[0] / 10), round(mouse_pos[1] / 10))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                draw_state = "start"
            if event.key == K_b:
                draw_state = "end"
            if event.key == K_c:
                draw_state = "wall"
            if event.key == K_BACKSPACE:
                walls = []
                path_nodes = []
            if event.key == K_RETURN:
                path_nodes = calc_path(end, start)
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            if draw_state == "start":
                start = cell_pos
                visible_start = cell_pos
            elif draw_state == "end":
                end = cell_pos
                visible_end = cell_pos
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False

    if mouse_down and draw_state == "wall" and not cell_pos in walls:
        walls.append(cell_pos)

    for wall in walls:
        pygame.draw.rect(win, (0, 0, 0), (wall[0] * 10 - 5, wall[1] * 10 - 5, 10, 10))

    if path_nodes != None:
        for node in path_nodes:
            pygame.draw.rect(win, (0, 200, 0), (node[0] * 10 - 5, node[1] * 10 - 5, 10, 10))

    pygame.draw.rect(win, (200, 0, 0), (end[0] * 10 - 5, end[1] * 10 - 5, 10, 10))
    pygame.draw.rect(win, (0, 0, 200), (start[0] * 10 - 5, start[1] * 10 - 5, 10, 10))

    clock.tick(60)
    pygame.display.update()
