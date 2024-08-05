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
class Test_C2555500_Tracking_of_tapping_on_Quick_links(Common):
    """
    TR_ID: C2555500
    NAME: Tracking of tapping on Quick links
    DESCRIPTION: This test case verifies tracking when user taps on any Quick link.
    PRECONDITIONS: 1. Feature toggle should be enabled
    PRECONDITIONS: 2. Quick links should be created and enabled on Homepage and Football landing page.
    PRECONDITIONS: 3. User should be logged in
    PRECONDITIONS: 4. Load Oxygen application and open browser's console
    PRECONDITIONS: 5. Navigate to "Featured" tab on Homepage
    PRECONDITIONS: <Sport category> - any Sport available in oxygen app(e.g Tennis, Football)
    PRECONDITIONS: Template of Record that appears in consoles after tapping on Quick link:
    PRECONDITIONS: dataLayer.push({
    PRECONDITIONS: 'event' : 'trackEvent',
    PRECONDITIONS: 'eventCategory' : 'quick links',
    PRECONDITIONS: 'eventAction' : '<< LOCATION >>',
    PRECONDITIONS: 'eventLabel' : '<< LINK TITLE >>'
    PRECONDITIONS: });
    """
    keep_browser_open = True

    def test_001_tap_on_any_quick_link_present_on_homepageverify_redirection_to_url_set_in_quick_link_configuration_in_cms(self):
        """
        DESCRIPTION: Tap on any Quick link present on homepage.
        DESCRIPTION: Verify redirection to URL set in Quick link configuration in CMS.
        EXPECTED: User is redirected to destination URL present in Quick link configuration in CMS.
        """
        pass

    def test_002_go_to_browser_console_and_type_datalayerverify_ga_tracking_record(self):
        """
        DESCRIPTION: Go to browser console and type "dataLayer".
        DESCRIPTION: Verify GA tracking record
        EXPECTED: Record that user did a tap on Quick link from homepage s present in console:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quick links',
        EXPECTED: 'eventAction' : 'home',
        EXPECTED: 'eventLabel' : '<< LINK TITLE >>'
        EXPECTED: });
        """
        pass

    def test_003_go_to_oxygen_app_and_navigate_to_sport_category_page(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport category> page
        EXPECTED: 
        """
        pass

    def test_004_tap_on_any_quick_link_present_on_sport_category_page(self):
        """
        DESCRIPTION: Tap on any Quick link present on <Sport category> page
        EXPECTED: User is redirected to destination URL present in Quick link configuration in CMS.
        """
        pass

    def test_005_go_to_browser_console_and_type_datalayerverify_ga_tracking_record(self):
        """
        DESCRIPTION: Go to browser console and type "dataLayer"
        DESCRIPTION: Verify GA tracking record
        EXPECTED: Record is present in console that user did a tap on Quick link from Football page.
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quick links',
        EXPECTED: 'eventAction' : '<Sport category> landing',
        EXPECTED: 'eventLabel' : '<< LINK TITLE >>'
        EXPECTED: });
        """
        pass
