# MATH6010-homework

Follow the commands below to start.

```shell
git clone https://github.com/sszxc/MATH6010-homework.git
cd MATH6010-homework/
python -m pip install -r requirements.txt
```
## Dependency

[NetworkX](https://networkx.org/) for
the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

[matplotlib](https://matplotlib.org/) for creating static, animated, and interactive visualizations.

[tqdm](https://github.com/tqdm/tqdm) for a smart progress meter.

## Homework 1: Minimum Dominating Set

Definition: A dominating set for a graph $G=(V,E)$ is a subset $D$ of $V$ such that every vertex not in $D$ is adjacent to at least one member of $D$.

Theorem: Let $G=(V,E)$ be a graph on $n$ vertices, with minimum degree $\delta>1$. Then $G$ has a dominating set of at most $n[1+\ln(\delta+1)]/(\delta+1)$ vertices.

Task: Design a greedy algorithm to find a dominating set that satisfies the theorem.

### Solution

```python
python hw1_MinDomSet\min_dom_set.py
```

![result](hw1_MinDomSet/result.jpg)

## Homework 2: Monochromatic K4

Definition: $K_n$ is a complete graph (a clique) with $n$ nodes.

Theorem: There is a two-coloring of $K_n$ with at most $C_n^4 2^{-5}$ monochromatic K4.

Task: Design an algorithm based on derandomization to find a method of coloring the edges that satisfies the theorem.

### Solution

```python
python hw2_MonochromaticK4\monochromatic_k4.py
```

The algorithm is specially optimized to take only 23 seconds for a problem of 100 vertices.

![result](hw2_MonochromaticK4/result.jpg)

## Homework 3: 0-1 Knapsack problem

Given weights and values of n items, put these items in a knapsack of capacity W to get the maximum total value in the knapsack. 

Task: Design an algorithm based on simulated annealing to solve the 0-1 knapsack problem.

### Solution

```python
python hw3_knapsack\SimulatedAnnealing.py
```

![result](hw3_knapsack/result.jpg)

## Homework 3: Steiner Triple Systems

Definition: A Steiner triple system is a set system $(V,B)$ in which every block has size three, and every pair of points from $V$ is contained in a unique block. If $|V| =v$, then we denote such a system as an STS(v).

Task: Design a hill-climbing algorithm to construct random STS(v).

### Solution

```python
python hw3_STS\STS_HillClimbing.py
```

![result](hw3_STS/result_9.gif)