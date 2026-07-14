"""Análisis de Brauer para el circuito QFT de 4 qubits (versión corregida).

Reproduce exactamente el ejemplo de las diapositivas:

1. Circuito QFT como polígonos W_1..W_10 (multiconjuntos de compuertas).
2. Invariantes: dim(A) = 293 y dim(Z(A)) = 21.
3. Carcaj de Brauer Q_QFT: ciclos especiales por compuerta (sucesión de
   sucesores), con lazos l^x_i y flechas alpha^x_i como en la lámina.
4. Grafo de cubrimiento g: 14 aristas etiquetadas (H, I, R_2, R_3, swap).
5. Entropías: H(g^1) = 1.53641, H(g^2) = 1.52193, H(g^3) = 2.09114.

Construcción clave (era el error del código anterior): las aristas NO se
obtienen conectando pares arbitrarios de vértices que comparten compuertas.
Para cada compuerta x se toma su sucesión de sucesores (la lista ordenada de
polígonos que la contienen, con repeticiones) y:

- En el carcaj: un ciclo especial orientado que recorre esas ocurrencias;
  las ocurrencias repetidas dentro del mismo polígono generan lazos.
- En el cubrimiento: el camino no orientado por los polígonos distintos
  consecutivos; aristas paralelas se funden y sus etiquetas se combinan
  (p. ej. la arista 3-7 queda etiquetada "H,R_3").
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import log
from typing import Dict, List, Sequence, Tuple

import cmath
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import networkx as nx
import numpy as np


# ---------------------------------------------------------------------------
# Paso 1: circuito QFT de 4 qubits como configuración de Brauer
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Vertex:
    """Polígono de la configuración: multiconjunto de compuertas."""

    name: str
    gates: Counter
    justification: str


def build_multiset(gate_sequence: Sequence[str]) -> Counter:
    return Counter(gate_sequence)


def qft4_vertices() -> List[Vertex]:
    """Los 10 polígonos W_1..W_10 exactamente como en la diapositiva."""

    raw_vertices = [
        ("W_1", ["H", "I", "I", "I"], "W1 = H (x) I (x) I (x) I"),
        ("W_2", ["R_2", "I", "I", "I"], "W2 = R2 (x) I (x) I (x) I"),
        ("W_3", ["H", "R_3", "I"], "W3 = H (x) R3 (x) I"),
        ("W_4", ["I", "SWAP", "I"], "W4 = I (x) SWAP (x) I"),
        ("W_5", ["R_2", "R_4"], "W5 = R2 (x) R4"),
        ("W_6", ["SWAP", "SWAP"], "W6 = SWAP (x) SWAP"),
        ("W_7", ["H", "R_3", "I"], "W7 = H (x) R3 (x) I"),
        ("W_8", ["I", "SWAP", "I"], "W8 = I (x) SWAP (x) I"),
        ("W_9", ["R_2", "I", "I"], "W9 = R2 (x) I (x) I"),
        ("W_10", ["H", "I", "I"], "W10 = H (x) I (x) I"),
    ]
    return [
        Vertex(name=name, gates=build_multiset(gates), justification=note)
        for name, gates, note in raw_vertices
    ]


def vertex_message(vertex: Vertex) -> str:
    parts = []
    for gate, count in sorted(vertex.gates.items()):
        parts.append(f"{gate}^{count}" if count > 1 else gate)
    return ", ".join(parts)


# ---------------------------------------------------------------------------
# Matrices de compuertas (se conservan para verificación del circuito)
# ---------------------------------------------------------------------------

def hadamard_matrix() -> np.ndarray:
    factor = 1.0 / np.sqrt(2.0)
    return np.array([[factor, factor], [factor, -factor]], dtype=complex)


def identity_matrix() -> np.ndarray:
    return np.eye(2, dtype=complex)


def rotation_matrix(k: int) -> np.ndarray:
    if k <= 0:
        raise ValueError("k must be positive")
    phase = cmath.exp(1j * (2.0 * np.pi / (2 ** k)))
    return np.array([[1.0, 0.0], [0.0, phase]], dtype=complex)


def swap_matrix() -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )


def gate_matrix(label: str) -> np.ndarray:
    if label == "H":
        return hadamard_matrix()
    if label == "I":
        return identity_matrix()
    if label == "SWAP":
        return swap_matrix()
    if label.startswith("R_"):
        return rotation_matrix(int(label.split("_", 1)[1]))
    raise ValueError(f"Unsupported gate label: {label}")


# ---------------------------------------------------------------------------
# Sucesiones de sucesores, valencias y multiplicidades
# ---------------------------------------------------------------------------

def successor_sequences(vertices: Sequence[Vertex]) -> Dict[str, List[int]]:
    """Para cada compuerta x, la lista ordenada de polígonos que la contienen
    (con repeticiones = número de ocurrencias dentro del polígono)."""

    sequences: Dict[str, List[int]] = {}
    for index, vertex in enumerate(vertices, start=1):
        for gate in sorted(vertex.gates):
            sequences.setdefault(gate, [])
            sequences[gate].extend([index] * vertex.gates[gate])
    return sequences


def valences(vertices: Sequence[Vertex]) -> Counter:
    """val(x) = total de ocurrencias de x en toda la configuración.

    Para la QFT de 4 qubits: I=16, H=4, SWAP=4, R_2=3, R_3=2, R_4=1.
    """

    totals: Counter = Counter()
    for vertex in vertices:
        totals.update(vertex.gates)
    return totals


def multiplicity(value: int) -> int:
    """mu(x) = 1, salvo cuando val(x) = 1, donde mu(x) = 2 (vértice no truncado)."""

    return 2 if value == 1 else 1


# ---------------------------------------------------------------------------
# Paso 2: invariantes dim(A) y dim(Z(A))
# ---------------------------------------------------------------------------

def calculate_brauer_dim(vertices: Sequence[Vertex]) -> int:
    """dim(A) = 2|Q_0| + sum_x val(x) * (mu(x) val(x) - 1)  (Green-Schroll).

    Con las valencias de la diapositiva:
      2*10 + 16*15 + 4*3 + 4*3 + 3*2 + 2*1 + 1*1 = 20 + 273 = 293.
    """

    totals = valences(vertices)
    n = len(vertices)
    return int(2 * n + sum(v * (v * multiplicity(v) - 1) for v in totals.values()))


def count_quiver_loops(vertices: Sequence[Vertex]) -> int:
    """Lazos del carcaj: ocurrencias consecutivas repetidas en un mismo
    polígono (8 lazos de I, 1 de SWAP) más el lazo de todo vértice con
    val(x)=1 y mu(x)=2 (el lazo l^{R_4} en W_5). Total: 10."""

    loops = 0
    for gate, sequence in successor_sequences(vertices).items():
        if len(sequence) == 1:
            if multiplicity(1) > 1:
                loops += 1
        else:
            loops += sum(1 for a, b in zip(sequence, sequence[1:]) if a == b)
    return loops


def calculate_center_dim(vertices: Sequence[Vertex]) -> int:
    """dim(Z(A)) = 1 + sum_x mu(x) + |Q_0| - |Gamma_0| + #lazos - |C_Gamma|.

    |C_Gamma| = #{x : val(x)=1, mu(x)>1}. Para la QFT:
      1 + 7 + 10 - 6 + 10 - 1 = 21.
    """

    totals = valences(vertices)
    n = len(vertices)
    loops = count_quiver_loops(vertices)
    sum_mu = sum(multiplicity(v) for v in totals.values())
    c_gamma = sum(1 for v in totals.values() if v == 1 and multiplicity(v) > 1)
    return int(1 + sum_mu + n - len(totals) + loops - c_gamma)


# ---------------------------------------------------------------------------
# Paso 3: carcaj de Brauer Q_QFT (ciclos especiales orientados)
# ---------------------------------------------------------------------------

def build_brauer_graph(vertices: Sequence[Vertex]) -> nx.MultiDiGraph:
    """Un ciclo especial por compuerta: recorre sus ocurrencias en orden y
    cierra en la primera. Ocurrencias repetidas en el mismo polígono => lazos.

    Flechas resultantes (30 en total):
      H:    W1->W3->W7->W10->W1                       (alpha^H_1..4)
      I:    16 flechas, 8 de ellas lazos l^I_1..l^I_8
      R_2:  W2->W5->W9->W2                            (alpha^R2_1..3)
      R_3:  W3->W7->W3                                (alpha^R3_1..2)
      R_4:  lazo en W5                                (l^R4, val=1, mu=2)
      SWAP: W4->W6, lazo en W6, W6->W8, W8->W4        (alpha^swap + l^swap)
    """

    graph = nx.MultiDiGraph()
    for index, vertex in enumerate(vertices, start=1):
        graph.add_node(
            index,
            name=vertex.name,
            message=vertex_message(vertex),
            justification=vertex.justification,
        )

    for gate, sequence in successor_sequences(vertices).items():
        short = gate.replace("SWAP", "swap").replace("_", "")
        if len(sequence) == 1:
            if multiplicity(1) > 1:
                node = sequence[0]
                graph.add_edge(node, node, gate=gate, label=f"$\\ell^{{{short}}}$",
                               kind="loop", weight=1.0)
            continue
        cycle = sequence + [sequence[0]]
        arrow_idx = 0
        loop_idx = 0
        for a, b in zip(cycle, cycle[1:]):
            if a == b:
                loop_idx += 1
                graph.add_edge(a, b, gate=gate,
                               label=f"$\\ell^{{{short}}}_{{{loop_idx}}}$",
                               kind="loop", weight=1.0)
            else:
                arrow_idx += 1
                graph.add_edge(a, b, gate=gate,
                               label=f"$\\alpha^{{{short}}}_{{{arrow_idx}}}$",
                               kind="arrow", weight=1.0)
    return graph


def graph_to_adjacency_matrix(graph: nx.MultiDiGraph, vertices: Sequence[Vertex]) -> np.ndarray:
    labels = list(range(1, len(vertices) + 1))
    return nx.to_numpy_array(graph, nodelist=labels, dtype=float, weight="weight")


def detect_cycles(graph: nx.MultiDiGraph) -> List[List[int]]:
    return list(nx.simple_cycles(nx.DiGraph(graph)))


# ---------------------------------------------------------------------------
# Paso 4: grafo de cubrimiento g (caminos no orientados por compuerta)
# ---------------------------------------------------------------------------

def build_covering_graph(vertices: Sequence[Vertex]) -> nx.Graph:
    """Para cada compuerta, camino por los polígonos distintos consecutivos de
    su sucesión (sin cerrar el ciclo). Aristas paralelas se funden combinando
    etiquetas. Resultado: las 14 aristas de la diapositiva:

      I:    1-2-3-4-7-8-9-10        (7 aristas)
      H:    1-3, 3-7, 7-10          (3 aristas; 3-7 se funde con R_3)
      R_2:  2-5, 5-9
      R_3:  3-7 (fundida: "H,R_3")
      swap: 4-6, 6-8
    """

    covering = nx.Graph()
    for index in range(1, len(vertices) + 1):
        covering.add_node(index)

    for gate, sequence in successor_sequences(vertices).items():
        distinct: List[int] = []
        for polygon in sequence:
            if not distinct or distinct[-1] != polygon:
                distinct.append(polygon)
        display = "swap" if gate == "SWAP" else gate
        for a, b in zip(distinct, distinct[1:]):
            if covering.has_edge(a, b):
                labels = covering[a][b]["labels"]
                if display not in labels:
                    labels.append(display)
            else:
                covering.add_edge(a, b, labels=[display])

    for a, b, data in covering.edges(data=True):
        order = {"H": 0, "I": 1, "R_2": 2, "R_3": 3, "R_4": 4, "swap": 5}
        data["label"] = ",".join(sorted(data["labels"], key=order.get))
    return covering


# ---------------------------------------------------------------------------
# Paso 5: entropías H(g^1), H(g^2), H(g^3)
# ---------------------------------------------------------------------------

def shannon_entropy(probabilities: Sequence[float]) -> float:
    entropy = 0.0
    for value in probabilities:
        if value > 0:
            entropy -= float(value) * log(float(value), 2)
    return entropy


def covering_graph_entropy(graph: nx.Graph) -> float:
    """H(g^1) = (1 / 2|E_g|) * sum_v delta_v log2(delta_v) = 1.53641."""

    degrees = np.array([degree for _, degree in graph.degree()], dtype=float)
    total = degrees.sum()  # = 2|E|
    if total == 0:
        return 0.0
    return float(sum(d * np.log2(d) for d in degrees if d > 0) / total)


def degree_distribution_entropy(graph: nx.Graph) -> float:
    """H(g^2) = entropía de la distribución de grados P(k) = n_k / n = 1.52193."""

    degrees = [degree for _, degree in graph.degree()]
    counts = Counter(degrees)
    n = float(len(degrees))
    return shannon_entropy([count / n for count in counts.values()])


def valence_entropy(vertices: Sequence[Vertex]) -> float:
    """H(g^3) = entropía de val(x)*mu(x) sobre las compuertas = 2.09114.

    Distribución: {I:16, H:4, SWAP:4, R_2:3, R_3:2, R_4:2}/31.
    """

    totals = valences(vertices)
    weighted = np.array([v * multiplicity(v) for v in totals.values()], dtype=float)
    probabilities = weighted / weighted.sum()
    return shannon_entropy(probabilities)


# ---------------------------------------------------------------------------
# Análisis completo
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BrauerAnalysis:
    vertices: List[Vertex]
    brauer_graph: nx.MultiDiGraph
    covering_graph: nx.Graph
    adjacency_matrix: np.ndarray
    brauer_dim: int
    center_dim: int


def analyze_brauer_qft(vertices: Sequence[Vertex]) -> BrauerAnalysis:
    brauer_graph = build_brauer_graph(vertices)
    covering_graph = build_covering_graph(vertices)
    adjacency_matrix = graph_to_adjacency_matrix(brauer_graph, vertices)
    return BrauerAnalysis(
        vertices=list(vertices),
        brauer_graph=brauer_graph,
        covering_graph=covering_graph,
        adjacency_matrix=adjacency_matrix,
        brauer_dim=calculate_brauer_dim(vertices),
        center_dim=calculate_center_dim(vertices),
    )


# ---------------------------------------------------------------------------
# Dibujo del carcaj (estilo de la diapositiva: W_1..W_10 en línea,
# ciclos especiales coloreados por compuerta, lazos arriba de cada nodo)
# ---------------------------------------------------------------------------

GATE_COLORS = {
    "I": "red",
    "H": "blue",
    "R_2": "magenta",
    "R_3": "green",
    "R_4": "darkcyan",
    "SWAP": "saddlebrown",
}


def draw_brauer_graph(graph: nx.MultiDiGraph, output_path: str | None = None,
                      show: bool = False) -> None:
    nodes = sorted(graph.nodes())
    pos = {node: (float(index), 0.0) for index, node in enumerate(nodes)}
    fig, ax = plt.subplots(figsize=(17, 7.5))

    node_radius = 0.22
    for node in nodes:
        x, y = pos[node]
        ax.add_patch(Circle((x, y), node_radius, facecolor="white",
                            edgecolor="black", zorder=5, linewidth=1.4))
        ax.text(x, y, f"$W_{{{node}}}$", ha="center", va="center",
                fontsize=12, zorder=6)

    # Curvaturas por compuerta para que los arcos no se solapen
    arc_side = {"I": -1, "H": -1, "R_2": 1, "R_3": 1, "SWAP": 1, "R_4": 1}
    arc_scale = {"I": 0.16, "H": 0.30, "R_2": 0.24, "R_3": 0.34, "SWAP": 0.30, "R_4": 0.2}

    loop_stack: Dict[int, int] = {node: 0 for node in nodes}
    for u, v, data in graph.edges(data=True):
        color = GATE_COLORS[data["gate"]]
        if u == v:
            level = loop_stack[u]
            loop_stack[u] += 1
            x, y = pos[u]
            cy = y + node_radius + 0.32 + 0.42 * level
            ax.add_patch(Circle((x, cy), 0.16, facecolor="none",
                                edgecolor=color, linewidth=1.6, zorder=3))
            ax.text(x + 0.21, cy + 0.10, data["label"], color=color,
                    fontsize=10, ha="left", va="center", zorder=7)
        else:
            distance = abs(pos[v][0] - pos[u][0])
            rad = arc_side[data["gate"]] * min(0.9, arc_scale[data["gate"]] + 0.045 * distance)
            arrow = FancyArrowPatch(
                pos[u], pos[v], connectionstyle=f"arc3,rad={rad}",
                arrowstyle="-|>", mutation_scale=14, color=color,
                linewidth=1.5, zorder=2,
                shrinkA=node_radius * 72, shrinkB=node_radius * 72,
            )
            ax.add_patch(arrow)
            mid_x = (pos[u][0] + pos[v][0]) / 2.0
            mid_y = (pos[u][1] + pos[v][1]) / 2.0
            offset = -1.05 * rad * distance / 2.0
            ax.text(mid_x, mid_y + offset, data["label"], color=color,
                    fontsize=10, ha="center", va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.08", facecolor="white",
                              edgecolor="none", alpha=0.75))

    handles = [plt.Line2D([0], [0], color=c, lw=2,
                          label=g.replace("SWAP", "swap").replace("_", ""))
               for g, c in GATE_COLORS.items()]
    ax.legend(handles=handles, loc="upper right", fontsize=10, framealpha=0.9)
    ax.set_title("Carcaj de Brauer ($Q_{QFT}$)", fontsize=15)
    ax.set_xlim(-0.8, len(nodes) - 0.2)
    ax.set_ylim(-3.2, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=160, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Dibujo del grafo de cubrimiento (disposición fija imitando la diapositiva)
# ---------------------------------------------------------------------------

COVERING_LAYOUT = {
    1: (0.0, 0.35),
    2: (0.9, -0.75),
    3: (1.15, 1.35),
    4: (2.45, 0.30),
    5: (2.35, -1.05),
    6: (3.35, -0.25),
    7: (3.60, 1.45),
    8: (4.35, 0.45),
    9: (4.55, -0.85),
    10: (5.55, 1.00),
}


def draw_covering_graph(graph: nx.Graph, output_path: str | None = None,
                        show: bool = False) -> None:
    pos = {node: COVERING_LAYOUT.get(node) for node in graph.nodes()}
    if any(value is None for value in pos.values()):
        pos = nx.spring_layout(graph, seed=11)

    plt.figure(figsize=(11, 7.5))
    nx.draw_networkx_nodes(graph, pos, node_color="white", edgecolors="black",
                           node_size=1300, linewidths=1.6)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color="black")
    nx.draw_networkx_edges(graph, pos, width=1.6, edge_color="black")
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                 font_size=10,
                                 bbox=dict(boxstyle="round,pad=0.1",
                                           facecolor="white", edgecolor="none",
                                           alpha=0.8))
    plt.title("Grafo de Cubrimiento ($\\mathfrak{g}$)", fontsize=15)
    plt.axis("off")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=160, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    vertices = qft4_vertices()
    analysis = analyze_brauer_qft(vertices)
    cycles = detect_cycles(analysis.brauer_graph)

    h_g1 = covering_graph_entropy(analysis.covering_graph)
    h_g2 = degree_distribution_entropy(analysis.covering_graph)
    h_g3 = valence_entropy(vertices)

    print("Paso 1: Definición del circuito")
    for vertex in vertices:
        print(f"- {vertex.name}: {vertex_message(vertex)}")

    totals = valences(vertices)
    print("\nValencias val(x):")
    for gate in sorted(totals):
        print(f"- val({gate}) = {totals[gate]}  (mu = {multiplicity(totals[gate])})")

    print("\nPaso 2: Cálculo de invariantes de Brauer")
    print(f"- dim(A) = {analysis.brauer_dim}   (diapositiva: 293)")
    print(f"- dim(Z(A)) = {analysis.center_dim}   (diapositiva: 21)")

    print("\nPaso 3: Construcción del carcaj de Brauer (Q_QFT)")
    print(f"- Nodos: {analysis.brauer_graph.number_of_nodes()}")
    print(f"- Flechas: {analysis.brauer_graph.number_of_edges()} "
          f"({count_quiver_loops(vertices)} lazos)")
    print(f"- Ciclos especiales detectados: {len(cycles)}")

    print("\nPaso 4: Grafo de cubrimiento (g)")
    print(f"- Nodos: {analysis.covering_graph.number_of_nodes()}")
    print(f"- Aristas: {analysis.covering_graph.number_of_edges()}   (diapositiva: 14)")
    for a, b, data in sorted(analysis.covering_graph.edges(data=True)):
        print(f"  {a} -- {b}: {data['label']}")

    print("\nPaso 5: Análisis de entropía")
    print(f"- H(g^1) = {h_g1:.5f}   (diapositiva: 1.53641)")
    print(f"- H(g^2) = {h_g2:.5f}   (diapositiva: 1.52193)")
    print(f"- H(g^3) = {h_g3:.5f}   (diapositiva: 2.09114)")

    draw_brauer_graph(analysis.brauer_graph, output_path="brauer_quiver.png")
    draw_covering_graph(analysis.covering_graph, output_path="covering_graph.png")
    print("\nGráfico guardado en brauer_quiver.png")
    print("Gráfico guardado en covering_graph.png")


if __name__ == "__main__":
    main()
