.PHONY: run

run:
	poetry run uvicorn superboite_api.main:app --reload

run-docker:
	docker run -p 8080:8080 superboite-api:latest

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
