# MATH6010-homework

Follow the commands below to start.

```shell
git clone https://github.com/sszxc/MATH6010-homework.git
cd MATH6010-homework/
python -m pip install -r requirements.txt
```
## Dependency

[NetworkX](https://networkx.org/) with [doc](https://networkx.org/documentation/stable/reference/generators.html).



## Assignments

1. Min Dominating Set

    > Theorem: Let $G=(V,E)$ be a graph on $n$ vertices, with minimum degree $\delta>1$. Then $G$ has a dominating set of at most $n[1+\ln(\delta+1)]/(\delta+1)$ vertices.

    Write a greedy algorithm to find a dominating set that satisfies the theorem.

    ![result](hw1_MinDomSet/demo.jpg)

2. Monochromatic K4
   
    > Theorem: There is a two-coloring of $K_n$ with at most $C_n^4 2^{-5}$ monochromatic K4.

    Write a greedy algorithm to find a method of coloring the edges that satisfies the theorem.