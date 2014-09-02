images: png

png: pageflow.png submit.png staffresponse.png userreply.png search.png

# generate PNG images from the GraphViz diagrams
%.png: %.dot
	dot -Tpng -o$@ $<
