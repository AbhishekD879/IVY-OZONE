import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10350055_Verify_Race_Card_displaying_without_Form_information(Common):
    """
    TR_ID: C10350055
    NAME: Verify Race Card displaying without 'Form' information
    DESCRIPTION: This test case verifies race card displaying without Form and Comment (Show More/Less link) information
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User is at Greyhound Race Card (Event Details page)
    PRECONDITIONS: - 'Form' AND/OR 'Comment' information for Selection(s) is NOT present in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/[eventID]
    """
    keep_browser_open = True

    def test_001_verify_selections_displaying_in_case_there_is_no_form_information_and_no_commentdev_tools__network__block_request_url_httpsraceinfo_apiladbrokescomrace_infoladbrokesdogevent_id(self):
        """
        DESCRIPTION: Verify selection(s) displaying in case there is NO 'Form' information and NO 'Comment'
        DESCRIPTION: (Dev Tools > Network > Block Request URL https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/{event id})
        EXPECTED: Only dog number and dog name along with bet odds button are displayed.
        EXPECTED: There are no 'Form' information nor 'SHOW MORE' link for selection(s)
        """
        pass

    def test_002_verify_selections_card_displaying_in_case_there_is_form_information_but_no_comment(self):
        """
        DESCRIPTION: Verify selection(s) Card displaying in case there IS 'Form' information but NO 'Comment'
        EXPECTED: - Form information is displayed for each dog under Dog's name, text "Form:" and 'value' in bold (e.g. "Form: 12345")
        EXPECTED: - 'SHOW MORE' link is NOT displayed
        """
        pass

    def test_003_verify_selections_card_displaying_in_case_there_is_comment_but_no_form_information(self):
        """
        DESCRIPTION: Verify selection(s) Card displaying in case there is 'Comment' but NO 'Form' information
        EXPECTED: - Form information is NOT displayed
        EXPECTED: - 'SHOW MORE' link is present, user is able to expand/collapse it and read comment
        """
        pass
