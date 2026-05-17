import networkx as nx
import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass
from typing import Dict

# ==========================================
# 1. DATA MODELS (BRANCH: TRANSACTIONAL DEIXIS)
# ==========================================

@dataclass
class Particle:
    word: str
    category: str
    mass: float = 1.0
    color: str = '#888888'
    is_anchor: bool = False
    is_payload: bool = False
    is_excluded: bool = False

# ==========================================
# 2. THE LINGUISTIC PHYSICS ENGINE
# ==========================================

class DeicticUniverse:
    def __init__(self, social_tension: float = 4.0, discourse_rep: float = 3.0, flow_velocity: float = 1.5):
        """
        Initializes the N-body semantic space for transactional linguistics.
        """
        self.social_tension = social_tension
        self.discourse_repulsion = discourse_rep
        self.flow_velocity = flow_velocity 
        
        self.G = nx.Graph()
        self.positions: Dict[str, np.ndarray] = {}
        
    def add_particle(self, particle: Particle):
        self.G.add_node(particle.word, attr=particle)
        
    def add_spring(self, word1: str, word2: str, weight: float):
        self.G.add_edge(word1, word2, weight=weight)
        
    def _compute_custom_forces(self, initial_pos: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        # Base physical layout
        pos = nx.spring_layout(
            self.G, 
            k=1/self.discourse_repulsion, 
            iterations=200, 
            weight='weight', 
            seed=42,
            pos=initial_pos
        )
        
        # Apply Transactional Flow and Exclusion Forces
        for node, coords in pos.items():
            particle = self.G.nodes[node]['attr']
            
            # Lock the Subject (I) to the left and Target (You) to the right
            if particle.is_anchor and particle.word == 'I':
                coords[0] = -2.0
                coords[1] = 0.0
            elif particle.is_anchor and particle.word == 'You':
                coords[0] = 2.0
                coords[1] = 0.0
                
            # The Payload (Gift) is pulled structurally toward "You" via flow velocity
            if particle.is_payload:
                coords[0] += self.flow_velocity
                
            # Excluded nodes get pushed radially outward
            if particle.is_excluded:
                radius = np.linalg.norm(coords)
                if radius > 0:
                    coords += (coords / radius) * self.discourse_repulsion
                    
        return pos

    def simulate(self):
        initial_pos = {node: np.random.rand(2) for node in self.G.nodes()}
        self.positions = self._compute_custom_forces(initial_pos)

    def render(self):
        if not self.positions:
            raise ValueError("Simulation must be run before rendering.")

        edge_x, edge_y = [], []
        for edge in self.G.edges():
            x0, y0 = self.positions[edge[0]]
            x1, y1 = self.positions[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=3, color='#555555', dash='dot'),
            hoverinfo='none',
            mode='lines'
        )

        node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
        
        for node in self.G.nodes():
            particle = self.G.nodes[node]['attr']
            x, y = self.positions[node]
            
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_color.append(particle.color)
            node_size.append(45 if particle.is_payload else (35 if not particle.is_excluded else 20))

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            textfont=dict(size=14, color='white', family="Courier New"),
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=node_color,
                size=node_size,
                line=dict(width=2, color='#ffffff')
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Deictic Topology: "I have a gift for you"',
                titlefont=dict(size=20, family="Courier New", color="#FFFFFF"),
                plot_bgcolor="#111111",
                paper_bgcolor="#111111",
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=60),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        fig.show()

# ==========================================
# 3. EXECUTION SCRIPT
# ==========================================

if __name__ == "__main__":
    # Instantiate the Universe with transactional flow
    universe = DeicticUniverse(social_tension=4.0, discourse_rep=3.0, flow_velocity=1.0)

    # 1. Define Particles
    universe.add_particle(Particle('I', 'Subject/Source', color='#1f77b4', is_anchor=True))
    universe.add_particle(Particle('You', 'Target/Beneficiary', color='#1f77b4', is_anchor=True))
    universe.add_particle(Particle('Have', 'Present State', color='#e377c2'))
    universe.add_particle(Particle('Gift', 'Payload', color='#9467bd', is_payload=True, mass=2.0))
    universe.add_particle(Particle('For', 'Directional Conduit', color='#2ca02c'))
    
    # Excluded conceptual nodes (Things not being given, or other recipients)
    universe.add_particle(Particle('Selfishness', 'Excluded Concept', color='#444444', is_excluded=True))
    universe.add_particle(Particle('Someone Else', 'Excluded Target', color='#444444', is_excluded=True))

    # 2. Define Syntactic/Semantic Springs (Edges)
    # The baseline relationship
    universe.add_spring('I', 'You', weight=universe.social_tension)
    
    # The syntax of the transaction
    universe.add_spring('I', 'Have', weight=3.0)
    universe.add_spring('Have', 'Gift', weight=4.0)
    universe.add_spring('Gift', 'For', weight=4.0)
    universe.add_spring('For', 'You', weight=5.0)

    # 3. Simulate and Render
    universe.simulate()
    universe.render()
