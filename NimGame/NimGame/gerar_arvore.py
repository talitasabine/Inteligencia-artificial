import graphviz
from game_engine import GameState

def construir_arvore_nim(palitos_iniciais):
    # Cria um novo grafo direcionado
    dot = graphviz.Digraph(comment='Árvore do Jogo Nim')
    dot.attr(rankdir='TB') # Orientação Top-to-Bottom (Cima para Baixo)
    
    # Contador para garantir um ID único para cada nó, 
    # já que caminhos diferentes podem levar ao mesmo estado.
    contador_nos = [0]
    
    def percorrer_arvore(estado, id_pai=None, acao_tomada=None):
        id_atual = str(contador_nos[0])
        contador_nos[0] += 1
        
        # Estilização do nó baseada no estado atual
        if estado.is_terminal():
            score = estado.evaluate()
            # Se o score é -1 no turno do MAX, significa que MIN fez a jogada da vitória
            vencedor = "MIN" if estado.turn == "MAX" else "MAX"
            label = f"Fim!\nRestam: {estado.sticks}\nVencedor: {vencedor}\nScore: {score}"
            dot.node(id_atual, label, shape='doubleoctagon', style='filled', fillcolor='lightcoral')
        else:
            label = f"Restam: {estado.sticks}\nTurno: {estado.turn}"
            shape = 'box' if estado.turn == 'MAX' else 'ellipse'
            cor_fundo = 'lightblue' if estado.turn == 'MAX' else 'lightgreen'
            dot.node(id_atual, label, shape=shape, style='filled', fillcolor=cor_fundo)
        
        # Conecta este nó ao seu pai (estado anterior)
        if id_pai is not None:
            dot.edge(id_pai, id_atual, label=f" Tira {acao_tomada} ")
        
        # Chamadas recursivas para gerar os filhos (próximos estados)
        if not estado.is_terminal():
            for acao in estado.get_actions():
                estado_filho = estado.generate_child(acao)
                percorrer_arvore(estado_filho, id_atual, acao)

    estado_inicial = GameState(sticks=palitos_iniciais, turn="MAX")
    percorrer_arvore(estado_inicial)
    
    return dot

if __name__ == "__main__":
    # Inicializa com 4 palitos para manter a árvore legível
    palitos = 4
    grafo = construir_arvore_nim(palitos)
    
    # Salva e tenta abrir o arquivo PDF gerado
    nome_arquivo = f'arvore_nim_{palitos}.gv'
    grafo.render(nome_arquivo, format='pdf', view=True)
    print(f"Árvore gerada e salva como {nome_arquivo}.pdf")