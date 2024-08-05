import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.reg167_fix
@pytest.mark.betslip
@vtest
class Test_C3233910_Betslip_counter_and_animation(BaseBetSlipTest, ComponentBase):
    """
    TR_ID: C3233910
    NAME: Betslip counter and animation
    DESCRIPTION: This test case verifies bestilp counter and animation during adding and removing selections from betslip.
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have no selections added to betslip
    """
    keep_browser_open = True

    def selections(self, start, selection):
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        for index in range(start, selection):
            selection_btn = bet_buttons_list[index]
            self.scroll_to_we(selection_btn)
            selection_btn.click()

    def test_001___tap_on_any_selection_and_add_to_betslip_via_quick_bet_window__verify_counter_updating_and_betslip_animation(self):
        """
        DESCRIPTION: - Tap on any selection and add to betslip via quick bet window
        DESCRIPTION: - Verify counter updating and betslip animation
        EXPECTED: Counter is updated to '1' in live and betslip animation is performed during adding
        """
        self.site.wait_content_state('Homepage')
        self.selections(0, 1)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_displayed(),
                        msg='"ADD TO BETSLIP" button is not displayed')
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False, timeout=15),
                         msg='Quick Bet is still opened')
        self.verify_betslip_counter_change(expected_value=1)

    def test_002___tap_on_any_another_selection__verify_counter_updating_and_betslip_animation(self):
        """
        DESCRIPTION: - Tap on any another selection
        DESCRIPTION: - Verify counter updating and betslip animation
        EXPECTED: Counter is updated to '2' in live and betslip animation is performed during adding
        """
        sleep(3)
        self.selections(1, 2)
        self.verify_betslip_counter_change(expected_value=2)

    def test_003___open_betslip_and_remove_one_of_the_selections__close_betslip_mobile_only__verify_counter_updating(self):
        """
        DESCRIPTION: - Open betslip and remove one of the selections
        DESCRIPTION: - Close betslip (Mobile only)
        DESCRIPTION: - Verify counter updating
        EXPECTED: Counter is updated to '1'
        EXPECTED: Counter is updated to '1' in live and betslip animation is performed during removing
        """
        self.site.open_betslip()
        self.site.close_all_dialogs()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.stake = list(singles_section.values())[0]
        self.stake.remove_button.click()
        self.site.close_betslip()
        self.site.wait_content_state('Homepage')
        self.verify_betslip_counter_change(expected_value=1)

    def test_004___tap_on_the_last_selection_added_to_betslip_to_deselect_it_to_remove_it_from_betslip__verify_counter_updating_and_betslip_animation(self):
        """
        DESCRIPTION: - Tap on the last selection added to betslip to deselect it (to remove it from betslip)
        DESCRIPTION: - Verify counter updating and betslip animation
        EXPECTED: Counter is updated to '0' in live and betslip animation is performed during removing
        """
        sleep(3)
        self.selections(1, 2)
        try:
            self.verify_betslip_counter_change(expected_value=0)
        except:
            self.assertFalse(self.site.has_betslip_notification(),msg='betslip notification is still reflected without any selection')
