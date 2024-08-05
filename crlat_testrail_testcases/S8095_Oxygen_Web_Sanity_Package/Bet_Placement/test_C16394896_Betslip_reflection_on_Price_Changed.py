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
class Test_C16394896_Betslip_reflection_on_Price_Changed(Common):
    """
    TR_ID: C16394896
    NAME: Betslip reflection on Price Changed
    DESCRIPTION: This test case verifies Betslip reflection on Football Price Changed.
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    PRECONDITIONS: To get SiteServer info about event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Sport> Event should be LiveServed:
    PRECONDITIONS: Event should be LIVE ( isStarted=true )
    PRECONDITIONS: Event should be IN-PLAY:
    PRECONDITIONS: drilldown TagNames=EVFLAG_BL
    PRECONDITIONS: isMarketBetInRun=true
    PRECONDITIONS: rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: Event, Market, Outcome should be:
    PRECONDITIONS: Active ( eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A" )
    PRECONDITIONS: Odds format is Fractional
    """
    keep_browser_open = True

    def test_001_load_oxygen_appadd_sport_selection_to_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Load Oxygen app
        DESCRIPTION: Add <Sport> selection to Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip is opened
        EXPECTED: Added selection is displayed
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventchange_price_for_selection_in_tiand_at_the_same_time_have_the_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: Change price for selection in TI
        DESCRIPTION: and at the same time have the Betslip page opened to watch for updates
        EXPECTED: Price Odds is changed on
        EXPECTED: - Betslip page
        EXPECTED: Developer tool -> Application tab -> Local Storage section -> 'OX.betSelections' -> price (priceDen and priceNum values)
        """
        pass

    def test_003_verify_price_changes_in_betslip(self):
        """
        DESCRIPTION: Verify price changes in Betslip
        EXPECTED: * updated price is shown for selection
        EXPECTED: * the selection price change is displayed via push above selection: 'Price changed from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * Only Ladbrokes: info message is displayed at the top of the betslip with animations - and is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: * **'Log In & Place Bet'/'Accept & Place Bet'**(Coral) / **'Log In and Place Bet'/'Accept and place bet'** (Ladbrokes) button is **disabled**
        EXPECTED: ![](index.php?/attachments/get/58929074)
        EXPECTED: ![](index.php?/attachments/get/58929094)
        """
        pass

    def test_004_close_and_open_betslip_again(self):
        """
        DESCRIPTION: Close and open Betslip again
        EXPECTED: Updated Odds and messages are still displaying
        """
        pass

    def test_005_enter_stake_in_stake_fieldverify_that_button_become_enabled_and_the_bottom_message_is_not_shown(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field
        DESCRIPTION: Verify that button become enabled and the bottom message is not shown
        EXPECTED: * the selection price change is displayed above selection: 'Price changed from x to y'
        EXPECTED: * info message is **NOT** displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * **'Log In & Place Bet'/'Accept & Place Bet'** (Coral) / **'Log In and Place Bet'/'Accept and place bet'** (Ladbrokes) button is **enabled**
        """
        pass

    def test_006_trigger_change_price_for_selection_in_ti_one_more_timeand_at_the_same_time_have_the_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger Change price for selection in TI one more time
        DESCRIPTION: and at the same time have the Betslip page opened to watch for updates
        EXPECTED: * updated price is shown for selection
        EXPECTED: * the selection price change is displayed via push above selection: 'Price changed from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * Only Ladbrokes: info message is displayed at the top of the betslip with animations - and is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: * **'Log In & Place Bet'/'Accept & Place Bet'**(Coral) / **'Log In and Place Bet'/'Accept and place bet'** (Ladbrokes) button is **enabled**
        """
        pass

    def test_007_add_few_selections_to_betslip_stakes_are_not_added_to_any_selectionchange_price_for_one_of_the_selections_in_tiand_at_the_same_time_have_the_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Add few selections to Betslip (Stakes are not added to any selection)
        DESCRIPTION: Change price for one of the selections in TI
        DESCRIPTION: and at the same time have the Betslip page opened to watch for updates
        EXPECTED: * updated price is shown for selection
        EXPECTED: * the selection price change is displayed via push above selection: 'Price changed from x to y'
        EXPECTED: * info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: * Only Ladbrokes: info message is displayed at the top of the betslip with animations - and is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: * **'Log In & Place Bet'/'Accept & Place Bet'**(Coral) / **'Log In and Place Bet'/'Accept and place bet'** (Ladbrokes) button is **disabled**
        EXPECTED: * 'Multiples' section is shown in the bet slip and Price changes don't affect Multiples
        EXPECTED: ![](index.php?/attachments/get/58929098)
        EXPECTED: ![](index.php?/attachments/get/58929083)
        """
        pass

    def test_008_go_to_settings_and_switch_odds_format_to_decimalprovide_same_verifications(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        DESCRIPTION: Provide same verifications
        EXPECTED: Results are the same and all prices on error messages are displayed in Decimal format
        """
        pass

    def test_009_provide_same_verification_for_race_event(self):
        """
        DESCRIPTION: Provide same verification for <Race> event
        EXPECTED: Results are the same
        """
        pass
