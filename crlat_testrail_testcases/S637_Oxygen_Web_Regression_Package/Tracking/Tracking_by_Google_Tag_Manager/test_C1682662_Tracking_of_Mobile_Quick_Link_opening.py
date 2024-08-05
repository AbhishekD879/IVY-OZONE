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
class Test_C1682662_Tracking_of_Mobile_Quick_Link_opening(Common):
    """
    TR_ID: C1682662
    NAME: Tracking of Mobile Quick Link opening
    DESCRIPTION: This test case verifies tracking of Mobile Quick Link opening
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Mobile Quick Link should be created and enabled in CMS
    PRECONDITIONS: * Mobile Quick Link should be set up to be displayed on
    PRECONDITIONS: - Home Tabs (e.g. Featured, In-Play, Top Bets)
    PRECONDITIONS: - Sport/Race (e.g. football, Horse Racing,Tennis)
    PRECONDITIONS: - Big Competition (e.g. World Cup)
    PRECONDITIONS: * Big Competition should be created, enabled and set up in CMS
    PRECONDITIONS: * To check 'eventAction' parameter open DevTools -> network tab -> XHR -> set 'mobile' filter -> select GET /cms/api/bma/initial-data/mobile request
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_go_to_mobile_quick_link_set_up_to_be_displayed_on_home_tabs_eg_featured_in_play_top_bets(self):
        """
        DESCRIPTION: Go to Mobile Quick Link set up to be displayed on Home Tabs (e.g. Featured, In-Play, Top Bets)
        EXPECTED: Mobile Quick Link is displayed above content of Home Tab
        """
        pass

    def test_003_tap_on_mobile_quick_link(self):
        """
        DESCRIPTION: Tap on Mobile Quick Link
        EXPECTED: User is navigated to destination page set up in CMS
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cta',
        EXPECTED: 'eventAction' : '<<CTA TEXT>>'
        EXPECTED: }
        EXPECTED: );
        """
        pass

    def test_005_verify_eventaction_parameter(self):
        """
        DESCRIPTION: Verify **eventAction** parameter
        EXPECTED: **eventAction** parameter  corresponds to **navigationPoints.[i].title** attribute from GET response (see preconditions)
        EXPECTED: where i - the number of all navigation poitns returned
        """
        pass

    def test_006_go_to_mobile_quick_link_set_up_to_be_displayed_on_sportrace_page_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Go to Mobile Quick Link set up to be displayed on Sport/Race page and repeat steps #3-5
        EXPECTED: 
        """
        pass

    def test_007_go_to_mobile_quick_link_set_up_to_be_displayed_on_big_competition_page_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Go to Mobile Quick Link set up to be displayed on Big Competition page and repeat steps #3-5
        EXPECTED: 
        """
        pass
