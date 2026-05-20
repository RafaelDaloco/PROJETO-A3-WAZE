# Importamos a classe e a função do arquivo que criamos anteriormente
# Certifique-se de que o outro arquivo se chama 'grafo.py'
from grafo import MapaGrafo, dijkstra
import argparse


def criar_mapa_padrao():
    """Cria e retorna um mapa exemplo com os nós A, B, C, D, E."""
    meu_mapa = MapaGrafo()
    meu_mapa.adicionar_aresta('A', 'B', distancia=5, tempo=10)
    meu_mapa.adicionar_aresta('A', 'C', distancia=2, tempo=3)
    meu_mapa.adicionar_aresta('C', 'B', distancia=1, tempo=2)
    meu_mapa.adicionar_aresta('B', 'D', distancia=2, tempo=2)
    meu_mapa.adicionar_aresta('C', 'D', distancia=6, tempo=8)
    meu_mapa.adicionar_aresta('D', 'E', distancia=3, tempo=4)
    return meu_mapa


def rodar_testes():
    meu_mapa = criar_mapa_padrao()

    print("==========================================")
    print("🚦 SIMULADOR DE ROTAS - TESTE NO TERMINAL 🚦")
    print("==========================================\n")

    print("--- TESTE 1: Rota Normal (Critério: Distância) ---")
    rota, custo = dijkstra(meu_mapa, inicio='A', fim='E', criterio='distancia')

    if rota:
        print(f"📍 Melhor rota encontrada: {' -> '.join(rota)}")
        print(f"📏 Custo total (Distância): {custo}\n")
    else:
        print("❌ Nenhuma rota encontrada.\n")

    print("--- TESTE 2: Acidente relatado! A rua entre C e B foi interditada. ---")
    print("Recalculando rota...\n")

    meu_mapa.bloquear_aresta('C', 'B')

    rota_bloqueada, custo_bloqueado = dijkstra(meu_mapa, inicio='A', fim='E', criterio='distancia')

    if rota_bloqueada:
        print(f"📍 Nova rota encontrada: {' -> '.join(rota_bloqueada)}")
        print(f"📏 Novo custo total (Distância): {custo_bloqueado}\n")
    else:
        print("❌ Nenhuma rota encontrada. Você está preso!\n")


def simular_interativo():
    """Permite ao usuário informar pontos, arestas e bloqueios via terminal."""
    meu_mapa = MapaGrafo()

    def ler_inteiro(pergunta, minimo=0):
        while True:
            texto = input(pergunta).strip()
            try:
                valor = int(texto)
                if minimo is not None and valor < minimo:
                    print(f'Digite um número maior ou igual a {minimo}.')
                    continue
                return valor
            except Exception:
                print('Valor inválido. Tente novamente.')

    def ler_float(pergunta):
        while True:
            texto = input(pergunta).strip().replace(',', '.')
            try:
                return float(texto)
            except Exception:
                print('Valor inválido. Tente novamente.')

    def ler_sim_nao(pergunta, padrao='s'):
        resposta = input(pergunta).strip().lower()
        if not resposta:
            resposta = padrao
        return resposta == 's'

    print('==========================================')
    print('🧭 SIMULADOR DE ROTAS (MODO INTERATIVO)')
    print('==========================================')
    print('Passo 1: cadastrar as arestas do grafo')

    n = ler_inteiro('Adicionar arestas: quantas arestas você quer? ', minimo=0)

    for i in range(1, n + 1):
        print(f"\nAresta {i}/{n}")
        origem = input('Origem: ').strip()
        destino = input('Destino: ').strip()
        distancia = ler_float('Qual a distância da aresta? ')
        tempo = ler_float('Qual o tempo da aresta? ')
        bidirecional = ler_sim_nao('Bidirecional? (s/n) [s]: ', padrao='s')

        meu_mapa.adicionar_aresta(
            origem,
            destino,
            distancia=distancia,
            tempo=tempo,
            bidirecional=bidirecional
        )

    if not meu_mapa.grafo:
        print('\nGrafo vazio. Execute novamente e adicione pelo menos uma aresta.')
        return

    print('\nPasso 2: bloquear ruas (opcional)')
    if ler_sim_nao('Deseja bloquear alguma rua agora? (s/n): ', padrao='n'):
        m = ler_inteiro('Quantas ruas deseja bloquear? ', minimo=0)
        for j in range(1, m + 1):
            print(f"\nBloqueio {j}/{m}")
            o = input('Origem da rua: ').strip()
            d = input('Destino da rua: ').strip()
            meu_mapa.bloquear_aresta(o, d)
            print(f'Rua entre {o} e {d} bloqueada.')

    print('\nPasso 3: calcular rotas')
    while True:
        inicio = input('Nó de início: ').strip()
        fim = input('Nó de destino: ').strip()
        criterio = input("Critério ('distancia' ou 'tempo') [distancia]: ").strip().lower() or 'distancia'

        if criterio not in ('distancia', 'tempo'):
            print("Critério inválido. Usando 'distancia'.")
            criterio = 'distancia'

        if inicio not in meu_mapa.grafo or fim not in meu_mapa.grafo:
            print('Nó de início ou destino não existe no grafo. Tente novamente.\n')
        else:
            rota, custo = dijkstra(meu_mapa, inicio=inicio, fim=fim, criterio=criterio)
            if rota:
                print(f"📍 Melhor rota: {' -> '.join(rota)}")
                print(f"📏 Custo ({criterio}): {custo}\n")
            else:
                print('❌ Rota não encontrada.\n')

        if not ler_sim_nao('Deseja calcular outra rota? (s/n): ', padrao='n'):
            print('Encerrando simulação.')
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulador de rotas')
    parser.add_argument('--tests', '-t', action='store_true', help='Executa os testes automáticos')
    args = parser.parse_args()

    if args.tests:
        rodar_testes()
    else:
        simular_interativo()