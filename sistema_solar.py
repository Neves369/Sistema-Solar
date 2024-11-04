import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 700
# Permite redimensionar a janela
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sistema Solar")

YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_GREY = (199, 205, 214)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (168, 86, 13)
LIGHT_YELLOW = (219, 205, 81)
LIGHT_BLUE = (145, 186, 227)
DARK_BLUE = (9, 15, 179)

FONT = pygame.font.SysFont("arial", 12)
FPS = 60


class Planet:
    # Variáveis de classe
    AU = 149.6e6 * 1000  # (m) 1 AU = distância entre a Terra e o Sol
    G = 6.67428e-11  # Constante gravitacional
    SCALE_PLANET = 50 / AU  # 250 / AU -> 1 AU = 100 pixels
    TIMESTEP = (3600 * 24) * 1  # Tempo para atualizar o quadro = 10 dias

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius  # (pixels)
        self.color = color
        self.mass = mass  # (kg)

        self.orbit = []  # Lista de todos os pontos que o planeta percorreu
        self.sun = False  # Se o objeto é um sol ou não
        self.distance_to_sun = 0  # Cada planeta tem uma distância única ao sol

        self.x_vel = 0
        self.y_vel = 0

    # Desenha o planeta
    def draw(self, win):
        # Altera o referencial para que a origem fique no centro da janela
        x = self.x * self.SCALE_PLANET + WIDTH / 2
        y = self.y * self.SCALE_PLANET + HEIGHT / 2

        # Obtém a lista de todos os pontos atualizados para a escala
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE_PLANET + WIDTH / 2
                y = y * self.SCALE_PLANET + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # Cria e desenha o texto de distância
        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun / (10 * 10**9), 1)}Gm", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() /
                     2, y - distance_text.get_height() / 2))

    # Retorna as componentes x e y da força gravitacional entre duas massas
    def attraction(self, other):
        # Calcula a distância (r) entre as duas massas
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        # Calcula a força usando a lei da gravidade de Newton
        force = (self.G * self.mass * other.mass) / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    # Chama essa função continuamente para atualizar a posição a cada TIMESTEP (cada "dia")
    def update_position(self, planets):
        total_fx = total_fy = 0

        # Soma as forças totais exercidas no planeta pelas outras massas
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Atualiza a componente x e y da velocidade usando a segunda lei de Newton
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Atualiza a posição x e y usando a velocidade
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Adiciona a posição atual à lista para permitir o desenho da órbita
        self.orbit.append((self.x, self.y))

    # Função para ajustar a escala do sistema solar com base na rolagem do mouse
    def update_scale(self, zoom_direction):
        # Incremento para ajustar a escala com cada rolagem
        zoom_factor = 1.05  # Valor de ajuste da escala

        if zoom_direction > 0:  # Rolagem para cima (zoom in)
            self.SCALE_PLANET *= zoom_factor
        elif zoom_direction < 0:  # Rolagem para baixo (zoom out)
            self.SCALE_PLANET /= zoom_factor

        print(f"Nova escala: {self.SCALE_PLANET}")

# Função principal


def main():
    global WIN, WIDTH, HEIGHT
    run = True
    clock = pygame.time.Clock()

    # planetas
    sun = Planet(0, 0, 5, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    mercury = Planet(0.387 * Planet.AU, 0, 4, DARK_GREY, 0.33 * 10**24)
    mercury.y_vel = -47.4 * 1000  # (m/s)
    venus = Planet(0.723 * Planet.AU, 0, 7, LIGHT_GREY, 4.87 * 10**24)
    venus.y_vel = -35 * 1000  # (m/s)
    earth = Planet(1 * Planet.AU, 0, 8, BLUE, 5.97 * 10**24)
    earth.y_vel = -29.8 * 1000  # (m/s)
    mars = Planet(1.524 * Planet.AU, 0, 6, RED, 0.642 * 10**24)
    mars.y_vel = -24.1 * 1000  # (m/s)
    jupiter = Planet(5.204 * Planet.AU, 0, 20, ORANGE, 1898 * 10**24)
    jupiter.y_vel = -13.1 * 1000  # (m/s)
    saturn = Planet(9.572 * Planet.AU, 0, 16, LIGHT_YELLOW, 568 * 10**24)
    saturn.y_vel = -9.7 * 1000  # (m/s)
    uranus = Planet(19.165 * Planet.AU, 0, 10, LIGHT_BLUE, 86.8 * 10**24)
    uranus.y_vel = -6.8 * 1000  # (m/s)
    neptune = Planet(30.181 * Planet.AU, 0, 12, DARK_BLUE, 102 * 10**24)
    neptune.y_vel = -5.4 * 1000  # (m/s)
    planets = [sun, mercury, venus, earth,
               mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(FPS)

        # Percorre a lista de todos os eventos que ocorrem
        for event in pygame.event.get():
            # Verifica se o usuário clicou no botão de sair
            if event.type == pygame.QUIT:
                run = False

            # Verifica de a tela foi maximizada
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                WIN = pygame.display.set_mode(
                    (WIDTH, HEIGHT), pygame.RESIZABLE)

            # Verifica se o scroll do mouse foi acionado
            if event.type == pygame.MOUSEWHEEL:
                for planet in planets:
                    # Ajusta a escala com base na rolagem
                    planet.update_scale(event.y)

        WIN.fill(BLACK)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
