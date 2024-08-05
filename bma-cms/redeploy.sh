#!/bin/bash
INST=${1:-"test"}
JMPHST=${2:-"jumphost"}
REV=${3:-"latest"}
AKAMAI_CREDS=''

case "${INST}" in
	test)
	SITESERVER_URL='https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.19'
	AKAMAI_CREDS='-e AKAMAI_TIMEOUT="200000" -e AKAMAI_KEY_NAME="bm-mobile-tst2" -e AKAMAI_KEY="16581CF46f02W7P5D4IZ3LbEIgLLUs6j4B2dG5B3xh7YZz61AJ" -e AKAMAI_HOST="coraliassets-nsu.akamaihd.net" -e AKAMAI_PATH="/328873/CORAL/bet-tst2.coral.co.uk/cms/" -e AKAMAI_CRED_USER="coral.ci@symphony-solutions.eu" -e AKAMAI_CRED_PASS="Lb3TdmLHOxzQ" -e AKAMAI_URL="https://bet-tst2.coral.co.uk/cms/"'
	IMAGEMIN_CFG='-e IMAGEMIN_ENABLED="true" -e IMAGEMIN_JPEG_QUALITY="95" -e IMAGEMIN_PNG_OPTIMIZATION_LEVEL="3"'
	API_TOKEN='-e PRIVATE_API_REQUEST_TOKEN="6SjuagYEptBUUgZ" -e PRIVATE_API_REQUEST_LIFETIME=60'
	;;
	dev)
	SITESERVER_URL='https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.19'
	AKAMAI_CREDS='-e AKAMAI_TIMEOUT="200000" -e AKAMAI_KEY_NAME="bm-mobile-tst2" -e AKAMAI_KEY="16581CF46f02W7P5D4IZ3LbEIgLLUs6j4B2dG5B3xh7YZz61AJ" -e AKAMAI_HOST="coraliassets-nsu.akamaihd.net" -e AKAMAI_PATH="/328873/CORAL/bet-tst2.coral.co.uk/invictus/" -e AKAMAI_CRED_USER="coral.ci@symphony-solutions.eu" -e AKAMAI_CRED_PASS="Lb3TdmLHOxzQ" -e AKAMAI_URL="https://bet-tst2.coral.co.uk/invictus/"'
	IMAGEMIN_CFG='-e IMAGEMIN_ENABLED="true" -e IMAGEMIN_JPEG_QUALITY="95" -e IMAGEMIN_PNG_OPTIMIZATION_LEVEL="3"'
	API_TOKEN='-e PRIVATE_API_REQUEST_TOKEN="6SjuagYEptBUUgZ" -e PRIVATE_API_REQUEST_LIFETIME=60'
	;;
	dev-v2)
	SITESERVER_URL='https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.19'
	AKAMAI_CREDS='-e AKAMAI_TIMEOUT="200000" -e AKAMAI_KEY_NAME="bm-mobile-tst2" -e AKAMAI_KEY="16581CF46f02W7P5D4IZ3LbEIgLLUs6j4B2dG5B3xh7YZz61AJ" -e AKAMAI_HOST="coraliassets-nsu.akamaihd.net" -e AKAMAI_PATH="/328873/CORAL/bet-tst2.coral.co.uk/invictus/" -e AKAMAI_CRED_USER="coral.ci@symphony-solutions.eu" -e AKAMAI_CRED_PASS="Lb3TdmLHOxzQ" -e AKAMAI_URL="https://bet-tst2.coral.co.uk/invictus/"'
	IMAGEMIN_CFG='-e IMAGEMIN_ENABLED="true" -e IMAGEMIN_JPEG_QUALITY="95" -e IMAGEMIN_PNG_OPTIMIZATION_LEVEL="3"'
	API_TOKEN='-e PRIVATE_API_REQUEST_TOKEN="6SjuagYEptBUUgZ" -e PRIVATE_API_REQUEST_LIFETIME=60'
	;;
	stage)
	SITESERVER_URL='https://ss-stg2.coral.co.uk/openbet-ssviewer/Drilldown/2.19'
	AKAMAI_CREDS='-e AKAMAI_TIMEOUT="200000" -e AKAMAI_KEY_NAME="bm-mobile-stg2" -e AKAMAI_KEY="WTJqdlJwKx3SA47647GCx819gz3T4s2LhP5pgg41i92yv9gNCG" -e AKAMAI_HOST="coraliassets-nsu.akamaihd.net" -e AKAMAI_PATH="/328873/CORAL/bm-stg2.coral.co.uk/cms/" -e AKAMAI_CRED_USER="coral.ci@symphony-solutions.eu" -e AKAMAI_CRED_PASS="Lb3TdmLHOxzQ" -e AKAMAI_URL="https://bm-stg2.coral.co.uk/cms/"'
	IMAGEMIN_CFG='-e IMAGEMIN_ENABLED="true" -e IMAGEMIN_JPEG_QUALITY="95" -e IMAGEMIN_PNG_OPTIMIZATION_LEVEL="3"'
	API_TOKEN='-e PRIVATE_API_REQUEST_TOKEN="6SjuagYEptBUUgZ" -e PRIVATE_API_REQUEST_LIFETIME=60'
	;;
	prod)
	SITESERVER_URL='https://ss.coral.co.uk/openbet-ssviewer/Drilldown/2.19'
	;;
	*)
	echo 'No suitable deployment instance given (dev|dev-v2|test|stage|prod)'
	;;
esac


SCRIPT=$(cat <<- 'FILE'
        IMAGES=$(docker images -q registry-coral.symphony-solutions.eu/bma-cms)
        echo $IMAGES
        docker pull registry-coral.symphony-solutions.eu/bma-cms:__REV__ &&
	NEWIMAGE=$(docker images -q registry-coral.symphony-solutions.eu/tennis-scb-be:__REV__)
        docker stop keystone 
        sleep 5
        docker rm -vf keystone 
        docker run -d -p 80:3000 --restart=on-failure -v /home/core/share/uploads:/home/bma/dist/public/images/uploads --link mongodb:mongodb __AKAMAI_CREDS__  __IMAGEMIN_CFG__  __API_TOKEN__ -e MONGODB="mongodb://mongodb/bma" -e CLOUDINARY_URL="cloudinary://333779167276662:_8jbSi9FB3sWYrfimcl8VKh34rI@keystone-demo" -e SITESERVER_URL="__SITESERVER_URL__/" -e ALLOWED_CORS_ORIGINS="*" --name keystone registry-coral.symphony-solutions.eu/bma-cms:__REV__
        echo ${IMAGES} | while read -r line
        do
                [ "${line}" != "${NEWIMAGE}" ] && docker rmi $line
        done
FILE
)

FINAL_SCRIPT=$(echo "$SCRIPT" | sed "s/__REV__/${REV}/g" | sed "s?__SITESERVER_URL__?${SITESERVER_URL}?g" | sed "s?__AKAMAI_CREDS__?${AKAMAI_CREDS}?g" | sed "s?__IMAGEMIN_CFG__?${IMAGEMIN_CFG}?g"  | sed "s?__API_TOKEN__?${API_TOKEN}?g" )
#echo ${FINAL_SCRIPT}
ssh -A ${JMPHST} "ssh ${INST}" <<< "${FINAL_SCRIPT}"
