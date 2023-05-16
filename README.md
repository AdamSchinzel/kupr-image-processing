# KUPR Image Processing

An API to analyze the similarity of shapes in images.

## Usage

Deployed to ```https://kupr-processing.esl.staging.decentree.com```

### POST `/analyze`

Body (multipart/form-data):

- `file`: the uploaded image to be analyzed
- `ref`: the name of the image to compare with, from the `images/` folder

Result (JSON):

```
{ "match": true/false }
```
# kupr-image-processing
