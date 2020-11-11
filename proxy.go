package main

import (
	"bufio"
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
)

// Global Value for PROXY
var proxyString string = "http://127.0.0.1:8080"

// Request URL, Default nil
// var reqURL io.Reader

// Color
var reset string = "\033[0m"
var red string = "\033[31m"
var green string = "\033[32m"

func main() {
	reader := bufio.NewReader(os.Stdin)

	var proxyStr string = ""
	var help bool = false
	flag.StringVar(&proxyStr, "p", "proxy", "Proxy URL")
	flag.BoolVar(&help, "h", false, "Help menu")
	flag.Parse()
	// Show Usage Info
	flag.Usage = func() {
		h := "Usage: Proxy to Burp ...\n\n"

		h += "Usage:\n"
		h += "  proxy [options]\n\n"

		h += "Options:\n"
		h += "  -p, --proxy     Use an alternate proxy\n" +
			"					In Case you don't want to use the default one"

		h += "Examples:\n"
		h += "  proxy\n"
		h += "  proxy -p \"http://85.133.183.66:8080\"\n"

		fmt.Fprintf(os.Stderr, h)
	}

	if len(os.Args) < 1 {
		flag.Usage()
		os.Exit(0)
	} else if help {
		flag.Usage()
		os.Exit(0)
	}

	if proxyStr != "" {
		proxyString = proxyStr
	}

	// reqURL = os.Stdin

	proxyURL, _ := url.Parse(proxyString)
	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxyURL),
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true,
			},
		},
	}

	for {
		input, _, err := reader.ReadLine()
		if err != nil && err == io.EOF {
			break
		}
		targetURL := string(input)
		request, err := http.NewRequest("GET", targetURL, nil)
		request.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")

		res, err := client.Do(request)

		if err != nil {
			fmt.Printf(red+"%v\n"+reset, err)
			continue
		}
		if res != nil {
			fmt.Printf(green+"%v %v [%v]\n"+reset, "[+] Forwarded =>", targetURL, res.StatusCode)
		}
	}
}
