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
class Test_C10644025_In_play_Module_tracking_of_adding_selection_to_Quick_Bet_from_Featured_In_play_module(Common):
    """
    TR_ID: C10644025
    NAME: In-play Module: tracking of adding selection to Quick Bet from Featured In-play module
    DESCRIPTION: This test case verifies GA tracking of adding selection from Featured In-Play module on home page to Quick bet
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Quick Bet GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should have a Featured In-Play module with events on home page
    PRECONDITIONS: - You should be on Home page > Featured tab in application
    """
    keep_browser_open = True

    def test_001___tap_odds_button_in_featured_in_play_module__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Tap ODDS button in Featured in-Play module
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to quickbet"
        EXPECTED: eventCategory: "quickbet"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "in-play module"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        pass