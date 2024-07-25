# AI assistant for SVUIT-MMTT
## Pull docker image 
To be written later.
Use these commands with the Docker client to pull the image. To use these commands, your Docker client must be configured to authenticate with asia-southeast1-docker.pkg.dev. If this is the first time that you are pulling an image from asia-southeast1-docker.pkg.dev with your Docker client, run the following command on the machine where Docker is installed.

$
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
Pull by tag
$
docker pull \
    asia-southeast1-docker.pkg.dev/avid-factor-428706-b2/docker-images-storage/svuit:v01
or
Pull by digest
$
docker pull \
    asia-southeast1-docker.pkg.dev/avid-factor-428706-b2/docker-images-storage/svuit@sha256:9fa7aef702b7fd03b1a6bd37cf51cecb11cfd5ec367365cc4b3300a4bd63b30e  
    
## RUN docker images
docker run -p 8080:4000 svuit
