import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C16627550_Vanilla_User_Balance_is_Too_Low_for_Placing_a_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C16627550
    NAME: [Vanilla] User Balance is Too Low for Placing a Single Bet
    DESCRIPTION: This test case verifies bet slip error handling in case when user balance is too low.
    PRECONDITIONS: 1. The user account is NOT sufficient to cover any stake
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> sport it is possible to place a bet from:
    PRECONDITIONS: - 'Next races' module
    PRECONDITIONS: - event landing page
    PRECONDITIONS: NOTE: in order to check Max Allowed Bet enter extremely large stake value in 'Stake' field and tap 'Bet Now' button to see what is Max allowed bet for selection.
    """
    keep_browser_open = True
    additional_amount = 5

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.quick_deposit_user)
        self.site.wait_content_state('homepage')
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = (event_params.selection_ids[event_params.team1])
        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        number_of_events=1)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(selection_ids.values())[0]

        self.open_betslip_with_selections(selection_ids=selection_id)

    def test_003_go_to_betslip_and_enter_a_stake_which_will_not_exceed_users_balance_and_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Go to 'Betslip' and enter a stake which will not exceed user's balance and won't exceed a max bet allowed
        EXPECTED: 'PLACE BET' button is available
        """
        section = self.get_betslip_sections().Singles
        stake_name, stake = list(section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.assertGreater(str(self.user_balance), stake.amount_form.input.value,
                           msg=f'User Balance  "{str(self.user_balance)}" is not greater than stake "{stake.amount_form.input.value}"')
        betnow_btn = self.get_betslip_content().bet_now_button
        self.assertTrue(betnow_btn.is_enabled(expected_result=True), msg='Bet Now button is disabled')

    def test_004_enter_a_stake_which_will_exceed_users_balance_but_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Enter a stake which will exceed user's balance but won't exceed a max bet allowed
        EXPECTED: * 'PLACE BET' button is not available
        EXPECTED: * 'MAKE A DEPOSIT' button is available
        """
        stake_value = self.user_balance + self.additional_amount
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
        info_panel_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        self.assertEqual(info_panel_text, expected_message_text,
                         msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')
        self.assertTrue(self.get_betslip_content().has_make_quick_deposit_button(timeout=20),
                        msg='"Make a Quick Deposit" button is not displayed')
        make_quick_deposit_button_name = self.get_betslip_content().make_quick_deposit_button.name
        self.assertEqual(make_quick_deposit_button_name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual message "{make_quick_deposit_button_name}" != '
                             f'Expected "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.assertTrue(self.get_betslip_content().make_quick_deposit_button.is_enabled(),
                        msg=f'"{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}" button is disabled')

    def test_005_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT'
        EXPECTED: 'Quick Deposit' module is displayed in Betslip
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')
