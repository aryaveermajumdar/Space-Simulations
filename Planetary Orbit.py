import pygame
import math

grav = 6.674e-11
anchor_mass = 1.989e30
delta = 100000

win_w = 800
win_h = 600
mid_x = win_w // 2
mid_y = win_h // 2

metric_to_pixel = 8e8

core_r = 30
body_r = 8

def pull_number(msg, fallback):
    try:
        raw = input(f"{msg} [default = {fallback}]: ")
        return float(raw) if raw.strip() != "" else fallback
    except ValueError:
        return fallback

print(" ")
print("ORBITAL SIMULATION SETUP")

dist_au = pull_number("Initial distance from Sun (AU)", 1.0)
tan_kms = pull_number("Tangential velocity (kms-1)", 24.0)
rad_kms = pull_number("Radial velocity (kms-1, inward negative)", 0.0)

pos_x = dist_au * 1.496e11
pos_y = 0.0
vel_x = rad_kms * 1e3
vel_y = tan_kms * 1e3

def grav_field(px, py):
    sep2 = px * px + py * py
    if sep2 == 0:
        return 0.0, 0.0
    sep = math.sqrt(sep2)
    coeff = -grav * anchor_mass / (sep ** 3)
    return coeff * px, coeff * py

def stepper(px, py, vx, vy, dt):
    ax1, ay1 = grav_field(px, py)
    dx1, dy1 = vx * dt, vy * dt
    dvx1, dvy1 = ax1 * dt, ay1 * dt

    ax2, ay2 = grav_field(px + dx1 / 2, py + dy1 / 2)
    dx2, dy2 = (vx + dvx1 / 2) * dt, (vy + dvy1 / 2) * dt
    dvx2, dvy2 = ax2 * dt, ay2 * dt

    ax3, ay3 = grav_field(px + dx2 / 2, py + dy2 / 2)
    dx3, dy3 = (vx + dvx2 / 2) * dt, (vy + dvy2 / 2) * dt
    dvx3, dvy3 = ax3 * dt, ay3 * dt

    ax4, ay4 = grav_field(px + dx3, py + dy3)
    dx4, dy4 = (vx + dvx3) * dt, (vy + dvy3) * dt
    dvx4, dvy4 = ax4 * dt, ay4 * dt

    px += (dx1 + 2 * dx2 + 2 * dx3 + dx4) / 6
    py += (dy1 + 2 * dy2 + 2 * dy3 + dy4) / 6
    vx += (dvx1 + 2 * dvx2 + 2 * dvx3 + dvx4) / 6
    vy += (dvy1 + 2 * dvy2 + 2 * dvy3 + dvy4) / 6

    return px, py, vx, vy

pygame.init()
panel = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Elliptical Orbit Simulator")
ticker = pygame.time.Clock()

trace = []
alive = True

while alive:
    ticker.tick(60)

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            alive = False
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_q:
            alive = False

    pos_x, pos_y, vel_x, vel_y = stepper(pos_x, pos_y, vel_x, vel_y, delta)
    trace.append((pos_x, pos_y))

    if len(trace) > 8000:
        trace.pop(0)

    panel.fill((0, 0, 0))

    pygame.draw.circle(panel, (255, 190, 0), (mid_x, mid_y), core_r)

    if len(trace) > 1:
        path = [
            (mid_x + int(tx / metric_to_pixel), mid_y + int(ty / metric_to_pixel))
            for tx, ty in trace
        ]
        pygame.draw.lines(panel, (130, 130, 130), False, path, 1)

    pygame.draw.circle(
        panel,
        (100, 150, 255),
        (mid_x + int(pos_x / metric_to_pixel), mid_y + int(pos_y / metric_to_pixel)),
        body_r
    )

    pygame.display.flip()

pygame.quit()
