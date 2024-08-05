import pytest
import voltron.environments.constants as vec
import tests
import re
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #odds cannot be granted for prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C58420433_Verify_calculation_of_the_potential_returns_for_boosted_multiple_bet(BaseBetSlipTest,
                                                                                          BaseSportTest,
                                                                                          BaseUserAccountTest):
    """
    TR_ID: C58420433
    NAME: Verify calculation of the potential returns for boosted multiple bet.
    DESCRIPTION: This test case verifies calculation of the potential returns for boosted multiple bet.
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS.
    PRECONDITIONS: Load application and login with User with odds boost token ANY available
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: OpenBet Systems: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def verify_odds_boost_remains_boosted(self, price_format=None):
        """
        This method verifies following points:
        - 'BOOSTED' button is shown
        - Boosted odds (fractional) is shown
        - Original odds (fractional) is displayed as crossed out
        - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown
        """
        if price_format == 'Decimal':
            self.enter_stake()

            initial_home_team_stake_est_returns = self.stake.est_returns
            self.assertTrue(initial_home_team_stake_est_returns, msg=f'Est. Returns is not shown')
            initial_total_est_returns = self.get_betslip_content().total_estimate_returns
            self.assertTrue(initial_total_est_returns, msg='Total Est. Returns is not shown')

            self.tap_on_odd_boost()
            sections = self.get_betslip_sections(multiples=True)
            stake = sections.Multiples.get('Double')
            self.assertTrue(stake, msg='"Double" stake not found')

            self.assertTrue(sections.Singles.ordered_collection[self.selection_name_1].is_original_odds_crossed,
                            msg='Original odds are not crossed out for selection-1')

            self.assertTrue(sections.Singles.ordered_collection[self.selection_name_2].is_original_odds_crossed,
                            msg='Original odds are not crossed out for selection-2')

            self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out for double stake')

            boosted_price_result_selection_1 = wait_for_result(
                lambda: sections.Singles.ordered_collection[self.selection_name_1].boosted_odds_container.price_value,
                name='Waiting for bet boosted price', timeout=15)
            self.assertTrue(boosted_price_result_selection_1, msg='Boosted price for selection-1 not displayed')

            boosted_price_result_selection_2 = wait_for_result(
                lambda: sections.Singles.ordered_collection[self.selection_name_2].boosted_odds_container.price_value,
                name='Waiting for bet boosted price', timeout=15)
            self.assertTrue(boosted_price_result_selection_2, msg='Boosted price for selection-2 not displayed')

            boosted_stake_est_returns = stake.est_returns
            boosted_price = stake.boosted_odds_container.price_value

            self.assertGreaterEqual(boosted_price, boosted_stake_est_returns,
                                    msg=f'boosted stake estimated return "{boosted_stake_est_returns}", is not same as boosted price "{boosted_price}')

            self.assertNotEqual(boosted_stake_est_returns, initial_home_team_stake_est_returns,
                                msg='Boosted Est. Returns value "%s" is the same as initial value "%s"' %
                                    (boosted_stake_est_returns, initial_home_team_stake_est_returns))

            boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
            self.assertNotEqual(boosted_total_est_returns, initial_total_est_returns,
                                msg='Boosted Total Est. Returns value "%s" is the same as initial value "%s"' %
                                    (boosted_total_est_returns, initial_total_est_returns))
        else:
            self.enter_stake()
            sections = self.get_betslip_sections(multiples=True)
            stake = sections.Multiples.get('Double')
            self.assertTrue(stake, msg='"Double" stake not found')

            self.__class__.boosted_stake_est_returns = float(stake.est_returns)
            self.__class__.boosted_price = stake.boosted_odds_container.price_value
            final_boosted_price = float(re.split('\/', self.boosted_price)[0]) + 1

            self.assertEqual(final_boosted_price, self.boosted_stake_est_returns,
                             msg=f'boosted stake estimated return "{self.boosted_stake_est_returns}", is not same as boosted price "{final_boosted_price}')

    def enter_stake(self):
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.stake = sections.Multiples.get('Double')
        self.assertTrue(self.stake, msg='"Double" stake not found')

        stake_name = self.stake.name
        stake_value = "1.00"

        stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, self.stake), stake_bet_amounts=stake_bet_amounts)

    def tap_on_odd_boost(self):

        self.odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header

        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation', timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

    def verify_price_changed(self, price_format=None):

        prices = list(self.get_price_odds_on_betslip().values())

        for price in prices:
            if not price.__contains__('SP') and price_format == 'Decimal':
                self.assertRegexpMatches(price, self.decimal_pattern,
                                         msg=f'Stake odds value "{price}" not match decimal pattern: "{self.decimal_pattern}"')
            elif not price.__contains__('SP') and price_format == 'Decimal':
                self.assertRegexpMatches(price.replace(".", ""), self.fractional_pattern,
                                         msg=f'Stake odds value "{price}" not match fractional pattern: "{self.fractional_pattern}"')

    def test_000_preconditions(self):
        """
         PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS.
         PRECONDITIONS: Load application and login with User with odds boost token ANY available
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        event_1 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id_1 = list(event_1.selection_ids.values())[0]
        self.__class__.selection_name_1 = list(event_1.selection_ids.keys())[0]

        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id_2 = list(event_2.selection_ids.values())[0]
        self.__class__.selection_name_2 = list(event_2.selection_ids.keys())[0]

        self.__class__.username = tests.settings.odds_boost_user
        self.__class__.offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=self.username, id=self.selection_id_1, level='selection',
                                              offer_id=self.offer_id)
        self.ob_config.grant_odds_boost_token(username=self.username, id=self.selection_id_2, level='selection',
                                              offer_id=self.offer_id)

    def test_001_log_in_into_the_app_and_open_settings_betting_settingschange_price_to_decimal(self):
        """
        DESCRIPTION: Log in into the app and open Settings->betting settings.
        DESCRIPTION: Change price to 'Decimal'
        EXPECTED: Price changed.
        """
        self.site.login(username=self.username)
        is_format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(is_format_changed, msg='Odds format is not changed to Decimal')
        # Price changed is verifed in step-2

    def test_002_add_selections_to_betslip__selection_1_selection_2_with_available_odds_boost(self):
        """
        DESCRIPTION: Add selections to Betslip:
        DESCRIPTION: - Selection_1, Selection_2 with available odds boost.
        EXPECTED: Selections are added. 'BOOST' button is available.
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')

        self.verify_price_changed(price_format='Decimal')

    def test_003___input_1__into_the_stake_field__tap_boost_button(self):
        """
        DESCRIPTION: - Input '1'  into the stake field.
        DESCRIPTION: - Tap 'BOOST' button
        EXPECTED: - ''BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Odds are boosted
        EXPECTED: - Original odds are displayed as crossed out for Selection_1 and Selection_2
        EXPECTED: - Updated  'potential returns'/'Est. Returns' are shown for singles and for multiples section.
        EXPECTED: Potential returns should be the same as the boosted price.
        EXPECTED: There could be small difference between price and potential payout with stake = 1 for example, because of roundation logic for potential payouts(we round down them). Example price is 11.6/1 and  potential payout is 11.5
        EXPECTED: ![](index.php?/attachments/get/101693959)
        """
        self.verify_odds_boost_remains_boosted(price_format='Decimal')

    def test_004_open_settings_betting_settingschange_price_to_fractional(self):
        """
        DESCRIPTION: Open Settings->betting settings.
        DESCRIPTION: Change price to 'Fractional'
        EXPECTED: Price changed.
        """
        is_format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(is_format_changed, msg='Odds format is not changed to Fractional')

        self.site.open_betslip()
        self.verify_price_changed(price_format='Fractional')

    def test_005_open_betslip_and_verify_potential_returnsest_returns_for_boosted_multiple(self):
        """
        DESCRIPTION: Open Betslip and verify 'potential returns'/'Est. Returns' for boosted multiple.
        EXPECTED: - Updated  'potential returns'/'Est. Returns' are shown for singles and for multiples section.
        EXPECTED: Potential returns should be the same as the 'boosted price+1'.
        EXPECTED: There could be small difference between price and potential payout with stake = 1 for example, because of roundation logic for potential payouts(we round down them). Example price is 11.6/1 and potential payout is 11.5
        EXPECTED: ![](index.php?/attachments/get/101693964)
        """
        self.verify_odds_boost_remains_boosted(price_format='Fractional')

    def test_006_tap_place_bet_buttonverify_that_bet_receipts_for_multiples_bet_is_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet receipts for multiples bet is shown
        EXPECTED: Receipts for multiple bet is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds taken by the user are shown
        EXPECTED: - 'potential returns'/'Est. Returns' are shown correspondingly to boosted odds.
        """
        place_bet_button = self.get_betslip_content().bet_now_button
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()

        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        double_sections = sections.get(vec.betslip.DBL)
        self.assertTrue(double_sections, msg='Double sections not found')

        boosted_value = double_sections.multiple_odds_bet.item_odds
        boosted_text = double_sections.multiple_odds_bet.multiple_boosted_section.text
        boot_icon = double_sections.multiple_odds_bet.multiple_boosted_section.icon
        est_return = double_sections.estimate_returns

        self.assertTrue(boot_icon.is_displayed(), msg='Boost icon is not displayed')
        self.assertEqual(boosted_text, vec.betslip.BOOSTED_MSG, msg=f'Boosted bet text "{boosted_text}" '
                                                                    f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        self.assertEqual(boosted_value.split('@')[1].strip(), self.boosted_price,
                         msg=f'Boosted odds "{boosted_value}" are not the same as expected "{self.boosted_price}"')

        self.assertAlmostEqual(float(est_return), self.boosted_stake_est_returns, delta=0.01,
                               msg=f'Estimated returns "{est_return}" are not the same as expected '
                                   f'"{self.boosted_stake_est_returns}"')
        self.site.bet_receipt.close_button.click()
