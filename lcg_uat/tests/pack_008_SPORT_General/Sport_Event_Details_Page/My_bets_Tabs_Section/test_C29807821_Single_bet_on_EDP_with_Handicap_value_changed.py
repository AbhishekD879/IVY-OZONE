import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import generate_name


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.prod # can not create OB event in Prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C29807821_Single_bet_on_EDP_with_Handicap_value_changed(BaseBetSlipTest):
    """
    TR_ID: C29807821
    NAME: Single bet on EDP with Handicap value changed
    DESCRIPTION: This test case verifies single in-play bet view on sport EDP after handicap value has changed
    DESCRIPTION: Prod Incident: https://jira.egalacoral.com/browse/BMA-47150
    DESCRIPTION: Related test case: https://ladbrokescoral.testrail.com/index.php?/cases/edit/28965790
    PRECONDITIONS: - user is logged in
    PRECONDITIONS: - user has navigated to Football In-Play page
    PRECONDITIONS: - event with handicap market should be available
    PRECONDITIONS: - user has placed football single in-play bet with handicap value
    PRECONDITIONS: NOTE: For new cashout (CMS -> Cashout'isV4Enabled') use 'bet-details' response to check the bet error.
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on EPD of event, user has placed bets
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        handicap_event = self.ob_config.add_autotest_premier_league_football_event(team1=generate_name(), team2=generate_name(),
                                                                                   markets=[('handicap_match_result', {'cashout': True})],
                                                                                   is_live=True)
        self.__class__.handicap_eventID = handicap_event.event_id
        handicap_selection_id = list(list(handicap_event.selection_ids.values())[0].values())[0]
        self.__class__.event_name = handicap_event.ss_response['event']['name']
        selection_id = handicap_selection_id
        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_football_edp_of_bet_placed_from_preconditions_to_my_bets_tab(self):
        """
        DESCRIPTION: Navigate to Football EDP of bet placed (from preconditions), to 'My Bets' tab
        EXPECTED: Bet placed is shown within the tab content
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created
        """
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.SGL, event_name=self.event_name)

    def test_002_trigger_cashout_unavailable_for_the_bet_eg_handicap_value_change_22___122(self):
        """
        DESCRIPTION: Trigger cashout unavailable for the bet (eg. handicap value change: 2.2 -> 12.2)
        EXPECTED: - Bet is still displayed on My Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is disabled)
        EXPECTED: - Error is received in Network: 'getBetDetail' response: cashoutStatus: "Cashout unavailable: Selections are not available for cashout" cashoutValue: "CASHOUT_SELN_NO_CASHOUT"
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Bet is still displayed on My Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is removed)
        EXPECTED: * cashoutStatus: "Cashout unavailable: Selections are not available for cashout" and cashoutValue: "CASHOUT_HCAP_CHANGED" are received in betUpdate
        EXPECTED: ![](index.php?/attachments/get/118215542)
        """
        self.ob_config.change_event_cashout_status(event_id=self.handicap_eventID, cashout_available=False)
        self.device.refresh_page()
        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.SGL, event_name=self.event_name)
        bet_sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bet_sections, msg='No one bet section found for event with id: %s' % self.handicap_eventID)
        bet = list(bet_sections.values())[0]
        self.assertFalse(bet.buttons_panel.has_full_cashout_button(),
                         msg='"FULL CASH OUT" button  found in bet section: "%s"')
