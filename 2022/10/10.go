package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Instruction struct {
	delay, addToX int
}

func ParseInstruction(s string) Instruction {
	toks := strings.Split(s, " ")
	if toks[0] == "noop" {
		return Instruction{delay: 0, addToX: 0}
	} else if toks[0] == "addx" {
		v, _ := strconv.Atoi(toks[1])
		return Instruction{delay: 1, addToX: v}
	}
	log.Fatalf("Unknown instruction: '%v'", s)
	return Instruction{delay: 0, addToX: 0}
}

func Abs(i int) int {
	if i < 0 {
		return i * -1
	} else {
		return i
	}
}

func main() {
	regX := 1
	instructions := aocutils.Lines(os.Args[1], ParseInstruction)
	var pipeline []Instruction
	sigSum := 0
	for cycle := 1; cycle <= 241; cycle++ {
		//fmt.Printf("At start of cycle %v, X: %v\n", cycle, regX)
		if len(pipeline) == 0 {
			if len(instructions) > 0 {
				pipeline = append(pipeline, instructions[0])
				instructions = instructions[1:]
			}
		}

		// Day 2
		scanPos := (cycle - 1) % 40
		if Abs(scanPos-regX) <= 1 {
			fmt.Print("#")
		} else {
			fmt.Print(".")
		}
		if cycle > 20 && cycle%40 == 0 {
			fmt.Print("\n")
		}

		if (cycle+20)%40 == 0 {
			sigStrength := cycle * regX
			sigSum += sigStrength
			//fmt.Printf("Signal strength at cycle %v: %v\n", cycle, sigStrength)
		}
		if len(pipeline) > 0 {
			i := &pipeline[0]
			if i.delay == 0 {
				regX += i.addToX
				pipeline = pipeline[1:]
			} else {
				i.delay--
			}
			//fmt.Printf("After executing instruction %v, X: %v\n", *i, regX)
		}
	}
	fmt.Printf("Sum of signal strengths: %v\n", sigSum)
}
