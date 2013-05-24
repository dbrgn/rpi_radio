#!/bin/bash

pdflatex wiring.tex && \
convert -flatten -density 300 wiring.pdf -quality 90 -resize 712x712 wiring_small.png
