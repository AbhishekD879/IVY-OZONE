import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C16291762_To_edit_Vanilla_Change_session_limit_during_session(Common):
    """
    TR_ID: C16291762
    NAME: [To edit] [Vanilla] Change session limit during session
    DESCRIPTION: This test case verifies Sessions Limit (Time management).
    PRECONDITIONS: 1. Load the app.
    PRECONDITIONS: 2. Login under user without session limits set.
    PRECONDITIONS: 3. Not applicable for bet placement - Sportsbook.
    PRECONDITIONS: * Time management section doesn't appear on accounts that are not UKGC players - it has to be a verified UK user
    """
    keep_browser_open = True

    def test_001_open_my_account_menuindexphpattachmentsget33800(self):
        """
        DESCRIPTION: Open "My Account" menu
        DESCRIPTION: ![](index.php?/attachments/get/33800)
        EXPECTED: 1. "My Account" menu appears over the blue overlay.
        EXPECTED: ![](index.php?/attachments/get/33799)
        """
        pass

    def test_002_select_settings_option(self):
        """
        DESCRIPTION: Select "Settings" option
        EXPECTED: 1. "Settings" sub-menu appears.
        EXPECTED: ![](index.php?/attachments/get/33801)
        """
        pass

    def test_003_select_gambling_controls_option(self):
        """
        DESCRIPTION: Select "Gambling Controls" option
        EXPECTED: 1. Gambling Controls panel appears.
        EXPECTED: ![](index.php?/attachments/get/33802)
        """
        pass

    def test_004_select_time_management_option(self):
        """
        DESCRIPTION: Select "Time Management" option
        EXPECTED: 1. "Time Management" option gets selected.
        EXPECTED: 2. Text under the options changes to the one appropriate for "Time management".
        EXPECTED: ![](index.php?/attachments/get/33803)
        """
        pass

    def test_005_click_the_green_choose_button(self):
        """
        DESCRIPTION: Click the green [CHOOSE] button
        EXPECTED: 1. "Time Management" view opens.
        EXPECTED: 2. "No time limit" should be selected by default.
        EXPECTED: ![](index.php?/attachments/get/33814)
        """
        pass

    def test_006_select_one_of_the_options_eg_15_minutesindexphpattachmentsget33830(self):
        """
        DESCRIPTION: Select one of the options (e.g. 15 minutes)
        DESCRIPTION: ![](index.php?/attachments/get/33830)
        EXPECTED: 1. Option gets selected and appears in the field.
        """
        pass

    def test_007_click_the_green_save_button(self):
        """
        DESCRIPTION: Click the green [SAVE] button
        EXPECTED: 1. Success message appears under the "Time management" header:
        EXPECTED: "Your time management settings have been successfully saved."
        EXPECTED: ![](index.php?/attachments/get/33831)
        """
        pass

    def test_008_navigate_back_to_the_app_and_play_a_game_for_x_minutes_time_selected_in_step_6(self):
        """
        DESCRIPTION: Navigate back to the app and play a game for X minutes (time selected in step 6)
        EXPECTED: 1. User should be notified that the time has ended while playing game (not applicable for bet placement - Sportsbook)
        EXPECTED: 2. User has option to keep playing or close the game.
        """
        pass
