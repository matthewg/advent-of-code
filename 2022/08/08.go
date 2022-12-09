package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Tree struct {
	R, C   int
	Height int
}

func (c Tree) Row() int {
	return c.R
}

func (c Tree) Col() int {
	return c.C
}

func GridConv(r rune, row, col int) Tree {
	h, _ := strconv.Atoi(string(r))
	return Tree{row, col, h}
}

func main() {
	var g aocutils.Grid[Tree]
	visibleCount := 0
	aocutils.LoadGrid(os.Args[1], GridConv, &g)
	i := g.NewIterator()
	maxSS := 0
	for t := i.Next(); t != nil; t = i.Next() {
		visible := false
		h := t.Height
		r := t.Row()
		c := t.Col()

		// Up
		s := 0
		if r == 1 {
			//fmt.Printf("...visible (U edge)!\n")
			visible = true
		} else {
			allShorter := true
			for n := r - 1; n > 0; n-- {
				h2 := g.Cell(n, c).Height
				s++
				//fmt.Printf("...U: %v vs. %v@%v,%v\n", h, h2, n, c)
				if h2 >= h {
					allShorter = false
					break
				}
			}
			if allShorter {
				//fmt.Printf("...visible (U)!\n")
				visible = true
			}
		}
		scenicScore := s

		// Down
		s = 0
		if r == g.RowLen() {
			//fmt.Printf("...visible (D edge)!\n")
			visible = true
		} else {
			allShorter := true
			for n := r + 1; n <= g.RowLen(); n++ {
				h2 := g.Cell(n, c).Height
				s++
				//fmt.Printf("...D: %v vs. %v@%v,%v\n", h, h2, n, c)
				if h2 >= h {
					allShorter = false
					break
				}
			}
			if allShorter {
				//fmt.Printf("...visible (D)!\n")
				visible = true
			}
		}
		scenicScore *= s

		// Left
		s = 0
		if c == 1 {
			visible = true
			//fmt.Printf("...visible (L edge)!\n")
		} else {
			allShorter := true
			for n := c - 1; n > 0; n-- {
				h2 := g.Cell(r, n).Height
				s++
				//fmt.Printf("...L: %v vs. %v@%v,%v\n", h, h2, r, n)
				if h2 >= h {
					allShorter = false
					break
				}
			}
			if allShorter {
				visible = true
				//fmt.Printf("...visible (L)!\n")
			}
		}
		scenicScore *= s

		// Right
		s = 0
		if c == g.ColLen() {
			visible = true
			//fmt.Printf("...visible (R edge)!\n")
		} else {
			allShorter := true
			for n := c + 1; n <= g.ColLen(); n++ {
				h2 := g.Cell(r, n).Height
				s++
				//fmt.Printf("...R: %v vs. %v@%v,%v\n", h, h2, r, n)
				if h2 >= h {
					allShorter = false
					break
				}
			}
			if allShorter {
				//fmt.Printf("...visible (R)!\n")
				visible = true
			}
		}
		scenicScore *= s

		fmt.Printf("Tree %v@%v,%v is visible: %v, ss=%v\n", h, r, c, visible, scenicScore)
		if visible {
			visibleCount++
		}
		if scenicScore > maxSS {
			maxSS = scenicScore
		}
	}

	fmt.Printf("Visible trees: %v\n", visibleCount)
	fmt.Printf("Maximum scenic score: %v\n", maxSS)
}
