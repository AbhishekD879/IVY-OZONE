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
class Test_C60618871_Verify_Service_for_Getting_Form_Tables_of_Season(Common):
    """
    TR_ID: C60618871
    NAME: Verify Service for Getting Form Tables of Season
    DESCRIPTION: This test case verifies displaying of form tables for particular season
    DESCRIPTION: **Jira ticket:** SFD-528
    PRECONDITIONS: Note, this test case verifies functionality when XMLs are sent manually
    PRECONDITIONS: The example of XMl with prematch service is attached to the test case
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

    def test_002_set_the_following_characteristics_in_postman_parameters___request_method__post___endpoint_domain8443messages___select_raw_tab_in_body_section(self):
        """
        DESCRIPTION: Set the following characteristics in Postman parameters:
        DESCRIPTION: *   request method = POST
        DESCRIPTION: *   endpoint ={domain}:8443/messages
        DESCRIPTION: *   Select 'raw' tab in 'Body' section
        EXPECTED: Parameters are set
        """
        pass

    def test_003_send_via_postman_the_xml_where_servicename__formtablesnote_put_5_digits_before_the_xml_text_and_only_after_that_tap_send_button(self):
        """
        DESCRIPTION: Send via Postman the XML where servicename = 'formtables'
        DESCRIPTION: NOTE, put 5 digits before the XML text and only after that tap 'Send' button
        EXPECTED: XML is sent
        EXPECTED: Success message is shown
        """
        pass

    def test_004_open_web_browser_and_tap_the_following_endpoint_for_checking_the_servicedomainapiformtablessportidareaidcompetitionidseasonid___param_sportid___id_of_sport___param_areaid___id_of_area___param_competitionid___id_of_competition___param_seasonid___id_of_seasonall_params_are_taken_from_the_xml_file(self):
        """
        DESCRIPTION: Open web browser and tap the following endpoint for checking the service:
        DESCRIPTION: {domain}/api/formtables/:sportId/:areaId/:competitionId/:seasonId
        DESCRIPTION: *   param :**sportId** - id of sport
        DESCRIPTION: *   param :**areaId** - id of area
        DESCRIPTION: *   param :**competitionId** - id of competition
        DESCRIPTION: *   param :**seasonId** - id of season
        DESCRIPTION: All params are taken from the XML file
        EXPECTED: Form tables for season is displayed correctly
        """
        pass

    def test_005_check_the_data_displayed_with_the_data_from_the_xml(self):
        """
        DESCRIPTION: Check the data displayed with the data from the XML
        EXPECTED: Whole data is displayed fully and correctly
        """
        pass
