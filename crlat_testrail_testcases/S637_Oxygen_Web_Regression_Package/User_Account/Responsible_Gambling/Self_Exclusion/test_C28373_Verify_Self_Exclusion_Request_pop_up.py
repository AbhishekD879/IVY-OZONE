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
class Test_C28373_Verify_Self_Exclusion_Request_pop_up(Common):
    """
    TR_ID: C28373
    NAME: Verify 'Self Exclusion Request' pop-up
    DESCRIPTION: This test case verifies 'Self Exclude' form
    DESCRIPTION: Jira tickets:
    DESCRIPTION: *   **BMA-3952 **LCCP Auto Self-Exclude Requirement
    DESCRIPTION: *   BMA-9931 Change self exclude green button to a text link as per old mobenga design
    PRECONDITIONS: * User is logged in to Oxygen app
    PRECONDITIONS: * Content for CMS configurable part of 'Self Exclusion Request' popup is added in CMS -> Admin -> Static blocks -> 'Self Exclusion Request EN'
    PRECONDITIONS: * Content for CMS configurable part of confirmation popup is added in CMS -> Admin -> Static blocks -> 'Self Exclusion Logged Out EN'
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu Icon
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_003_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_004_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap 'Responsible Gambling'
        EXPECTED: The 'Responsible Gambling' page is opened
        """
        pass

    def test_005_tap_read_more_about_self_exclusion_button(self):
        """
        DESCRIPTION: Tap 'Read More About Self Exclusion' button
        EXPECTED: The 'Self Exclusion' page is opened
        """
        pass

    def test_006_tap_request_self_exclusion_link(self):
        """
        DESCRIPTION: Tap 'Request Self Exclusion' link
        EXPECTED: The 'Self Exclusion Request' pop-up is shown immediately
        """
        pass

    def test_007_verify_self_exclusion_request_pop_up(self):
        """
        DESCRIPTION: Verify 'Self Exclusion Request' pop-up
        EXPECTED: The 'Self Exclusion Request' pop-up consists of the next elements:
        EXPECTED: *   The 'Self Exclusion Request' header and the 'X'  icon
        EXPECTED: *   The CMS-controlled content (text with image) is displayed
        EXPECTED: *  Drop down menu with Self-Exclusion period ("Choose Self Exclusion Period" is selected by default) Drop down include the following options:
        EXPECTED: - 6 Months
        EXPECTED: - 1 Year
        EXPECTED: - 2 Years
        EXPECTED: - 3 Years
        EXPECTED: - 4 Years
        EXPECTED: - 5 Years
        EXPECTED: *   Link 'Click here' with text 'to Confirm that you wish to Self Exclude'
        EXPECTED: * The CMS-controlled content (text with red warning icon) is displayed below 'Click here' link
        EXPECTED: * 'see here' link is displayed within CMS-controlled static block
        """
        pass

    def test_008_verify_see_here_link(self):
        """
        DESCRIPTION: Verify 'see here' link
        EXPECTED: User is navigated to https://gvc-plc.com/about/business-overview/our-brands/ website after clicking the link
        """
        pass

    def test_009_verify_the_x_icon(self):
        """
        DESCRIPTION: Verify the 'X' icon
        EXPECTED: *   The 'Self Exclusion Request' pop-up disappears after tapping the icon
        EXPECTED: *   The page where user stayed is shown
        """
        pass

    def test_010_verify_the_click_here_link(self):
        """
        DESCRIPTION: Verify the  'Click here' link
        EXPECTED: * 'Click here' link is disabled by default
        """
        pass

    def test_011_select_some_period_from_choose_self_exclusion_period_dropdown(self):
        """
        DESCRIPTION: Select some period from 'Choose Self Exclusion Period' dropdown
        EXPECTED: Text "In order to complete self-exclusion, please provide your password:" and "Password" field (with Type Password placeholder) becomes available
        """
        pass

    def test_012_enter_a_invalid_password_into_password_field_and_tap_click_here_to_confirm_that_you_wish_to_self_exclude_link(self):
        """
        DESCRIPTION: Enter a invalid password into "Password" field and tap 'CLICK HERE to confirm that you wish to Self-Exclude' link
        EXPECTED: * Error message "Your password is invalid.Please try again" is displayed under "Password" field (field is highlighted with red color)
        EXPECTED: * User is not logged out and user account is not frozen
        """
        pass

    def test_013_enter_a_valid_password_for_user_account_and_click__click_here_to_confirm_that_you_wish_to_self_exclude_link(self):
        """
        DESCRIPTION: Enter a valid password for user account and click   'CLICK HERE to Confirm that you wish to Self Exclude' link
        EXPECTED: *   Confirmation pop-up "Account Self-Excluded"  is shown after user enter password and tap the link
        """
        pass
