import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732048_Verify_toggles_configurations_for_QE(Common):
    """
    TR_ID: C57732048
    NAME: Verify toggles configurations for QE
    DESCRIPTION: This test case verifies toggles configurations for QE
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_001___open_cms__switch_to_coral_brandconfigure_toggles_in_this_wayshow_submit_pop_up__on__displayedshow_exit_pop_up__on__displayedshow_splash_page___on___displayedshow_event_details__on__displayedshow_progress_bar___on__displayedshow_question_numbering___on__displayedshow_swipe_tutorial___on__displayedshow_use_back_button_to_exit_quiz__hide_close_button___offshow_history_page___on___displayed__save_changes(self):
        """
        DESCRIPTION: - Open CMS
        DESCRIPTION: - Switch to 'Coral' brand
        DESCRIPTION: Configure toggles in this way:
        DESCRIPTION: Show submit Pop-up- ON / DISPLAYED
        DESCRIPTION: Show Exit Pop-up- ON / DISPLAYED
        DESCRIPTION: Show Splash Page - ON  / DISPLAYED
        DESCRIPTION: Show Event Details -ON / DISPLAYED
        DESCRIPTION: Show Progress Bar - ON / DISPLAYED
        DESCRIPTION: Show Question Numbering - ON / DISPLAYED
        DESCRIPTION: Show swipe tutorial - ON / DISPLAYED
        DESCRIPTION: Show Use back button to exit Quiz & Hide close button - OFF
        DESCRIPTION: Show History page - ON  / DISPLAYED
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_002_log_in_and_open_coral_fe_environment_to_run_correct_4(self):
        """
        DESCRIPTION: Log in and open Coral FE environment to run Correct 4
        EXPECTED: - All data retrieved from CMS and successfully styled for Correct 4
        EXPECTED: - 'Back' button will navigate to previous page
        EXPECTED: - 'Close' button will close the quiz
        """
        pass

    def test_003___open_cms__switch_to_ladbrokes_brandconfigure_toggles_in_this_wayshow_submit_pop_up__off__dont_displayshow_exit_pop_up__off__dont_displayshow_splash_page___off__dont_displayshow_event_details__off__dont_displayshow_progress_bar___off__dont_displayshow_question_numbering___on__displayshow_swipe_tutorial___off_dont_displayshow_use_back_button_to_exit_quiz__hide_close_button___onshow_history_page___off_dont_display__save_changes(self):
        """
        DESCRIPTION: - Open CMS
        DESCRIPTION: - Switch to 'Ladbrokes' brand
        DESCRIPTION: Configure toggles in this way:
        DESCRIPTION: Show submit Pop-up- OFF / DON'T DISPLAY
        DESCRIPTION: Show Exit Pop-up- OFF / DON'T DISPLAY
        DESCRIPTION: Show Splash Page - OFF / DON'T DISPLAY
        DESCRIPTION: Show Event Details -OFF / DON'T DISPLAY
        DESCRIPTION: Show Progress Bar - OFF / DON'T DISPLAY
        DESCRIPTION: Show Question Numbering - ON / DISPLAY
        DESCRIPTION: Show swipe tutorial - OFF/ DON'T DISPLAY
        DESCRIPTION: Show Use back button to exit Quiz & Hide close button - ON
        DESCRIPTION: Show History page - OFF/ DON'T DISPLAY
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_004_log_in_and_open_coral_fe_environment_to_run_cash_for_questions(self):
        """
        DESCRIPTION: Log in and open Coral FE environment to run Cash For Questions
        EXPECTED: - All data retrieved from CMS and successfully styled for Cash For Questions
        EXPECTED: - 'Close' button (X) is not show.
        EXPECTED: - 'Back' button is shown and exit's quiz when selected
        """
        pass

    def test_005_try_different_combinations_of_toggles_for_each_brand_to_verify_if_no_critical_ui_issues_appear(self):
        """
        DESCRIPTION: Try different combinations of toggles for each brand to verify if no critical UI issues appear
        EXPECTED: 
        """
        pass
