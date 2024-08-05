import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


# @pytest.mark.lad_tst2 TODO adapt for vanilla once story related to BMA-48323 will be completed
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-48323')
@pytest.mark.login
@vtest
class Test_C402585_Quick_Deposit_link_open_Section_User_with_Credit_Cards(BaseBetSlipTest):
    """
    TR_ID: C402585
    NAME: 'Quick Deposit' link open Section User with Credit Cards
    DESCRIPTION: This test case verifies whether Quick Deposit section is opened through 'Quick Deposit' link in the Betslip header if user has registered credit cards
    PRECONDITIONS: User account with added credit cards and positive balance
    PRECONDITIONS: Applies for Mobile
    """
    # TODO adapt for vanilla once story related to BMA-48323 will be completed
    keep_browser_open = True
    add_deposit = 5.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self._logger.debug(f'*** Found Horse racing event with selection ids:"{self.selection_ids}"')
        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: - Homepage is opened
        """
        # Done in next step

    def test_002_log_in_user_account__from_preconditions(self):
        """
        DESCRIPTION: Log in User account ( from Preconditions)
        EXPECTED: - User is logged in
        """
        self.site.login(username=tests.settings.quick_deposit_user)

    def test_003_add_a_selection_to_the_betslip___open_betslip_page(self):
        """
        DESCRIPTION: Add a selection to the Betslip -> Open Betslip page
        EXPECTED: - Selection is displayed within Betslip content area
        EXPECTED: - 'QUICK DEPOSIT' section is not opened
        """
        self.open_betslip_with_selections(selection_ids=(list(self.selection_ids.values())[0]))
        has_deposit_form = self.get_betslip_content().has_deposit_form(expected_result=False)
        self.assertFalse(has_deposit_form, msg='There\'s Quick deposit form!')

    def test_004_tap_account_balance_area_in_the_betslip_header__deposit_button(self):
        """
        DESCRIPTION: **(Archived from OX99)** Tap on 'Quick Deposit' link in header
        DESCRIPTION: **(Applicable from OX99)** Tap 'Account Balance' area in the Betslip header > Deposit button
        EXPECTED: - Betslip is opened
        EXPECTED: - Selection is displayed within Betslip content area
        EXPECTED: - 'QUICK DEPOSIT' section is opened
        """
        self.get_betslip_content().quick_deposit_link.click()
        has_deposit_form = self.get_betslip_content().has_deposit_form()
        self.assertTrue(has_deposit_form, msg='There\'s no Quick deposit form')

    def test_005_enter_any_amount_in_quick_deposit_section(self):
        """
        DESCRIPTION: Enter any 'Amount *' in 'QUICK DEPOSIT' section
        EXPECTED: - 'Amount *' field is populated with entered value
        """
        self.get_betslip_content().quick_deposit.amount_form.input.click()
        self.enter_value_using_keyboard(value=self.add_deposit)
        deposit_amount = float(self.get_betslip_content().quick_deposit.amount_form.input.value)
        self.assertEqual(deposit_amount, self.add_deposit,
                         msg=f'Expected amount is "{deposit_amount}", but found "{self.add_deposit}"')

    def test_006_tap_account_balance_area_in_the_betslip_header___deposit_button_againx_icon_in_quick_deposit_section(self):
        """
        DESCRIPTION: **(Archived from OX99)** Tap on 'Quick Deposit' link again/'X' icon in 'QUICK DEPOSIT' section
        DESCRIPTION: **(Applicable from OX99)** Tap 'Account Balance' area in the Betslip header  > Deposit button again/'X' icon in 'QUICK DEPOSIT' section
        EXPECTED: - 'QUICK DEPOSIT' section disappears
        """
        self.get_betslip_content().quick_deposit_link.click()
        has_deposit_form = self.get_betslip_content().has_deposit_form(expected_result=False)
        self.assertFalse(has_deposit_form, msg='There\'s Quick deposit form!')

    def test_007_enter_stake_amount_that_is_covered_by_users_balance(self):
        """
        DESCRIPTION: Enter Stake amount that is covered by user's balance
        EXPECTED: - 'QUICK DEPOSIT' section is not opened
        """
        user_balance = self.site.header.user_balance
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self._logger.info(f'*** Verifying stake {stake_name}')
        stake.amount_form.input.click()
        self.enter_value_using_keyboard(value=user_balance)
        has_deposit_form = self.get_betslip_content().has_deposit_form(expected_result=False)
        self.assertFalse(has_deposit_form, msg='There\'s Quick deposit form!')

    def test_008_tap_on_quick_deposit_link(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' link
        EXPECTED: - 'QUICK DEPOSIT' section appears
        EXPECTED: - 'Amount *' field shows default value: "<currency symbol>5/50 (for user with default currency Kr) Min"
        """
        self.get_betslip_content().quick_deposit_link.click()
        amount_placeholder = self.get_betslip_content().quick_deposit.amount_form.default_value
        expected_amount_placeholder = '£5 Min'
        self.assertEqual(amount_placeholder, expected_amount_placeholder,
                         msg=f'Amount placeholder "{amount_placeholder}" is not the same as expected '
                             f'placeholder "{expected_amount_placeholder}"')

    def test_009_close_the_betslip_page_x(self):
        """
        DESCRIPTION: Close the Betslip page ('X')
        EXPECTED: - Betslip is closed
        """
        self.site.close_betslip()

    def test_010_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: - Selection is displayed within Betslip
        EXPECTED: - 'QUICK DEPOSIT' section is not opened
        """
        self.site.open_betslip()
        has_deposit_form = self.get_betslip_content().has_deposit_form(expected_result=False)
        self.assertFalse(has_deposit_form, msg='There\'s Quick deposit form!')
