import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.insprint_auto
@pytest.mark.bet_history_open_bets
@pytest.mark.staking_information
@vtest
# This test is covering C66114122, C66114123
class Test_C66114121_Verify_the_Location_of_Potential_Returns_of_placed_bets_in_open(BaseBetSlipTest):
    """
    TR_ID: C66114121
    NAME: Verify the Location of Potential Returns of placed bets  in open
    DESCRIPTION: This test case is to verify the Location of Potential Returns of placed bets  in open
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def verify_my_bets_potential_returns_location(self, bets=[], tab_name=None):
        expected_potential_returns_location = 'right'
        for i in range(len(bets)):
            actual_potential_returns_location = bets[i].potential_returns_value.css_property_value('text-align')
            self.assertEqual(expected_potential_returns_location, actual_potential_returns_location,
                             msg=f'Expected My bets >> {tab_name} potential returns location is {expected_potential_returns_location} but '
                                 f'Actual potential return location '
                                 f'is {actual_potential_returns_location}')

            stake_y_value = bets[i].stake.location['y']
            potential_returns_y_value = bets[i].est_returns.location['y']
            self.assertTrue(stake_y_value == potential_returns_y_value, msg=f'Stake and Potential returns are not in line under {tab_name}')

            self.assertTrue(bets[i].is_expanded(expected_result=True),
                             msg=f'Bet is not expanded by default under {tab_name}')
            bets[i].chevron_arrow.click()
            self.assertFalse(bets[i].is_expanded(expected_result=False),
                             msg=f'Bet is not collapsed after clicking on chevron arrow under {tab_name}')

            # Revalidate the potential returns location after collapsing
            actual_potential_returns_location_after = bets[i].potential_returns_value.css_property_value('text-align')
            self.assertEqual(expected_potential_returns_location, actual_potential_returns_location_after,
                             msg=f'Expected My bets >> {tab_name} potential returns location after collapsing the bet is {expected_potential_returns_location} but '
                                 f'actual potential return location is {actual_potential_returns_location_after}')

            bets[i].chevron_arrow.click()
            self.assertTrue(bets[i].is_expanded(),
                            msg=f'Bet is not expanded after clicking on chevron arrow under {tab_name}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
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

        self.__class__.table_tennis_selection_id = list(self.get_active_event_selections_for_category(
            category_id=59, additional_filters=cashout_filter).values())[0]

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        self.site.login()

    def test_002_go_to_any_sport_from_sports_ribbon__a_z_menu(self):
        """
        DESCRIPTION: Go to any sport from sports ribbon / A-Z menu
        EXPECTED: Should be able to navigate to sport landing page
        """
        pass

    def test_003_place_single_and_multiple_bets_from_different_events(self):
        """
        DESCRIPTION: place single and multiple bets from different events
        EXPECTED: single and multiple bets should be placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_go_to_my_bets_and_verify_recently_placed_bets(self):
        """
        DESCRIPTION: Go to My bets and verify recently placed bets
        EXPECTED: Recently placed bets should be listed down under open Note: The bets will display in expanded state by default
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = [
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(open_tab_bet), tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cashout_tab_bet = [
            list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(cashout_tab_bet), tab_name='Cash Out tab')

        cashout_tab_bet[0].buttons_panel.full_cashout_button.click()
        cashout_tab_bet[0].buttons_panel.cashout_button.click()
        self.assertTrue(cashout_tab_bet[0].cash_out_successful_message is not None, msg='Cash Out is not successful')
        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(settled_bet), tab_name='Settled tab')

    def test_005_verify_the_location_of_the_potential_returns_for_recently_placed_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet
        EXPECTED: Location of the potential returns should be displayed in line with odds and right justified within the staking area
        EXPECTED: ![](index.php?/attachments/get/e2dee708-24b2-44ec-acc6-10120edb45b2)
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.DBL, sections.keys(),
                      msg=f'No "{vec.betslip.DBL}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.DBL)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        open_bet =[
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(open_bet), tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cashout_tab_bet = [
            list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(cashout_tab_bet), tab_name='Cash Out tab')

        cashout_tab_bet[0].buttons_panel.full_cashout_button.click()
        cashout_tab_bet[0].buttons_panel.cashout_button.click()
        self.assertTrue(cashout_tab_bet[0].cash_out_successful_message is not None, msg='Cash Out is not successful')
        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(settled_bet), tab_name='Settled tab')

    def test_006_click_on_anywhere_on_the_bet_header_to_collapse_the_bet_and_verify(self):
        """
        DESCRIPTION: Click on anywhere on the bet header to collapse the bet and verify
        EXPECTED: User should be able to collapse bet by clicking on bet header
        """
        # covered in above step

    def test_007_verify_the_location_of_the_potential_returns_for_recently_placed_bet_after_collapsing_the_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet after collapsing the bet
        EXPECTED: Location of the potential returns should be displayed in line with stake and right side alligned
        """
        # covered in above

    def test_008_repeat_step_3_to_step_8_by_placing_bets_in_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat step 3 to step 8 by placing bets in lottos and pools along with races
        EXPECTED: Result will be same as above
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
        open_pools_tab_bet = [
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_location(bets=list(open_pools_tab_bet), tab_name='Open >> Pools tab')
