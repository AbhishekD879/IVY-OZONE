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
class Test_C2080048_Verify_tracking_of_viewing_AEM_Banners(Common):
    """
    TR_ID: C2080048
    NAME: Verify tracking of viewing AEM Banners
    DESCRIPTION: This test case verifies tracking of AEM banners viewing across an app
    DESCRIPTION: NOTE: Works for Betslip banners the same way
    PRECONDITIONS: - AEM Banners are enabled in CMS (System-configuration > DYNAMICBANNERS)
    PRECONDITIONS: - User is not logged in
    PRECONDITIONS: - To check banner's name&position parameter: Right-click on any AEM banners > click Inspect: data-title="......" is responsible for 'eventLabel' : '<< BANNER TITLE >>'; data-personalised = ".........." is responsible for <<PERSONALISED>> attribute; data-position ="#" is responsible for 'position': '<< POSITION >>'
    PRECONDITIONS: - This test case covers Mobile, Tablet, Desktop
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

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * The next static parameters are present:
        EXPECTED: {dataLayer.push( { }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'view',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. location: "/";
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g. for logged out user: "null";
        EXPECTED: 'position' : '<< POSITION >>'
        EXPECTED: })
        """
        pass

    def test_003_wait_till_aem_banners_are_auto_switched__type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Wait till AEM banners are auto switched > Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * The next static parameters are present for next available banners:
        EXPECTED: {dataLayer.push( { }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'view',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. location: "/";
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g. for logged out user: "null";
        EXPECTED: 'position' : '<< POSITION >>'
        EXPECTED: })
        EXPECTED: * Each available banner is tracked only during its first cycle round (unless page is refreshed or user is navigated from the page and comes back)
        """
        pass

    def test_004_navigate_to_any_sportracecompetition_landing_page_where_aem_banners_are_set_up(self):
        """
        DESCRIPTION: Navigate to any Sport/Race/Competition landing page where AEM banners are set up
        EXPECTED: - Sport/Race landing page is opened;
        EXPECTED: - AEM banners are loaded;
        """
        pass

    def test_005_wait_till_aem_banners_are_auto_switched__type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Wait till AEM banners are auto switched > Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * The next static parameters are present:
        EXPECTED: {dataLayer.push( { }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'view',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. location: "/football/matches/today";
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g. for logged out user: "null";
        EXPECTED: 'position' : '<< POSITION >>' e.g. order # of a banner
        EXPECTED: })
        EXPECTED: * Each available banner is tracked only during its first cycle round (unless page is refreshed or user is navigated from the page and comes back)
        """
        pass

    def test_006_repeat_1_5_steps_for_logged_users_with_different_viplevel(self):
        """
        DESCRIPTION: Repeat 1-5 steps for logged users with different VipLevel
        EXPECTED: * The next static parameters are present:
        EXPECTED: {dataLayer.push( { }}
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'view',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. location: "/";
        EXPECTED: 'personalised' : <<PERSONALISED>> , e.g. true/false,
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', e.g.  e.g. vipLevel: "10";
        EXPECTED: 'position' : '<< POSITION >>'
        EXPECTED: })
        EXPECTED: * Each available banner is tracked only during its first cycle round (unless page is refreshed or user is navigated from the page and comes back)
        """
        pass
