## This contains the Random Agent and the Alpha-Beta Agent.
## Definidas as “inteligências” que vão jogar o jogo descrito em game_engine.py.

import random


# --- PART 2: THE AGENTS (The AI) ---
"""
RandomAgent:
- Método get_move(self, state) escolhe aleatoriamente uma ação válida (1 a 3 palitos) usando random.choice.
- Serve como oponente estocástico para testar outros algoritmos.

"""
class RandomAgent:
    def get_move(self, state):
        return random.choice(state.get_actions())


"""
AlphaBetaAgent:
- Construído com um parâmetro depth (padrão 10) que limita a profundidade da busca.
- Métodos:
    - get_move(self, state):
        - invoca o método alphabeta para determinar o melhor movimento partindo do estado atual, 
        - inicializando alpha e beta com (-\infty) e (+\infty).
    - alphabeta(self, state, depth, alpha, beta, is_max) é a implementação recursiva do algoritmo de minimax com poda α β:
            - Situação de parada: 
                - Se a profundidade é zero ou o estado é terminal → retorna a avaliação do nó.
            - Se for o turno de MAX:
                - Itera sobre ações possíveis, realiza chamadas recursivas com is_max=False e atualiza alpha, guardando o melhor movimento. 
                - Encerra cedo se beta <= alpha.

            - Se for o turno de MIN:
                - faz o análogo com beta e alpha invertidos.                
"""
class AlphaBetaAgent:
    def __init__(self, depth=10):
        self.depth = depth

    def get_move(self, state):
        # We start with alpha = -infinity, beta = +infinity
        _, move = self.alphabeta(state, self.depth, -float('inf'), float('inf'), True)
        return move

    def alphabeta(self, state, depth, alpha, beta, is_max):
        if depth == 0 or state.is_terminal():
            return state.evaluate(), None
        
        best_move = None
        if is_max:
            v = -float('inf')
            for action in state.get_actions():
                score, _ = self.alphabeta(state.generate_child(action), depth-1, alpha, beta, False)
                if score > v:
                    v, best_move = score, action
                alpha = max(alpha, v)
                if beta <= alpha: break # Pruning
            return v, best_move
        else:
            v = float('inf')
            for action in state.get_actions():
                score, _ = self.alphabeta(state.generate_child(action), depth-1, alpha, beta, True)
                if score < v:
                    v, best_move = score, action
                beta = min(beta, v)
                if beta <= alpha: break # Pruning
            return v, best_move
