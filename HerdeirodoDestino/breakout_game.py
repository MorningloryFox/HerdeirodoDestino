import pygame
import random

class BreakoutGame:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.paddle_width = 100
        self.paddle_height = 20
        self.ball_radius = 10
        self.score = 0
        self.lives = 3
        self.running = True

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()

        # Create paddle and ball
        self.paddle = pygame.Rect((self.width - self.paddle_width) // 2, self.height - 50, self.paddle_width, self.paddle_height)
        self.ball = pygame.Rect(self.width // 2, self.height // 2, self.ball_radius, self.ball_radius)
        self.ball_speed_x = 5 * random.choice((1, -1))
        self.ball_speed_y = -5

        # Create bricks
        self.bricks = []
        self.create_bricks()

    def create_bricks(self):
        brick_width = 75
        brick_height = 20
        for i in range(7):
            for j in range(5):
                brick = pygame.Rect(i * (brick_width + 10) + 35, j * (brick_height + 10) + 50, brick_width, brick_height)
                self.bricks.append(brick)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.x -= 10
        if keys[pygame.K_RIGHT] and self.paddle.right < self.width:
            self.paddle.x += 10

        # Move the ball
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Ball collision with walls
        if self.ball.left <= 0 or self.ball.right >= self.width:
            self.ball_speed_x *= -1
        if self.ball.top <= 0:
            self.ball_speed_y *= -1
        if self.ball.bottom >= self.height:
            self.lives -= 1
            self.reset_ball()

        # Ball collision with paddle
        if self.ball.colliderect(self.paddle):
            self.ball_speed_y *= -1

        # Ball collision with bricks
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.ball_speed_y *= -1
                self.score += 1
                break

    def reset_ball(self):
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        self.ball_speed_x = 5 * random.choice((1, -1))
        self.ball_speed_y = -5

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), self.paddle)
        pygame.draw.ellipse(self.screen, (255, 0, 0), self.ball)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, (0, 255, 0), brick)
        pygame.display.flip()

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
    pygame.quit()
