import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29417_Verify_More_Link(Common):
    """
    TR_ID: C29417
    NAME: Verify 'More' Link
    DESCRIPTION: This test case is for checking of 'View Full Race Card' link ('More' for Mobile)
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon__gt_module_created_by_ltracegt_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -&gt; Module created by &lt;Race&gt; type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by &lt;Race&gt; type ID is shown
        """
        pass

    def test_003_for_desktopscroll_the_page_down_to_featured_section__gt_gt_module_created_by_ltracegt_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section -&gt;-&gt; Module created by &lt;Race&gt; type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by &lt;Race&gt; type ID is shown
        """
        pass

    def test_004_on_ltracegt_events_carousel_find_view_full_race_card_link(self):
        """
        DESCRIPTION: On &lt;Race&gt; events carousel find 'View Full Race Card' link
        EXPECTED: 1.  'View Full Race Card' ('More' for Mobile)
        EXPECTED: is displayed for each event in &lt;Race&gt; events carousel
        EXPECTED: 2.  Link is displayed at the bottom of section
        EXPECTED: 3.  Both text and icon are hyperlinked
        EXPECTED: 4.  Link is internationalised
        """
        pass

    def test_005_tap_more_link_more_also_mobile(self):
        """
        DESCRIPTION: Tap 'More' link ('More' also Mobile)
        EXPECTED: User is redirected to event details page
        """
        pass

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap back button
        EXPECTED: User is redirected to the page he navigated from
        """
        pass