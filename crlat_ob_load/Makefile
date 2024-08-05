SHELL=/bin/bash -ex

NUM_OF_EVENTS?=0
IS_ALL_MARKET?=True
NUM_OF_PARALLEL_PROCESS?=1
PERFORM_STREAM?=False
IMG_STREAM?=False
ENV?=tst2
BRAND?=bma
FILE_WITH_EVENTS_IDS?=file_with_events_ids.json
IS_LIVE?=True
IS_UPCOMING?=False
ADD_EXTENDED_MARKETS?=False
EVENT_PREFIX?=MQA

add_events:
	    mkdir target || true; \
		python create_events.py \
			${NUM_OF_EVENTS} \
	 	 	${IS_ALL_MARKET} \
	   	 	${NUM_OF_PARALLEL_PROCESS} \
	     	${PERFORM_STREAM} \
	     	${IMG_STREAM} \
	      	"${ENV}" \
	      	"${BRAND}" \
	      	"${IS_LIVE}" \
	      	"${IS_UPCOMING}" \
	      	"${ADD_EXTENDED_MARKETS}" \
	      	"${EVENT_PREFIX}";

delete_events:
	python delete_events.py "${ENV}" "${BRAND}" "target/${FILE_WITH_EVENTS_IDS}"
