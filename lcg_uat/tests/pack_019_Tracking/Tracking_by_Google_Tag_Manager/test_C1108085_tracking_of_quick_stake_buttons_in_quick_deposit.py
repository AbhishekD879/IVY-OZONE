import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
# import pytest


# this functionality was implemented but currently it's turned off,
# test should be rechecked after it back
# @pytest.mark.crl_prod
# @pytest.mark.crl_tst2
# @pytest.mark.crl_stg2
# @pytest.mark.numeric_keyboard
# @pytest.mark.quick_deposit
# @pytest.mark.google_analytics
# @pytest.mark.mobile_only
# @pytest.mark.quarantine
# @pytest.mark.other
# @pytest.mark.login
@vtest
class Test_C1108085_Verifies_Quick_Stake_Buttons_Tracking(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C1108085
    VOL_ID: C1108088
    NAME: This test case verifies Quick Stake buttons tracking in Betslip for 'Amount' field ('Quick Deposit' section)
    """
    keep_browser_open = True
    selection_id = None
    device_name = 'Nexus 5X' if not tests.use_browser_stack else tests.default_pixel

    def test_001_create_event(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        team1, selection_ids = event_params.team1, event_params.selection_ids
        self.__class__.selection_id = selection_ids[team1]

    def test_002_login_to_oxygen_application(self):
        """
        DESCRIPTION: Log in with account with positive balance
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_003_add_selection_with_deep_link(self):
        """
        DESCRIPTION: Add selection with deep link
        """
        self.open_betslip_with_selections(self.selection_id)

    def test_004_tap_on_quick_deposit_link_in_betslip_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' link in the Betslip header
        EXPECTED: 'Quick Deposit' section is opened
        """
        self.get_betslip_content().quick_deposit_link.click()
        has_deposit_form = self.get_betslip_content().has_deposit_form()
        self.assertTrue(has_deposit_form, msg='There\'s no Quick deposit form')

    def test_005_tap_on_amount_field(self):
        """
        DESCRIPTION: Tap on 'Amount' field
        EXPECTED: Numeric keyboard with 'Quick Deposit' buttons is opened
        """
        self.get_betslip_content().quick_deposit.amount_form.input.click()

        quick_stake_panel = self.get_betslip_content().betnow_section.quick_stake_panel
        self.assertTrue(quick_stake_panel.is_displayed(), msg='Numeric keyboard for "Quick Deposit" is not opened')
        self.__class__.quick_deposit_buttons = quick_stake_panel.items_as_ordered_dict
        self.assertTrue(self.quick_deposit_buttons, msg='"Quick Stake" buttons are not displayed')

    def test_006_tap_on_any_quick_deposit_button(self):
        """
        DESCRIPTION: Tap on any 'Quick Deposit' button (e.g. +<currency symbol>5, 10, 50, 100/+kr50, 100, 500, 1000)
        EXPECTED: Quick Deposit amount is shown in 'Amount' field
        """
        button_name, button = list(self.quick_deposit_buttons.items())[1]
        self.quick_deposit_buttons.currencies.append('+')
        self.__class__.deposit_amount = self.quick_deposit_buttons.strip_currency_sign(button_name)
        button.click()

        deposit_value = self.get_betslip_content().quick_deposit.amount_form.input.value
        self.assertEqual(deposit_value, self.deposit_amount,
                         msg='Current deposit value: "%s" does not match with expected: "%s"'
                             % (deposit_value, self.deposit_amount))

    def test_007_verify_quick_deposit_data_layer_object(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' datalayer response added as expected
        EXPECTED: The following object with corresponding parameters is present in data layer:
            dataLayer.push({
                'event' : 'trackEvent',
                'eventCategory' : 'betslip',
                'eventAction' : 'quick deposit',
                'eventLabel' : '<< SELECTED AMOUNT >>'})
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='quick deposit')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'betslip',
                             'eventAction': 'quick deposit',
                             'eventLabel': self.deposit_amount}
        self.compare_json_response(actual_response, expected_response)
