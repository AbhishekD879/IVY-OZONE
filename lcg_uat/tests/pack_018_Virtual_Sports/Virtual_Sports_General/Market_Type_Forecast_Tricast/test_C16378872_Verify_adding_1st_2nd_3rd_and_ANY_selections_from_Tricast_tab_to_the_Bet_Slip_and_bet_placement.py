import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from random import choice
from time import sleep
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.virtual_sports
@pytest.mark.forecast_tricast
@pytest.mark.tricast
@pytest.mark.reg157_fix
@pytest.mark.open_bets
@pytest.mark.login
@pytest.mark.portal_dependant
@vtest
class Test_C16378872_Verify_adding_1st_2nd_3rd_and_ANY_selections_from_Tricast_tab_to_the_Bet_Slip_and_bet_placement(BaseRacing, BaseBetSlipTest, BaseVirtualsTest):
    """
    TR_ID: C16378872
    NAME: Verify adding 1st, 2nd, 3rd and ANY selections from Tricast tab to the Bet Slip and bet placement
    DESCRIPTION: This test case verifies adding 1st, 2nd, 3rd and ANY selections from Tricast tab to the Bet Slip and bet placement.
    PRECONDITIONS: 1. Forecast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling.
    PRECONDITIONS: Note: Forecast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is logged in, has positive balance and located on Virtual Sports page.
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True

    def place_single_bet_validate_bet_receipt(self):
        bet_info = self.place_and_validate_single_bet(number_of_stakes=1)
        expected_user_balance = self.user_balance - bet_info['total_stake']
        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(betslip_info=bet_info, sp=True)
        page = 'betreceipt' if self.device_type in ['mobile', 'tablet'] else 'all'
        self.verify_user_balance(expected_user_balance=expected_user_balance, page=page)
        return bet_info

    def my_bets_open_bet_verification(self, market_name=vec.bet_history.SINGLE_TRICAST_MY_BETS_NAME):
        bet_name, tricast = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=market_name, number_of_bets=2)
        bet_legs = tricast.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: {bet_name}')
        betleg_name, betleg = list(bet_legs.items())[0]
        outcome_names = betleg.outcome_names
        return outcome_names, tricast

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sport categories
        PRECONDITIONS: User is logged in, has positive balance and located on Virtual Sports page.
        PRECONDITIONS: 1. Tricast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling. Note: Tricast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
        PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
        PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
        PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
        PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
        PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
        PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
        """
        self.__class__.bet_amount = 0.2
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        event = None
        events = None
        ss_class_id = None
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            additional_filter2 = \
                exists_filter(LEVELS.EVENT,
                              simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                            OPERATORS.INTERSECTS, 'CF,TC')), \
                exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                          ATTRIBUTES.IS_EACH_WAY_AVAILABLE,
                                                          OPERATORS.IS_TRUE))
            events = self.get_active_event_for_class(class_id=class_id, additional_filters=additional_filter2,
                                                     raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id not in virtuals_cms_class_ids:
                continue
            break
        if not event or not events:
            raise SiteServeException('There are no available virtual event with Forecast tab')

        tab_name = self.cms_virtual_sport_tab_name_by_class_ids(class_ids=[ss_class_id])
        self.__class__.expected_tab = tab_name[0]

        self.site.login()
        self.navigate_to_page('virtual-sports')
        self.site.wait_content_state('VirtualSports', timeout=5)

    def test_001_tap_virtual_sport_from_preconditions_where_tricast_market_is_configured(self):
        """
        DESCRIPTION: Tap Virtual Sport from preconditions where Tricast market is configured
        EXPECTED: Separate Tricast tabs is displayed.
        virtual sports hub is configured to a new page and from virtual sports hub we navigate to virtual sports page.
        """
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != 'NEXT EVENTS'), None)
            list(virtual_section.items_as_ordered_dict.values())[0].click()
        self.__class__.virtual_sports_list = self.site.virtual_sports
        self.virtual_sports_list.sport_carousel.open_tab(self.expected_tab)
        self.__class__.event_off_times_list = self.virtual_sports_list.tab_content.event_off_times_list
        self.assertTrue(self.event_off_times_list.is_displayed(), msg=f'No events of times found')

    def test_002_add_to_betslip_1st_2nd_and_3rd_selections_tricast_tab(self, any_bet_button=False,
                                                                       market_name=vec.racing.RACING_EDP_TRICAST_MARKET_TAB):
        """
        DESCRIPTION: Tap Tricast tab
        DESCRIPTION: Tap 1st, 2nd and 3rd selections for some runners
        DESCRIPTION: Tap Add to Betslip button
        EXPECTED: - Selected selections were successfully added to the BetSlip;
        EXPECTED: - 'Tricast' market is displayed below added selections;
        EXPECTED: - Time, place and date is displayed below 'Tricast' market (e.g. - 15:20 Cartmel);
        EXPECTED: - Stake field is empty;
        EXPECTED: - Est. Returns field is populated by 'N/A'.
        """
        event_off_time_tabs = self.event_off_times_list.items_as_ordered_dict.keys()
        self.assertTrue(event_off_time_tabs, msg=f'No events tabs found')
        event_off_time_tab = choice(list(event_off_time_tabs)[3:9])
        self.event_off_times_list.select_off_time(event_off_time_tab)

        tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
        open_tab = self.virtual_sports_list.tab_content.event_markets_list.market_tabs_list.open_tab(tab_name)
        sleep(5)
        wait_for_result(lambda: open_tab, name=vec.racing.RACING_EDP_TRICAST_MARKET_TAB,
                        timeout=20)
        self.assertTrue(open_tab, msg=f'Tab "{tab_name}" is not opened')

        selections = wait_for_result(
            lambda: self.virtual_sports_list.tab_content.event_markets_list.items_as_ordered_dict,
            timeout=10,
            name='Selection is not empty')
        self.assertTrue(selections, msg='No selections were found')

        outcome_names = self.place_forecast_tricast_bet_from_event_details_page(sport_name='virtual-sports',
                                                                                tricast=True, any_button=any_bet_button)
        self.virtual_sports_list.tab_content.event_markets_list.add_to_betslip_button.click()
        self.site.open_betslip()
        if any_bet_button:
            selection_name = f'{outcome_names[0]}\n{outcome_names[1]}\n{outcome_names[2]}'
        else:
            selection_name = f'1st.{outcome_names[0]}\n2nd.{outcome_names[1]}\n3rd.{outcome_names[2]}'

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(selection_name, stake_name,
                         msg=f'Actual selection: "{stake_name}" is not matched with Expected: "{selection_name}"')
        self.assertEqual(stake.market_name, market_name.title(),
                         msg=f'Market name "{stake.market_name}" is not matched with Expected: "{market_name.title()}"')
        event_name = stake.event_name
        self.assertTrue(event_name, msg='Event name is not displayed')
        self.assertEqual(stake.est_returns, 'N/A',
                         msg=f'Estimate Returns "{stake.est_returns}" is not matched with expected: "N/A" ')

        actual_value = stake.amount_form.input.value
        self.assertEqual(actual_value, "",
                         msg=f'Stake field is not empty actual value is "{actual_value}"')

    def test_003_enter_some_valid_stake_into_stake_field_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter some valid stake into Stake field
        DESCRIPTION: Tap Place Bet button
        EXPECTED: - Bet was placed successfully;
        EXPECTED: - All information regarding the bet is correct (bet - type, price, market, time and date, selections, stake, total stake, potential returns) on the Bet Receipt;
        EXPECTED: - User balance has decreased on the correct number based on stake.
        """
        bet_info = self.place_single_bet_validate_bet_receipt()
        self.__class__.bet = list(bet_info.values())[0]

    def test_004_go_back_to_the_tricast_tab_and_add_three_any_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go back to the Tricast tab
        DESCRIPTION: Add three ANY selections to the BetSlip
        EXPECTED: - Selected selections were successfully added to the BetSlip;
        EXPECTED: - 'Combination Tricast 6' market is displayed below added selections;
        EXPECTED: - Time, place and date is displayed below 'Combination Tricast 6' market (e.g. - 15:20 Cartmel);
        EXPECTED: - Stake field is empty;
        EXPECTED: - Est. Returns field is populated by 'N/A'.
        """
        self.navigate_to_page('virtual-sports')
        self.site.wait_content_state('VirtualSports', timeout=10)
        self.test_001_tap_virtual_sport_from_preconditions_where_tricast_market_is_configured()
        sleep(2)
        self.test_002_add_to_betslip_1st_2nd_and_3rd_selections_tricast_tab(
            any_bet_button=True, market_name=f'{vec.betslip.COMBINATION_TRICAST} 6')

    def test_005_enter_some_valid_stake_into_stake_field_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter some valid stake into Stake field
        DESCRIPTION: Tap Place Bet button
        EXPECTED: - Bet was placed successfully;
        EXPECTED: - All information regarding the bet is correct (bet - type, price, market, time and date, selections, stake, total stake, potential returns) on the Bet Receipt;
        EXPECTED: - User balance has decreased on the correct number based on stake.
        """
        reverse_bet_info = self.place_single_bet_validate_bet_receipt()
        self.__class__.reverse_bet = list(reverse_bet_info.values())[0]

    def test_006_go_to_the_my_accountsmy_betsopen_betsregular_tab(self):
        """
        DESCRIPTION: Go to the My Accounts/My Bets/Open Bets/Regular tab
        EXPECTED: Bets, placed on the previous steps are displayed with the correct information on Open Bets/Regular tab.
        """
        self.site.open_my_bets_open_bets()
        outcome_names, tricast_bet_details = self.my_bets_open_bet_verification()
        actual_selection_name = f'1st.{outcome_names[0]}\n2nd.{outcome_names[1]}\n3rd.{outcome_names[2]}'
        self.assertEqual(actual_selection_name, self.bet['outcome_name'],
                         msg=f'Actual selection name "{actual_selection_name}" does not match with expected "'
                             f'{self.bet["outcome_name"]}"')
        self.assertEqual(tricast_bet_details.est_returns.value, self.bet['estimate_returns'],
                         msg=f'Estimated returns: "{tricast_bet_details.est_returns.value,}" '
                             f'does not match with required: "{self.bet["estimate_returns"]}"')
        reverse_outcome_names, reverse_tricast_bet_details = self.my_bets_open_bet_verification(
            market_name=vec.bet_history.SINGLE_COMBINATION_TRICAST_MY_BETS_NAME)
        actual_selection_name1 = f'{reverse_outcome_names[0]}\n{reverse_outcome_names[1]}\n{reverse_outcome_names[2]}'
        self.assertEqual(actual_selection_name1, self.reverse_bet['outcome_name'],
                         msg=f'Actual selection name "{actual_selection_name1}" does not match with expected "'
                             f'{self.reverse_bet["outcome_name"]}"')
        self.assertEqual(reverse_tricast_bet_details.est_returns.value, self.reverse_bet['estimate_returns'],
                         msg=f'Estimated returns: "{reverse_tricast_bet_details.est_returns.value,}" '
                             f'does not match with required: "{self.reverse_bet["estimate_returns"]}"')
