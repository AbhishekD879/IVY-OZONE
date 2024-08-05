import json
import pytest
from voltron.environments import constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.staking_information
@vtest
class Test_C66114126_Verify_Denoting_Free_bet_journey_in_my_bets_by_placing_a_bet_with_stake_and_free_bet(BaseBetSlipTest):
    """
    TR_ID: C66114126
    NAME: Verify Denoting Free bet journey in my bets by placing a bet with stake and free bet
    DESCRIPTION: This test case is to verify Denoting Free bet journey in my bets by placing a bet with stake and free bet
    PRECONDITIONS: 
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    bet_amount = 0.50
    selection_outcomes = []

    def verify_free_bet_signposting_in_my_bets(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')

        self.assertTrue(bet.has_free_bet_icon(expected_result=True),
                        msg=f'Free Bet icon is not displayed for bet under {tab_name}')
        self.assertTrue(bet.has_free_bet_value(expected_result=True),
                        msg=f'Free Bet value is not displayed for bet under {tab_name}')

        bet.chevron_arrow.click()
        self.assertFalse(bet.is_expanded(expected_result=False),
                        msg=f'Bet is not collapsed after clicking on chevron arrow under {tab_name}')

        self.assertTrue(bet.has_free_bet_icon(expected_result=True),
                        msg=f'Free Bet icon is not displayed after collapsing the bet under {tab_name}')
        self.assertTrue(bet.has_free_bet_value(expected_result=True),
                        msg=f'Free Bet value is not displayed after collapsing the bet under {tab_name}')

        bet.chevron_arrow.click()
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded after expanding the bet under {tab_name}')

    def test_000_preconditions(self):
        """
        Get selections to place the bet
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    additional_filters=cashout_filter,
                                                    number_of_events=1)[0]
        match_result_market = next((market['market'] for market in event['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        self.__class__.username = tests.settings.freebet_user
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=f'OX.freeBets-{self.username}')
        self.__class__.bet_tokens = json.loads(cookie_value)
        self.__class__.free_bets = []
        for free_bet in self.bet_tokens:
            if free_bet['freeBetType'] == 'Free Bet':
                self.__class__.free_bets.append(free_bet)
        if len(self.free_bets) <= 0:
            raise VoltronException(f'Free bet is not available for this user {self.username}')

    def test_003_navigate_to_any_sport_from_sports_ribbona_z_menu(self):
        """
        DESCRIPTION: Navigate to any sport from Sports ribbon/A-Z menu
        EXPECTED: Should be able to navigate to sports landing page
        """
        # Covered in above step

    def test_004_place_a_single_bet_by_using_free_bet_along_with_stake_and_verify(self):
        """
        DESCRIPTION: place a single bet by using free bet along with stake and verify
        EXPECTED: should be able to place single bet successfully with free bet and stake amount
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        if self.device_type == 'mobile':
            stake.amount_form.input.click()
            bet_slip = self.get_betslip_content()
            self.assertTrue(
                bet_slip.keyboard.is_displayed(name='Bet slip keyboard shown', timeout=3),
                msg='Bet slip keyboard is not shown')
            bet_slip.keyboard.enter_amount_using_keyboard(value='free-bet')
        else:
            self.assertTrue(stake.has_use_free_bet_link(), msg='"Use Free Bet" link was not found')
            stake.use_free_bet_link.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE,
                                           verify_name=False)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" has not appeared')
        dialog.select_first_free_bet()
        self.assertTrue(dialog.wait_dialog_closed(),
                        msg=f'{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} was not closed')
        self.enter_stake_amount(stake=(stake_name, stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_005_go_to_my_bets_and_verify(self):
        """
        DESCRIPTION: Go to my bets and verify
        EXPECTED: Recently placed bets should display under open and bets will be display in expanded state by default
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_free_bet_signposting_in_my_bets(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_free_bet_signposting_in_my_bets(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_free_bet_signposting_in_my_bets(bet=settled_bet, tab_name='Settled tab')

    def test_006_verify_free_bet_sign_posting_under_open(self):
        """
        DESCRIPTION: Verify free bet sign posting under open
        EXPECTED: Free bet signposting with text of its worth should be displayed beside stake amount for 'stake'
        EXPECTED: ![](index.php?/attachments/get/4094d8aa-49c0-4c67-add4-fe7cd6e34956)
        """
        # Covered in above step

    def test_007_collapse_the_bet_by_clicking_anywhere_on_the_bet_header_and_verify(self):
        """
        DESCRIPTION: collapse the bet by clicking anywhere on the bet header and verify
        EXPECTED: Should be able to collapse bets
        """
        # Covered in above step

    def test_008_verify_free_bet_sign_posting_under_open_after_collapsing_bet(self):
        """
        DESCRIPTION: Verify free bet sign posting under open after collapsing bet
        EXPECTED: Free bet signposting with text of its worth should be displayed beside stake amount for 'stake'
        """
        # Covered in above step

    def test_009_repeat_the_step_4_to_step_8_for_cashout_and_settled_tabs(self):
        """
        DESCRIPTION: Repeat the step 4 to step 8 for cashout and settled tabs
        EXPECTED: Result should be same as above
        """
        # Covered in above step

    def test_010_repeat_the_step_3_to_step_9_by_placing_bets_in_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat the step 3 to step 9 by placing bets in lottos and pools along with races
        EXPECTED: Result should be same as above
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
        self.verify_free_bet_signposting_in_my_bets(bet=open_pools_tab_bet, tab_name='Open >> Pools tab')
