package aocutils

import "testing"

type TestCell struct {
	R, C int
	Data rune
}

func (c TestCell) Row() int {
	return c.R
}

func (c TestCell) Col() int {
	return c.C
}

func GridConv(r rune, row, col int) TestCell {
	return TestCell{row, col, r}
}

func TestGrid(t *testing.T) {
	var g Grid[TestCell]
	LoadGrid("test", GridConv, &g)
	gp := &g

	if rowlen := gp.RowLen(); rowlen != 4 {
		t.Fatalf("rowlen for %v is %v", g, rowlen)
	}

	if collen := gp.ColLen(); collen != 3 {
		t.Fatalf("collen for %v is %v", g, collen)
	}

	n := GridNeighbors(gp, gp.Cell(1, 1), false)
	if len(n) != 2 || n[0].Data != 'b' || n[1].Data != 'd' {
		t.Fatalf("neighbors(1, 1): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(1, 2), false)
	if len(n) != 3 || n[0].Data != 'a' || n[1].Data != 'c' || n[2].Data != 'e' {
		t.Fatalf("neighbors(1, 2): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(1, 3), false)
	if len(n) != 2 || n[0].Data != 'b' || n[1].Data != 'f' {
		t.Fatalf("neighbors(1, 3): %v", n)
	}

	n = GridNeighbors(gp, gp.Cell(2, 1), false)
	if len(n) != 3 || n[0].Data != 'a' || n[1].Data != 'e' || n[2].Data != 'g' {
		t.Fatalf("neighbors(2, 1): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(2, 2), false)
	if len(n) != 4 || n[0].Data != 'b' || n[1].Data != 'd' || n[2].Data != 'f' || n[3].Data != 'h' {
		t.Fatalf("neighbors(2, 2): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(2, 3), false)
	if len(n) != 3 || n[0].Data != 'c' || n[1].Data != 'e' || n[2].Data != 'i' {
		t.Fatalf("neighbors(2, 3): %v", n)
	}

	n = GridNeighbors(gp, gp.Cell(3, 1), false)
	if len(n) != 3 || n[0].Data != 'd' || n[1].Data != 'h' || n[2].Data != 'j' {
		t.Fatalf("neighbors(3, 1): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(3, 2), false)
	if len(n) != 4 || n[0].Data != 'e' || n[1].Data != 'g' || n[2].Data != 'i' || n[3].Data != 'k' {
		t.Fatalf("neighbors(3, 2): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(3, 3), false)
	if len(n) != 3 || n[0].Data != 'f' || n[1].Data != 'h' || n[2].Data != 'l' {
		t.Fatalf("neighbors(3, 3): %v", n)
	}

	n = GridNeighbors(gp, gp.Cell(4, 1), false)
	if len(n) != 2 || n[0].Data != 'g' || n[1].Data != 'k' {
		t.Fatalf("neighbors(4, 1): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(4, 2), false)
	if len(n) != 3 || n[0].Data != 'h' || n[1].Data != 'j' || n[2].Data != 'l' {
		t.Fatalf("neighbors(4, 2): %v", n)
	}
	n = GridNeighbors(gp, gp.Cell(4, 3), false)
	if len(n) != 2 || n[0].Data != 'i' || n[1].Data != 'k' {
		t.Fatalf("neighbors(4, 3): %v", n)
	}
}

func LinesConv(s string) string {
	return s
}

func TestLines(t *testing.T) {
	lines := Lines("test", LinesConv)
	if len(lines) != 4 {
		t.Fatalf("lines have wrong len: %v", lines)
	}
	if lines[0] != "abc" {
		t.Fatalf("lines[0]: %v", lines)
	}
	if lines[1] != "def" {
		t.Fatalf("lines[1]: %v", lines)
	}
	if lines[2] != "ghi" {
		t.Fatalf("lines[2]: %v", lines)
	}
	if lines[3] != "jkl" {
		t.Fatalf("lines[3]: %v", lines)
	}
}

func RecordsConv(s string) string {
	return s
}

func TestRecords(t *testing.T) {
	records := Records("test2", "---\n", RecordsConv)
	if len(records) != 2 {
		t.Fatalf("records have wrong len: %v", records)
	}
	if records[0] != "abc\ndef\n" {
		t.Fatalf("records[0]: %v", records)
	}
	if records[1] != "ghi\njkl\n" {
		t.Fatalf("records[1]: %v", records)
	}
}
