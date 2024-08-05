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
class Test_C10375626_Verify_Race_Card_displaying_without_Racing_Post_Pick(Common):
    """
    TR_ID: C10375626
    NAME: Verify Race Card displaying without Racing Post Pick
    DESCRIPTION: This test case verifies displaying Greyhound event Race Card without Racing Post Pick information
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
    PRECONDITIONS: - There is an event with Racing Post information
    PRECONDITIONS: - Racing Post Pick information is NOT available (blocked) in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/[eventID] in 'postPick' attribute, (e.g. "postPick": "3-6-4")
    PRECONDITIONS: - Ladbrokes OB (TI) Environments https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments#LadbrokesEnvironments-LadbrokesOB/IMSendpoints
    """
    keep_browser_open = True

    def test_001_verify_race_card_with_no_racing_post_pick_informationdev_tools__network__block_request_url_httpsraceinfo_apiladbrokescomrace_infoladbrokesdogevent_id(self):
        """
        DESCRIPTION: Verify Race Card with NO Racing Post Pick information
        DESCRIPTION: (Dev Tools > Network > Block Request URL https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/{event id})
        EXPECTED: 'RACING POST PICK' information is not displayed
        """
        pass

    def test_002_open_ti__locate_needed_event__market__selections__set_to_not_displayed_and_save(self):
        """
        DESCRIPTION: Open TI > Locate needed event > Market > Selection(s) > Set to 'Not Displayed' and Save
        EXPECTED: Changes successfully saved
        """
        pass

    def test_003_verify_race_card_when_racing_post_pick_is_present_but_oneall_of_the_racing_post_pick_selections_are_not_present_in_the_event(self):
        """
        DESCRIPTION: Verify Race Card when Racing Post Pick IS present but ONE/ALL of the Racing Post Pick Selections are NOT present in the Event
        EXPECTED: - 'RACING POST PICK' information is properly displayed
        EXPECTED: - Disabled selection(s) are NOT displayed
        """
        pass
