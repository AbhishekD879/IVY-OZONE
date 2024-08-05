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
class Test_C44870379_Verify_that_functionality_and_display_of_Responsible_Gambling_button_navigation_to_Responsible_Gambling_page_and_when_click_on_back_button_navigate_back_to_sportsbook_application(Common):
    """
    TR_ID: C44870379
    NAME: Verify that functionality and display of Responsible Gambling button, navigation to Responsible Gambling page and when click on "back"  button navigate back to sportsbook application
    DESCRIPTION: Verify that functionality and display of Responsible Gambling button, navigation to Responsible Gambling page and when click on 'X' button navigate back to sportsbook application
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded.
        """
        pass

    def test_002_clicktap_my_account_button_avatar(self):
        """
        DESCRIPTION: Click/tap My Account button (Avatar)
        EXPECTED: For Mobile: Menu overlay is displayed with list of items
        EXPECTED: For Desktop: Right menu is displayed with list of items
        """
        pass

    def test_003_clicktap_gambling_control_option(self):
        """
        DESCRIPTION: Click/tap "Gambling control" option
        EXPECTED: User is taken to "Gambling control" page with options of
        EXPECTED: Deposit limits/Time management/Account closure & reopening~
        EXPECTED: along with "Responsible gambling" link just below the CHOOSE tab.
        """
        pass

    def test_004_click_on_the_responsible_gambling_linkor_click_on_the_responsible_gambling_link_from_the_footer_menu_under_help__information(self):
        """
        DESCRIPTION: Click on the "Responsible gambling" link
        DESCRIPTION: OR Click on the "Responsible gambling link" from the footer menu under "HELP & INFORMATION"
        EXPECTED: User is navigated to "RESPONSIBLE GAMBLING" page
        EXPECTED: for desktop > https://help.coral.co.uk/en/general-information/responsible-gaming
        """
        pass

    def test_005_verify_the_user_is_navigated_to_the_correct_pages_when_clicked_on_all_the_options_available_under_responsible_gambling_page(self):
        """
        DESCRIPTION: Verify the user is navigated to the correct pages when clicked on all the options available under "Responsible gambling" page
        EXPECTED: The user is navigated to the respective pages when clicked on all the options available under "Responsible gambling" page
        """
        pass

    def test_006_verify_the_user_is_able_to_navigate_back_to_the_sports_page_when_clicked_back(self):
        """
        DESCRIPTION: Verify the user is able to navigate back to the sports page when clicked "back"
        EXPECTED: The user is navigated to the sports page.
        """
        pass
