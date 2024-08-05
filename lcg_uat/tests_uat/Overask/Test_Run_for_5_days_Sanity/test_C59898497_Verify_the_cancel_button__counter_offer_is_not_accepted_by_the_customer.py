import pytest
import voltron.environments.constants as vec
import tests
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898497_Verify_the_cancel_button__counter_offer_is_not_accepted_by_the_customer(BaseBetSlipTest):
    """
    TR_ID: C59898497
    NAME: Verify the cancel button - counter offer is not accepted by the customer
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1
    suggested_max_bet = 0.25
    prices = {0: '1/12'}

    def test_000_precondition(self):
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add__selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add  selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask not triggered for the User')

    def test_002_counter_by_stake_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: Counter offer with the new stake highlighted and updated potential returns shown to the customeron FE
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask not yet closed')
        cms_overask_trader_message = self.get_overask_trader_offer()
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        sections = self.get_betslip_sections().Singles
        amount = float(sections.overask_trader_offer.stake_content.stake_value.value.strip('£'))
        self.assertEqual(amount, self.suggested_max_bet,
                         msg=f'The value of suggested stake "{self.suggested_max_bet}" is not present in '
                             f'the "Stake" field, the value is: "{amount}"')
        self.assertEqual(sections.overask_trader_offer.stake_content.stake_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for stake is not highlighted in yellow')
        expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=expected_return, bet_amount=amount, odds=self.prices[0])

    def test_003_verify_the_cancel_button(self):
        """
        DESCRIPTION: Verify the cancel button
        EXPECTED: On clicking Cancel -  a pop up should appear asking the customer to confirm by clicking the 'Cancel Offer' button or return to the offer by clicking on the 'No, Return button'
        EXPECTED: On clicking 'Cancel Offer', the counter offer should close.
        EXPECTED: My Bets and Account History should not show any record of this offer and cancellation.
        """
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg="Cancel button not present")
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        self.assertTrue(dialog, msg='"Cancel Offer?" pop up is not displayed')
        cancel_offer_text = dialog.cancel_offer_button.name
        self.assertEqual(cancel_offer_text, vec.betslip.OVERASK_ELEMENTS.confirm_cancel_traders_offer,
                         msg=f'"{cancel_offer_text}" is not same as "{vec.betslip.OVERASK_ELEMENTS.confirm_cancel_traders_offer}"')
        no_returns_text = dialog.no_return_button.name
        self.assertEqual(no_returns_text, vec.betslip.OVERASK_ELEMENTS.cancel_cancel_traders_offer,
                         msg=f'"{no_returns_text}" is not same as "{vec.betslip.OVERASK_ELEMENTS.cancel_cancel_traders_offer}"')
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
