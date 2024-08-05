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
class Test_C883644_Quick_Bet_Reflection_on_Race_Price_Changed_for_live_served_events(Common):
    """
    TR_ID: C883644
    NAME: Quick Bet Reflection on <Race> Price Changed for live served events
    DESCRIPTION: This test case verifies Quick Bet reflection on Race Price Changed.
    DESCRIPTION: AUTOTEST [C2009625]
    PRECONDITIONS: 1. To get SiteServer info about event use the following URL: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: Event should not be 'Live' ('isStarted' - absent)
    PRECONDITIONS: Event, Market, Outcome should be Active
    PRECONDITIONS: 4. Price format should be Fractional
    PRECONDITIONS: 5. Link to backoffice tool for price changing: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 6. Price updates are received in Quick Bet microservice:
    PRECONDITIONS: Development tool> Network> WS> remotebetslip/?EIO=3&transport=websocket
    PRECONDITIONS: NOTE: test case may be run for selections with LP price
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

    def test_003_go_to_thetoday_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: Events for current day are displayed
        """
        pass

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_make_single_selections_where_price_is_lp(self):
        """
        DESCRIPTION: Make single selections where price is LP
        EXPECTED: * Quick Bet is opened with selection added
        EXPECTED: * Price is shown in drop down.
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
        EXPECTED: Old Odds are instantly changed to New Odds
        EXPECTED: *
        EXPECTED: When clicked into, dropdown shows both updated Odds value and 'SP' value as selectable options
        EXPECTED: NOTE: Price corresponds to value received in 'remotebetslip/?EIO=3&transport=websocket' response
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
        EXPECTED: When clicked into, dropdown shows both updated Odds value and 'SP' value as selectable options
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: 3. Estimated Returns(for Coral) and Potential Returns(for ladbrokes) should be recalculated
        EXPECTED: 4.'LOGIN & PLACE BET' button becomes enabled
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
        EXPECTED: Results are the same, only 'PLACE BET'(ACCEPT & PLACE BET) button instead of 'LOGIN & PLACE BET' is displayed
        """
        pass
