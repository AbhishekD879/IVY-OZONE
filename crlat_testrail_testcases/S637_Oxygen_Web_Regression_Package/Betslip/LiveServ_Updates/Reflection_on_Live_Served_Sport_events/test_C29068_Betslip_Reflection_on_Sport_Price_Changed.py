import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C29068_Betslip_Reflection_on_Sport_Price_Changed(Common):
    """
    TR_ID: C29068
    NAME: Betslip Reflection on <Sport> Price Changed
    DESCRIPTION: This test case verifies Betslip reflection on Football Price Changed.
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    DESCRIPTION: **JIRA tickets:**
    DESCRIPTION: BMA-20464: New betslip - Price change functionality 1 - Cards and remove old message
    DESCRIPTION: BMA-20610: New betslip - Price change functionality 2 - new notification and CTA
    DESCRIPTION: AUTOTEST [C9698104]
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
    PRECONDITIONS: 3. Event, Market, Outcome should be:
    PRECONDITIONS: **Active** ( **eventStatusCode="A",** **marketStatusCode="A",** **outcomeStatusCode="A"** )
    PRECONDITIONS: 4. Odds format is Fractional
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
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
        DESCRIPTION: Go to the **In-Play** tab
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
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_006_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selection is displayed
        """
        pass

    def test_007_trigger_the_following_situation_for_this_eventchange_pricenum_and_pricedenand_at_the_same_time_have_the_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have the Betslip page opened to watch for updates
        EXPECTED: Price Odds is changed on
        EXPECTED: * Betslip page
        EXPECTED: * Developer tool -> Application tab -> Local Storage section -> 'OX.betSelections' -> price (priceDen and priceNum values)
        """
        pass

    def test_008_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: **[Not actual from OX 99]** * *NO* Error message: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: * Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds:
        EXPECTED: a. in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: b. in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: * 'Log In & Bet' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * Only Ladbrokes: info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: 'Log In & Place Bet'(Coral) / 'Log In and Place Bet'(Ladbrokes) button is disabled
        """
        pass

    def test_009_close_and_open_betslip_again__mobile(self):
        """
        DESCRIPTION: Close and open Betslip again  (**MOBILE**)
        EXPECTED: Updated Odds are still displaying
        """
        pass

    def test_010_enter_stake_in_stake_field_and_trigger_price_change(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and trigger price change
        EXPECTED: **Before OX99**
        EXPECTED: * Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds:
        EXPECTED: a. in Red color with Red colored Down direct arrows if Odds decreased
        EXPECTED: b. in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * Est. Returns and Total Est. Returns should be recalculated
        EXPECTED: * General Error Message on Yellow background disappears
        EXPECTED: * 'Log In & Bet' button becomes enabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed' (Ladbrokes only)
        EXPECTED: * 'Log In & Place Bet'(Coral) / 'Log In and Place Bet'(Ladbrokes) button is disabled (should be enabled I think?)
        """
        pass

    def test_011_add_few_selections_to_betslipstakes_are_not_added_to_any_selectionrepeat_steps_2_5(self):
        """
        DESCRIPTION: Add few selections to Betslip(Stakes are not added to any selection)
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: **[Not actual from OX 99]** * *NO* Error message: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: * Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: a. in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: b. in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that X of your selections had a price change", where X is the number of selections with price changes
        EXPECTED: * After entering Stake for selection with price change X counter in error message is decreased by 1.
        EXPECTED: When User enters Stakes for all selections with price changes, error message disappers.
        EXPECTED: * 'Log In & Bet' button is disabled
        EXPECTED: * 'Multiples' section is shown in the bet slip and Price changes don't affect Multiples
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * Only Ladbrokes: info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: *'Log In & Place Bet'(Coral) / 'Log In and Place Bet'(Ladbrokes) button is disabled
        EXPECTED: * 'Multiples' section is shown in the bet slip and Price changes don't affect Multiples (ACCA bet, which is multiple, should be affected I think)
        """
        pass

    def test_012_log_in_to_the_app_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Log in to the app, go to Settings and switch Odds format to Decimal
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_1_6(self):
        """
        DESCRIPTION: Repeat steps #1-6
        EXPECTED: All prices on error messages are displayed in Decimal format
        """
        pass

    def test_014_login_with_user_account_with_positive_balancerepeat_steps_2_13_for_logged_in_user(self):
        """
        DESCRIPTION: Login with user account with positive balance
        DESCRIPTION: Repeat steps 2-13 for Logged In User
        EXPECTED: **[Not actual from OX 99]** *
        EXPECTED: *NO* Error message: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: * Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds:
        EXPECTED: a. in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: b. in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that X of your selections had a price change", where X is the number of selections with price changes
        EXPECTED: * a. 'Accept & Bet (X)' button is disabled when no stakes are entered
        EXPECTED: b. 'Accept & Bet (X)' button is enabled when at least 1 stake is entered
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed' (Ladbrokes only)
        EXPECTED: Button is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass
