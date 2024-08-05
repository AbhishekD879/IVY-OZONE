import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C9771300_Tracking_of_See_all_link(Common):
    """
    TR_ID: C9771300
    NAME: Tracking of 'See all' link
    DESCRIPTION: This test case verifies tracking of clicking on 'See all' link in HR Module 'by type id' on Home page Featured tab
    PRECONDITIONS: HR module 'Race by type ID' is created in CMS and displayed on Featured tab on Home page.
    PRECONDITIONS: User is on Homepage with focus on module created.
    """
    keep_browser_open = True

    def test_001_click_on_see_all_link_in_hr_module_header(self):
        """
        DESCRIPTION: Click on 'See all' link in HR module header
        EXPECTED: User is redirected to the HR landing page
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following code is fired:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent', 'eventCategory' : 'featured module', 'eventAction' : '<< LOCATION >>', 'eventLabel' : 'see all', 'sportName' : '<< SPORT NAME >>' }
        """
        pass
