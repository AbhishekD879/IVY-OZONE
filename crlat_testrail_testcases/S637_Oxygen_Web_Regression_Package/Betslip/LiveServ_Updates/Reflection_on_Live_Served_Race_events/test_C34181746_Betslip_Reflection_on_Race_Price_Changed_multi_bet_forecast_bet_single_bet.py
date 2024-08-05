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
class Test_C34181746_Betslip_Reflection_on_Race_Price_Changed_multi_bet_forecast_bet_single_bet(Common):
    """
    TR_ID: C34181746
    NAME: Betslip Reflection on <Race>  Price Changed (multi bet-forecast bet +single bet)
    DESCRIPTION: This test case verifies Betslip reflection on HR Price Change with forecast and single E/W bets.
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
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
    PRECONDITIONS: ![](index.php?/attachments/get/10750319)
    """
    keep_browser_open = True

    def test_001_load_invictus_applicationtap_ltracegt_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Load Invictus application.
        DESCRIPTION: Tap &lt;Race&gt; icon from the sports ribbon.
        EXPECTED: &lt;Race&gt; Landing page is opened
        """
        pass

    def test_002_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_forecast_bet_to_betslip_or_bet_with_multiple_outcomes(self):
        """
        DESCRIPTION: Add Forecast Bet to BetSlip or Bet with multiple outcomes.
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_004_add_single_bet_to_betslip_it_should_be_the_first_id_from_legpart_in_forecast_bet_see_preconditions(self):
        """
        DESCRIPTION: Add single Bet to BetSlip (it should be the first ID from legPart in forecast Bet, see preconditions).
        EXPECTED: Betslip counter is increased.
        """
        pass

    def test_005_open_betslip_and_check_ew_checkbox_for_the_single_bet(self):
        """
        DESCRIPTION: Open 'Betslip' and check E/W checkbox for the single bet.
        EXPECTED: 
        """
        pass

    def test_006_open_ti_backofficetrigger_the_following_situation_for_this_eventchange_price_for_single_betand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Open ti backoffice.
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: Change price for single Bet.
        DESCRIPTION: And at the same time have Betslip page opened to watch for updates
        EXPECTED: - New Odds prices are displayed
        EXPECTED: - Forecast Bet is displayed
        """
        pass

    def test_007_place_a_bets_from_the_betslip_go_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Place a bets from the betslip. Go to the Open Bets tab.
        EXPECTED: All bets placed are displayed
        """
        pass

    def test_008_repeat_steps_2_6_try_different_options_of_price_changing_for_a_single_bet_increasingdecreasing_value(self):
        """
        DESCRIPTION: Repeat steps 2-6. Try different options of price changing for a single bet (increasing/decreasing value).
        EXPECTED: - New Odds prices are displayed
        EXPECTED: - Forecast Bet is displayed
        """
        pass

    def test_009_place_bets_from_the_betslip_go_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Place bets from the betslip. Go to the Open Bets tab.
        EXPECTED: Forecast Bet is placed and displayed.
        EXPECTED: All bets placed are displayed.
        """
        pass

    def test_010_repeat_steps_2_4open_ti_backofficechange_price_for_single_betplace_bets_from_betslip_without_checking_ew_checkbox(self):
        """
        DESCRIPTION: Repeat steps 2-4.
        DESCRIPTION: Open ti backoffice.
        DESCRIPTION: Change price for single Bet.
        DESCRIPTION: Place bets from betslip without checking E/W checkbox.
        EXPECTED: Forecast Bet is placed and displayed.
        EXPECTED: All bets placed are displayed.
        """
        pass
