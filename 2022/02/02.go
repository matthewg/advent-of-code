package main

import (
	"fmt"
	"os"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Move int64

const (
	Rock     Move = 1
	Paper    Move = 2
	Scissors Move = 3
)

type Outcome int64

const (
	Win  Outcome = 6
	Lose Outcome = 0
	Draw Outcome = 3
)

type MovePair1 struct {
	Opponent Move
	You      Move
}
type MovePair2 struct {
	Opponent Move
	Outcome  Outcome
}
type MovePairs struct {
	I  MovePair1
	II MovePair2
}

func (p MovePair1) Score() int {
	score := int(p.You)
	var o Outcome

	switch p.You {
	case Rock:
		switch p.Opponent {
		case Rock:
			o = Draw
		case Paper:
			o = Lose
		case Scissors:
			o = Win
		}
	case Paper:
		switch p.Opponent {
		case Rock:
			o = Win
		case Paper:
			o = Draw
		case Scissors:
			o = Lose
		}
	case Scissors:
		switch p.Opponent {
		case Rock:
			o = Lose
		case Paper:
			o = Win
		case Scissors:
			o = Draw
		}
	}

	score += int(o)
	//fmt.Printf("Score for %+v: %v\n", p, score)
	return score
}

func (p MovePair2) To1() MovePair1 {
	var you Move

	if p.Outcome == Draw {
		you = p.Opponent
	} else {
		switch p.Opponent {
		case Rock:
			switch p.Outcome {
			case Win:
				you = Paper
			case Lose:
				you = Scissors
			}
		case Paper:
			switch p.Outcome {
			case Win:
				you = Scissors
			case Lose:
				you = Rock
			}
		case Scissors:
			switch p.Outcome {
			case Win:
				you = Rock
			case Lose:
				you = Paper
			}
		}
	}

	return MovePair1{
		Opponent: p.Opponent,
		You:      you,
	}
}

func LineToMovePairs(line string) MovePairs {
	var opponent, you Move

	switch line[0] {
	case 'A':
		opponent = Rock
	case 'B':
		opponent = Paper
	case 'C':
		opponent = Scissors
	}

	switch line[2] {
	case 'X':
		you = Rock
	case 'Y':
		you = Paper
	case 'Z':
		you = Scissors
	}

	i := MovePair1{
		Opponent: opponent,
		You:      you,
	}

	var o Outcome
	switch line[2] {
	case 'X':
		o = Lose
	case 'Y':
		o = Draw
	case 'Z':
		o = Win
	}
	ii := MovePair2{
		Opponent: opponent,
		Outcome:  o,
	}

	return MovePairs{i, ii}
}

func main() {
	movePairs := aocutils.Lines(os.Args[1], LineToMovePairs)
	totalScore1 := 0
	totalScore2 := 0
	for _, movePair := range movePairs {
		totalScore1 += movePair.I.Score()
		totalScore2 += movePair.II.To1().Score()
	}
	fmt.Printf("total score (part 1): %v\n", totalScore1)
	fmt.Printf("total score (part 2): %v\n", totalScore2)
}
