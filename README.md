# A Maze Ing

Un générateur et solveur de labyrinthe en Python avec interface MLX (2D pixels), accompagné de code robuste, tests et typage statique.

## Description

A Maze Ing vise à implémenter un ensemble de fonctionnalités complètes pour la génération, représentation et résolution d’un labyrinthe, dans un contexte pédagogique :
- génération de labyrinthe avec deux algorithmes classiques (`DepthFirstSearch` et `Kruskal`);
- représentation textuelle et structurelle de la grille via `Cell` et `Maze`;
- solveurs (`DepthFirstSearchSolver`, `AStar`) pour retrouver un chemin source/target;
- interface graphique avec `mlx` pour visualiser en temps réel.

Le but est de coder un moteur de maze complet, testable et maintenable, tout en appliquant des pratiques modernes (typing, tests, CI via Makefile).

## Objectifs

- comprendre et placer les algorithmes de génération dans un pipeline complet
- offrir un usage reproductible via config + API
- démontrer la compatibilité avec `pytest` et `mypy`
- fournir un produit avec UI interactive et animation de chemin

## Instructions

### Prérequis

- Python 3.10+
- Numpy, Pydantic, Pytest, Mypyc/ Mypy, Flake8, mlx (via distribution locale `mlx-2.2-py3-none-any.whl`)

### Installation

```
git clone <url> amazing
cd amazing
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt  # si présent, sinon :
pip install pydantic numpy pytest mypy
pip install mlx-2.2-py3-none-any.whl
```

### Exécution

- Direct :
  ```
  PYTHONPATH=src python3 a_maze_ing.py config.txt
  ```
- Make :
  ```sh
  make run
  ```

### Tests

```
PYTHONPATH=src pytest
```

### Lint / mypy

```
make lint
make lint-strict
```

ou

```
PYTHONPATH=src python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs -p mazegen -p AMazeIng
```

## Structure du projet

- `a_maze_ing.py` : point d’entrée CLI / application MLX.
- `src/AMazeIng.py` : modèle Pydantic + orchestration `Maze`/`MazeGenerator`/`MazeSolver`.
- `src/mazegen/Cell.py` : classe `Cell` (int bitmask) + méthodes accès.
- `src/mazegen/Maze.py` : stockage et opérations sur la grille.
- `src/mazegen/MazeGenerator.py` : interfaces + `DepthFirstSearch`, `Kruskal`.
- `src/mazegen/MazeSolver.py` : `DepthFirstSearchSolver`, `AStar`.
- `src/parsing/Parsing.py` : lecture et validation du `config.txt`.
- `tests/` : tests unitaires.
- `Makefile` : cibles build/install/run/lint.

## Config file (complète)

- `config.txt` doit contenir au moins :
  - largeur/hauteur
  - entrée et sortie (coordonnées 1-based)
  - nom du solveur, nom du générateur
  - paramètres de visualisation.

(Le parser `src/parsing/Parsing.py` gère la validation et erreur 1/2/3 etc.)

## Algorithme de génération choisi

- `Kruskal` (fusion d’ensembles) comme méthode principale.
- `DepthFirstSearch` (backtracking) complémentaire.

### Pourquoi Kruskal

- génère un labyrinthe parfait, totalement plein sans cycles, très lisible.
- bonne base pour `unperfect_maze` (possibilité de briser des murs).
- facile à tester et à raisonner, code modulaire.

## Reusable code

- `Cell` et `Maze` peuvent servir à n’importe quelle appli de grille / labyrinthes.
- `MazeGenerator` / `MazeSolver` sont des interfaces réutilisables pour autres implémentations.
- `Parsing` est un parser général de config (validation Pydantic).

## Usage / features avancées

- supports `perfect` ou `imperfect` (avec openning randomisé)
- render loop avec maj dynamique et chemins animés
- switch generator/solver à l’exécution
- couleur de chemin et patterns (42)

## Resources

