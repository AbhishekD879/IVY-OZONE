import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2031747_Tracking_of_Help_and_Contact_Us_links_on_Desktop_Universal_Header_on_the_Homepage(Common):
    """
    TR_ID: C2031747
    NAME: Tracking of 'Help' and 'Contact Us' links on Desktop Universal Header on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Help' and 'Contact Us' links on Desktop Universal Header on the Homepage.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is loaded
        EXPECTED: * 'Help' link is displayed at Desktop Universal Header
        """
        pass

    def test_002_click_on_help_link_at_desktop_universal_header(self):
        """
        DESCRIPTION: Click on 'Help' link at Desktop Universal Header
        EXPECTED: * User is navigating to the Coral Help Center page (https://help.coral.co.uk/s/)
        EXPECTED: * Page is opened in a separate browser tab
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' a: 'secondary',
        EXPECTED: 'eventLabel' : '<< NAV ITEM >>' //e.g. help
        EXPECTED: })
        """
        pass

    def test_004_click_on_contact_us_link_at_desktop_universal_header(self):
        """
        DESCRIPTION: Click on 'Contact Us' link at Desktop Universal Header
        EXPECTED: * User is navigating to the Coral Support page (https://help.coral.co.uk/s/contactsupport)
        EXPECTED: * Page is opened in a separate browser tab
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' a: 'secondary',
        EXPECTED: 'eventLabel' : '<< NAV ITEM >>' //e.g. contact us
        EXPECTED: })
        """
        pass

    def test_006_repeat_steps_2_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Logged In user
        EXPECTED: 
        """
        pass
