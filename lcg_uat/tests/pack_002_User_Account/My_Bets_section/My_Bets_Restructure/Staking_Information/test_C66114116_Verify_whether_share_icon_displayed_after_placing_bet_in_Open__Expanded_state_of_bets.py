import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.staking_information
@vtest
# This test is covering C66114117, C66114118, C66111685, C66111690, C66111701
class Test_C66114116_Verify_whether_share_icon_displayed_after_placing_bet_in_Open__Expanded_state_of_bets(BaseBetSlipTest):
    """
    TR_ID: C66114116
    NAME: Verify whether share icon displayed after placing bet in Open - Expanded state of bets
    DESCRIPTION: This test case is to verify the share icon displaying under open bets or not
    PRECONDITIONS:
    """
    keep_browser_open = True
    selection_outcomes = []

    def verify_my_bets_share_button(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                        msg=f'Share button is not displayed under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details is not expanded after click on Bet Details chevron under {tab_name}')
        self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                        msg=f'Share button is not displayed under {tab_name} after expanded the Bet Details')
        bet.bet_details.chevron_arrow.click()
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                        msg=f'Bet Details is not collapsed after click on Bet Details chevron under {tab_name}')
        self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                        msg=f'Share button is not displayed under {tab_name} after collapsing the Bet Details')
        potential_returns_y_value = bet.potential_returns_value.location['y']
        share_button_y_value = bet.bet_details.share_button.location['y']
        self.assertTrue(potential_returns_y_value < share_button_y_value,
                        msg=f'potential returns are not above the share button under {tab_name}')
        bet.chevron_arrow.click()
        self.assertFalse(bet.is_expanded(expected_result=False),
                        msg=f'Bet is not collapsed after clicking on chevron arrow under {tab_name}')
        self.assertFalse(bet.has_bet_details(expected_result=False),
                        msg=f'Bet Details section is displayed under {tab_name}')
        bet.chevron_arrow.click()
        self.assertTrue(bet.is_expanded(expected_result=True),
                         msg=f'Bet is not expanded after clicking on chevron arrow under {tab_name}')

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        self.__class__.number_of_events = 3
        self.__class__.selection_ids = []
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        fb_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=self.number_of_events)
        for fb_event in fb_events:
            match_result_market = next((market['market'] for market in fb_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            fb_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            fb_selection_id = list(fb_all_selection_ids.values())[0]
            self.selection_ids.append(fb_selection_id)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        self.site.login()

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        # Covered in above step

    def test_003_navigate_to_any_sport_landing_page_from_sports_ribbon_a_z_menu(self):
        """
        DESCRIPTION: Navigate to any sport landing page from sports ribbon /A-Z menu
        EXPECTED: User should be able to navigate to SLP
        """
        # Covered in above step

    def test_004_place_single_and_mutiple_bets_from_different_events(self):
        """
        DESCRIPTION: Place single and mutiple bets from different events
        EXPECTED: Single and multiple bets should be placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_005_go_to_my_bets_and_verify_recently_placed_bets_under_open(self):
        """
        DESCRIPTION: Go to my bets and verify recently placed bets under open
        EXPECTED: Should be match the bet details under open with recently placed single/multiple bets Note: Bets will be in expanded state by default
        """
        self.site.open_my_bets_open_bets()

    def test_006_verify_share_icon_displaying_under_open(self):
        """
        DESCRIPTION: Verify share icon displaying under open
        EXPECTED: Share icon should be displayed in Open and to be in line with the Bet Details information  Note: Potential returns should be in the above line of share icon
        EXPECTED: ![](index.php?/attachments/get/f0f82504-aa21-4c86-8f04-ce97ffac2c72)
        """
        open_tab_bet = next(iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())), None)
        self.assertIsNotNone(open_tab_bet,msg='Bet is not available under Open tab')
        self.verify_my_bets_share_button(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())), None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_my_bets_share_button(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())), None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_my_bets_share_button(bet=settled_bet, tab_name='Settled tab')

    def test_007_repeat_the_step_3_to_step_6__by_placing_bets_for_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat the step 3 to step 6  by placing bets for lottos and pools along with races
        EXPECTED: Result will be the same as above
        """
        base_uk_tote_instance = BaseUKTote()
        event = base_uk_tote_instance.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.bet_amount = event.min_total_stake
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='Tote Pool tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')
        for index, (outcome_name, outcome) in enumerate(self.outcomes[:2]):
            self.__class__.selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
        bet_builder.summary.add_to_betslip_button.click()
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(), msg='Remove button was not found')
        self.__class__.stake = stake
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        result = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(result, msg=f'{vec.bet_history.POOLS_TAB_NAME} tab is not opened')
        open_pools_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(open_pools_tab_bet, msg='Bet is not available under Open >> Pools tab')
        self.verify_my_bets_share_button(bet=open_pools_tab_bet, tab_name='Open >> Pools tab')