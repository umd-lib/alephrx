images: png svg

png: pageflow.png submit.png staffresponse.png

svg: pageflow.svg submit.svg staffresponse.svg

# generate SVG images from the GraphViz diagrams
%.svg: %.dot
	dot -Tsvg -o$@ $<

# generate PNG images from the GraphViz diagrams
%.png: %.dot
	dot -Tpng -o$@ $<
