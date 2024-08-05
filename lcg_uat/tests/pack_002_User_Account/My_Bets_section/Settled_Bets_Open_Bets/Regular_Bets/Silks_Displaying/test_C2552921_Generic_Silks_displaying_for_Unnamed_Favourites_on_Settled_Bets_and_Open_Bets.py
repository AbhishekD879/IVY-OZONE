import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.bet_history
@pytest.mark.silks
@pytest.mark.race_form
@pytest.mark.slow
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C2552921_Generic_Silks_displaying_for_Unnamed_Favourites_on_Settled_Bets_and_Open_Bets(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2552921
    NAME: Generic Silks displaying for Unnamed Favourites on Settled Bets and Open Bets
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled Bets
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed a bet on Unnamed Favourite and Unnamed 2nd Favourite
    """
    keep_browser_open = True
    horses = ['Unnamed Favourite', 'Unnamed 2nd Favourite']

    def get_market_outcomes_for_event(self, event_id):
        """
        Gets outcomes for all markets for specific event
        :param event_id: int, event id
        :return: dictionary where the key is market name, value is dictionary of outcome names and ids
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []
        markets_outcomes = {}
        for market in markets:
            if 'market' in market and 'children' in market['market']:
                outcomes = {}
                for outcome in market['market']['children']:
                    outcomes.update({outcome['outcome']['name'].replace('|', ''): outcome['outcome']['id']})
                markets_outcomes[market['market']['name'].replace('|', '')] = {'id': market['market']['id'], 'outcomes': outcomes}
        return markets_outcomes

    def verify_correct_silk_is_displayed_for_bet(self, tab_name, bet_name):
        """
        :param tab_name: tab title (for example 'OPEN BETS' or 'Settled Bets')
        :param bet_name: bet title that should be displayed with silk image

        This method iterates through the all bets available at tab with <tab_name> title. Once it has found necessary
        bet with <bet_name> title, it verifies whether generic grey silk image is displayed within that bet and
        terminates further method execution immediately.
        """
        sections = None
        if tab_name == vec.bet_history.SETTLED_BETS_TAB_NAME:
            sections = wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict,
                                       name='Sections to appear',
                                       timeout=3)
        elif tab_name == vec.bet_history.OPEN_BETS_TAB_NAME:
            sections = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict,
                                       name='Sections to appear',
                                       timeout=3)
        self.assertTrue(sections, msg=f'There are no sections available under "{tab_name}" tab')

        for section_name, section_bets in sections.items():
            bet_leg_items = section_bets.items_as_ordered_dict
            self.assertTrue(bet_leg_items, msg=f'"{section_name}" has no bet items')
            for open_bet_name, open_bet in bet_leg_items.items():
                if bet_name in bet_leg_items.keys():
                    self.assertTrue(open_bet.has_silk(timeout=4), msg=f'"{tab_name}": "{open_bet_name}" silk not found')
                    self.assertTrue(open_bet.silk.is_shown, msg=f'"{tab_name}": "{open_bet_name}" silk not displayed')
                    self.assertTrue(open_bet.silk.is_generic, msg=f'"{tab_name}": "{open_bet_name}" silk not generic')
                    break
                break

    def test_000_preconditions(self):
        """
        DESCRIPTION: User is logged in
        DESCRIPTION: User has placed a bet on Unnamed Favourite and Unnamed 2nd Favourite
        """
        race_event = self.ob_config.add_UK_racing_event(number_of_runners=0, unnamed_favorites=True)
        self.__class__.eventID = race_event.event_id
        self.__class__.marketID = race_event.market_id
        self.__class__.selection_ids = list(race_event.selection_ids.values())

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('Homepage')

    def test_001_navigate_to_open_bets_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        """
        self.site.open_my_bets_open_bets()

    def test_002_verify_single_horse_racing_bet_placed_on_unnamed_favourite(self):
        """
        DESCRIPTION: Verify Single horse racing bet placed on Unnamed Favourite
        EXPECTED: Generic grey silk image is displayed for placed bet
        """
        self.verify_correct_silk_is_displayed_for_bet(tab_name=vec.bet_history.OPEN_BETS_TAB_NAME,
                                                      bet_name='Unnamed Favourite')

    def test_003_verify_single_horse_racing_bet_placed_on_unnamed_2nd_favourite(self):
        """
        DESCRIPTION: Verify Single horse racing bet placed on Unnamed 2nd Favourite
        EXPECTED: Generic grey silk image is displayed for placed bet
        """
        self.verify_correct_silk_is_displayed_for_bet(tab_name=vec.bet_history.OPEN_BETS_TAB_NAME,
                                                      bet_name='Unnamed 2nd Favourite')

        self.result_event(selection_ids=self.selection_ids, market_id=self.marketID, event_id=self.eventID)

    def test_004_repeat_step_2_and_3_for_bet_history_tab(self):
        """
        DESCRIPTION: Repeat step 2 and 3 for 'Settled Bets' tab
        """
        self.site.open_my_bets_settled_bets()
        for horse in self.horses:
            self.verify_correct_silk_is_displayed_for_bet(tab_name=vec.bet_history.SETTLED_BETS_TAB_NAME, bet_name=horse)
