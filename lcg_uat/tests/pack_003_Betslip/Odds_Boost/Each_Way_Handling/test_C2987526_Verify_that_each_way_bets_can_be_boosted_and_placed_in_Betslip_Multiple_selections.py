import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  Can't grant odds boost tokens on prod
# @pytest.mark.hl    Can't grant odds boost tokens on prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.odds_boost
@pytest.mark.desktop
@vtest
class Test_C2987526_Verify_that_each_way_bets_can_be_boosted_and_placed_in_Betslip_Multiple_selections(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C2987526
    NAME: Verify that each way bets can be boosted and placed in Betslip (Multiple selections)
    DESCRIPTION: This test case verifies that each way bet can be boosted and placed in Betslip for Multiple selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add 2(two) just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1
    PRECONDITIONS: Add two selections from Horse Racing/Greyhounds (E/W market with LP available) to Betslip
    """
    keep_browser_open = True
    prices = {0: '4/12', 1: '5/14'}
    username = tests.settings.betplacement_user
    bet_amount = 0.11

    def add_stake_verify_boost(self, multiple):
        for stake_name, stake in self.singles_section.items():
            stake.amount_form.input.value = self.bet_amount
        self.__class__.multiple_stake_title, self.__class__.multiple_stake = list(self.multiples_section.items())[0]
        if multiple == vec.betslip.DBL:
            self.assertEquals(self.multiple_stake_title, vec.betslip.DBL, msg="stake is not displayed as double")
        else:
            self.assertEquals(self.multiple_stake_title, vec.betslip.TBL, msg="stake is not displayed as double")
        self.multiple_stake.amount_form.input.value = self.bet_amount
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg=f'Button text "{self.odds_boost_header.boost_button.name}" '
                             f'is not the same as expected "{vec.odds_boost.BOOST_BUTTON.disabled}"')
        self.__class__.stake_value = self.get_betslip_content().total_stake
        self.__class__.estimate_returns = self.get_betslip_content().total_estimate_returns

    def tap_boost_verify_boosted_section(self):
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name='"BOOST" button to become "BOOSTED" button with animation',
            timeout=2)

        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        if self.brand == 'bma':
            self.assertTrue(self.odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        else:
            self.assertIn('enabled', self.odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')

    def placebet_verify_receipt(self, multiple):
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt = self.site.bet_receipt
        sections = bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        single_sections = sections.get(vec.betslip.SINGLE)
        if multiple == vec.betslip.DBL:
            multiple_sections = sections.get(vec.betslip.DBL)
        else:
            multiple_sections = sections.get(vec.betslip.TBL)
        self.assertIsNotNone(single_sections, msg='Single sections not found')
        single_section = single_sections.items_as_ordered_dict

        self.__class__.stake_value = 0
        self.__class__.multiple_stake_value = 0
        for stake_name in dict(single_section.items()):
            bet = single_section.get(stake_name)
            self.assertIsNotNone(bet, msg=f'Bet "{bet.name}" not found in section')
            if bet.odds == "SP":
                self.assertFalse(bet.has_boosted_section(expected_result=False),
                                 msg='Boost icon is displayed')
            else:
                self.assertTrue(bet.boosted_section.icon.is_displayed(),
                                msg='Boost icon is not displayed')

                self.assertEqual(bet.boosted_section.text, vec.betslip.BOOSTED_MSG,
                                 msg=f'Boosted bet text "{bet.boosted_section.text}" '
                                     f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
                self.assertEqual(bet.odds, self.boosted_odds,
                                 msg=f'Boosted odds "{bet.odds}"'
                                     f'are not the same as expected "{self.boosted_odds}"')
            self.stake_value += float(bet.total_stake)
            bet_ew = bet.ew_terms.split('\n')[1]
            ew_txt = f'2 Lines at £{self.bet_amount} per line'
            self.assertEquals(bet_ew, ew_txt, msg="eachway msg is not displayed")
        if multiple == vec.betslip.DBL:
            self.assertTrue(multiple_sections.multiple_odds_bet.multiple_boosted_section.icon.is_displayed(),
                            msg='Boost icon is not displayed')

            self.assertEqual(multiple_sections.multiple_odds_bet.multiple_boosted_section.text, vec.betslip.BOOSTED_MSG,
                             msg=f'Boosted bet text "{multiple_sections.multiple_odds_bet.multiple_boosted_section.text}" '
                                 f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        else:
            self.assertFalse(multiple_sections.multiple_odds_bet.has_multiple_boosted_section(expected_result=False),
                             msg='Boost section is displayed')

        self.multiple_stake_value = multiple_sections.multiple_odds_bet.total_stake
        self.assertEquals(multiple_sections.multiple_odds_bet.ew_terms_lines, ew_txt,
                          msg="eachway msg is not displayed")
        footer = self.site.bet_receipt.footer
        total_stake = footer.total_stake
        total_est_returns = footer.total_estimate_returns
        actual_total_stake = self.stake_value + float(self.multiple_stake_value)
        total_stake_betreceipt = float(total_stake.replace(',', ''))
        self._logger.info(f'*** Total stake {total_stake_betreceipt}, total est returns {total_est_returns}')
        self.assertEqual(actual_total_stake, total_stake_betreceipt,
                         msg=f'Total stake on betslip {actual_total_stake} doesn\'t match with total '
                             f'stake on betreceipt {total_stake_betreceipt}')

    def test_000_precondition(self):
        """
        DESCRIPTION: "Odds Boost" Feature Toggle is enabled in CMS
        DESCRIPTION: CREATE Odds Boost token with ANY Bet Type
        DESCRIPTION: Login with USER1
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        self.__class__.expected_odds_boost_amount = 0
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.expected_odds_boost_amount += 1

        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                           lp_prices=self.prices)
        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                           lp_prices=self.prices)
        self.__class__.selection_ids = (list(event_params1.selection_ids.values())[0],
                                        list(event_params2.selection_ids.values())[0])
        event_params3 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1)

        self.__class__.selection_ids_3 = (list(event_params3.selection_ids.values())[0])
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('HomePage')
        self.site.login(username=self.username)

    def test_001_navigate_to_betslipadd_a_stake_to_singles_and_doubleverify_that_odds_boost_section_is_available(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Add a Stake to SINGLES and DOUBLE
        DESCRIPTION: Verify that odds boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
        self.add_stake_verify_boost(multiple=vec.betslip.DBL)

    def test_002_check_each_way_checkbox_for_singles_and_doubleverify_that_total_stake_and_est_returns_are_updated_appropriately(
            self):
        """
        DESCRIPTION: Check 'Each Way' checkbox for SINGLES and DOUBLE
        DESCRIPTION: Verify that Total Stake and Est. Returns are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked for SINGLES and DOUBLE
        EXPECTED: - Updated Est. Returns for SINGLES and DOUBLE are shown
        EXPECTED: - Updated Estimated/Potential Returns is shown
        EXPECTED: - Updated Total Stake is shown
        """
        for stake_name, stake in self.singles_section.items():
            boost_est_ret = stake.est_returns
            stake.each_way_checkbox.click()
            self.assertTrue(stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
            self.__class__.est_ret = stake.est_returns
            self.assertGreater(self.est_ret, boost_est_ret,
                               msg=f'Actual est returns value "{self.est_ret}" < Expected "{boost_est_ret}"')
        dbl_boost_est_ret = self.multiple_stake.est_returns
        self.multiple_stake.each_way_checkbox.click()
        self.assertTrue(self.multiple_stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        dbl_est_ret = self.multiple_stake.est_returns
        self.assertGreater(dbl_est_ret, dbl_boost_est_ret,
                           msg=f'Actual est value "{dbl_est_ret}" less than "{dbl_boost_est_ret}"')
        each_way_stake = self.get_betslip_content().total_stake
        each_way_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertGreater(each_way_stake, self.stake_value,
                           msg=f'Actual "Total Stake" value "{each_way_stake}" less than expected "{self.stake_value}"')
        self.assertGreater(each_way_estimate_returns, self.estimate_returns,
                           msg=f'Actual Total est returns value "{each_way_estimate_returns}" are less than "{self.estimate_returns}"')

    def test_003_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: Betslip is shown with appropriate elements for SINGLES and DOUBLE:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown for SINGLES and DOUBLE
        EXPECTED: - Updated Est. Returns are shown for SINGLES are shown
        EXPECTED: - Updated Est. Returns are shown for DOUBLE as N/A
        EXPECTED: - Updated Estimated/Potential Returns is shown
        """
        self.tap_boost_verify_boosted_section()
        for stake_name, stake in self.singles_section.items():
            self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
            self.__class__.boosted_odds = stake.boosted_odds_container.price_value
            self.assertEquals(self.est_ret, stake.est_returns,
                              msg=f'Actual Total est returns value "{self.est_ret}" not equals to "{stake.est_returns}"')
        self.assertTrue(self.multiple_stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.__class__.multiple_boosted_odds = self.multiple_stake.boosted_odds_container.price_value
        self.assertEquals(self.multiple_stake.est_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                          msg="for double, est returns is not displayed as N/A")
        self.__class__.stake_value = self.get_betslip_content().total_stake
        self.__class__.estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEquals(self.estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                          msg=f'New Potential Returns value "{self.estimate_returns}" is not updated')

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_each_way_stake_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with each way stake and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements for SINGLES and DOUBLE:
        EXPECTED: - Odds boost title
        EXPECTED: - Calculated odds
        EXPECTED: - 2Lines at (Amount) per line
        EXPECTED: - Stake = Total Stake
        """
        self.placebet_verify_receipt(multiple=vec.betslip.DBL)

    def test_005_tap_reuse_selection_buttonadd_one_more_selection_from_horse_racinggreyhounds_ew_market_with_sp_only_to_betslipand_add_stake_for_singles_and_trebleverify_that_odds_boost_button_is_shown(
            self):
        """
        DESCRIPTION: Tap 'Reuse selection' button
        DESCRIPTION: Add one more selection from Horse Racing/Greyhounds (E/W market with SP ONLY) to Betslip
        DESCRIPTION: And add Stake for SINGLES and TREBLE
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.expected_odds_boost_amount += 1
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Cannot find "Reuse selection" button')
        self.site.bet_receipt.footer.reuse_selection_button.click()
        self.site.close_betslip()
        self.open_betslip_with_selections(selection_ids=self.selection_ids_3, timeout=15)
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, self.__class__.multiples_section = sections.Singles, sections.Multiples
        self.add_stake_verify_boost(multiple=vec.betslip.TBL)

    def test_006_tap_boost_button(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        EXPECTED: Betslip is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown for SINGLES with LP
        EXPECTED: - 'i' icon is shown for SINGLE with SP and for TREBLE
        EXPECTED: - Updated Est. Returns is shown for SINGLES with LP
        EXPECTED: - N/A Est. returns is shown for SINGLE with SP and for TREBLE
        EXPECTED: - N/A Estimated/Potential Returns is shown
        """
        self.tap_boost_verify_boosted_section()
        for stake_name, stake in self.singles_section.items():
            if stake.odds == 'SP':
                self.assertTrue(stake.odds_boost_info_icon.is_displayed(), msg='i icon is not shown')
                self.assertEquals(stake.est_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                                  msg='for SP, est returns are not displayed as N/A')
            else:
                self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
                self.__class__.boosted_odds = stake.boosted_odds_container.price_value
                self.assertGreater(stake.est_returns, "0.00",
                                   msg=f'Actual Total est returns not updated "{stake.est_returns}"')
        self.multiple_stake_title, self.multiple_stake = list(self.multiples_section.items())[0]
        self.assertEquals(self.multiple_stake_title, vec.betslip.TBL, msg="stake is not displayed as triple")
        self.assertTrue(self.multiple_stake.odds_boost_info_icon.is_displayed(), msg='i icon is not shown')
        self.assertEquals(self.multiple_stake.est_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                          msg='for Trebles, est returns are not displayed as N/A')
        estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEquals(estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                          msg=f'New Potential Returns value "{estimate_returns}" is not updated')

    def test_007_check_each_way_checkbox_for_singles_and_trebleverify_that_total_stake_and_est_return_are_updated_appropriately(
            self):
        """
        DESCRIPTION: Check 'Each Way' checkbox for SINGLES and TREBLE
        DESCRIPTION: Verify that Total Stake and Est. Return are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked for SINGLES and TREBLE
        EXPECTED: - Updated Total Stake is shown
        EXPECTED: - Estimated/Potential Returns is N/A
        """
        for stake_name, stake in self.singles_section.items():
            stake.each_way_checkbox.click()
            self.assertTrue(stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.multiple_stake.each_way_checkbox.click()
        self.assertTrue(self.multiple_stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        each_way_stake = self.get_betslip_content().total_stake
        each_way_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertGreater(each_way_stake, self.stake_value,
                           msg=f'Actual "Total Stake" value "{each_way_stake}" less than expected "{self.stake_value}"')
        self.assertEquals(each_way_estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                          msg=f'Actual "Estimated/Potential Returns is not updated')

    def test_008_tap_place_bet_buttonverify_that_bet_is_placed_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements for for SINGLES and TREBLE:
        EXPECTED: - Odds boost title
        EXPECTED: - Calculated odds for LP SINGLES
        EXPECTED: - N/A odds for TREBLE and SP Single
        EXPECTED: - 2Lines at (Amount) per line
        EXPECTED: - Stake = Total Stake
        """
        self.placebet_verify_receipt(multiple=vec.betslip.TBL)
