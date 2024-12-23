import pygame
from settings import *
from sprites import *
pygame.init()
pygame.font.init() 

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.board = None 

    def new(self):
        self.board = Board()  
        self.board.display_board()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()  
            self.draw()  

            if self.check_win():
                self.win = True
                self.playing = False 
                self.show_win_screen() 
                
        self.end_screen()  

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)  
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if event.button == 1:  # Left click to dig
                    if not self.board.board_list[mx][my].flagged:
                        if not self.board.dig(mx, my):  # Exploded
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "X":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == "X":
                                        tile.revealed = True
                            self.playing = False  # End the game when a bomb is triggered

                if event.button == 3:  
                    if not self.board.board_list[mx][my].revealed:
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged

    def show_win_screen(self):
        font = pygame.font.SysFont('Arial', 40)
        win_text = font.render("You Win!", True, GREEN)
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  

    def end_screen(self):
        
        font = pygame.font.SysFont('Arial', 40)
        end_text = font.render("Game Over!", True, RED)
        self.screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  
        pygame.quit()
        quit(0)


game = Game()
while True:
    game.new()  
    game.run()  
