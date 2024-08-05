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
class Test_C60618882_Verify_Service_for_Getting_Team_Logo_and_Player_Photo(Common):
    """
    TR_ID: C60618882
    NAME: Verify Service for Getting Team Logo and Player Photo
    DESCRIPTION: This test case verifies displaying of team logo and player photo information
    DESCRIPTION: **Jira ticket:** SFD-528
    PRECONDITIONS: Note, this test case verifies functionality when XMLs are sent manually
    PRECONDITIONS: The example of XMl with needed service is attached to the test case
    PRECONDITIONS: Currently there are 3 {domains}:
    PRECONDITIONS: *   Current tst environment (domain) - https://spark-br-tst.symphony-solutions.eu
    PRECONDITIONS: *   Current stage environment (domain) - https://spark-br-stg2.symphony-solutions.eu
    PRECONDITIONS: *   Current prod environment (domain) - https://spark-br.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_postman_rest_client(self):
        """
        DESCRIPTION: Load Postman Rest client
        EXPECTED: Postman Rest Client is loaded
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

    def test_003_send_via_postman_the_xml_where_servicename__teaminfonote_put_5_digits_before_the_xml_text_and_only_after_that_tap_send_button(self):
        """
        DESCRIPTION: Send via Postman the XML where serviceName = 'teaminfo'
        DESCRIPTION: NOTE, put 5 digits before the XML text and only after that tap 'Send' button
        EXPECTED: XML is sent
        EXPECTED: Success message is shown
        """
        pass

    def test_004_open_web_browser_and_tap_the_following_endpoint_for_checking_the_servicedomainapiteamteamidlogo___param_teamid___id_of_team(self):
        """
        DESCRIPTION: Open web browser and tap the following endpoint for checking the service:
        DESCRIPTION: {domain}/api/team/:teamId/logo
        DESCRIPTION: *   param :**teamId** - id of team
        EXPECTED: The endpoint returns the team logo
        """
        pass

    def test_005_send_via_postman_the_xml_where_servicename__playerstatisticnote_put_5_digits_before_the_xml_text_and_only_after_that_tap_send_button(self):
        """
        DESCRIPTION: Send via Postman the XML where serviceName = 'playerstatistic'
        DESCRIPTION: NOTE, put 5 digits before the XML text and only after that tap 'Send' button
        EXPECTED: XML is sent
        EXPECTED: Success message is shown
        """
        pass

    def test_006_open_web_browser_and_tap_the_following_endpoint_for_checking_the_servicedomainapiplayertonguelayeridlogo___param_playerid___id_of_player(self):
        """
        DESCRIPTION: Open web browser and tap the following endpoint for checking the service:
        DESCRIPTION: {domain}/api/player/(tongue)layerId/logo
        DESCRIPTION: *   param :**playerId** - id of player
        EXPECTED: The endpoint returns the player photo
        """
        pass
