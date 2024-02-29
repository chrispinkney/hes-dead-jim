package main

import (
	"fmt"
	"golang.org/x/net/html"
	"net/http"
	"os"
	"strings"
)

func main() {
	if len(os.Args) == 1 {
		fmt.Println("This program checks for broken links. Please specify -h for help.")
		os.Exit(1)
	}

	parseArgs()
}

func parseArgs() {
	if len(os.Args) < 3 {
		printUsage()
	}

	option := os.Args[1]
	switch option {
	case "-h":
		printUsage()
	case "-u":
		processLink(os.Args[2])
	case "-f":
		links := processFile(os.Args[2])
		processLinks(links)
	default:
		printUsage()
	}
}

func printUsage() {
	fmt.Println("Usage: hdj -f [filename.html] or hdj -u [url]")
	os.Exit(0)
}

func processLink(link string) {
	fmt.Println(link)
	os.Exit(0)
}

func processFile(filename string) []string {
	bs, err := os.ReadFile(filename)
	if err != nil {
		fmt.Println("Error reading file: ", err)
		os.Exit(1)
	}

	doc, err := html.Parse(strings.NewReader(string(bs)))
	if err != nil {
		fmt.Println("Error parsing HTML:", err)
		os.Exit(1)
	}

	var links []string

	var getLinks func(*html.Node)
	getLinks = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "a" {
			for _, attr := range n.Attr {
				if attr.Key == "href" {
					links = append(links, attr.Val)
				}
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			getLinks(c)
		}
	}

	getLinks(doc)

	return links
}

func processLinks(links []string) {
	for _, l := range links {
		resp, err := http.Get(l)
		if err != nil {
			fmt.Println(err.Error())
			continue
		}

		fmt.Println(resp.Request.URL, "has a status of", resp.StatusCode)
	}
}
