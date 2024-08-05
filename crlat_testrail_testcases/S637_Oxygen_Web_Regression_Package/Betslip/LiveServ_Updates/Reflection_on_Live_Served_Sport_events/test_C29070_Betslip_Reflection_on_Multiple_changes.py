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
class Test_C29070_Betslip_Reflection_on_Multiple_changes(Common):
    """
    TR_ID: C29070
    NAME: Betslip Reflection on Multiple changes
    DESCRIPTION: This test case verifies Betslip reflection on Multiple changes
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    DESCRIPTION: AUTOTEST [C9690062]
    PRECONDITIONS: 1. To get SiteServer info about event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Sport> Event should be LiveServed:
    PRECONDITIONS: *   Event should be **Live (isStarted=true)**
    PRECONDITIONS: *   Event should be **in-Play**:
    PRECONDITIONS: *   **drilldownTagNames=EVFLAG_BL**
    PRECONDITIONS: *   **isMarketBetInRun=true**
    PRECONDITIONS: *   **rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"**
    PRECONDITIONS: 3. <Sport> Event, Market, Outcome should be **Active** (**eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A"**)
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_go_to_the_liveserved_sport_event(self):
        """
        DESCRIPTION: Go to the LiveServed <Sport> event.
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_add_to_the_betslipone_sport_selection(self):
        """
        DESCRIPTION: Add to the betslip one <Sport> selection
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_005_trigger_the_following_situation_for_some_eventchange_pricenum_and_pricedenand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for some event:
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Price Odds is changed
        """
        pass

    def test_006_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: 1. *NO* Error message: 'Price changed from FROM to NEW' on red background
        EXPECTED: 2. Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: - in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: - in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: 4. 'Log In & Bet' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: 'Log In & Bet' button is disabled
        EXPECTED: **Additional for Ladbrokes**:
        EXPECTED: Info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        """
        pass

    def test_007_trigger_the_following_situation_for_this_event_againchange_pricenum_and_pricedenand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event again:
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Price Odds is changed, a new price change overrides the old price change
        """
        pass

    def test_008_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: 1. *NO* Error message: 'Price changed from FROM to NEW' on red background
        EXPECTED: 2. Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: - in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: - in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: 4. 'Log In & Bet' button is disabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: 'Log In & Bet' button is disabled
        EXPECTED: **Additional for Ladbrokes**:
        EXPECTED: Info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: 'Multiples' section is shown in the bet slip and Price changes don't affect Multiples
        """
        pass

    def test_009_trigger_the_following_situation_for_same_eventeventstatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for same event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Event becomes suspended
        """
        pass

    def test_010_verify_error_message_and_odds_indicator_for_bet(self):
        """
        DESCRIPTION: Verify Error message and Odds indicator for Bet
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Sorry, The Event/Market/Outcome Has Been Suspended.' error message should be displayed on red background, the earlier error message should be closed
        EXPECTED: 2. General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that X of your selections has been suspended"
        EXPECTED: 3. 'Stake' field, 'Quick Stake', 'Log In & Bet' button, 'Odds' and 'Estimated results'  - disabled and greyed out.
        EXPECTED: **From OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: *  Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_011_trigger_the_following_situation_for_this_suspended_eventchange_pricenum_and_pricedenand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this suspended event:
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * Price Odds is changed
        EXPECTED: * There is no visible animation (color changes) since selection is suspended
        """
        pass

    def test_012_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: **Before OX99**
        EXPECTED: 1. *NO* Error message: 'Price changed from FROM to NEW' on red background
        EXPECTED: 2. Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: - in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: - in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. General Error Message on Yellow background is still displayed above Footer with text:
        EXPECTED: "Please beware that X of your selections has been suspended"
        EXPECTED: and message about price changes doesn't appear
        EXPECTED: 4. 'Sorry, The Event/Market/Outcome Has Been Suspended.' error message should be displayed on red background below suspended selection
        EXPECTED: 5. 'Log In & Bet' button is disabled
        EXPECTED: **After OX99**
        EXPECTED: 1. *NO* Message: 'Price changed from FROM to NEW'
        EXPECTED: 2. Coral: Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: 3. 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: 4. 'Login & Place Bet' (Coral) 'Login and Place Bet' (Ladbrokes) button is disabled
        """
        pass

    def test_013_trigger_the_following_situation_for_this_suspended_eventeventstatuscodeachange_pricenum_and_pricedenand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this suspended event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * Selection becomes enable
        EXPECTED: * Price Odds is changed
        EXPECTED: * Animation is visible (color changes) (**N/A for OX 99)
        """
        pass

    def test_014_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: 1. There are no general error messages on Yellow background or below added selection
        EXPECTED: 2. Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: - in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: - in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: 3. 'Log In & Bet' button is disabled
        """
        pass

    def test_015_repeat_steps_3_14_but_add_few_sport_selections_to_the_betslip(self):
        """
        DESCRIPTION: Repeat steps 3-14 but add few <Sport> selections to the betslip
        EXPECTED: *   'Multiples' section is shown in the bet slip
        EXPECTED: *   Price change affects 'Multiples' (Double with 1 bet or a Multiple in 'Place your ACCA' section): Odds from each Single selections are multiplied and new Odds value is displayed. Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: - in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: - in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * If Stake value is entered for a Multiple with available Odds, new 'Estimated Returns' value is shown for a Multiple
        """
        pass

    def test_016_login_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: User is logged in
        """
        pass

    def test_017_repeat_steps_2_15_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 2-15 for Logged In User
        EXPECTED: 
        """
        pass
