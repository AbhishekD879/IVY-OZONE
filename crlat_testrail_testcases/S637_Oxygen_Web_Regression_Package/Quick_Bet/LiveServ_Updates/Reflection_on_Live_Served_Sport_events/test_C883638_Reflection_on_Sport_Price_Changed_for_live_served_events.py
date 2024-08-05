import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C883638_Reflection_on_Sport_Price_Changed_for_live_served_events(Common):
    """
    TR_ID: C883638
    NAME: Reflection on <Sport> Price Changed for live served events
    DESCRIPTION: This test case verifies Quick Bet reflection on Sports Price Changed.
    PRECONDITIONS: 1. To get SiteServer info about event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: * XXXXXXX - event id
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Sport> Event should be LiveServed:
    PRECONDITIONS: * Event should be LIVE ( **isStarted=true** )
    PRECONDITIONS: * Event should be IN-PLAY:
    PRECONDITIONS: * **drilldown** **TagNames=EVFLAG_BL**
    PRECONDITIONS: * **isMarketBetInRun=true**
    PRECONDITIONS: * **rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"**
    PRECONDITIONS: Event, Market, Outcome should be:  **Active** ( **eventStatusCode="A",** **marketStatusCode="A",** **outcomeStatusCode="A"** )
    PRECONDITIONS: 3. Price format should be Fractional
    PRECONDITIONS: 4. Link to backoffice tool for price changing: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 5.  Price updates are received in Quick Bet microservice:
    PRECONDITIONS: Development tool> Network> WS> quickbet/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_go_to_thein_play_tab(self):
        """
        DESCRIPTION: Go to the 'In-Play' tab
        EXPECTED: 'In-Play' page with list of events is opened
        """
        pass

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_make_single_selections(self):
        """
        DESCRIPTION: Make single selections
        EXPECTED: Quick Bet is opened with selection added
        """
        pass

    def test_006_change_price_for_the_selection_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection in Backoffice tool
        EXPECTED: 
        """
        pass

    def test_007_check_that_price_is_updated_in_quick_bet(self):
        """
        DESCRIPTION: Check that price is updated in Quick Bet
        EXPECTED: Old Odds are instantly changed to New Odds
        """
        pass

    def test_008_verify_warning_message_and__login__place_bet_button_displaying(self):
        """
        DESCRIPTION: Verify warning message and  'LOGIN & PLACE BET' button displaying
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: * 'LOGIN & PLACE BET' button is disabled
        """
        pass

    def test_009_enter_stake_in_stake_field_and_trigger_price_change(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and trigger price change
        EXPECTED: 1. Old Odds are instantly changed to New Odds
        EXPECTED: 2. Warning Message should remain during the input of at least 1 number into the stake field and refresh(update) its values after the price change trigger
        EXPECTED: 3. Est. Returns and Total Est. Returns should be recalculated
        EXPECTED: 4. 'LOGIN & PLACE BET' button becomes enabled
        """
        pass

    def test_010_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps #2-9
        EXPECTED: All prices are displayed in Decimal format
        """
        pass

    def test_012_login_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: User is logged in
        """
        pass

    def test_013_repeat_steps_2_11_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-11 for Logged In User
        EXPECTED: Results are the same, only 'PLACE BET' button is instead of 'LOGIN & PLACE BET'
        EXPECTED: -
        EXPECTED: During the price change operation, 'PLACE BET' button changes to 'ACCEPT & PLACE BET'
        """
        pass
