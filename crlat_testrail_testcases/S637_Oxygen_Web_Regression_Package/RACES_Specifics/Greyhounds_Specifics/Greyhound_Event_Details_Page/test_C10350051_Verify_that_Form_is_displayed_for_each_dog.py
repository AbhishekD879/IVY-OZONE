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
class Test_C10350051_Verify_that_Form_is_displayed_for_each_dog(Common):
    """
    TR_ID: C10350051
    NAME: Verify that 'Form' is displayed for each dog
    DESCRIPTION: This test case verifies displaying of 'Form' information for each dog on race card
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE : [C24110186]
    DESCRIPTION: DESKTOP: [C24203597]
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
    PRECONDITIONS: - 'Form' information for each selection is present in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/[eventID]
    PRECONDITIONS: - Form value is taken from 'last5Runs' param (e.g. last5Runs: "23522")
    """
    keep_browser_open = True

    def test_001_verify_that_form_information_for_each_selection(self):
        """
        DESCRIPTION: Verify that 'Form' information for each selection
        EXPECTED: Form information is displayed for each selection under Dog's name:
        EXPECTED: text "Form:" and 'value' in bold (e.g. "Form: **12345**")
        """
        pass
