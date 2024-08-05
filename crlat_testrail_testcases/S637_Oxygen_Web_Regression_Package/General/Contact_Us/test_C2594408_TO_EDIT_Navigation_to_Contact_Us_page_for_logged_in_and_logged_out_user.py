import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2594408_TO_EDIT_Navigation_to_Contact_Us_page_for_logged_in_and_logged_out_user(Common):
    """
    TR_ID: C2594408
    NAME: [TO EDIT] Navigation to 'Contact Us' page for logged in and logged out user
    DESCRIPTION: This test case verifies navigation to 'Contact Us' page for logged in and logged out user
    DESCRIPTION: **NOTE[TO EDIT]: ui is changed, and we don't have possibility to understand the users status(logged in or not)**
    PRECONDITIONS: * Make sure that 'Contact Us' item is created in CMS, please see the following instruction:
    PRECONDITIONS: CMS Settings:
    PRECONDITIONS: Menus->Header Contact Menu->Contact Us:
    PRECONDITIONS: 'Auth Required' and 'Active' checkboxes are ticked
    PRECONDITIONS: Link Title: Contact Us
    PRECONDITIONS: Target Uri: https://help.coral.co.uk/HelpCentreLogin
    PRECONDITIONS: Start Url: https://help.coral.co.uk/s/article/Contact-Us
    PRECONDITIONS: Label: Contact Us
    PRECONDITIONS: System ID: <_1055>_
    PRECONDITIONS: Menus->Bottom Menu->Contact Us:
    PRECONDITIONS: 'Auth Required' and 'Active' checkboxes are ticked
    PRECONDITIONS: Link Title: Contact Us
    PRECONDITIONS: Target Uri: https://help.coral.co.uk/HelpCentreLogin
    PRECONDITIONS: Start Url: https://help.coral.co.uk/s/article/Contact-Us
    PRECONDITIONS: Section: Help
    PRECONDITIONS: System ID: <_1055>_
    PRECONDITIONS: Menus->Right Menu->Contact Us:
    PRECONDITIONS: 'Auth Required' and 'Active' checkboxes are ticked
    PRECONDITIONS: Link Title: Contact Us
    PRECONDITIONS: Target Uri: https://help.coral.co.uk/HelpCentreLogin
    PRECONDITIONS: Start Url: https://help.coral.co.uk/s/article/Contact-Us
    PRECONDITIONS: QA: contactUs
    PRECONDITIONS: System ID: <_1055>_
    PRECONDITIONS: * System ID for different environments:
    PRECONDITIONS: * TEST2 System ID = 1058
    PRECONDITIONS: * STAGE (PT STG1) System ID = 1056
    PRECONDITIONS: * HL System ID = 1055
    PRECONDITIONS: * PRODUCTION System ID = 1055
    PRECONDITIONS: 1. Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_click_on_contact_us_link_on_the_universal_header_for_logged_out_user_on_desktop(self):
        """
        DESCRIPTION: Click on 'Contact Us' link on the Universal Header for Logged Out user on Desktop
        EXPECTED: * The user navigates to https://help.coral.co.uk/s/article/Contact-Us
        EXPECTED: * The user is NOT logged in on Help Centre website
        """
        pass

    def test_002_click_on_contact_us_link_on_the_universal_header_for_logged_in_user_on_desktop(self):
        """
        DESCRIPTION: Click on 'Contact Us' link on the Universal Header for Logged In user on Desktop
        EXPECTED: * The user navigates to https://help.coral.co.uk/s/article/Contact-Us
        EXPECTED: * The user is logged in and username is displayed on Help Centre website
        """
        pass

    def test_003_click_on_contact_us_link_in_the_right_menu_for_logged_in_user_on_mobile(self):
        """
        DESCRIPTION: Click on 'Contact Us' link in the 'Right Menu' for Logged In user on Mobile
        EXPECTED: * The user navigates to https://help.coral.co.uk/s/article/Contact-Us
        EXPECTED: * The user is logged in on Help Centre website
        """
        pass

    def test_004_click_on_contact_us_link_on_the_bottom_menu_for_logged_out_user_on_all_devices(self):
        """
        DESCRIPTION: Click on 'Contact Us' link on the 'Bottom Menu' for Logged Out user on all devices
        EXPECTED: * The user navigates to https://help.coral.co.uk/s/article/Contact-Us
        EXPECTED: * The user is NOT logged in on Help Centre website
        """
        pass

    def test_005_click_on_contact_us_link_on_the_bottom_menu_for_logged_in_user_on_all_devices(self):
        """
        DESCRIPTION: Click on 'Contact Us' link on the 'Bottom Menu' for Logged In user on all devices
        EXPECTED: * The user navigates to https://help.coral.co.uk/s/article/Contact-Us
        EXPECTED: * The user is logged in on Help Centre website
        EXPECTED: * On Desktop: Username is displayed on Help Centre website
        """
        pass
