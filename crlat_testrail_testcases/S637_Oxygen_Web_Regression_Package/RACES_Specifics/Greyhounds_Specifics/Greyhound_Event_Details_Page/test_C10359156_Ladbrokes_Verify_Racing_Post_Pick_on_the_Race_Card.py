import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C10359156_Ladbrokes_Verify_Racing_Post_Pick_on_the_Race_Card(Common):
    """
    TR_ID: C10359156
    NAME: [Ladbrokes] Verify Racing Post Pick on the Race Card
    DESCRIPTION: This test case verifies displaying of Racing Post Pick information on Greyhound event Race Card
    DESCRIPTION: AUTOTEST_ID Mobile: [C21831398]
    DESCRIPTION: AUTOTEST_ID Desktop: [C22221365]
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
    PRECONDITIONS: - Racing Post Pick information is present in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/[eventID] in 'postPick' attribute, (e.g. "postPick": "3-6-4")
    """
    keep_browser_open = True

    def test_001_verify_racing_post_pick_information(self):
        """
        DESCRIPTION: Verify Racing Post Pick information
        EXPECTED: - 'RACING POST PICK' logo is displayed in Race Card meeting details section
        EXPECTED: - Greyhound racing numbers sequence is displayed to the right of 'RACING POST PICK' logo (e.g. "3" "6" "4")
        EXPECTED: - Racing numbers design and colors are the same as Runner Number
        """
        pass
