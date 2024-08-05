import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C34375889_Set_Game_Play_Reminder(Common):
    """
    TR_ID: C34375889
    NAME: Set Game Play Reminder
    DESCRIPTION: This test case verifies confirming of Game Play Reminder Frequency
    PRECONDITIONS: Application is opened
    PRECONDITIONS: User is successfully logged in
    """
    keep_browser_open = True

    def test_001_open_my_account_menu__select_gambling_controls(self):
        """
        DESCRIPTION: Open 'My Account' menu > Select 'Gambling Controls'
        EXPECTED: 'Gambling Controls' page is opened
        """
        pass

    def test_002_selecttime_management_option(self):
        """
        DESCRIPTION: Select 'Time Management' option
        EXPECTED: *   'Time Management' option is selected
        EXPECTED: *   Description is changed to:
        EXPECTED: - Control how long you spend gaming and get notified once your time limit is reached
        EXPECTED: - You can change your settings at any time
        """
        pass

    def test_003_click_choose_button(self):
        """
        DESCRIPTION: Click 'CHOOSE' button
        EXPECTED: 'Time Management' page is opened with following controls:
        EXPECTED: *   'Time limit' drop-down with options to select: 15 minutes, 30 minutes, 45 minutes, 60 minutes
        EXPECTED: (Default or previously set value is selected in the drop-down)
        EXPECTED: *   'Save' button
        """
        pass

    def test_004_change_the_selected_value_in_the_drop_down(self):
        """
        DESCRIPTION: Change the selected value in the drop-down
        EXPECTED: *   New value is shown in the drop-down
        """
        pass

    def test_005_tap_save_button(self):
        """
        DESCRIPTION: Tap 'Save' button
        EXPECTED: Success message appears:
        EXPECTED: * 'Your time management settings have been successfully saved.'
        """
        pass

    def test_006_refresh_time_management_page(self):
        """
        DESCRIPTION: Refresh 'Time Management' page
        EXPECTED: *   Success message is not displayed
        EXPECTED: *   New value is set and shown in the drop-down
        """
        pass
