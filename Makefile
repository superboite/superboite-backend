.PHONY: run

clean : 
	docker system prune -a --volumes

local:
	poetry run uvicorn superboite_api.main:app --reload

# run-docker:
# 	docker run -p 8080:8080 superboite-api:latest

build : 
	docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG} .

repo: 
	docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG}

run:
	gcloud run deploy ${IMAGE_NAME} \
		--image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG} \
		--service-account google-drive-api@superboite.iam.gserviceaccount.com \
		--platform managed \
		--region ${REGION} \
		--allow-unauthenticated \
		--memory "256Mi" \
		--cpu "1" \
		--max-instances=1

deploy : 
	make build
	make repo
	make run
