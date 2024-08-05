import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #odds cannot be granted for prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2694493_Verify_showing_Odds_Boost_section_in_Quickbet_bet_receipt_when_the_bet_was_placed_with_Odds_Boost(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2694493
    NAME: Verify showing Odds Boost section in Quickbet bet receipt when the bet was placed with Odds Boost
    DESCRIPTION: This test case verifies displaying of Odds Boost section in Quickbet bet receipt when the bet was placed with odds boost
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application
    PRECONDITIONS: Add selection with Odds Boost token available  to Quickbet
    PRECONDITIONS: Boost the Odds
    PRECONDITIONS: Place a Bet
    """
    keep_browser_open = True
    bet_amount = 0.10

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
        PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
        PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Load application and Login into the application
        PRECONDITIONS: Add selection with Odds Boost token available  to Quickbet
        PRECONDITIONS: Boost the Odds
        PRECONDITIONS: Place a Bet
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        eventID = event_params.event_id
        expected_market = normalize_name(
            self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)
        username = tests.settings.odds_boost_user
        self.site.login(username=username)
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=username, level='selection', offer_id=offer_id)
        self.navigate_to_edp(event_id=eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=expected_market)
        self.__class__.quick_bet = self.site.quick_bet_panel
        result = wait_for_result(lambda: self.quick_bet.has_odds_boost_button(timeout=5),
                                 expected_result=True,
                                 timeout=20)
        self.assertTrue(result, msg='Odds boost button not displayed')
        self.site.wait_content_state_changed()
        self.quick_bet.selection.content.amount_form.input.value = self.bet_amount
        amount = float(self.quick_bet.selection.content.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')
        self.quick_bet.odds_boost_button.click()
        boosted_button_result = wait_for_result(
            lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name='"BOOST" button to become "BOOSTED" button with animation',
            timeout=2)
        self.assertTrue(boosted_button_result, msg='"BOOST" button to not become "BOOSTED" button with animation')
        boosted_price_result = wait_for_result(
            lambda: self.quick_bet.selection.content.boosted_odds_container.price_value,
            name='Waiting for Quick bet boosted pice',
            timeout=15)
        self.assertTrue(boosted_price_result, msg='"Quick Bet boosted price" not displayed')
        self.__class__.boosted_price = self.quick_bet.selection.content.boosted_odds_container.price_value
        self.site.quick_bet_panel.place_bet.click()

    def test_001_verify_that_odds_boost_taken_by_the_user_is_displayed_in_quickbet_receipt(self):
        """
        DESCRIPTION: Verify that Odds Boost taken by the user is displayed in Quickbet receipt
        EXPECTED: - The boost odds taken by the user is displayed
        EXPECTED: - The bet receipt confirms the bet has been boosted through an icon and line of hardcoded text  "This bet has been boosted!"
        """
        bet_receipt_displayed = self.quick_bet.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        bet_receipt = self.site.quick_bet_panel.bet_receipt
        self.assertTrue(bet_receipt.boosted_section.icon.is_displayed(),
                        msg='Boost icon is not displayed')
        self.assertEqual(bet_receipt.boosted_section.text, vec.betslip.BOOSTED_MSG,
                         msg=f'Boosted bet text "{bet_receipt.boosted_section.text}" '
                             f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        self.assertEqual(bet_receipt.odds, self.boosted_price,
                         msg=f'Boosted odds "{bet_receipt.odds}" '
                             f'are not the same as expected "{self.boosted_price}"')
