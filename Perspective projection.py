import pygame as pg
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np

# pygame setup
pg.init()
X = 1080
Y = 720

pg.display.set_caption("3D Projection")
screen = pg.display.set_mode((X, Y))
clock = pg.time.Clock()

rpm_slider = Slider(screen, int(X / 2 - X / 10) , int(Y - Y / 10), X / 5, int(Y / 75), min = 0, max = 100, step=((100)/100))
focal_slider = Slider(screen, int(X / 2 - X / 10 + X / 3) , int(Y - Y / 10), X / 5, int(Y / 75), min = 0, max = 200, step=((100)/100))
z0_slider = Slider(screen, int(X / 2 - X / 10 - X / 3) , int(Y - Y / 10), X / 5, int(Y / 75), min = 0, max = 500, step=((100)/100))

font = pg.font.Font('freesansbold.ttf', 32)
rpm_text = font.render('RPM: ' + str(rpm_slider.getValue()), True, (0,0,0), (255,255,255))
focal_text = font.render('RPM: ' + str(focal_slider.getValue()), True, (0,0,0), (255,255,255))
z0_text = font.render('z0: ' + str(z0_slider.getValue()), True, (0,0,0), (255,255,255))

rpm_textRect = rpm_text.get_rect()
rpm_textRect.center = (X / 2, Y - Y / 30)

focal_textRect = focal_text.get_rect()
focal_textRect.center = (X / 2 + X / 3, Y - Y / 30)

z0_textRect = focal_text.get_rect()
z0_textRect.center = (X / 2 - X / 3, Y - Y / 30)


fps = 60
theta = 0
rpm = 10
z0 = 256
focal = 64
running = True
centre = [screen.get_width() / 2, screen.get_height() / 2]

vertex_table_cube = [[63, 63, 63],
                [63, -63, 63],
                [-63, -63, 63],
                [-63, 63, 63],
                [63, 63, -63],
                [63, -63, -63],
                [-63, -63, -63],
                [-63, 63, -63]]

vertex_table_pyramid = [[63, 63, 63],
                [-63, 63, 63],
                [63, 63, -63],
                [-63, 63, -63],
                [0, -63, 0]]



edge_table_cube = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]

edge_table_pyramid = [[0, 1], [0, 2], [3, 1], [3, 2],
                      [0, 4], [1, 4], [2, 4], [3, 4]]



def perspective_projection(vertex: list[int, int, int], focal_length: int, scale: int = None) -> list[int, int]:
    if scale == None:
        scale = 1

    x, y, z = vertex

    x_projected = scale * x * focal_length / \
        (z + focal_length + z0) + centre[0]
    y_projected = scale * y * focal_length / \
        (z + focal_length + z0) + centre[1]

    return [x_projected, y_projected]

while running:

    # Update the clock frequency
    clock.tick(fps)
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    
    rpm_text = font.render('RPM: ' + str(rpm_slider.getValue()), True, (0,0,0), (255,255,255))
    focal_text = font.render('focal: ' + str(focal_slider.getValue()), True, (0,0,0), (255,255,255))
    z0_text = font.render('z0: ' + str(z0_slider.getValue()), True, (0,0,0), (255,255,255))

    screen.blit(rpm_text, rpm_textRect)
    screen.blit(focal_text, focal_textRect)
    screen.blit(z0_text, z0_textRect)
    
    rpm = rpm_slider.getValue()
    focal = focal_slider.getValue()
    z0 = z0_slider.getValue()
    
    pygame_widgets.update(events)

    rotation_x = [[1, 0, 0],
                   [0, np.cos(theta), -np.sin(theta)],
                   [0, np.sin(theta) , np.cos(theta)]]
    
    rotation_y = [[np.cos(theta), 0, np.sin(theta)],
                   [0, 1, 0],
                   [-np.sin(theta) ,0 , np.cos(theta)]]
    
    rotation_z = [[np.cos(theta), -np.sin(theta), 0],
                   [np.sin(theta), np.cos(theta), 0],
                   [0, 0, 1]]
    

    rotation_x = np.array(rotation_x)
    rotation_y = np.array(rotation_y)
    rotation_z = np.array(rotation_z)
    
    
    vertex_table = np.array(vertex_table_pyramid)
    #vertex_table = np.matmul(vertex_table, rotation_x)
    vertex_table = np.matmul(vertex_table, rotation_y)
    #vertex_table = np.matmul(vertex_table, rotation_z)
    projection_points = []

    for point in vertex_table:
        projection_points.append(perspective_projection(point, focal, 15))

    for point in projection_points:
        pg.draw.circle(screen, 'black', point, 5)

    for edge in edge_table_pyramid:
        pg.draw.line(screen, 'black',
                     projection_points[edge[0]], projection_points[edge[1]])

    theta += 2*np.pi*rpm/3600

    # update() the display to put your work on screen
    pg.display.update()

pg.quit()