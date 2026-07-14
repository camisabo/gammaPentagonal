import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gamma_pentagonal import GammaPentagonalCipher, QuantumCoverAnalyzer


class QuantumCoverAnalyzerTests(unittest.TestCase):
    def test_analyze_returns_quantum_structure(self):
        cipher = GammaPentagonalCipher()
        coords = cipher.encrypt("ab")

        analyzer = QuantumCoverAnalyzer()
        analysis = analyzer.analyze(coords, layer_size=2)

        self.assertIn("tensor_network", analysis)
        self.assertIn("layers", analysis)
        self.assertIn("reduced_covering_graph", analysis)
        self.assertIn("qft", analysis)

        self.assertTrue(analysis["tensor_network"]["identity_tensors"] >= 0)
        self.assertEqual(len(analysis["layers"]), 1)
        self.assertTrue(analysis["qft"]["dominant_frequency_index"] >= 0)
        self.assertGreaterEqual(len(analysis["qft"]["top_frequencies"]), 1)


if __name__ == "__main__":
    unittest.main()
