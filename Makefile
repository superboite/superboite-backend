.PHONY: run

run:
	poetry run uvicorn superboite_api.main:app --reload

run-docker: 
	docker run -e GOOGLE_APPLICATION_CREDENTIALS=/service-accout.json \
					-v /home/mdelobelle/.gcp/service-accout.json:/service-accout.json \
					-p 8080:8080 superboite-api:latest

# export PROJECT_ID=superboite
# export IMAGE_NAME=superboite-api
# export TAG=0.0.1
# export REGION=europe-west1
# export REPOSITORY_NAME=superboite-api-repo


docker-build : 
	docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG} .

push-to-repo: 
	docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG}

push-to-cloud-run:
	gcloud run deploy superboite-api-service \
		--image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG} \
		--platform managed \
		--region ${REGION} \
		--allow-unauthenticated \
		--memory "256Mi" \
		--cpu "1" \
		--max-instances=1

deploy-new-version : 
	make docker-build
	make push-to-repo
	make push-to-cloud-run
