import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C60618870_Verify_Service_for_Getting_Results_Table_of_Seasons(Common):
    """
    TR_ID: C60618870
    NAME: Verify Service for Getting Results Table of Seasons
    DESCRIPTION: This test case verifies displaying of results tables for seasons
    DESCRIPTION: **Jira ticket:** SFD-528
    PRECONDITIONS: Note, this test case verifies functionality when XMLs are sent manually
    PRECONDITIONS: Currently there are 3 {domains}:
    PRECONDITIONS: *   Current tst environment (domain) - https://spark-br-tst.symphony-solutions.eu
    PRECONDITIONS: *   Current stage environment (domain) - https://spark-br-stg2.symphony-solutions.eu
    PRECONDITIONS: *   Current prod environment (domain) - https://spark-br.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_postman_rest_client(self):
        """
        DESCRIPTION: Load Postman Rest client
        EXPECTED: Postman Rest client is loaded
        """
        pass

    def test_002_set_the_following_values_in_postman_parameters___request_method__post___endpoint_domain8443messages___select_raw_tab_in_body_section(self):
        """
        DESCRIPTION: Set the following values in Postman parameters:
        DESCRIPTION: *   request method = POST
        DESCRIPTION: *   endpoint ={domain}:8443/messages
        DESCRIPTION: *   Select 'raw' tab in 'Body' section
        EXPECTED: Parameters are set
        """
        pass

    def test_003_send_via_postman_the_xml_where_servicename__resulstablenote_put_5_digits_before_the_xml_text_and_only_after_that_tap_send_button(self):
        """
        DESCRIPTION: Send via Postman the XML where servicename = 'resulstable'
        DESCRIPTION: NOTE, put 5 digits before the XML text and only after that tap 'Send' button
        EXPECTED: XML is sent
        EXPECTED: Success message is shown
        """
        pass

    def test_004_open_web_browser_and_tap_the_following_endpoint_for_checking_servicedomainapiresultstablessportidareaidcompetitionidseasonid___param_sportid___id_of_sport___param_areaid___id_of_area___param_competitionid___id_of_competition___param_seasonid___id_of_seasonall_params_are_taken_from_the_xml(self):
        """
        DESCRIPTION: Open web browser and tap the following endpoint for checking service:
        DESCRIPTION: {domain}/api/resultstables/:sportId/:areaId/:competitionId/:seasonId
        DESCRIPTION: *   param :**sportId** - id of sport
        DESCRIPTION: *   param :**areaId** - id of area
        DESCRIPTION: *   param :**competitionId** - id of competition
        DESCRIPTION: *   param :**seasonId** - id of season
        DESCRIPTION: all params are taken from the XML
        EXPECTED: Results table of indicated season is displayed
        """
        pass

    def test_005_check_the_dispalyed_data_with_the_data_from_the_xml_file(self):
        """
        DESCRIPTION: Check the dispalyed data with the data from the XML file
        EXPECTED: All data is displayed fully and correctly
        """
        pass
