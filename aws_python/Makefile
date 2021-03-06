SHELL=/bin/bash

PACKAGENAME=aws_python
REMOTEUSER=ubuntu
REMOTE=opposingviews.media
SSH_ARGS=-i $(KEY)
KEY=$(HOME)/.ssh/id_rsa

$(PACKAGENAME).zip:
	#create zip package to upload to AWS
	ls | grep --invert-match --regexp="bin\|lib\|lib64" | zip -r -@ $(PACKAGENAME).zip

bin lib:
	python3 -m virtualenv .

.PHONY: deploy depend start clean cleandep cleanall

cleandep:
	if [ -e bin ]; then rm -r bin; fi;
	if [ -e lib ]; then rm -r lib; fi;
	if [ -h lib64 ]; then rm lib64; fi;
	if [ -e pip-selfcheck.json ]; then rm pip-selfcheck.json; fi
	if [ -e include ]; then rm -r include; fi

clean:
	if [ -e $(PACKAGENAME).zip ]; then rm $(PACKAGENAME).zip; fi;

cleanall:
	$(MAKE) cleandep
	$(MAKE) clean

depend: bin lib
	bash -c 'source "bin/activate" ; pip3 install -r requirements.txt ; deactivate'

deploy: $(PACKAGENAME).zip
	ssh $(SSH_ARGS) $(REMOTEUSER)@$(REMOTE) "mkdir -p $(PACKAGENAME)"
	scp $(SSH_ARGS) $(PACKAGENAME).zip "$(REMOTEUSER)@$(REMOTE):$(PACKAGENAME)/"
	ssh $(SSH_ARGS) $(REMOTEUSER)@$(REMOTE) "cd $(PACKAGENAME); unzip -o $(PACKAGENAME).zip"

start:
	$(MAKE) depend
	killall -q python3 || echo 1
	bash -c 'source "bin/activate" ; ./server.py & '
	#At this point is is safe to Ctrl-C if necessary
