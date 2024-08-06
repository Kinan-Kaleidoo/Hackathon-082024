call the api with a url:
curl -X POST http://127.0.0.1:5000/ms/doc \
    -H "Content-Type: application/json" \
    -d '{"file_url": "gs://hackathon-082024/docs/cv.pdf"}'
