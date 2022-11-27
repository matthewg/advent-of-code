package aocutils

import (
	"bufio"
	"io"
	"log"
	"os"
	"strings"
)

func Lines[T any](path string, convFn func(string) T) []T {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var lines []T
	reader := bufio.NewReader(file)
	for {
		line, err := reader.ReadString('\n')
		line = strings.TrimSuffix(line, "\n")
		convLine := convFn(line)
		if err == nil {
			lines = append(lines, convLine)
		} else if err == io.EOF {
			return lines
		} else {
			log.Fatalf("Error reading %v: %v", path, err)
		}
	}
}
