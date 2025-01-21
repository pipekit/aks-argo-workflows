DOCKER_REPO ?= joibel

workflow: workflow.yaml .calc .calcengine .consumer .fanout .report .scenario .stream .nats-dispatch .nats-consume .nats-wait .nats-create
	kubectl create -f $<

.%: %.yaml
#	argo template lint $<
	kubectl apply -f $<
	touch $@

.nats-dispatch: Dockerfile dispatch.py
	docker build . --target dispatch -t $(DOCKER_REPO)/nats-dispatch:latest
	docker push $(DOCKER_REPO)/nats-dispatch:latest
	touch $@
.nats-consume: Dockerfile consume.py
	docker build . --target consume -t $(DOCKER_REPO)/nats-consume:latest
	docker push $(DOCKER_REPO)/nats-consume:latest
	touch $@
.nats-wait: Dockerfile wait.py
	docker build . --target wait -t $(DOCKER_REPO)/nats-wait:latest
	docker push $(DOCKER_REPO)/nats-wait:latest
	touch $@
.nats-create: Dockerfile create.py
	docker build . --target create -t $(DOCKER_REPO)/nats-create:latest
	docker push $(DOCKER_REPO)/nats-create:latest
	touch $@
