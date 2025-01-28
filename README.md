# 🧩 8-Puzzle Heuristics Study 🧩

<div align="center">
  <img src="https://github.com/user-attachments/assets/336f6d7c-3696-4de3-b38e-c69f716c7faf" alt="Image Description">
</div>

Welcome to the **8-Puzzle** project! This repository contains the implementation of various heuristics and search algorithms to solve the classic 8-puzzle problem. The project is designed to explore the efficiency of different heuristic functions and search strategies in finding the optimal solution to the puzzle.

## 🌟 Introduction

The 8-puzzle is a classic sliding puzzle that consists of a 3x3 grid with 8 numbered tiles and one empty space. The goal is to rearrange the tiles from a given initial state to a specified goal state by sliding the tiles into the empty space. This project focuses on implementing and comparing different heuristic functions and search algorithms to solve the 8-puzzle efficiently.

## 🔍 Heuristics Implemented

We implemented four admissible heuristics to guide the search algorithms:

1. **h1: Number of Misplaced Tiles** 🧩
   - Counts the number of tiles that are not in their goal positions.

2. **h2: Sum of Euclidean Distances** 📏
   - Calculates the Euclidean distance of each tile from its goal position and sums them up.

3. **h3: Sum of Manhattan Distances** 🚕
   - Computes the Manhattan distance of each tile from its goal position and sums them up.

4. **h4: Number of Tiles Out of Row + Number of Tiles Out of Column** 🔢
   - Counts the number of tiles that are out of their correct row or column.

## 🛠️ Search Algorithms

We implemented and compared the following search algorithms:

- **Depth-First Search (DFS)** 🔍
- **Breadth-First Search (BFS)** 🌐
- **A* Search** ⭐
- **Uniform Cost Search (UCS)** ⚖️

Each algorithm was tested with the four heuristics to evaluate their performance in terms of solution depth, number of expanded nodes, and fringe size.

## 📝 Tasks

The project was divided into the following tasks:

1. **Task 1: Implement 4 Different Heuristics**  
   - Implemented the four heuristics (h1, h2, h3, h4) and verified their admissibility.

2. **Task 2: Comparing Heuristics**  
   - Compared the performance of the four heuristics by solving a large number of randomly generated puzzles.

3. **Task 3: Overall Comparison Between Strategies**  
   - Compared the best heuristic (h3) with uninformed search algorithms (BFS, DFS, UCS).

4. **Task 4: Extra Credit - Scaling to NxN Puzzle**  
   - Extended the project to solve NxN puzzles and reran the performance tests.

## 📊 Results

After extensive testing, we found that the **A* Search** algorithm combined with the **Manhattan Distance heuristic (h3)** performed the best in terms of solution optimality and efficiency. Below are some key findings:

- **A* Search** had the smallest fringe size and explored fewer nodes compared to BFS and DFS.
- **h3 (Manhattan Distance)** provided the most accurate estimate of the remaining cost to reach the goal state.
- **DFS** was the fastest but often returned suboptimal solutions due to its depth-limited nature.

For more detailed results, refer to the [project report](#).
