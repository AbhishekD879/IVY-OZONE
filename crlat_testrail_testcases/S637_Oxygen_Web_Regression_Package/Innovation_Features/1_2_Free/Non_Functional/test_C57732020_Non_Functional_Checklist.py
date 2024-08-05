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
class Test_C57732020_Non_Functional_Checklist(Common):
    """
    TR_ID: C57732020
    NAME: Non-Functional Checklist
    DESCRIPTION: This checklist covers Non-Functional requirements of 1-2-Free Mobile and Web application
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    """
    keep_browser_open = True

    def test_001_usabilityitems_to_check__screen_modes___landscapeportrait__responsive_design__tapclick_events___should_be_obvious_that_element_was_selectedclickedtouchedchosen__double_taps_on_buttons_and_links__scroll_is_smooth_and_necessary__element_isnt_interfering_with_other_elementsfunctionalities__general_consistency_error_handling_dialogs_buttons_menus_icons__navigation_should_be_obvious_and_depends_on_specific_devices_navigation_bottom_bar_is_present_hide_swipe_navigation__localization(self):
        """
        DESCRIPTION: **Usability**
        DESCRIPTION: Items to check:
        DESCRIPTION: - Screen modes - landscape/portrait
        DESCRIPTION: - Responsive design
        DESCRIPTION: - Tap(click) events - should be obvious that element was selected/clicked/touched/chosen
        DESCRIPTION: - Double taps on buttons and links
        DESCRIPTION: - Scroll is smooth and necessary
        DESCRIPTION: - Element isn't interfering with other elements/functionalities
        DESCRIPTION: - General consistency: error handling, dialogs, buttons, menus, icons
        DESCRIPTION: - Navigation should be obvious and depends on specific devices: navigation bottom bar is present (hide), swipe navigation
        DESCRIPTION: - Localization
        EXPECTED: - Any Usability issues
        EXPECTED: - Error handling for different scenarios
        EXPECTED: - No content duplication
        """
        pass

    def test_002_recoveryitems_to_check__sleep_modes___lock_application_at_least_for_1_minute__background_mode___should_be_in_bg_more_than_1_minute_after_3_minutes_application_should_re_initialize__kill_application_and_reopen__in_come_callsmspush_notifications_using_app__turn_off_internet_on_different_pages_of_app__switch_3gwi_fi_on_different_pages_of_app(self):
        """
        DESCRIPTION: **Recovery**
        DESCRIPTION: Items to check:
        DESCRIPTION: - Sleep modes - Lock application at least for 1 minute
        DESCRIPTION: - Background mode - should be in bg more than 1 minute, after 3 minutes application should re-initialize
        DESCRIPTION: - Kill application and reopen
        DESCRIPTION: - In-come call/SMS/Push-notifications using app
        DESCRIPTION: - Turn off Internet on different pages of app
        DESCRIPTION: - Switch 3g/Wi-Fi on different pages of app
        EXPECTED: - Any Recovery issues
        EXPECTED: - No data lost
        EXPECTED: - User returned to previously opened page
        """
        pass

    def test_003_reliabilityitems_to_check__cache_on_call_to_you_ms_ms_handling_the_same_calls_few_times__how_siteapp_respond_when_few_applications_is_working_in_bg_with_your__incorrect_data_entered__handling_of_max_amount_of_data(self):
        """
        DESCRIPTION: **Reliability**
        DESCRIPTION: Items to check:
        DESCRIPTION: - Cache on call to you MS, MS handling the same calls few times
        DESCRIPTION: - How site/app respond when few applications is working in bg with your
        DESCRIPTION: - Incorrect data entered
        DESCRIPTION: - Handling of max amount of data
        EXPECTED: - Any Reliability issues
        EXPECTED: - No ability to enter incorrect data
        """
        pass

    def test_004_accessibilityitems_to_check__location_restriction_gps(self):
        """
        DESCRIPTION: **Accessibility**
        DESCRIPTION: Items to check:
        DESCRIPTION: - Location restriction (GPS)
        EXPECTED: Access only from UK location
        """
        pass

    def test_005_securityitems_to_check__open_app_using_authorized_usernon_authorized_user(self):
        """
        DESCRIPTION: **Security**
        DESCRIPTION: Items to check:
        DESCRIPTION: - Open app using authorized user/non-authorized user
        EXPECTED: Access to app should be provided only for authorized users
        """
        pass

    def test_006_perfomanceitems_to_check__app_load_time___check_app_on_slow_3g__pages_load_time___check_app_on_slow_3g(self):
        """
        DESCRIPTION: **Perfomance**
        DESCRIPTION: Items to check:
        DESCRIPTION: - App load time - check app on slow 3g
        DESCRIPTION: - Pages Load time - check app on slow 3g
        EXPECTED: Any issues during surfing using Slow 3G
        """
        pass
