import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C59898489_Customer_with_an_odds_boost_token_tries_to_place_a_bet_using_the_token_and_a_stake_which_is_both_greater_than_the_max_stake_for_a_selection_and_max_stake_for_the_odds_boost(BaseBetSlipTest):
    """
    TR_ID: C59898489
    NAME: Customer with an odds boost token tries to place a bet using the token and a stake which is both greater than the max stake for a selection and max stake for the odds boost
    """
    keep_browser_open = True
    max_bet = 1.1
    prices = {0: '1/20'}
    new_price = '1/6'
    odds_boost_amount = 51

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)
        self.site.login(self.username)

    def test_001_add_a_selection_to_bet_slip_or_quick_bet_click_on_the_odds_boost_button_and_add_a_stake_which_is_greater_than_both_the_max_stake_for_the_selection_and_the_max_stake_allowed_for_odds_boost(self):
        """
        DESCRIPTION: Add a selection to bet slip or Quick Bet, click on the Odds Boost button and add a stake which is greater than both the max stake for the selection and the max stake allowed for Odds Boost.
        EXPECTED: Customer should see a pop up telling them the max stake associated with the Odds Boost token and they should not be able to place the bet. They should be able to change their stake and try to place a bet again.
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 1
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        self.site.wait_content_state_changed()
        boosted = odds_boost_header.boost_button.name
        self.assertEqual(boosted, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg=f'Actual button"{boosted}" not changed to Expected button "{vec.odds_boost.BOOST_BUTTON.enabled}"')
        stake.amount_form.input.value = self.odds_boost_amount
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP_EXCEEDED, timeout=5, verify_name=False)
        self.assertTrue(info_popup, msg='Information pop-up is not shown')
        self.assertEqual(info_popup.description.replace('\n', ' '), vec.odds_boost.MAX_STAKE_EXCEEDED.text,
                         msg='Hint text \n"%s" is not the same as expected \n"%s"' %
                             (info_popup.description, vec.odds_boost.INFO_DIALOG.text))
        info_popup.click_ok()
        self.__class__.bet_amount = self.max_bet + 0.5
        self.place_single_bet(number_of_stakes=1)
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, max_bet=self.bet_amount)
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=10)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