- Documentation python : https://docs.python.org/3/
- Mypy : https://mypy.readthedocs.io/
- Pydantic : https://docs.pydantic.dev/
- Algorithme labyrinthe : https://en.wikipedia.org/wiki/Maze_generation_algorithm 
- A* : https://en.wikipedia.org/wiki/A*_search_algorithm
- Tutoriel DFS / Kruskal maze : https://weblog.jamisbuck.org/2011/1/16/maze-generation-depth-first-search

### IA utilisée

- Copilot Chat (Raptor mini) : aide à :
  - correction d’erreurs `mypy` / import module
  - refactorisation import `from mazegen.Cell import Cell`
  - création du README complet
  - recommandations de workflow et tests

## Équipe et gestion de projet

- Dev unique ou équipe réduite (à préciser) :
  - Rôles : dev, tests, doc, releases.
- Planning anticipé :
  - 1 semaine : structure + model
  - 1 semaine : générateur + solveur
  - 1 semaine : interface MLX + tests
  - 1 semaine : typage / CI / docs
- Ce qui a bien marché :
  - architecture modulaire, tests automatisés
  - apprentissage sur typage et mypy
- Améliorations possibles :
  - ajout d’une UI web/SDL
  - stubs type pour `mlx`
  - config utilisateur plus riche / JSON

## Outils

- Python 3.10
- pytest, mypy, flake8
- uv/make
- Mlx (graphique)
- Git + GitHub

---

> Carte de sortie : ce README inclut toutes les parties demandées et est orienté projet complet A-Z.

## 🚀 Installation

1. Cloner le dépôt :
   ```sh
   git clone <url> amazing
   cd amazing
   ```
2. Créer un environnement :
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip setuptools
   pip install -r requirements.txt  # si présent ; sinon pip install pydantic numpy pytest mypy
   ```

## ▶️ Exécution

- Mode commande :
  ```sh
  PYTHONPATH=src python3 a_maze_ing.py config.txt
  ```
- Avec Makefile :
  ```sh
  make run
  ```

Le programme ouvre une fenêtre MLX et affiche le labyrinthe généré ; contrôles :
- 1 : regénérer
- 2 : afficher le chemin
- 3 : changer la couleur
- 4 : quitter

## 🧪 Tests

- Lancer tous les tests :
  ```sh
  PYTHONPATH=src pytest
  ```
- Fichiers de tests existants :
  - `tests/test_Cell.py`
  - `tests/test_Depth.py`
  - `tests/test_Maze.py`
  - `tests/test_MazeGenerator.py`
  - `tests/test_MazeSolver.py`
  - `tests/test_parsing.py`

## 🧹 Lint / typage

- Flake8 + MyPy (configuration dans Makefile)
  ```sh
  make lint
  make lint-strict
  ```
- Sur le projet, utilisez ces commandes :
  ```sh
  PYTHONPATH=src python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs -p mazegen -p AMazeIng
  ```

### Problèmes connus
- `mypy` en mode strict détecte :
  - `mlx` non typé, donc `no-untyped-call` (bibliothèque native sans stub)
  - `AMazeIng` identifié comme module installé sans `py.typed` pour l’autocomplétion stricte.

## 🛠️ Architecture

- `Cell` : gestion binaire des murs (N, E, S, W).
- `MazeGenerator.DepthFirstSearch` : génération récursive avec backtracking.
- `MazeGenerator.Kruskal` : génération via graphe d’ensembles disjoints.
- `MazeSolver.DepthFirstSearchSolver` : recherche DFS.
- `MazeSolver.AStar` : recherche A* avec heuristique Manhattan.

## 📝 Notes

- Préférer des imports relatifs depuis `src` :
  - `from mazegen.Cell import Cell` plutôt que `from mazegen import Cell` pour éviter les conflits `module is not valid as type`.
  - `from parsing.Parsing import DataMaze` pour la configuration.
- Le code est déjà prêt pour packaging avec `pyproject.toml` / `setup.cfg`.

## 📦 Distribution

- Makefile contient cible `build` générant 1 roue `.whl` via `uv build`.
- `install`|`run` sont inclus.

---

Projet maintenu en mode éducatif. Contribution bienvenue via issues et PR.

