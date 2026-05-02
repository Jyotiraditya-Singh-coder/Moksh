# ai-services/quant-mentor/knowledge_graph.py
import networkx as nx
import json

class QuantKnowledgeGraph:
    """Knowledge graph for quant trading topics with prerequisites and relationships."""
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        # Core nodes
        nodes = [
            # Mathematics
            ("probability", {"category": "math", "difficulty": 2, "description": "Probability theory including Bayes, expectation, distributions"}),
            ("statistics", {"category": "math", "difficulty": 2, "description": "Statistical inference, regression, hypothesis testing"}),
            ("linear_algebra", {"category": "math", "difficulty": 2, "description": "Vectors, matrices, eigenvalues"}),
            ("calculus", {"category": "math", "difficulty": 2, "description": "Derivatives, integrals, optimization"}),
            ("combinatorics", {"category": "math", "difficulty": 2, "description": "Counting, permutations, combinations"}),
            ("stochastic_calculus", {"category": "math", "difficulty": 4, "description": "Ito calculus, Brownian motion"}),

            # Programming
            ("python", {"category": "programming", "difficulty": 1, "description": "Python for data analysis and modeling"}),
            ("cpp", {"category": "programming", "difficulty": 3, "description": "C++ for low-latency systems"}),
            ("data_structures", {"category": "programming", "difficulty": 2, "description": "Arrays, trees, graphs, hash tables"}),
            ("algorithms", {"category": "programming", "difficulty": 3, "description": "Sorting, searching, dynamic programming"}),
            ("time_complexity", {"category": "programming", "difficulty": 2, "description": "Big O analysis"}),

            # Quant specific
            ("market_making", {"category": "quant", "difficulty": 3, "description": "Market microstructure, bid-ask spread"}),
            ("options", {"category": "quant", "difficulty": 3, "description": "Options pricing, Greeks, Black-Scholes"}),
            ("order_books", {"category": "quant", "difficulty": 3, "description": "Limit order books, order flow"}),
            ("arbitrage", {"category": "quant", "difficulty": 3, "description": "Arbitrage strategies, statistical arbitrage"}),
            ("risk_management", {"category": "quant", "difficulty": 3, "description": "Value at Risk, stress testing"}),
            ("time_series", {"category": "quant", "difficulty": 3, "description": "ARIMA, GARCH, cointegration"}),

            # Brainteasers & mental math
            ("mental_math", {"category": "skills", "difficulty": 1, "description": "Rapid arithmetic without calculator"}),
            ("brainteasers", {"category": "skills", "difficulty": 2, "description": "Logic puzzles and lateral thinking"}),
        ]

        for node_id, attrs in nodes:
            self.graph.add_node(node_id, **attrs)

        # Prerequisite edges
        edges = [
            ("probability", "statistics"),
            ("probability", "stochastic_calculus"),
            ("calculus", "stochastic_calculus"),
            ("linear_algebra", "stochastic_calculus"),
            ("python", "data_structures"),
            ("data_structures", "algorithms"),
            ("algorithms", "time_complexity"),
            ("probability", "options"),
            ("calculus", "options"),
            ("statistics", "time_series"),
            ("options", "arbitrage"),
            ("market_making", "order_books"),
            ("brainteasers", "mental_math"),  # mental math is a sub-skill
        ]
        for u, v in edges:
            self.graph.add_edge(u, v)

    def get_prerequisites(self, topic: str):
        """Return list of prerequisite topic IDs."""
        return list(self.graph.predecessors(topic))

    def get_related(self, topic: str, depth=1):
        """Get topics within depth steps."""
        related = set()
        try:
            # nodes within depth steps (outgoing)
            for node in self.graph.nodes:
                try:
                    if nx.shortest_path_length(self.graph, topic, node) <= depth:
                        related.add(node)
                except nx.NetworkXNoPath:
                    continue
            # also incoming?
        except:
            pass
        return list(related)

    def get_all_topics(self):
        return list(self.graph.nodes(data=True))

    def get_topic_info(self, topic: str):
        return self.graph.nodes.get(topic)