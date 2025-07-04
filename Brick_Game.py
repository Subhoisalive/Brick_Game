import pygame
import cv2
import mediapipe as mp
import sys
import threading
import random
import os

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Out - Gesture Powered")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 30, bold=True)

# Colors
WHITE, RED, GREEN, BLUE, BLACK, YELLOW, ORANGE, CYAN, PURPLE = (
    (255, 255, 255), (255, 0, 0), (0, 255, 0), (50, 50, 255), (0, 0, 0),
    (255, 255, 0), (255, 165, 0), (0, 255, 255), (128, 0, 128))

# Background
background_image = pygame.Surface((WIDTH, HEIGHT))
background_image.fill((20, 20, 30))

# Game Variables
MAX_LEVELS = 50
high_scores_file = "scores.txt"
paddle_x_from_cam = 300

# Power-Up Class
class PowerUp:
    def __init__(self, x, y, kind):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.kind = kind
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        color = YELLOW if self.kind == "life" else CYAN if self.kind == "multi" else ORANGE
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        label = font.render(self.kind[0].upper(), True, BLACK)
        screen.blit(label, (self.rect.x + 2, self.rect.y))

# Brick Generator
BRICK_COLORS = [RED, GREEN, BLUE, PURPLE, ORANGE]
def generate_bricks(level):
    new_bricks = []
    rows = min(3 + level // 5, 12)
    for row in range(rows):
        for col in range(10):
            x = col * 75 + 20
            y = row * 35 + 50
            brick = pygame.Rect(x, y, 70, 30)
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            new_bricks.append((brick, color))
    return new_bricks

# Scoreboard Functions
def update_high_scores(current_score):
    scores = []
    if os.path.exists(high_scores_file):
        with open(high_scores_file, 'r') as f:
            scores = [int(line.strip()) for line in f.readlines()]
    scores.append(current_score)
    scores = sorted(scores, reverse=True)[:3]
    with open(high_scores_file, 'w') as f:
        for s in scores:
            f.write(f"{s}\n")
    return scores

# Webcam Thread
def webcam_thread():
    global paddle_x_from_cam
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * WIDTH)
            paddle_x_from_cam = x - 75
        cv2.imshow("Gesture Control - Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

threading.Thread(target=webcam_thread, daemon=True).start()

# Main Game Loop
level, score, lives = 1, 0, 3
while True:
    bricks = generate_bricks(level)
    balls = [pygame.Rect(400, 300, 15, 15)]
    ball_speed = [[4, -4]]
    power_ups = []
    paddle = pygame.Rect(325, 550, 150, 15)
    running = True

    while running:
        screen.blit(background_image, (0, 0))
        paddle.x = max(0, min(paddle_x_from_cam, WIDTH - paddle.width))
        pygame.draw.rect(screen, BLUE, paddle, border_radius=10)

        for i, b in enumerate(balls):
            b.x += ball_speed[i][0]
            b.y += ball_speed[i][1]
            pygame.draw.ellipse(screen, RED, b)

            if b.left <= 0 or b.right >= WIDTH:
                ball_speed[i][0] *= -1
            if b.top <= 0:
                ball_speed[i][1] *= -1
            if b.bottom >= HEIGHT:
                lives -= 1
                balls[i].x, balls[i].y = WIDTH // 2, HEIGHT // 2
                ball_speed[i] = [random.choice([-4, 4]), -4]

            if b.colliderect(paddle):
                ball_speed[i][1] *= -1

            for idx, (brick, _) in enumerate(bricks):
                if b.colliderect(brick):
                    del bricks[idx]
                    score += 10
                    ball_speed[i][1] *= -1
                    if random.random() < 0.2:
                        kind = random.choice(["life", "widen", "multi"])
                        bx, by = b.center
                        power_ups.append(PowerUp(bx, by, kind))
                    break

        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick, border_radius=5)

        for pu in power_ups[:]:
            pu.move()
            pu.draw()
            if pu.rect.colliderect(paddle):
                if pu.kind == "life":
                    lives += 1
                elif pu.kind == "widen":
                    paddle.width = min(paddle.width + 30, 250)
                elif pu.kind == "multi" and len(balls) < 3:
                    balls.append(pygame.Rect(paddle.centerx, paddle.top - 20, 15, 15))
                    ball_speed.append([random.choice([-4, 4]), -4])
                power_ups.remove(pu)
            elif pu.rect.y > HEIGHT:
                power_ups.remove(pu)

        level_text = font.render(f"Level: {level}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        if not bricks:
            level += 1
            if level > MAX_LEVELS:
                running = False
                break
            pygame.time.wait(1000)
            break

        if lives <= 0:
            update_high_scores(score)
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_high_scores(score)
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    # Game Over or Win Menu
    while True:
        screen.fill(BLACK)
        msg = font.render(f"Game Over! Final Score: {score}", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 100))
        top_scores = update_high_scores(score)
        for i, s in enumerate(top_scores):
            score_line = font.render(f"{i + 1}. {s}", True, GREEN)
            screen.blit(score_line, (WIDTH // 2 - score_line.get_width() // 2, 150 + i * 40))

        retry_msg = font.render("Retry? Press Y (New) | H (Same Level) | N (Exit)", True, YELLOW)
        screen.blit(retry_msg, (WIDTH // 2 - retry_msg.get_width() // 2, 300))
        pygame.display.update()

        retry_choice = None
        while retry_choice not in ['y', 'n', 'h']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        level = 1
                        score = 0
                        lives = 3
                        retry_choice = 'y'
                    elif event.key == pygame.K_h:
                        lives = 3
                        retry_choice = 'h'
                    elif event.key == pygame.K_n:
                        cap.release()
                        cv2.destroyAllWindows()
                        pygame.quit()
                        sys.exit()

        if retry_choice in ['y', 'h']:
            break
