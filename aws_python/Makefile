BUILDDIR = .deploy

all:
	#create zip package to upload to AWS
	mkdir -p $(BUILDDIR)
	cp -r * $(BUILDDIR)
	cd $(BUILDDIR); pip3 install -t . -r requirements.txt; zip -r aws.zip *
	cp $(BUILDDIR)/aws.zip .

.PHONY: deploy
deploy:
	$(if ! -f aws.zip, make all)
	aws lambda update-function-code --function-name arn:aws:lambda:eu-west-1:285737895683:function:extensionBackend --zip-file fileb://./aws.zip

clean:
	rm aws.zip
	rm -r .deploy/


