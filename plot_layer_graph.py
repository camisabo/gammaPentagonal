import os
from gamma_pentagonal import GammaPentagonalCipher, QuantumCoverAnalyzer


def main() -> None:
    cipher = GammaPentagonalCipher()
    coords = cipher.encrypt("abcdefghijkl")

    analyzer = QuantumCoverAnalyzer()
    analysis = analyzer.analyze(coords, layer_size=2)

    project_root = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(project_root, "grafo_capas_quantum.png")

    analyzer.visualize_layer_graph(
        analysis=analysis,
        title="Grafo de Capas Tensoriales W",
        save_path=output_path,
    )
    print(f"Imagen guardada en {output_path}")


if __name__ == "__main__":
    main()
