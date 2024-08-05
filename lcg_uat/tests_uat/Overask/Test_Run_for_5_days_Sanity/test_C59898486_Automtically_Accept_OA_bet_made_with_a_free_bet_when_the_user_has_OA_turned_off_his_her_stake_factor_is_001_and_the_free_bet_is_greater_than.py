import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.medium
@vtest
class Test_C59898486_Automtically_Accept_OA_bet_made_with_a_free_bet_when_the_user_has_OA_turned_off_his_her_stake_factor_is_001_and_the_free_bet_is_greater_than_the_his_her_max_stake_but_less_than_the_max_stake_of_a_10_stake_factor_user(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C59898486
    NAME: Automtically Accept OA bet made with a free bet when the user has OA turned off, his/her stake factor is 0.01 and the free bet is greater than the his/her max stake, but less than the max stake of a 1.0 stake factor user
    """
    keep_browser_open = True
    max_bet = 1.00
    prices = {'odds_home': '1/2', 'odds_away': '1/10', 'odds_draw': '1/9'}

    def register_new_user(self):
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount,
                                  card_number=tests.settings.visa_card)
        self.site.login(self.username, async_close_dialogs=False)
        self.site.wait_content_state("HomePage")

    def test_001_change_your_users_stake_factor_to_001_and_select_the_block_bet_intercept_option_in_the_block_bet_column_using_the_following_steps1_click_on_customer_in_the_ti2_enter_your_username_and_click_on_search3_when_you_are_in_your_users_record_click_on_account_rules4_at_the_global_level_change_the_stake_to_001_and_select_the_block_bet_intercept_option_in_the_block_bet_column(self):
        """
        DESCRIPTION: Change your user's stake factor to 0.01 and select the Block Bet Intercept option in the BLOCK_BET column using the following steps:
        DESCRIPTION: 1. Click on Customer in the TI
        DESCRIPTION: 2. Enter your username and click on Search
        DESCRIPTION: 3. When you are in your user's record, click on Account Rules
        DESCRIPTION: 4. At the Global level, change the Stake to 0.01 and select the Block Bet Intercept option in the BLOCK_BET column
        EXPECTED: You should have changed your user's stake factor to 0.01 and block bet intercept for your user
        """
        self.register_new_user()
        self.bet_intercept.add_account_rules(username=self.username, block_bet='NO_INTERCEPT', stake_factor=0.01)

    def test_002_using_openbet_make_the_max_stake_for_any_selection_to_1(self):
        """
        DESCRIPTION: Using Openbet, make the max stake for any selection to £1.
        EXPECTED: You should have changed the max bet for any selection to £1.
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices,
                                                                                 max_bet=self.max_bet)
        self.__class__.team1 = event_params.team1
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]

    def test_003_award_yourself_a_free_bet_of_02(self):
        """
        DESCRIPTION: Award yourself a free bet of £0.02
        EXPECTED: You should have awarded yourself a free bet of £0.02
        """
        self.__class__.freebet_value = 0.02
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.freebet_value)

    def test_004_click_on_the_selection_that_you_changed_the_max_stake_for_in_step_2_and_use_your_free_bet_to_place_the_bet(self):
        """
        DESCRIPTION: Click on the selection that you changed the max stake for in step 2 and use your free bet to place the bet.
        EXPECTED: Your bet should go through and you should see the bet receipt.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        selection = singles_section.get(self.team1, None)
        self.assertTrue(selection, msg=f'Selection "{self.team1}" not found in the Betslip')
        self.assertTrue(selection.has_use_free_bet_link(), msg='"Use Free Bet" link not found')
        selection.freebet_tooltip.click()
        selection.use_free_bet_link.click()
        freebet_stake = self.select_free_bet(self.get_freebet_name(value=self.freebet_value))
        self.assertTrue(freebet_stake, msg='No Free Bet stake available')
        self.assertTrue(selection.has_remove_free_bet_link(), msg=f'"- Remove Free Bet" link was not found')
        total_stake, freebet_value = self.get_betslip_content().total_stake, selection.free_bet_stake
        self.assertEqual(total_stake, freebet_value,
                         msg=f'Free Bet value: "{freebet_value}" '
                             f'does not match Total Stake value: "{total_stake}"')
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        total_stake = self.site.bet_receipt.footer.total_stake
        self.assertEqual(total_stake, str(self.freebet_value),
                         msg=f'"Actual Free Bet stake: "{total_stake}" '
                             f'is not as expected: "{str(self.freebet_value)}"')
