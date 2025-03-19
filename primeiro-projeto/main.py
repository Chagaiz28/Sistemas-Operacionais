import pygame
import threading
import random
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pipa Combate")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Pipa(threading.Thread):
    def __init__(self, name, game):
        super().__init__()
        self.name = name
        self.game = game
        self.alive = True
        self.color = random.choice([RED, GREEN, BLUE])
        self.rect = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 40, 40)
        self.line_length = 100

    def run(self):
        while self.alive and self.game.status == "active":
            self.move()
            time.sleep(0.1)  # Reduz o intervalo de tempo entre os movimentos

    def move(self):
        # Simula o movimento da pipa em direção a outra pipa
        if self.game.pipas:
            target_pipa = random.choice(self.game.pipas)
            if target_pipa != self:
                if self.rect.x < target_pipa.rect.x:
                    self.rect.x += 5
                elif self.rect.x > target_pipa.rect.x:
                    self.rect.x -= 5
                if self.rect.y < target_pipa.rect.y:
                    self.rect.y += 5
                elif self.rect.y > target_pipa.rect.y:
                    self.rect.y -= 5

        # Lógica para cortar outra pipa
        for pipa in self.game.pipas:
            if pipa != self and self.alive and pipa.alive:
                if self.check_collision(pipa) or self.check_line_collision(pipa):
                    self.cut(pipa)

    def check_collision(self, other_pipa):
        # Lógica simplificada para detectar colisão
        return self.rect.colliderect(other_pipa.rect)

    def check_line_collision(self, other_pipa):
        # Verifica se a linha colide com outra pipa
        line_rect = pygame.Rect(self.rect.centerx, self.rect.centery, self.line_length, 1)
        return line_rect.colliderect(other_pipa.rect)

    def cut(self, other_pipa):
        if random.choice([True, False]):
            print(f"{self.name} cortou a linha de {other_pipa.name}!")
            other_pipa.alive = False
        else:
            print(f"{other_pipa.name} cortou a linha de {self.name}!")
            self.alive = False

    def draw(self, screen):
        # Desenha a pipa como um losango
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.centery),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.left, self.rect.centery)
        ]
        pygame.draw.polygon(screen, self.color, points)
        # Desenha a linha da pipa
        if self.rect.centerx < screen_width / 2:
            pygame.draw.line(screen, BLACK, (self.rect.centerx, self.rect.centery), (0, self.rect.centery))
        else:
            pygame.draw.line(screen, BLACK, (self.rect.centerx, self.rect.centery), (screen_width, self.rect.centery))

class Game:
    def __init__(self):
        self.players = []
        self.scores = {}
        self.status = "waiting"  # possible statuses: waiting, active, finished
        self.pipas = []

    def add_player(self, player_name):
        if player_name not in self.players:
            self.players.append(player_name)
            self.scores[player_name] = 0
            pipa = Pipa(player_name, self)
            self.pipas.append(pipa)

    def start_game(self):
        if len(self.players) > 1:
            self.status = "active"
            for pipa in self.pipas:
                pipa.start()

    def finish_game(self):
        self.status = "finished"
        for pipa in self.pipas:
            pipa.alive = False

    def get_game_state(self):
        return {
            "players": self.players,
            "scores": self.scores,
            "status": self.status
        }

def main():
    game = Game()
    game.add_player("Player1")
    game.add_player("Player2")
    game.add_player("Player3")

    game.start_game()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        for pipa in game.pipas:
            if pipa.alive:
                pipa.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    game.finish_game()
    pygame.quit()

if __name__ == "__main__":
    main()