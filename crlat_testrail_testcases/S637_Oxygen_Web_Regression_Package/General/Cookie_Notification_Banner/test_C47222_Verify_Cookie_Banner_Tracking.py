import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C47222_Verify_Cookie_Banner_Tracking(Common):
    """
    TR_ID: C47222
    NAME: Verify Cookie Banner Tracking
    DESCRIPTION: This test case verifies tracking of cookie banner
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-15772 Cookie Banner Tracking
    DESCRIPTION: BMA-46701 Coral IOS app - please remove the cookie banner
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: 2. User is logged out
    PRECONDITIONS: 3. Make sure that Cookie Banner **is NOT DISPLAYED** on Coral iOS wrapper v.5.1.1 build 1157 and higher regardless of the CMS configuration.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is opened
        EXPECTED: * Cookies Notification Banner is displayed above the Header at the top of the page
        """
        pass

    def test_002_open_developments_toolconsole(self):
        """
        DESCRIPTION: Open developments tool>console
        EXPECTED: 
        """
        pass

    def test_003_type_in_console_datalayer__tap_enter_and_check_the_attributes(self):
        """
        DESCRIPTION: Type in console 'dataLayer' , tap 'Enter' and check the attributes
        EXPECTED: Following code is present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cookie banner',
        EXPECTED: 'eventAction' : 'display',
        EXPECTED: 'eventNonInteraction' : true
        EXPECTED: });
        """
        pass

    def test_004_click_more_infoon_cookie_banner(self):
        """
        DESCRIPTION: Click 'More Info'on cookie banner
        EXPECTED: Hyperlink https://coral-eng.custhelp.com/app/answers/detail/a_id/8331 is opened in new tab
        """
        pass

    def test_005_type_in_console_datalayer__tap_enter_and_check_the_attributes(self):
        """
        DESCRIPTION: Type in console 'dataLayer' , tap 'Enter' and check the attributes
        EXPECTED: Following code is present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cookie banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'more info'
        EXPECTED: });
        """
        pass

    def test_006_click_cookie_policy_on_cookie_banner(self):
        """
        DESCRIPTION: Click 'Cookie Policy' on cookie banner
        EXPECTED: Hyperlink  https://coral-eng.custhelp.com/app/answers/detail/a_id/2132#cookies is opened in new tab
        """
        pass

    def test_007_type_in_console_datalayer__tap_enter_and_check_the_attributes(self):
        """
        DESCRIPTION: Type in console 'dataLayer' , tap 'Enter' and check the attributes
        EXPECTED: Following code is present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cookie banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'cookie policy'
        EXPECTED: });
        """
        pass

    def test_008_click_accept__close_on_cookie_banner(self):
        """
        DESCRIPTION: Click 'Accept & Close' on cookie banner
        EXPECTED: Following code is present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cookie banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'accept & close'
        EXPECTED: });
        """
        pass

    def test_009_clear_cookies_and_cachelog_in_oxygen_app(self):
        """
        DESCRIPTION: Clear cookies and cache
        DESCRIPTION: Log in Oxygen app
        EXPECTED: Cookies Notification Banner is displayed above the Header at the top of the page
        """
        pass

    def test_010_repet_step_2_8(self):
        """
        DESCRIPTION: Repet step #2-8
        EXPECTED: 
        """
        pass
