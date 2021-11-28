# Agente de Pesquisa aplicada à determinação do Trajeto de um Robô


Objetivo:
Agente para determinar o melhor percurso a realizar por um robô, que se movimenta num espaço conhecido onde
deve recolher objetos, procurando minimizar a distância percorrida.

Descrição:
Numa fábrica existe um robô responsável pela recolha de caixas, que se encontram espalhadas pela fábrica, que são
depois colocadas no armazém. O robô possui capacidade limitada, pelo que pode ter de efetuar mais que uma
viagem até ao armazém para depositar todas as caixas. O robô possui dimensão e pode andar em frente ou rodar,
parado, em qualquer direção.

O espaço onde o robô se movimenta (fábrica) é conhecido e contém obstáculos (de posição também conhecida),
que o robô terá de contornar. A localização das caixas a recolher é conhecida. A localização do armazém também é
conhecida. Deve ser possível especificar o espaço onde o robô se movimenta (posição dos obstáculos), a posição de
todas as caixas a recolher, a posição do armazém e a posição inicial do robô

Devem ser utilizados métodos de pesquisa informada (nomeadamente A*) para encontrar o melhor percurso a
realizar pelo robô. O melhor percurso é aquele que minimiza a distancia que o robô percorre até que deposita a
última caixa no armazém.

Ferramentas:
Java ou Java + Jade ou Python

Bibliografia:
Apontamentos das Aulas; "Artificial Intelligence: A Modern Approach"
