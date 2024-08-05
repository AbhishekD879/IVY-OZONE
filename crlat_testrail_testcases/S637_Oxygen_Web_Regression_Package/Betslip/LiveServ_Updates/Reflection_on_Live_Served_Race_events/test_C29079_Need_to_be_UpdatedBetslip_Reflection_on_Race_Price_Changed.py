import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29079_Need_to_be_UpdatedBetslip_Reflection_on_Race_Price_Changed(Common):
    """
    TR_ID: C29079
    NAME: [Need to be Updated]Betslip Reflection on <Race>  Price Changed
    DESCRIPTION: This test case verifies Betslip reflection on HR Price Changed.
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    DESCRIPTION: **JIRA tickets:**
    DESCRIPTION: BMA-20464: New betslip - Price change functionality 1 - Cards and remove old message
    DESCRIPTION: BMA-20610: New betslip - Price change functionality 2 - new notification and CTA
    PRECONDITIONS: 1. To get SiteServer info about event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: *   Event should not be **Live** (**isStarted - absent)**
    PRECONDITIONS: 3. Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports ribbon
        EXPECTED: <Race> Landing page is opened
        """
        pass

    def test_003_go_to_today_tab(self):
        """
        DESCRIPTION: Go to 'Today' tab
        EXPECTED: Evenets for current day are displayed
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
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_007_trigger_the_following_situation_for_this_eventchange_pricenum_and_pricedenand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Price Odds is changed
        """
        pass

    def test_008_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: **[Not actual from OX 99]** 1. *NO* Error message: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: 2. New Odds are displayed :
        EXPECTED: - in Red color if Odds decreased
        EXPECTED: - in Green color if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: 4. 'Log In & Bet' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: 'Log In & Bet' button is disabled
        """
        pass

    def test_009_go_to_tomorrow_tab(self):
        """
        DESCRIPTION: Go to 'Tomorrow' tab
        EXPECTED: Events for tomorrow day are displayed
        """
        pass

    def test_010_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps 4-8
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_8_but_add_few_selection_to_the_betslip(self):
        """
        DESCRIPTION: Repeat steps 2-8 but add few selection to the betslip
        EXPECTED: **[Not actual from OX 99]** 1. *NO* Error message: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: 2. New Odds are displayed :
        EXPECTED: - in Red color if Odds decreased
        EXPECTED: - in Green color if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: 4. 'Log In & Bet' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: 'Log In & Bet' button is disabled
        """
        pass

    def test_012_go_to_tomorrow_tab(self):
        """
        DESCRIPTION: Go to 'Tomorrow' tab
        EXPECTED: Events for tomorrow day are displayed
        """
        pass

    def test_013_repeat_step_11_for_tomorrow_tab(self):
        """
        DESCRIPTION: Repeat step 11 for 'Tomorrow' tab
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_2_8_but_add_few_selection_to_the_betslip(self):
        """
        DESCRIPTION: Repeat steps 2-8 but add few selection to the betslip
        EXPECTED: 'Multiples' section is shown in the bet slip
        """
        pass

    def test_015_trigger_the_following_situation_for_few_ofactiverace_eventschangepricenumandpricedenand_have_betslippage_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for few of active <Race> events:
        DESCRIPTION: change** priceNum **and **priceDen**
        DESCRIPTION: and have Betslip page opened to watch for updates
        EXPECTED: **[Not actual from OX 99]** 1. *NO* Error messages: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: 2. New Odds are displayed:
        EXPECTED: - in Red color if Odds decreased
        EXPECTED: - in Green color if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that X of your selections had a price change", where X -  number of selections with price change
        EXPECTED: 4. 'Log In & Bet' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: 'Log In & Bet' button is disabled
        """
        pass

    def test_016_go_to_tomorrow_tab(self):
        """
        DESCRIPTION: Go to 'Tomorrow' tab
        EXPECTED: Events for tomorrow day are displayed
        """
        pass

    def test_017_repeat_steps_14_15_for_tomorrow_tab(self):
        """
        DESCRIPTION: Repeat steps 14-15 for 'Tomorrow' tab
        EXPECTED: 
        """
        pass

    def test_018_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: 
        """
        pass

    def test_019_repeat_steps_2_8(self):
        """
        DESCRIPTION: Repeat steps 2-8
        EXPECTED: All prices on error messages are displayed in Decimal format
        """
        pass

    def test_020_login_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: user is logged in
        """
        pass

    def test_021_repeat_steps_2_19_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 2-19 for Logged In User
        EXPECTED: **[Not actual from OX 99]** 1. *NO* Error message: 'Price changed from FROM to NEW' should be displayed on red background
        EXPECTED: 2. New Odds are displayed:
        EXPECTED: - in Red color if Odds decreased
        EXPECTED: - in Green color if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: 4. 'Accept & Bet (1)' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT & PLACE BET'
        EXPECTED: Coral: 'ACCEPT AND PLACE BET'
        """
        pass
