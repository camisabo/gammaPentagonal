import os
from gamma_pentagonal import GammaPentagonalCipher, QuantumCoverAnalyzer


def main() -> None:
    cipher = GammaPentagonalCipher()
    coords = cipher.encrypt("abcd")

    analyzer = QuantumCoverAnalyzer()
    analysis = analyzer.analyze(coords, layer_size=1)

    project_root = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(project_root, "grafo_qft_capas.png")

    analyzer.visualize_qft_layer_graph(
        analysis=analysis,
        title="Estructura QFT de W1..W10",
        save_path=output_path,
    )
    print(f"Imagen guardada en {output_path}")


if __name__ == "__main__":
    main()
