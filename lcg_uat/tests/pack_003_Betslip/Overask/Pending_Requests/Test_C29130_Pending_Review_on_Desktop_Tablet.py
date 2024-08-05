import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest

@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not create events in Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C29130_Pending_Review_on_Desktop_Tablet(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29130
    NAME: Pending Review on Desktop/Tablet
    DESCRIPTION:
    PRECONDITIONS: 1. User is logged in to apllication on tablet/desktop
    PRECONDITIONS: 2. Overask functionality is enabled for the user
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    max_bet = 20
    selection_ids_list = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events with bet limit
        DESCRIPTION: - User is logged in to application
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=self.max_bet)
        self.__class__.selection_ids = event_params.selection_ids
        self.selection_ids_list.append(list(self.selection_ids.values())[0])
        self.site.login()

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.site.close_all_dialogs(timeout=3)

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        EXPECTED:
        """
        section = self.get_betslip_sections().Singles
        stake_name1, stake = list(section.items())[0]
        stake_bet_amount = {stake_name1: self.max_bet + 2}
        self.enter_stake_amount(stake=(stake_name1, stake), stake_bet_amounts=stake_bet_amount)

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED:    Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute message is displayed on yellow background anchored to the footer
        EXPECTED:    Loading spinner is shown on the green button, replacing 'Bet Now' label
        EXPECTED:    'Clear Betslip' and 'Bet Now' buttons become disabled
        EXPECTED:    'Stake' field becomes disabled
        EXPECTED:   From OX 99
        EXPECTED:    CMS configurable title topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer
        EXPECTED:    Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED:  Background is disabled and not clickable
        """
        self.get_betslip_content().bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=30)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')
        self.site.wait_content_state_changed(timeout=15)

    def test_004_while_review_is_pending_tap_disabled_clear_betslip_button(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Clear Betslip' button
        EXPECTED: Nothing happens, it is impossible to clear betslip
        """
        # Can not be automate

    def test_005_while_review_is_pending_tap_disabled_bet_now_button(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Bet Now' button
        EXPECTED: Nothing happens, it is impossible to place a Bet
        """
        # Can not be automate

    def test_006_while_review_is_pending_tap_disabled_stake_field(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Stake' field
        EXPECTED: Nothing happens, it is impossible to modify entered Stake
        """
        # Can not be automate

    def test_007_while_review_is_pending_go_to_another_pages_and_try_to_add_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: While review is pending go to another pages and try to add more selections to the Betslip
        EXPECTED: *   Selection is not added to the Betslip
        EXPECTED: *   Notification pop-up is shown to the User
        """
        url = f'https://{tests.HOSTNAME}/betslip/add/{list(self.selection_ids.values())[0]}'
        self.device.navigate_to(url=url)

    def test_008_verify_notification_pop_up_elements(self):
        """
        DESCRIPTION: Verify notification pop-up elements
        EXPECTED: It consists of:
        EXPECTED:  Title: Betslip is busy
        EXPECTED:  Body: Please wait until the betslip is finished processing your bets before adding more selections. Thanks
        EXPECTED:  'Close' button
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_BETSLIP_IS_BUSY, timeout=35)
        self.assertEquals(dialog.text, vec.betslip.OVERASK_ELEMENTS.in_progress_notification,
                          msg=f'Actual response keys: "{dialog.text}" is not same as'
                              f'Expected response keys: "{vec.betslip.OVERASK_ELEMENTS.in_progress_notification}"')
        self.assertEquals(dialog.description, vec.betslip.OVERASK_ELEMENTS.in_progress_notification_message,
                          msg=f'Actual response keys: "{dialog.description}" is not same as'
                              f'Expected response keys: "{vec.betslip.OVERASK_ELEMENTS.in_progress_notification_message}"')
        self.assertTrue(dialog.continue_button.is_displayed(), msg='Continue button not displayed')
        dialog.continue_button.click()
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'Failed to close {vec.betslip.OVERASK_ELEMENTS.in_progress_notification,} dialog')

    def test_009_try_to_cancel_review_process(self):
        """
        DESCRIPTION: Try to cancel review process
        EXPECTED: User cannot cancel review process himself
        """
        # Can Not be automated as user can not cancel the review process himself
