import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C22037804_Vanilla_Place_bet_after_manual_product_reopening(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C22037804
    NAME: [Vanilla] Place bet after manual product reopening
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in on user account that had Sports product closed, but reopened it manually
    PRECONDITIONS: 3. User has enough balance to place a bet
    """
    keep_browser_open = True
    product_name = 'Sports'

    def product_open_reopen(self, close=True):
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name=vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_content_state_changed()
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        if close:
            self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1).click()
        else:
            self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_3).click()
        self.site.account_closure.continue_button.click()
        self.site.wait_content_state_changed()
        closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(closure_details, msg='List of products isn\'t available to the user')
        product = closure_details.get(self.product_name)
        if close:
            self.assertTrue(product.close_button.is_displayed(), msg='"CLOSE button" is not displayed')
            product.close_button.click()
            duration_options = self.site.service_closure.duration_options.items_as_ordered_dict
            self.assertTrue(duration_options, msg='Duration radio buttons aren\'t displayed')
            reason_options = self.site.service_closure.reason_options.items_as_ordered_dict
            self.assertTrue(reason_options, msg='Reason radio buttons aren\'t displayed')
            list(duration_options.values())[0].click()
            list(reason_options.values())[0].click()
            self.site.service_closure.continue_button.click()
            self.site.service_closure.close_button.click()
            expected_info_text = f'Successfully closed: {self.product_name}'
        else:
            self.assertTrue(product.open_button.is_displayed(), msg='"OPEN button" is not displayed')
            product.open_button.click()
            expected_info_text = f'Successfully opened: {self.product_name}'
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, expected_info_text,
                         msg=f'Actual text: "{actual_info_text}" is not same as Expected text: "{expected_info_text}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Log in on user account that had Sports product closed, but reopened it manually
        PRECONDITIONS: 3. User has enough balance to place a bet
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_id = outcomes[0]['outcome']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = list(event.selection_ids.values())[0]

        username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=username, amount=tests.settings.min_deposit_amount,
                                  card_number=tests.settings.visa_card)
        self.site.login(username=username)
        self.product_open_reopen()
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.product_open_reopen(close=False)

    def test_001_make_a_selection(self):
        """
        DESCRIPTION: Make a selection
        """
        self.open_betslip_with_selections(self.selection_id)

    def test_002_enter_stake_within_the_available_balance(self):
        """
        DESCRIPTION: Enter stake (within the available balance)
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No Single bets found')
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))

    def test_003_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: Bet is successfully placed.
        """
        self.site.betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
