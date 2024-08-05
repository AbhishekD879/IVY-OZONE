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
class Test_C1641273_Tracking_of_clicking_on_AEM_Banners(Common):
    """
    TR_ID: C1641273
    NAME: Tracking of clicking on AEM Banners
    DESCRIPTION: This test case verifies AEM Banners tracking
    PRECONDITIONS: 1. AEM Banners is enabled in CMS -> 'System Configuration' section -> 'DYNAMICBANNERS' item
    PRECONDITIONS: 2. The user is not login
    PRECONDITIONS: 3. To check banner's name&position parameter: Right-click on any AEM banners > click Inspect: data-title="......" is responsible for 'eventLabel' : '<< BANNER TITLE >>'; data-personalised = ".........." is responsible for <<PERSONALISED>> attribute; data-position ="#" is responsible for 'position': '<< POSITION >>'
    PRECONDITIONS: 4. To perform this test: Right-click on any AEM banners > click Inspect > find <div class="swipper-slide" > parameter **target="_self"** need change to **target="_blank"** for each AEM banners to be opened in a separate window
    PRECONDITIONS: 5. This test case covers Mobile, Tablet, Desktop
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners  please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: - Homepage is opened;
        EXPECTED: - AEM banners are loaded;
        """
        pass

    def test_002_click_on_the_any_aem_banner_on_the_carousel(self):
        """
        DESCRIPTION: Click on the any AEM banner on the carousel
        EXPECTED: Banner is opened in new tab
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The next static parameters are present:
        EXPECTED: {dataLayer.push( {   }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. location: "/";
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g. for not loggin user vipLevel: "null";
        EXPECTED: 'position' : '<< POSITION >>'
        EXPECTED: })
        """
        pass

    def test_004_navigate_to_any_sportracecompetition_landing_page_where_aem_banners_are_set_up(self):
        """
        DESCRIPTION: Navigate to any Sport/Race/Competition landing page where AEM banners are set up
        EXPECTED: - Sport/Race landing page is opened;
        EXPECTED: - AEM banners are loaded;
        """
        pass

    def test_005_click_on_the_any_aem_banner_on_the_carousel(self):
        """
        DESCRIPTION: Click on the any AEM banner on the carousel
        EXPECTED: Banner is opened in new tab
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The next static parameters are present:
        EXPECTED: {dataLayer.push( {   }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. location: "/horseracing/featured";
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g. for not loggin user vipLevel: "null";
        EXPECTED: 'position' : '<< POSITION >>'
        EXPECTED: })
        """
        pass

    def test_007_repeat_1_6_steps_for_logged_users_with_different_viplevel(self):
        """
        DESCRIPTION: Repeat 1-6 steps for logged users with different VipLevel
        EXPECTED: The next static parameters are present:
        EXPECTED: {dataLayer.push( {   }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>',
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g. vipLevel: "10";
        EXPECTED: 'position' : '<< POSITION >>'
        EXPECTED: })
        """
        pass
