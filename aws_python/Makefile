PACKAGENAME=aws_python_test
REMOTEUSER=ubuntu
REMOTE=ec2-34-240-199-221.eu-west-1.compute.amazonaws.com

$(PACKAGENAME).zip:
	#create zip package to upload to AWS
	ls | grep --invert-match --regexp="bin\|lib\|lib64" | zip -r -@ $(PACKAGENAME).zip

bin lib:
	python3 -m virtualenv .

.PHONY: deploy depend start clean cleandep cleanall

cleandep:
	$(if -d bin, rm -r bin)
	$(if -d lib, rm -r lib)
	$(if -r lib64, rm -r lib64)

clean:
	$(if -f $(PACKAGENAME).zip, rm $(PACKAGENAME).zip)

cleanall:
	$(MAKE) cleandep
	$(MAKE) clean

depend: bin lib
	bash -c 'source "bin/activate" ; pip3 install -r requirements.txt ; deactivate'

deploy: $(PACKAGENAME).zip
	ssh $(REMOTEUSER)@$(REMOTE) "mkdir -p $(PACKAGENAME)"
	scp $(PACKAGENAME).zip "$(REMOTEUSER)@$(REMOTE):$(PACKAGENAME)/"
	ssh $(REMOTEUSER)@$(REMOTE) "cd $(PACKAGENAME); unzip -o $(PACKAGENAME).zip; $(MAKE) start"

start:
	$(MAKE) depend
	killall -q python3 ; echo 1
	bash -c 'source "bin/activate" ; ./server.py & '
	#At this point is is safe to Ctrl-C if necessary
