import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732153_To_editVerify_messages_logging_by_customer_name(Common):
    """
    TR_ID: C57732153
    NAME: [To-edit]Verify messages logging by customer name
    DESCRIPTION: [To-edit] - The links need to be updated
    DESCRIPTION: This test case verifies error message logging
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. Some exception/errors already happens related to a customer request is logged (e.g. saving/getting predictions, calculated upsell, saving to big query, any error, etc.)
    PRECONDITIONS: 2. Kibana access provided (Copy string to URL browser field)
    PRECONDITIONS: DEVO:
    PRECONDITIONS: `https://search-ladbrokescoral-logs-dev-qwxuyxesgs3eucjfy33g534srq.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'2019-06-12T21:00:00.000Z',mode:absolute,to:'2019-06-18T10:05:15.291Z'))&_a=(columns:!(_source),index:'otf-api-*',interval:auto,query:(match_all:()),sort:!('@timestamp',desc))`
    PRECONDITIONS: HLV0:
    PRECONDITIONS: 'https://search-ladbrokes-logs-hlv0-r4klh7rr53kpppyvnxbxambn4u.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=()&_a=(columns:!(_source),index:%276fd9d810-37b4-11ea-ae0d-091a508a2709%27,interval:auto,query:(language:lucene,query:%27%27),sort:!(%27@timestamp%27,desc))'
    """
    keep_browser_open = True

    def test_001_open_kibanacopy_string_to_url_browser_fieldhttpssearch_ladbrokescoral_logs_dev_qwxuyxesgs3eucjfy33g534srqeu_west_2esamazonawscom_pluginkibanaappkibanadiscover_grefreshintervaldisplayoffpausefvalue0timefrom2019_06_12t210000000zmodeabsoluteto2019_06_18t100515291z_acolumns_sourceindexotf_api_intervalautoquerymatch_allsorttimestampdesc(self):
        """
        DESCRIPTION: Open Kibana(Copy string to URL browser field)
        DESCRIPTION: `https://search-ladbrokescoral-logs-dev-qwxuyxesgs3eucjfy33g534srq.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'2019-06-12T21:00:00.000Z',mode:absolute,to:'2019-06-18T10:05:15.291Z'))&_a=(columns:!(_source),index:'otf-api-*',interval:auto,query:(match_all:()),sort:!('@timestamp',desc))`
        EXPECTED: Kibana is successfully opened
        """
        pass

    def test_002_type_in_search_field_upsell_prediction_customer_id(self):
        """
        DESCRIPTION: Type in Search field 'Upsell', 'Prediction', 'Customer ID'
        EXPECTED: Errors related to Question Engine displayed
        EXPECTED: (e.g. saving/getting predictions, calculated upsell, saving to big query, any error, etc.),
        """
        pass
