## Define o ambiente para o problema de busca adversarial que o jogo irá utilizar:
##   define as regras e a dinâmica do jogo de retirar palitos e 
##   fornece uma classe de controle (Referee) para simular uma partida entre dois agentes. 
## É a base sobre a qual algoritmos de busca adversarial (minimax, α β, etc.) podem ser testados.

import random

# --- PART 1: THE GAME ENGINE (The Environment) ---

"""
GameState: representa o estado atual do jogo
- sticks: quantos palitos ainda estão na pilha.
- turn: quem joga a seguir ("MAX" → nosso agente, "MIN" → o oponente).

- get_actions() devolve os movimentos legais (1 a 3 palitos, não mais do que os que restam).
- generate_child(action) cria um novo estado resultante de executar uma ação.
- is_terminal() verifica se o jogo acabou (0 ou menos palitos).
- evaluate() função de utilidade para estados terminais: 
    se não há palitos e é a vez de MAX, 
         então MAX foi obrigado a apanhar o último palito e perde (-1); 
    caso contrário, 
         então MAX ganha (+1). 

    Fora dos terminais devolve 0.
"""
class GameState:
    def __init__(self, sticks, turn="MAX"):
        self.sticks = sticks
        self.turn = turn  # "MAX" (Agent) or "MIN" (Opponent)

    def get_actions(self):
        """Returns possible moves (cannot take more than are left)."""
        if self.sticks >= 3: return [1, 2, 3]
        if self.sticks == 2: return [1, 2]
        if self.sticks == 1: return [1]
        return []

    def generate_child(self, action):
        """Returns a new state after taking 'action' sticks."""
        next_turn = "MIN" if self.turn == "MAX" else "MAX"
        return GameState(self.sticks - action, next_turn)

    def is_terminal(self):
        return self.sticks <= 0

    def evaluate(self):
        """
        Terminal utility:
        If it's MAX's turn and 0 sticks are left, MAX was forced 
        to take the last stick and lost.
        """
        if self.sticks <= 0:
            return -1 if self.turn == "MAX" else 1
        return 0


"""
Referee: um árbitro que “faz jogar” dois agentes (controle)
- Inicializa-se com um GameState inicial e duas instâncias de agentes (um para MAX e outro para MIN).
- O método play() itera até o estado ser terminal: 
    - pergunta ao agente da vez qual o movimento, 
    - aplica o movimento,
    - imprime o resultado e alterna o turno.
- Ao fim anuncia o vencedor (o jogador que não tem mais jogadas, porque o outro tirou o último palito).
"""
class Referee:
    def __init__(self, state, agent_max, agent_min):
        self.state = state
        self.agent_max = agent_max
        self.agent_min = agent_min

    def play(self):
        print(f"--- Game Start! Sticks: {self.state.sticks} ---")
        while not self.state.is_terminal():
            current_agent = self.agent_max if self.state.turn == "MAX" else self.agent_min
            move = current_agent.get_move(self.state)
            
            print(f"{self.state.turn} takes {move} sticks.")
            self.state = self.state.generate_child(move)
            print(f"Sticks remaining: {self.state.sticks} \n")

        winner = "MIN" if self.state.turn == "MAX" else "MAX"
        print(f"--- Game Over! Winner is {winner} ---")

