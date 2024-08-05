/**
 * Deploy to CloudFlare through AWS S3 bucket
 */

def purgeCache(Map arguments) {

    def cloudFlareZone     = arguments.cloudFlareZone
    def cloudFlareUrl      = arguments.cloudFlareUrl

    sh """

#!/bin/bash
set -ex

GR='\\033[0;32m'
NC='\\033[0m'

_post_data()
{
  cat <<EOF
    {
      "hosts":["${cloudFlareUrl}"]
    }
EOF
}

ZONE_ID=\$(curl -s -S -X GET "https://api.cloudflare.com/client/v4/zones?name=${cloudFlareZone}" \\
               -H "Content-Type: application/json" \\
               -H "Authorization: Bearer \${API_TOKEN}" | jq -r '.result[].id')

PURGE_CACHE=\$(curl -s -S -X POST "https://api.cloudflare.com/client/v4/zones/\${ZONE_ID}/purge_cache" \\
               -H "Authorization: Bearer \${API_TOKEN}" \\
               -H "Content-Type: application/json" \\
               --data "\$(_post_data)")

if [ \$(echo \${PURGE_CACHE} | jq -r .success) != true ]; then 
    echo \${PURGE_CACHE}
    exit 1;
else 
    echo "\${GR}Purge cache - OK!\${NC}"             
    exit 0;
fi  
    """
}
