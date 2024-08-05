import pytest
import tests
from random import choice
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C15392949_Verify_Tricast_Bet_receipt_for_Horse_racing_Greyhounds(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C15392949
    NAME: Verify Tricast Bet receipt for Horse racing/Greyhounds
    DESCRIPTION: This test case verifies Tricast bet receipt for Horse Racing/Greyhound bets
    PRECONDITIONS: User logged in and Placed a Tricast bet in HorseRacing/Greyhound page
    """
    keep_browser_open = True
    number_of_stakes = 1
    event_ids = []

    def placing_tricast_bet(self, event_id, combination_bet=False):

        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        tabs = self.market_tabs.items_as_ordered_dict
        self.assertTrue(tabs, msg='No market tabs found')
        self.assertIn(vec.racing.RACING_EDP_FORECAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_FORECAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')
        self.assertIn(vec.racing.RACING_EDP_TRICAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_TRICAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')

        if combination_bet:
            expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(tricast=True,
                                                                                              any_button=True,
                                                                                              any_iteration_range=4)
        else:
            expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(tricast=True)

        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        if combination_bet:
            self.assertIn(vec.betslip.COMBINATION_TRICAST, self.stake.market_name,
                          msg=f'Market name "{vec.betslip.COMBINATION_TRICAST}" '
                              f'is not the same as expected "{self.stake.market_name}"')
        else:
            self.assertEqual(self.stake.market_name, vec.betslip.TRICAST,
                             msg=f'Market name "{self.stake.market_name}" '
                                 f'is not the same as expected "{vec.betslip.TRICAST}"')

        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and login
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.horseracing_config.category_id
            class_ids = self.get_class_ids_for_category(category_id=category_id)
            for i in range(0, 2):
                events_filter = self.ss_query_builder \
                    .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                        LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'SF,CF,RF,'))) \
                    .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                        LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT,TC,'))) \
                    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))

                ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
                resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
                events = [event for event in resp if
                          event.get('event') and event['event'] and event['event'].get('children')]

                if not events:
                    raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')

                event = choice(events)
                start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                              ob_format_pattern=self.ob_format_pattern,
                                                              future_datetime_format=self.my_bets_event_future_time_format_pattern,
                                                              ss_data=True)
                self.__class__.event_name = f'{event["event"]["name"]} {start_time_local}'
                self.__class__.event_id = event['event']['id']
                self.event_ids.append(self.event_id)

                market_name, outcomes = next(
                    ((market['market']['name'], market['market']['children']) for market in event['event']['children']
                     if market['market'].get('children')), None)
                if outcomes is None:
                    raise SiteServeException('There are no available outcomes')
                self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                self.__class__.selection_name, self.__class__.selection_id = list(self.selection_ids.items())[1]
                self.__class__.selection_id1 = list(self.selection_ids.values())[0]
                self._logger.info(
                    f'*** Found Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')
        else:
            for i in range(0, 2):
                event = self.ob_config.add_UK_racing_event(number_of_runners=5,
                                                           forecast_available=True,
                                                           tricast_available=True)
                event_start_time = event.event_date_time
                start_time_local = self.convert_time_to_local(date_time_str=event_start_time)
                self.__class__.event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
                self.__class__.event_id = event.event_id
                self.event_ids.append(self.event_id)

        self.site.login()
        self.placing_tricast_bet(event_id=self.event_ids[0])

    def test_001_verify_tricast_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Tricast Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: 'X' button
        EXPECTED: 'Bet Receipt' title
        EXPECTED: 'User Balance' button
        """
        self.__class__.bet_receipt = self.site.bet_receipt
        if self.device_type == 'mobile':
            self.assertTrue(self.bet_receipt.close_button.is_displayed(),
                            msg='"X" button not displayed on BET RECEIPT header')
            self.assertEqual(self.bet_receipt.bet_receipt_header_name, vec.betslip.BET_RECEIPT,
                             msg=f'Page title "{self.bet_receipt.bet_receipt_header_name}" is '
                                 f'not the same as expected "{vec.betslip.BET_RECEIPT}"')

    def test_002_verify_tricast_bet_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Tricast Bet Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        self.assertTrue(self.bet_receipt.receipt_header.check_icon.is_displayed(), msg='"Check" icon is not displayed')
        self.assertEqual(self.bet_receipt.receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.bet_receipt.receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        actual_date_time = self.bet_receipt.receipt_header.bet_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        your_bets = f'{vec.betslip.YOUR_BETS}: ({self.number_of_stakes})'
        self.assertEqual(self.bet_receipt.receipt_sub_header.bet_counter_text, your_bets,
                         msg=f'Actual bet count: {self.bet_receipt.receipt_sub_header.bet_counter_text} is '
                             f'not the same as expected: "{your_bets}"')

    def test_003_verify_tricast_bet_receipt(self):
        """
        DESCRIPTION: Verify Tricast bet receipt
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: Bet type name
        EXPECTED: Bet ID
        EXPECTED: Selection name
        EXPECTED: Bet Type name / Meeting
        EXPECTED: Stake - Stake on this Bet / Estimated - Potential Returns
        EXPECTED: Total Stake / Estimate - Potential Returns
        EXPECTED: Coral:
        EXPECTED: Single @SP
        EXPECTED: Bet ID: 0/17781521/0000041
        EXPECTED: 1st. Drops of Jupitor
        EXPECTED: 2nd. Massina
        EXPECTED: 3rd. Embour
        EXPECTED: Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake: £0.10
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £0.10
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single @SP
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: 1st. Drops of Jupitor
        EXPECTED: 2nd. Massina
        EXPECTED: 3rd. Embour
        EXPECTED: Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        bet_receipt_singles_section = bet_receipt_sections[vec.betslip.BETSLIP_SINGLES_NAME.title()]
        section_items = bet_receipt_singles_section.items_as_ordered_dict
        bet_info = list(section_items.values())[0]

        for section_name, section in bet_receipt_sections.items():
            receipts = section.items_as_ordered_dict
            self.assertTrue(receipts, msg='No Receipt legs found')
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                self._logger.info(f'*** Receipt name "{receipt_name}" has type "{receipt_type}"')
                if receipt_type == 'ReceiptSingles':
                    self.__class__.bet_id = receipt.bet_id
                    self.assertTrue(self.bet_id is not None, msg='Bet id on Bet Receipt is empty')
                    selection_names = list(bet_receipt_singles_section.items_as_ordered_dict)[0].split('\n')
                    self.assertTrue(selection_names, msg=f'"{selection_names}" are not displayed')

        self.assertTrue(bet_info.total_stake,
                        msg='Actual total stake amount value "%s" is not the same as expected "%s"')
        self.assertEqual(self.site.bet_receipt.estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                         msg='for SP, est returns are not displayed as N/A')

        self.assertTrue(self.site.bet_receipt.footer.total_stake,
                        msg="total stake amount is not displayed in the betreceipt")
        self.assertTrue(self.site.bet_receipt.footer.total_estimate_returns, msg=" Total Estimated are not displayed")

        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='"Reuse Selections" button is not shown, Bet was not placed')
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')

    def test_004_place_a_combination_tricast_betverify_bet_receipt_card_in_the_betslip(self):
        """
        DESCRIPTION: Place a Combination Tricast bet
        DESCRIPTION: Verify bet receipt card in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: Bet type name
        EXPECTED: Bet ID
        EXPECTED: Selection name
        EXPECTED: Bet Type name / Meeting
        EXPECTED: Stake - Stake on this Bet / Estimated - Potential Returns
        EXPECTED: Total Stake / Estimate - Potential Returns
        EXPECTED: Coral:
        EXPECTED: Single @SP
        EXPECTED: Bet ID: 0/17781521/0000041
        EXPECTED: Drops of Jupitor
        EXPECTED: Massina
        EXPECTED: Massina 1
        EXPECTED: Combination Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake: £0.10
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £0.10
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single @SP
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: Drops of Jupitor
        EXPECTED: Massina
        EXPECTED: Massina 1
        EXPECTED: Combination Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        self.site.bet_receipt.close_button.click()
        self.placing_tricast_bet(event_id=self.event_ids[1], combination_bet=True)
        self.test_003_verify_tricast_bet_receipt()

    def test_005_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        # covered in step 3

    def test_006_verify_stake__stake_for_this_bet(self):
        """
        DESCRIPTION: Verify Stake / Stake for this bet
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        # covered in step 3

    def test_007_verify_est_returns__potential_returns(self):
        """
        DESCRIPTION: Verify Est. Returns / Potential Returns
        EXPECTED: Est. Returns/Potential value is "N/A"
        """
        # covered in step 3

    def test_008_verify_total_stake_and_estpotential_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Est./Potential Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Est./Potential Returns value is "N/A"
        """
        # covered in step 3

    def test_009_click_on_the_reuse_selection_button(self):
        """
        DESCRIPTION: Click on the 'Reuse Selection' button
        EXPECTED: Tricast bet appears in the BetSlip again
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        self.get_betslip_content()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.ordered_collection.values())[0]
        self.assertIn(vec.betslip.COMBINATION_TRICAST, stake.market_name,
                      msg=f'Market name "{vec.betslip.COMBINATION_TRICAST}" '
                          f'is not the same as expected "{stake.market_name}"')

    def test_010_place_tricast_bet_again(self):
        """
        DESCRIPTION: Place Tricast bet again
        EXPECTED: * Tricast bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
