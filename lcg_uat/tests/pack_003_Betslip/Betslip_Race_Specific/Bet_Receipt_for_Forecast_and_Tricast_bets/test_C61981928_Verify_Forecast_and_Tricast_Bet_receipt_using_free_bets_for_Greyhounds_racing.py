import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot grant freebet in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C61981928_Verify_Forecast_and_Tricast_Bet_receipt_using_free_bets_for_Greyhounds_racing(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C61981928
    NAME: Verify Forecast and Tricast Bet receipt using free bets for Greyhounds racing
    DESCRIPTION: This test case verifies Forecast and Tricast bet receipt for Greyhound Racing when free bets token is used while placing the bet.
    PRECONDITIONS: User logged in and has placed a Forecast and Tricast bet in Greyhound page using free bets token.
    """
    keep_browser_open = True
    bets_on_betslip = []

    def place_forecast_tricast_bet(self, multiple=False, forecast=True, tricast=False):
        self.ob_config.grant_freebet(username=self.username)
        self.navigate_to_edp(event_id=self.event.event_id, sport_name='greyhound-racing')
        market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        expected_market_tab = vec.racing.RACING_EDP_FORECAST_MARKET_TAB if forecast else vec.racing.RACING_EDP_TRICAST_MARKET_TAB
        self.assertIn(expected_market_tab, market_tabs,
                      msg=f'"{expected_market_tab}" not found in the list of tabs {list(market_tabs.keys())}')
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='greyhound-racing',
                                                                                          forecast=forecast,
                                                                                          tricast=tricast)
        if multiple:
            self.bets_on_betslip.append(expected_selection_name)
            self.ob_config.grant_freebet(username=self.username)
            self.navigate_to_edp(event_id=self.event1.event_id, sport_name='greyhound-racing')
            expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='greyhound-racing',
                                                                                              forecast=forecast,
                                                                                              tricast=tricast)
            self.bets_on_betslip.append(expected_selection_name)
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        self.stake.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()
        self.__class__.expected_market_name = vec.betslip.FORECAST if forecast else vec.betslip.TRICAST
        self.assertEqual(self.stake.market_name, self.expected_market_name,
                         msg=f'Market name "{self.stake.market_name}" '
                             f'is not the same as expected "{self.expected_market_name}"')
        if multiple:
            self.__class__.stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
            self.assertTrue(self.stake2, msg=f'Stake "{expected_selection_name}" was not found')
            self.stake2.use_free_bet_link.click()
            self.__class__.freebet_stake2 = self.select_free_bet()
            self.assertEqual(self.stake2.market_name, self.expected_market_name,
                             msg=f'Market name "{self.stake2.market_name}" '
                                 f'is not the same as expected "{self.expected_market_name}"')
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_000_preconditions(self):
        self.__class__.event = self.ob_config.add_UK_greyhound_racing_event(forecast_available=True,
                                                                            tricast_available=True)
        self.__class__.event1 = self.ob_config.add_UK_greyhound_racing_event(forecast_available=True,
                                                                             tricast_available=True)
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.place_forecast_tricast_bet()

    def test_001_verify_forecast_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Forecast Bet Receipt header.
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
            self.assertTrue(self.bet_receipt.user_header.has_user_balance,
                            msg='"User balance" button is not displayed')

    def test_002_verify_forecast_bet_bet_receipt_sub_header(self):
        """
        DESCRIPTION: Verify Forecast Bet Bet Receipt sub header.
        EXPECTED: Bet Receipt sub header contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text.
        EXPECTED: Date and time in the format: i.e. 19/09/2019, 14:57 and aligned by the right side.
        EXPECTED: Bet count in the format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt.
        """
        self.assertTrue(self.bet_receipt.receipt_header.check_icon.is_displayed(), msg='"Check" icon is not displayed')
        self.assertEqual(self.bet_receipt.receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.bet_receipt.receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        actual_date_time = self.bet_receipt.receipt_header.bet_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        expected_your_bets = f'{vec.betslip.YOUR_BETS}: (1)'
        actual_your_bets = self.bet_receipt.receipt_sub_header.bet_counter_text
        self.assertEqual(expected_your_bets, actual_your_bets,
                         msg=f'Actual bet count: {expected_your_bets} is '
                             f'not the same as expected: "{actual_your_bets}"')

    def test_003_verify_forecast_bet_receipt_placed_using_free_bet_token(self):
        """
        DESCRIPTION: Verify Forecast bet receipt placed using free bet token.
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
        EXPECTED: Free Bet Amount: -'freebet value'
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
        EXPECTED: Free Bet Amount: -'freebet value'
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

        self.assertEqual(bet_info.event_market, self.expected_market_name,
                         msg=f'Market name "{bet_info.event_market_name}" '
                             f'is not the same as expected "{self.expected_market_name}"')
        self.assertTrue(bet_info.event_name, msg='"Event name" is not displayed')
        self.assertTrue(bet_info.line_at, msg='"Line at" is not displayed')
        self.assertEqual(self.site.bet_receipt.estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                         msg='for SP, est returns are not displayed as N/A')
        self.assertTrue(self.site.bet_receipt.footer.total_stake,
                        msg="total stake amount is not displayed in the betreceipt")
        self.assertTrue(self.site.bet_receipt.footer.total_estimate_returns, msg=" Total Estimated are not displayed")
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='"Reuse Selections" button is not shown, Bet was not placed')
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')

    def test_004_place_multiple_single_bets_and_check_the_bet_receipt(self, forecast=True, tricast=False):
        """
        DESCRIPTION: Place Multiple single bets and check the Bet receipt.
        EXPECTED: Bet count information is updated according to the number of single bets Your bets (2)
        EXPECTED: Followed by Single bet cards in Order
        EXPECTED: At the End Total Stake and Estimated/Potential Returns
        """
        self.site.bet_receipt.close_button.click()
        self.place_forecast_tricast_bet(multiple=True, forecast=forecast, tricast=tricast)
        expected_your_bets = f'{vec.betslip.YOUR_BETS}: (2)'
        actual_your_bets = self.site.bet_receipt.receipt_sub_header.bet_counter_text
        self.assertEqual(actual_your_bets, expected_your_bets,
                         msg=f'Actual bet count: {actual_your_bets} is '
                             f'not the same as expected: "{expected_your_bets}"')
        self.assertTrue(self.site.bet_receipt.footer.total_stake,
                        msg="total stake amount is not displayed in the betreceipt")
        self.assertTrue(self.site.bet_receipt.footer.total_estimate_returns,
                        msg=" Total Estimated are not displayed")
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        bet_receipt_singles_section = bet_receipt_sections[vec.betslip.BETSLIP_SINGLES_NAME.title()]
        section_items = bet_receipt_singles_section.items_as_ordered_dict
        self.assertEqual(len(section_items), 2,
                         msg=f'Actual single sections order count "{len(section_items)}" is not same as Expected count: "{2}"')

    def test_005_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        # Covered in above step

    def test_006_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: Forecast bet appears in the BetSlip again
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')
        for bet_nme, bet in singles_section.items():
            if bet_nme in self.bets_on_betslip:
                self.assertEqual(bet.market_name, self.expected_market_name,
                                 msg=f'Market name "{bet.market_name}" '
                                     f'is not the same as expected "{self.expected_market_name}"')
        self.clear_betslip()
        self.place_forecast_tricast_bet(forecast=False, tricast=True)
        self.test_001_verify_forecast_bet_receipt_header()
        self.test_002_verify_forecast_bet_bet_receipt_sub_header()
        self.test_003_verify_forecast_bet_receipt_placed_using_free_bet_token()
        self.test_004_place_multiple_single_bets_and_check_the_bet_receipt(forecast=False, tricast=True)
        self.site.bet_receipt.footer.reuse_selection_button.click()
