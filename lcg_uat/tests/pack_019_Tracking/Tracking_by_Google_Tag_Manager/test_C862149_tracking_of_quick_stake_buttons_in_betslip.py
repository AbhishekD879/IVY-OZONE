import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only (Quick Stakes are not available in ladbrokes)
@pytest.mark.crl_stg2
@pytest.mark.numeric_keyboard
@pytest.mark.google_analytics
@pytest.mark.quick_stake
@pytest.mark.mobile_only
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C862149_Verifies_Quick_Stake_Buttons_Tracking(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C862149
    VOL_ID: C9698056
    NAME: This test case verifies Quick Stake buttons tracking in Betslip for 'Stake' field
    """
    keep_browser_open = True
    selection_id = None
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

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

    def test_004_set_cursor_over_any_stake_field(self):
        """
        DESCRIPTION: Set cursor over any 'Stake' field
        EXPECTED: Numeric keyboard with 'Quick Stake' buttons is opened
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(self.zip_available_stakes(section=singles_section).items())[0]
        self.stake.mouse_over()

        quick_stake_panel = self.get_betslip_content().betnow_section.quick_stake_panel
        self.assertTrue(quick_stake_panel.is_displayed(), msg='Numeric keyboard for "Quick Stake" is not opened')
        self.__class__.quick_stake_buttons = quick_stake_panel.items_as_ordered_dict
        self.assertTrue(self.quick_stake_buttons, msg='"Quick Stake" buttons are not displayed')

    def test_005_tap_on_any_quick_stake_button(self):
        """
        DESCRIPTION: Tap on any 'Quick Stake' button (e.g. +<currency symbol>5, 10, 50, 100/+kr50, 100, 500, 1000)
        EXPECTED: Quick Stake amount is shown in a corresponding 'Stake' field
        """
        button_name, button = list(self.quick_stake_buttons.items())[0]
        self.stake.currencies.append('+')
        self.__class__.stake_amount = self.stake.strip_currency_sign(button_name)
        button.click()

        stake_value = self.stake.amount_form.input.value
        self.assertEqual(stake_value, self.stake_amount,
                         msg='Current stake value: "%s" does not match with expected: "%s"'
                             % (stake_value, self.stake_amount))

    def test_006_check_data_layer_object(self):
        """
        DESCRIPTION: Verify 'Quick Stake' datalayer response added as expected
        EXPECTED: The following object with corresponding parameters is present in data layer:
            dataLayer.push({
                'event' : 'trackEvent',
                'eventCategory' : 'betslip',
                'eventAction' : 'quick stake',
                'eventLabel' : '<< SELECTED AMOUNT >>'})
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='quick stake')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'betslip',
                             'eventAction': 'quick stake',
                             'eventLabel': self.stake_amount}
        self.compare_json_response(actual_response, expected_response)
