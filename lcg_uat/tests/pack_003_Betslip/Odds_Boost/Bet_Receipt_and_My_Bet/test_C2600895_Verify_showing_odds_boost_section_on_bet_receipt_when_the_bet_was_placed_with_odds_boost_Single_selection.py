import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't grant odds boost tokens on prod
# @pytest.mark.hl - can't grant odds boost tokens on hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2600895_Verify_showing_odds_boost_section_on_bet_receipt_when_the_bet_was_placed_with_odds_boost_Single_selection(BaseBetSlipTest):
    """
    TR_ID: C2600895
    NAME: Verify showing odds boost section on bet receipt when the bet was placed with odds boost (Single selection)
    DESCRIPTION: This test case verifies that 'This bet has been boosted' text with boost icon is shown on bet receipt in case the bet was placed with odds boost for Single selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True
    bet_amount = 0.7

    def test_000_preconditions(self):
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost', {})
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event_params.event_id
        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        selection_ids = event_params.selection_ids
        self.__class__.selection_name, self.__class__.selection_id = list(selection_ids.items())[0]
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.__class__.username = tests.settings.betplacement_user

        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id,
                                              offer_id=offer_id)
        self.site.login(username=self.username, async_close_dialogs=False,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, close_free_bets_notification=False)
        self.__class__.expected_betslip_counter_value = 0

    def test_001_navigate_to_betslip_and_tap_boost_button(self):
        """
        DESCRIPTION: Navigate to Betslip and tap 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns are shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.__class__.initial_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertTrue(self.initial_total_est_returns, msg='Total Est. Returns is not shown')
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name='"BOOST" button to become "BOOSTED" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        self.assertTrue(self.stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(self.stake.is_original_odds_crossed, msg='Original odds are not crossed out')
        self.__class__.boosted_odds = self.stake.boosted_odds_container.price_value
        self.__class__.boosted_est_returns = self.stake.est_returns

        self.assertEqual(self.initial_total_est_returns, self.boosted_est_returns,
                         msg=f'Boosted estimated returns "{self.boosted_est_returns}" are not same as '
                             f'original estimated returns "{self.initial_total_est_returns}"')

    def test_002_add_stake_and_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Add Stake and tap 'Place Bet' button
        DESCRIPTION: Verify that bet receipt is shown
        EXPECTED: Bet receipt is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds was taken by the user
        EXPECTED: - potential returns/total potential returns appropriate to boosted odds
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.assertTrue(self.get_betslip_content().has_bet_now_button(), msg='Place Bet button is not present.')
        self.__class__.boosted_est_returns = self.stake.est_returns
        place_bet_button = self.get_betslip_content().bet_now_button
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()

        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        single_sections = sections.get(vec.betslip.SINGLE)
        self.assertIsNotNone(single_sections, msg='Single sections not found')
        single_section = single_sections.items_as_ordered_dict
        bet = single_section.get(self.selection_name)
        self.assertIsNotNone(bet, msg=f'Bet "{bet.name}" not found in single section')

        self.assertTrue(bet.boosted_section.icon.is_displayed(),
                        msg='Boost icon is not displayed')
        self.assertEqual(bet.boosted_section.text, vec.betslip.BOOSTED_MSG,
                         msg=f'Boosted bet text "{bet.boosted_section.text}" '
                             f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        self.assertEqual(bet.odds, self.boosted_odds,
                         msg=f'Boosted odds "{bet.odds}" '
                             f'are not the same as expected "{self.boosted_odds}"')
        self.verify_estimated_returns(est_returns=float(self.boosted_est_returns), odds=self.boosted_odds,
                                      bet_amount=self.bet_amount)
        self.site.bet_receipt.close_button.click()
