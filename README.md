# Deictic Force Simulation

A physics-inspired linguistic visualisation model that represents sentence meaning as a force-directed graph using deictic forces, network theory, and interactive Plotly rendering.

This project simulates how pronouns, discourse structure, and temporal orientation behave like physical forces in a constrained semantic field.

---

## Conceptual Model

This system is based on a simple proposition:

> Language behaves like a constrained physical system where meaning emerges from tension between reference points.

We map linguistic constructs to physical analogues:

- **Person deixis ("I", "You")** → social attraction force
- **Discourse scope ("All")** → repulsive boundary constraint
- **Temporal reference ("Needed")** → directional gravity
- **Excluded referents** → repelled external space

---

## Core Parameters

These parameters control the “physics of meaning”:

```python
SOCIAL_DEIXIS_TENSION = 5.0
DISCOURSE_REPULSION = 2.5
TIME_DEIXIS_GRAVITY = -1.0
```

Interpretation:
SOCIAL_DEIXIS_TENSION
Controls intimacy between speaker and listener
Higher values compress "I" and "You"
DISCOURSE_REPULSION
Expands semantic space and increases structural separation
TIME_DEIXIS_GRAVITY
Shifts temporal reference points along a directional axis (past/future)

### Graph Construction

The model uses NetworkX to define a semantic graph:

Nodes represent linguistic entities
Edges represent relational tension (spring forces)
Weights define equilibrium distance between concepts

### Core structure:

External concepts are intentionally excluded and pushed outward.

### Physics Engine

The layout is computed using:

Fruchterman–Reingold force-directed algorithm
Spring stiffness based on linguistic weights
Custom perturbations for:
temporal drift
discourse exclusion zones

Key equation conceptually approximated:

Attractive force along edges + global repulsive field = emergent semantic structure

### Visualisation

Rendered using Plotly Graph Objects:

Interactive node positioning
Hover labels for semantic inspection

Color-coded linguistic roles:

🔵 Person deixis (I / You)
🟠 Temporal deixis (Needed)
🟢 Discourse scope (All)
⚫ Excluded context
