#!/bin/bash
INST=${1:-"test"}
REV=${2:-"latest"}

case "${INST}" in
	test)
	SITESERVER_URL='https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.14'
	;;
	stage)
	SITESERVER_URL='https://ss.coral.co.uk/openbet-ssviewer/Drilldown/2.14'
	;;
	prod)
	SITESERVER_URL='https://ss.coral.co.uk/openbet-ssviewer/Drilldown/2.14'
	;;
	*)
	echo 'No suitable deployment instance given (test|stage|prod)'
	;;
esac

SCRIPT=$(cat <<- 'FILE'
        IMAGES=$(docker images -q registry-coral.symphony-solutions.eu/bma-cms)
        echo $IMAGES
        docker pull registry-coral.symphony-solutions.eu/bma-cms:__REV__ &&
	NEWIMAGE=$(docker images -q registry-coral.symphony-solutions.eu/tennis-scb-be:__REV__)
        docker stop keystone 
        docker rm -v keystone 
        docker run -d -p 80:3000 --restart=on-failure -v /home/core/share/uploads:/home/bma/dist/public/images/uploads --link mongodb:mongodb -e MONGODB="mongodb://mongodb/bma" -e CLOUDINARY_URL="cloudinary://333779167276662:_8jbSi9FB3sWYrfimcl8VKh34rI@keystone-demo" -e SITESERVER_URL="__SITESERVER_URL__/" -e ALLOWED_CORS_ORIGINS="*" --name keystone registry-coral.symphony-solutions.eu/bma-cms:__REV__
        echo ${IMAGES} | while read -r line
        do
                [ "${line}" != "${NEWIMAGE}" ] && docker rmi $line
        done
FILE
)

FINAL_SCRIPT=$(echo "$SCRIPT" | sed "s/__REV__/${REV}/g" | sed "s?__SITESERVER_URL__?${SITESERVER_URL}?g")
