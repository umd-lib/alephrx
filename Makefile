DEPLOY_DIR=/apps/usmai/alephrx

# gets updates to the repo and updates the CGI scripts and document root
deploy:
	/usr/local/bin/git pull
	cp -rpv cgi-bin lib htdocs $(DEPLOY_DIR)
