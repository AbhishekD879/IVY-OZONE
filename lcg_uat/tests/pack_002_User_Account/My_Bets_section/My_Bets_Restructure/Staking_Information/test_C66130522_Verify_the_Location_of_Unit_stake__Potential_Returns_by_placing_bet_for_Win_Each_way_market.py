import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


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
class Test_C66130522_Verify_the_Location_of_Unit_stake__Potential_Returns_by_placing_bet_for_Win_Each_way_market(BaseBetSlipTest):
    """
    TR_ID: C66130522
    NAME: Verify the Location of Unit stake &  Potential Returns by placing bet for Win/Each way market
    DESCRIPTION: This test case is to verify the location of Unit stake & Potential Returns by placing bet for Win/Each way market
    PRECONDITIONS: 
    """
    keep_browser_open = True
    selection_ids = []
    runner_names = []
    market_names_edp = []

    def verify_my_bets_potential_returns_and_unit_stake_location(self, bets=[], tab_name=None):
        expected_potential_returns_location = 'right'
        for i in range(len(bets)):
            actual_potential_returns_location = bets[i].potential_returns_value.css_property_value('text-align')
            self.assertEqual(expected_potential_returns_location, actual_potential_returns_location,
                             msg=f'Expected My bets >> {tab_name} potential returns location is {expected_potential_returns_location} but '
                                 f'Actual potential return location '
                                 f'is {actual_potential_returns_location}')
            unit_stake_y_value = bets[i].unit_stake.location['y']
            potential_returns_y_value = bets[i].potential_returns.location['y']
            self.assertTrue(unit_stake_y_value == potential_returns_y_value,
                            msg=f'unit stake and Potential returns are not in line under {tab_name}')
            odds_y_value = bets[i].odds.location['y']
            self.assertGreater(potential_returns_y_value, odds_y_value,
                               msg=f'odds y  value is not greater than potential returns y value {tab_name}')

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
        EXPECTED: Application should be launched succesfully
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        for event in events:
            if event['event']['cashoutAvail'] != 'Y':
                continue
            market = next((market for market in event['event']['children'] if
                           market['market']['templateMarketName'] == 'Win or Each Way'), None)
            if market['market']['cashoutAvail'] != 'Y':
                continue
            outcomes_resp = market['market']['children']
            selection = next((i for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']),
                             None)
            if not selection:
                continue
            self.selection_ids.append(selection['outcome']['id'])
            self.runner_names.append(selection['outcome']['name'])
            self.market_names_edp.append(
                f"Win or Each Way, {market['market']['eachWayFactorNum']}/{market['market']['eachWayFactorDen']} odds - places {','.join([str(i) for i in range(1, int(market['market']['eachWayPlaces']) + 1)])}")
            if len(self.selection_ids) == 3:
                break
        if len(self.selection_ids) < 3:
            raise SiteServeException('Enough Events are not available to place treble bet.')

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        self.site.login()

    def test_002_go_to_horse_racing_from_a_z_menu_or_sports_ribbon(self):
        """
        DESCRIPTION: Go to Horse racing from A-Z menu or sports ribbon
        EXPECTED: Should be able to navigate to sport landing page
        """
        pass

    def test_003_go_to_any_uk_and_irish_meeting_then_click_on_wineach_way(self):
        """
        DESCRIPTION: Go to any uk and irish meeting then click on Win/each way
        EXPECTED: should be able to navigate to win/Each way market in meeting edp
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])

    def test_004_place_single_and_multiple_bets_from_different_events(self):
        """
        DESCRIPTION: place single and multiple bets from different events
        EXPECTED: single and multiple bets should be placed successfully
        """
        self.place_single_bet(number_of_stakes=1, each_way=True)
        self.check_bet_receipt_is_displayed()

    def test_005_go_to_my_bets_and_verify_recently_placed_bets(self):
        """
        DESCRIPTION: Go to My bets and verify recently placed bets
        EXPECTED: Recently placed bets should be listed down under open Note: The bets will display in expanded state by default
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = [
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_and_unit_stake_location(bets=list(open_tab_bet), tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cashout_tab_bet = [
            list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_and_unit_stake_location(bets=list(cashout_tab_bet), tab_name='Cash Out tab')
        cashout_tab_bet[0].buttons_panel.full_cashout_button.click()
        cashout_tab_bet[0].buttons_panel.cashout_button.click()
        self.assertTrue(cashout_tab_bet[0].cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_and_unit_stake_location(bets=list(settled_bet), tab_name='Settled tab')

    def test_006_verify_the_location_of_the_potential_returns_for_recently_placed_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet
        EXPECTED: Location of the potential returns should be displayed in line with odds and right justified within the staking area.
        EXPECTED: Potential Returns should be inlined with the Unit stake line.
        EXPECTED: Note: Unit stake and Stake will display for Win or Each way bets
        EXPECTED: ![](index.php?/attachments/get/682208c9-1701-479f-bb04-e82970816aa5)
        """
        #multiple bet placement
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_info = self.place_multiple_bet(number_of_stakes=1, each_way=True)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        open_tab_bet = [
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_and_unit_stake_location(bets=list(open_tab_bet), tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cashout_tab_bet = [
            list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_and_unit_stake_location(bets=list(cashout_tab_bet),
                                                                      tab_name='Cash Out tab')
        cashout_tab_bet[0].buttons_panel.full_cashout_button.click()
        cashout_tab_bet[0].buttons_panel.cashout_button.click()
        self.assertTrue(cashout_tab_bet[0].cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_potential_returns_and_unit_stake_location(bets=list(settled_bet), tab_name='Settled tab')

    def test_007_click_on_anywhere_on_the_bet_header_to_collapse_the_bet_and_verify(self):
        """
        DESCRIPTION: Click on anywhere on the bet header to collapse the bet and verify
        EXPECTED: User should be able to collapse bet by clicking on bet header
        """
        #covered in above step

    def test_008_verify_the_location_of_the_potential_returns_for_recently_placed_bet_after_collapsing_the_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet after collapsing the bet
        EXPECTED: Location of the potential returns should be displayed in line with stake and right side aligned
        """
        #covered in above step

    def test_009_repeat_step_3_to_step_and_verify_under_cashout_and_settled_tabs(self):
        """
        DESCRIPTION: Repeat step 3 to step and verify under cashout and settled tabs
        EXPECTED: Result will be same as above
        """
        #covered in above step
