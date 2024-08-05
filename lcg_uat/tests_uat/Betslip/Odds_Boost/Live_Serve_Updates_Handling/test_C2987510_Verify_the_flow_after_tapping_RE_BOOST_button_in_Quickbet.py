import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.betslip
@vtest
class Test_C2987510_Verify_the_flow_after_tapping_RE_BOOST_button_in_Quickbet(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2987510
    NAME: Verify the flow after tapping RE-BOOST button in Quickbet
    DESCRIPTION: This test case verifies the flow after tapping RE-BOOST button in Quickbet
    """
    keep_browser_open = True
    bet_amount = 0.3
    change_price = '5/3'

    def create_events(self):
        event = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.event_id = event.event_id
        self.__class__.selection_name = event.team1
        self.__class__.selection_id = event.selection_ids.get(self.selection_name)
        market_name = self.ob_config.football_config.england.premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Quick Bet functionality should be enabled in CMS
        PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
        PRECONDITIONS: Enable Odds Boost in CMS
        PRECONDITIONS: Load Application
        PRECONDITIONS: Login into App by user with Odds boost token generated
        PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Add selection to the Quickbet
        PRECONDITIONS: Tap 'Boost' button
        PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
        PRECONDITIONS: Tap 'Re-boost' button
        """
        # Granting odds boost and login
        username = tests.settings.betplacement_user
        for i in range(4):
            self.ob_config.grant_odds_boost_token(username=username, level='selection')
        self.create_events()
        self.site.login(username=username)
        self.site.wait_content_state_changed()
        self.navigate_to_edp(event_id=self.event_id, sport_name='football', timeout=60)

        # Placing bet
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name, selection_name=self.selection_name)
        self.site.wait_content_state(state_name='EventDetails')
        result = wait_for_result(lambda: self.site.quick_bet_panel.has_odds_boost_button(timeout=5),
                                 expected_result=True,
                                 timeout=20)
        self.assertTrue(result,
                        msg='Odds boost button not displayed')
        self.__class__.quick_bet = self.site.quick_bet_panel
        amount = self.quick_bet.selection.content.amount_form.input
        amount.click()
        self.assertTrue(amount.is_enabled(timeout=1),
                        msg='Amount field is not enabled.')
        amount.value = self.bet_amount
        self.__class__.non_boosted_price = self.site.quick_bet_panel.selection.content.odds_value
        self.quick_bet.odds_boost_button.click()
        self.__class__.previous_value = self.site.quick_bet_panel.selection.content.boosted_odds_container.price_value
        boosted_button_result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                                name='"BOOST" button to become "BOOSTED" button with animation',
                                                timeout=2)
        self.assertTrue(boosted_button_result, msg='"BOOST" button to not become "BOOSTED" button with animation')
        self.__class__.boosted_price = self.site.quick_bet_panel.selection.content.odds_value
        quick_bet_panel_after_boosted = self.site.quick_bet_panel.selection.content
        self.assertTrue(quick_bet_panel_after_boosted.is_original_odds_crossed,
                        msg='odds are not crossed')
        self.ob_config.change_price(selection_id=self.selection_id, price=self.change_price)
        result = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_quick_bet_info_panel(timeout=80),
                                 name='Waiting for Quick bet text',
                                 timeout=80)
        self.assertTrue(result, msg='"Quick Bet text" not displayed')
        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_quick_bet_info_panel(timeout=40, expected_result=False),
                                 name='Waiting for Quick bet text',
                                 timeout=40)
        self.assertFalse(result, msg='"Quick Bet text PLACE BET" is displayed')

    def test_001_verify_that_non_boosted_prices_are_updated(self):
        """
        DESCRIPTION: Verify that non-boosted prices are updated
        EXPECTED: Non-boosted prices are updated
        """
        self.__class__.odds_value = self.site.quick_bet_panel.selection.content.odds_value
        self.assertNotEqual(self.odds_value, self.non_boosted_price,
                            msg=f'Actual odd value: "{self.odds_value}" is same as'
                                f'Expected odds vasle: "{self.non_boosted_price}."')

    def test_002_verify_that_the_boosted_prices_are_updated(self):
        """
        DESCRIPTION: Verify that the boosted prices are updated
        EXPECTED: The boosted prices are updated
        """
        self.assertNotEqual(self.odds_value, self.boosted_price,
                            msg=f'Actual odd value: "{self.odds_value}" is same as'
                                f'Expected odds value: "{self.boosted_price}."')

    def test_003_verify_the_boost_button(self):
        """
        DESCRIPTION: Verify the 'Boost' button
        EXPECTED: The boost button text changes to 'BOOSTED'
        EXPECTED: The boost button remains selected
        """
        quick_bet = self.site.quick_bet_panel
        boosted_button_result = wait_for_result(lambda: quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                                name='"BOOST" button to become "BOOSTED" button with animation',
                                                timeout=2)
        self.assertTrue(boosted_button_result, msg='"BOOST" button to not become "BOOSTED" button with animation')

    def test_004_verify_that_the_returns_values_are_updated(self):
        """
        DESCRIPTION: Verify that the returns values are updated
        EXPECTED: The returns values are updated
        """
        self.after_odds = self.site.quick_bet_panel.selection.content.boosted_odds_container.price_value
        self.assertNotEqual(self.after_odds, self.previous_value,
                            msg=f' Actual Value: "{self.after_odds}" is same as'
                                f' Expected value: "{self.previous_value}"')

    def test_005_verify_that_the_header_notification_message_price_changed_from_xx_to_yy_is_removed(self):
        """
        DESCRIPTION: Verify that the header notification message 'Price changed from X/X to Y/Y' is removed
        EXPECTED: The header notification message is removed
        """
        result = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_quick_bet_info_panel(timeout=2),
                                 name='Waiting for Quick bet text',
                                 timeout=2)
        self.assertFalse(result, msg='"Quick Bet text" is displayed')
