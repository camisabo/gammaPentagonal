import os
import matplotlib
matplotlib.use("Agg")

from gamma_pentagonal import GammaPentagonalCipher, QuantumCoverAnalyzer


def main() -> None:
    cipher = GammaPentagonalCipher()
    coords = cipher.encrypt("ab")

    analyzer = QuantumCoverAnalyzer()
    analysis = analyzer.analyze(coords, layer_size=2)

    project_root = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(project_root, "grafo_cobertura_quantum.png")

    analyzer.visualize_reduced_covering_graph(
        analysis=analysis,
        title="Grafo de Cobertura Reducido",
        save_path=output_path,
    )
    print(f"Imagen guardada en {output_path}")


if __name__ == "__main__":
    main()
