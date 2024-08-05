import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from random import uniform

from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets
# @pytest.mark.hl
@pytest.mark.freebets
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.login
@vtest
class Test_C883830_Verify_Successful_Bet_Placement_with_Free_Bets(BaseSportTest, BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C883830
    VOL_ID: C23220557
    NAME: Verify Successful Bet Placement with Free Bets
    DESCRIPTION: This test case verifies Successful Bet Placement with Free Bets within Quick Bet
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3.  User is logged in and has positive balance
    """
    keep_browser_open = True

    selection_free_bet_value = f'{uniform(1, 2):.2f}'
    market_free_bet_value = f'{uniform(2, 3):.2f}'
    event_free_bet_value = f'{uniform(3, 4):.2f}'
    type_free_bet_value = f'{uniform(4, 5):.2f}'
    class_free_bet_value = f'{uniform(5, 6):.2f}'
    any_free_bet_value = f'{uniform(6, 7):.2f}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login as a user with Freebets available
        """
        event = self.ob_config.add_football_event_to_england_championship()
        self.__class__.eventID = event.event_id
        selection_id = event.selection_ids[vec.sb.DRAW.title()]
        market_short_name = self.ob_config.football_config. \
            england.championship.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[event.event_id][market_short_name]
        class_id = self.ob_config.football_config.england.class_id
        type_id = self.ob_config.football_config.england.championship.type_id

        expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)

        self.__class__.username = tests.settings.freebet_user

        self.ob_config.grant_freebet(username=self.username, freebet_value=self.selection_free_bet_value, level='selection', id=selection_id)
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.market_free_bet_value, level='market', id=market_id)
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.event_free_bet_value, level='event', id=self.eventID)
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.type_free_bet_value, level='type', id=type_id)
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.class_free_bet_value, level='class', id=class_id)
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.any_free_bet_value)
        self.site.login(username=self.username)

        self.__class__.free_bet_value = self.selection_free_bet_value
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value,
                                                             redemption_name=self.get_freebet_redemption_name(level='selection'))

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on selection level
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * "Use Free Bet" link is displayed under event name
        EXPECTED: "Place Bet" CTA is inactive, "Add to Betslip" active
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.assertTrue(self.quick_bet.has_use_free_bet_link(), msg='"Use Free Bet" link is not present')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='"Place Bet" is enabled')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

        self.__class__.user_balance = self.site.header.user_balance

    def test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link and Select Free bet token which is applied to the added selection AND click on 'ADD' button.
        EXPECTED: * Free bet is selected
        EXPECTED: * 'Stake' field is NOT changed
        EXPECTED: * '- Remove Free Bet' link is displayed under the event name in the 'Quick bet'
        EXPECTED: * Total stake is updated with the Freebet value
        EXPECTED: * Free bet icon is displayed near Freebet value in the total stake
        EXPECTED: * Potential returns/Est returns based on odds taken also updated
        EXPECTED: * Free bet icon below the stake box is displayed in the 'Quick bet'
        EXPECTED: 'Stake' field is filled with 0.00:
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.click()  # it's needed to hide pop-up message, don't remove this line
        self.quick_bet.use_free_bet_link.click()

        self.select_free_bet(free_bet_name=self.free_bet_name)
        self.assertEqual(self.quick_bet.amount_form.default_value, 'Stake',
                         msg=f'Actual default amount value "{self.quick_bet.amount_form.default_value}" '
                             f'does not match expected "Stake"')
        actual_stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        expected_stake = f'£{self.free_bet_value}'
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual Total Stake amount value "{actual_stake}" '
                             f'does not match expected "{expected_stake}"')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                        msg='Place Bet button is not enabled')
        self.assertTrue(self.site.quick_bet_panel.selection.content.has_remove_free_bet_link(),
                        msg='"Remove Free Bet" link is not shown')

        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=[self.ob_config.event.prices['odds_draw']],
                                      bet_amount=0,
                                      freebet_amount=float(self.free_bet_value))
        self.assertTrue(self.site.quick_bet_panel.selection.bet_summary.has_free_bet_icon(),
                        msg='Free bet icon is not displayed')
        self.assertTrue(self.site.quick_bet_panel.selection.content.has_free_bet_icon(),
                        msg='Free bet icon is not displayed')

    def test_004_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is NOT changed
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * Free bet icon is displayed near Freebet value for the stake in Bet Receipt:
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet receipt is not displayed')

        user_balance = self.site.header.user_balance
        self.assertEqual(user_balance, self.user_balance, msg='User balance was changed')
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.has_free_bet_icon(),
                        msg='Free bet icon is not displayed')

    def test_005_click_on_x_button(self):
        """
        DESCRIPTION: Click on 'X' button
        EXPECTED: Quick Bet is closed
        """
        self.site.quick_bet_panel.close()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_006_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_market_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on market level and repeat steps #2-5
        """
        self.__class__.free_bet_value = self.market_free_bet_value
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value, redemption_name=self.get_freebet_redemption_name(level='market'))

        self.test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level()
        self.test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button()
        self.test_004_tap_place_bet_button()
        self.test_005_click_on_x_button()

    def test_007_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_event_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on event level and repeat steps #2-5
        """
        self.__class__.free_bet_value = self.event_free_bet_value
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value, redemption_name=self.get_freebet_redemption_name(level='event'))

        self.test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level()
        self.test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button()
        self.test_004_tap_place_bet_button()
        self.test_005_click_on_x_button()

    def test_008_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_type_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on type level and repeat steps #2-5
        """
        self.__class__.free_bet_value = self.type_free_bet_value
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value, redemption_name=self.get_freebet_redemption_name(level='type'))

        self.test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level()
        self.test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button()
        self.test_004_tap_place_bet_button()
        self.test_005_click_on_x_button()

    def test_009_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_class_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on class level and repeat steps #2-5
        """
        self.__class__.free_bet_value = self.class_free_bet_value
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value, redemption_name=self.get_freebet_redemption_name(level='class'))

        self.test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level()
        self.test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button()
        self.test_004_tap_place_bet_button()
        self.test_005_click_on_x_button()

    def test_010_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_all_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on all level and repeat steps #2-5
        """
        self.__class__.free_bet_value = self.any_free_bet_value
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value)

        self.test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level()
        self.test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button()
        self.test_004_tap_place_bet_button()
        self.test_005_click_on_x_button()
