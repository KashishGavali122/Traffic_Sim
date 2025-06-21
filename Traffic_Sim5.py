import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚦 Smart Traffic Light Simulation (Realistic Mode)")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
CAR_COLOR = (200, 200, 255)

# Directions
NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
DIRECTION_NAMES = ["North", "South", "East", "West"]

# Font
font = pygame.font.SysFont('Arial', 22)

# Initial traffic counts
vehicle_counts = {
    NORTH: random.randint(1, 5),
    SOUTH: random.randint(1, 5),
    EAST: random.randint(1, 5),
    WEST: random.randint(1, 5)
}

# Current green light
current_green = NORTH
green_duration = 5
yellow_duration = 1
light_state = "GREEN"
last_switch_time = time.time()
last_spawn_time = time.time()

# Vehicle positions for animation
vehicle_positions = {
    NORTH: [],
    SOUTH: [],
    EAST: [],
    WEST: []
}


def draw_intersection():
    pygame.draw.rect(screen, GRAY, (300, 0, 200, HEIGHT))  # Vertical road
    pygame.draw.rect(screen, GRAY, (0, 250, WIDTH, 100))   # Horizontal road


def draw_traffic_lights():
    coords = [(370, 150), (370, 430), (180, 320), (620, 320)]
    for i, (x, y) in enumerate(coords):
        if i == current_green:
            color = GREEN if light_state == "GREEN" else YELLOW if light_state == "YELLOW" else RED
        else:
            color = RED
        pygame.draw.circle(screen, color, (x, y), 20)


def update_traffic():
    global current_green, last_switch_time, vehicle_counts, last_spawn_time, light_state

    current_time = time.time()
    time_elapsed = current_time - last_switch_time

    if light_state == "GREEN" and time_elapsed >= green_duration:
        light_state = "YELLOW"
        last_switch_time = current_time

    elif light_state == "YELLOW" and time_elapsed >= yellow_duration:
        # Choose the busiest direction
        busiest = max(vehicle_counts, key=lambda k: vehicle_counts[k])
        current_green = busiest
        light_state = "GREEN"
        last_switch_time = current_time

    # Remove one vehicle per second if green
    if light_state == "GREEN" and vehicle_counts[current_green] > 0:
        if int(time_elapsed) > 0:
            vehicle_counts[current_green] -= 1

    # Spawn new vehicles
    if current_time - last_spawn_time >= 2:
        for direction in vehicle_counts:
            if random.random() < 0.7:
                vehicle_counts[direction] += 1
        last_spawn_time = current_time


def draw_vehicles():
    spacing = 30
    for direction in vehicle_counts:
        for i in range(vehicle_counts[direction]):
            if direction == NORTH:
                x = 400
                y = 50 + i * spacing
            elif direction == SOUTH:
                x = 430
                y = 550 - i * spacing
            elif direction == EAST:
                x = 750 - i * spacing
                y = 330
            else:  # WEST
                x = 50 + i * spacing
                y = 270
            pygame.draw.rect(screen, CAR_COLOR, (x, y, 20, 15))


def draw_text():
    texts = [
        f"North: {vehicle_counts[NORTH]}",
        f"South: {vehicle_counts[SOUTH]}",
        f"East:  {vehicle_counts[EAST]}",
        f"West:  {vehicle_counts[WEST]}",
        f"Green Light: {DIRECTION_NAMES[current_green]} ({light_state})",
    ]

    if light_state == "GREEN":
        countdown = max(0, green_duration - (time.time() - last_switch_time))
    elif light_state == "YELLOW":
        countdown = max(0, yellow_duration - (time.time() - last_switch_time))
    else:
        countdown = 0

    texts.append(f"Time Left: {countdown:.1f}s")
    texts.append("Smart Traffic Light System (Realistic Mode)")

    for i, line in enumerate(texts):
        surface = font.render(line, True, WHITE)
        screen.blit(surface, (20, 20 + i * 30))


def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_traffic()
        draw_intersection()
        draw_traffic_lights()
        draw_vehicles()
        draw_text()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
