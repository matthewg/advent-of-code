package main

import (
	"fmt"
	"math"
	"os"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Square struct {
	Height, R, C   int
	IsStart, IsEnd bool
}

func (s Square) Row() int { return s.R }
func (s Square) Col() int { return s.C }

type Node = *aocutils.Node[*Square]

func ParseHeight(c rune, row, col int) Square {
	var h int
	if c == 'S' {
		h = 1
	} else if c == 'E' {
		h = 26
	} else {
		h = strings.IndexRune("_abcdefghijklmnopqrstuvwxyz", c)
	}
	return Square{
		Height:  h,
		R:       row,
		C:       col,
		IsStart: c == 'S',
		IsEnd:   c == 'E',
	}
}

func main() {
	var heightmap aocutils.Grid[Square]
	aocutils.LoadGrid(os.Args[1], ParseHeight, &heightmap)

	var start, end Node
	var starts []Node
	nodes := make(map[*Square]Node)
	for r := 1; r <= heightmap.RowLen(); r++ {
		for c := 1; c <= heightmap.ColLen(); c++ {
			s := heightmap.Cell(r, c)
			node, ok := nodes[s]
			if !ok {
				node = aocutils.NewNode(s)
				nodes[s] = node
			}
			if s.IsStart {
				start = node
			} else if s.IsEnd {
				end = node
			}

			if s.Height == 1 {
				starts = append(starts, node)
			}

			for _, n := range aocutils.GridNeighbors(&heightmap, *s, false) {
				if (n.Height - 1) <= s.Height {
					m, ok := nodes[n]
					if !ok {
						m = aocutils.NewNode(n)
						nodes[n] = m
					}
					node.AddEdge(1, m, false)
				}
			}
		}
	}

	steps := start.DijkstraShortestPath(end)
	fmt.Printf("Steps (part 1): %v\n", steps)

	ms := math.MaxInt
	for _, strt := range starts {
		scnt := strt.DijkstraShortestPath(end)
		if scnt < ms && scnt > 0 {
			ms = scnt
		}
	}
	fmt.Printf("Shortest steps (part 2): %v\n", ms)
}
