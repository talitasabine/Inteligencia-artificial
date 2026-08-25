# Jogo da Velha (faz uso da easyAI library)

from easyAI import TwoPlayersGame, AI_Player, Negamax
from easyAI.Player import Human_Player

class GameController(TwoPlayersGame):
    def __init__(self, players):
        # Definindo os jogadores
        self.players = players

        # Definindo quen inicia o jogo - jogador 1
        self.nplayer = 1 

        # Definindo o tabuleiro - 3x3 numerado de um a nove linhas
        self.board = [0] * 9
    
    # Definindo os movimentos possíveis
    def possible_moves(self):
        return [a + 1 for a, b in enumerate(self.board) if b == 0]
    
    # Realizando um movimento
    def make_move(self, move):
        self.board[int(move) - 1] = self.nplayer

    # O adversário tem três em uma linha?
    def loss_condition(self):
        possible_combinations = [[1,2,3], [4,5,6], [7,8,9],
            [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]

        return any([all([(self.board[i-1] == self.nopponent)
                for i in combination]) for combination in possible_combinations]) 
        
    # Verificando se jogo acabou
    def is_over(self):
        return (self.possible_moves() == []) or self.loss_condition()
        
    # Monstrando a posição atual
    def show(self):
        print('\n'+'\n'.join([' '.join([['.', 'O', 'X'][self.board[3*j + i]]
                for i in range(3)]) for j in range(3)]))
                 
    # Calculando a pontuação
    def scoring(self):
        return -100 if self.loss_condition() else 0

if __name__ == "__main__":
    # Definido o algoritmo
    algorithm = Negamax(7)

    # Começando o jogo
    GameController([Human_Player(), AI_Player(algorithm)]).play()

