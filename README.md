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

> Theorem: Let $G=(V,E)$ be a graph on $n$ vertices, with minimum degree $\delta>1$. Then $G$ has a dominating set of at most $n[1+\ln(\delta+1)]/(\delta+1)$ vertices.

Write a greedy algorithm to find a dominating set that satisfies the theorem.

### Solution

```python
python hw1_MinDomSet\min_dom_set.py
```

![result](hw1_MinDomSet/result.jpg)

## Homework 2: Monochromatic K4

> Theorem: There is a two-coloring of $K_n$ with at most $C_n^4 2^{-5}$ monochromatic K4. Here, $K_n$ is a complete graph (a clique) with $n$ nodes.

Write a greedy algorithm to find a method of coloring the edges that satisfies the theorem.

### Solution

```python
python hw2_MonochromaticK4\monochromatic_k4.py
```

The algorithm is specially optimized to take only 23 seconds for a problem of 100 vertices.

![result](hw2_MonochromaticK4/result.jpg)
