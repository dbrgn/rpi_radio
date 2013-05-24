#!/bin/bash

pdflatex wiring.tex && \
convert -flatten -density 300 wiring.pdf -quality 90 -resize 920x920 wiring.png
