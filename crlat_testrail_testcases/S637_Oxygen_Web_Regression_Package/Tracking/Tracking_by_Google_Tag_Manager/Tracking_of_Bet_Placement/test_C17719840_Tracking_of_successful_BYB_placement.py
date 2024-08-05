import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C17719840_Tracking_of_successful_BYB_placement(Common):
    """
    TR_ID: C17719840
    NAME: Tracking of successful BYB placement
    DESCRIPTION: This test case verifies GA tracking of successful BYB placement
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: - User should be logged in
    PRECONDITIONS: - Navigate to Football Landing page
    PRECONDITIONS: - Go to the Event details page with the BYB (Leagues with available BYB are marked with BYB icon on accordion) > 'Build Your Bet' t
    """
    keep_browser_open = True

    def test_001_add_selections_from_markets_accordion_to_the_byb_dashboard(self):
        """
        DESCRIPTION: Add selections from Markets accordion to the BYB Dashboard
        EXPECTED: The selections are added to BYB Dashboard
        """
        pass

    def test_002___make_a_stake_and_tap_bet_now__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Make a stake and tap 'BET NOW'
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: betID: "<<BET ID>>"
        EXPECTED: betType: "Multiples"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "place bet"
        EXPECTED: eventCategory: "quickbet"
        EXPECTED: eventLabel: "success"
        EXPECTED: location: "yourcall"
        """
        pass
