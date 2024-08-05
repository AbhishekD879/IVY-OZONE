import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import generate_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create OB event in Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C28965790_ACCA_9_bet_on_Open_Bets_containing_selection_with_Handicap_value_changed(BaseBetSlipTest):
    """
    TR_ID: C28965790
    NAME: ACCA 9 bet on Open Bets containing selection with Handicap value changed
    DESCRIPTION: This test case verifies ACCA 9 bet on Open Bets tab when one of selections has handicap value changed.
    DESCRIPTION: Prod Incident: https://jira.egalacoral.com/browse/BMA-47150
    DESCRIPTION: Related test case: https://ladbrokescoral.testrail.com/index.php?/cases/edit/28965790
    PRECONDITIONS: - user is logged in
    PRECONDITIONS: - user has navigated to Football In-Play page
    PRECONDITIONS: - event with handicap market should be available
    PRECONDITIONS: NOTE: For new cashout (CMS -> Cashout'isV4Enabled') use 'bet-details' response to check the bet error.
    """
    keep_browser_open = True
    selection_ids = []
    event_names = []
    new_price_increased = '10/1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        handicap_event = self.ob_config.add_autotest_premier_league_football_event(team1=generate_name(), team2=generate_name(),
                                                                                   markets=[('handicap_match_result', {'cashout': True})],
                                                                                   is_live=True)
        self.__class__.handicap_eventID = handicap_event.event_id
        self.__class__.handicap_selection_id = list(list(handicap_event.selection_ids.values())[0].values())[0]
        self.event_names.append(handicap_event.ss_response['event']['name'])
        self.selection_ids.append(self.handicap_selection_id)

        for i in range(8):
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.eventID = event_params.event_id
            self.event_names.append(event_params.ss_response['event']['name'])
            self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.site.login()

    def test_001_place_acca_9_bet_on_football_in_play_events_one_of_which_contains_handicap_value(self):
        """
        DESCRIPTION: Place ACCA 9 bet on Football In-play events one of which contains HANDICAP value
        EXPECTED: Bet is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        EXPECTED: - tab is opened
        EXPECTED: - Placed ACCA 9 bet is displayed
        """
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.ACC9, event_name=self.event_names[0])

    def test_003_trigger_any_live_update_for_the_bet_and_observe_the_bet__price_change(self):
        """
        DESCRIPTION: Trigger any live update for the bet and observe the bet:
        DESCRIPTION: - price change
        EXPECTED: Bet is still displayed on Open Bets tab and does not disappear (even when update is received)
        """
        self.ob_config.change_price(selection_id=self.handicap_selection_id, price=self.new_price_increased)
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.ACC9, event_name=self.event_names[0])

    def test_004_trigger_cashout_unavailable_for_the_bet_eg_handicap_value_change_22___122(self):
        """
        DESCRIPTION: Trigger cashout unavailable for the bet (eg. handicap value change: 2.2 -> 12.2)
        EXPECTED: - Bet is still displayed on Open Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is disabled)
        EXPECTED: - Error is received in Network: 'getBetDetail' response:
        EXPECTED: cashoutStatus: "Cashout unavailable: Selections are not available for cashout"
        EXPECTED: cashoutValue: "CASHOUT_SELN_NO_CASHOUT"
        EXPECTED: ![](index.php?/attachments/get/3169181)
        """
        self.ob_config.change_event_cashout_status(event_id=self.eventID, cashout_available=False)
        self.device.refresh_page()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.ACC9, event_name=self.event_names[0])
        bet_sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bet_sections, msg='No one bet section found for event with id: %s' % self.eventID)
        multi_bet_section = list(bet_sections.values())[0]
        self.assertFalse(multi_bet_section.buttons_panel.has_full_cashout_button(),
                         msg='"FULL CASH OUT" button  found in bet section: "%s"')
