import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C15755566_Verify_message_presence_for_price_change_case_of_Race_event_selection(Common):
    """
    TR_ID: C15755566
    NAME: Verify message presence for price change case of Race event selection
    DESCRIPTION: This test case verifies presence of a warning message about price change within QuickBet while interaction with fields shown before bet placement
    PRECONDITIONS: To get SiteServer info about event use the following URL: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Race> Event should be LiveServed:
    PRECONDITIONS: Event should not be 'Live' ('isStarted' - absent)
    PRECONDITIONS: Event, Market, Outcome should be Active
    PRECONDITIONS: Price format should be Fractional
    PRECONDITIONS: Link to backoffice tool for price changing: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Price updates are received in Quick Bet microservice:
    PRECONDITIONS: Development tool> Network> WS> remotebetslip/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports ribbon
        EXPECTED: <Race> Landing page is opened
        """
        pass

    def test_003_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: Events for current day are displayed
        """
        pass

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_make_single_selection_where_price_has_both_lp_and_sp_values(self):
        """
        DESCRIPTION: Make single selection where price has both LP and SP values
        EXPECTED: * Quick Bet is opened with selection added
        EXPECTED: * LP Price is shown in drop down
        """
        pass

    def test_006_increasedecrease_price_for_the_selection_in_backoffice_tool(self):
        """
        DESCRIPTION: Increase/Decrease price for the selection in Backoffice tool
        EXPECTED: 
        """
        pass

    def test_007_check_price_displaying_in_quick_bet(self):
        """
        DESCRIPTION: Check price displaying in Quick Bet
        EXPECTED: Old Odds(Price) are instantly changed to New Odds(Price)
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        """
        pass

    def test_008_click_into_dropdown(self):
        """
        DESCRIPTION: Click into dropdown
        EXPECTED: * Both updated Odds value and 'SP' value are shown as selectable options
        EXPECTED: * Warning message remains shown below 'QUICK BET' header
        """
        pass

    def test_009_repeat_steps_2_8_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-8 for Logged In User
        EXPECTED: 
        """
        pass
