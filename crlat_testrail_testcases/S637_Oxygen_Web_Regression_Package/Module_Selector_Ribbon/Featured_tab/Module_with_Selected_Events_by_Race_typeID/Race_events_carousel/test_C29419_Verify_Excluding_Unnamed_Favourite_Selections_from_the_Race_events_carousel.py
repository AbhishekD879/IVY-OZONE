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
class Test_C29419_Verify_Excluding_Unnamed_Favourite_Selections_from_the_Race_events_carousel(Common):
    """
    TR_ID: C29419
    NAME: Verify Excluding 'Unnamed Favourite' Selections from the <Race> events carousel
    DESCRIPTION: This test case verifies 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selections excluding from the displaying within <Race> events carousel within modules created by <Race> typeID.
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day which contain 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selections with 'selection type'='Unnamed Favorite/Unnamed 2nd Favorite' set on selection level in TI tool
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
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

    def test_004_pick_event_from_ltracegt_module__gt_remove_all_but_one_selections_fromwin_or_each_way_marketmake_sure_two_unnamed_favourite_selections_are_also_remain(self):
        """
        DESCRIPTION: Pick event from &lt;Race&gt; module -&gt; Remove all but one selections from 'Win or Each Way' market
        DESCRIPTION: Make sure two 'Unnamed Favourite' selections are also remain
        EXPECTED: Only three selections are available for the Win or Each Way market
        """
        pass

    def test_005_go_to_the_invictus_application_and_check_the_event_in_the_verified_module_created_by_ltracegt_typeid(self):
        """
        DESCRIPTION: Go to the Invictus application and check the event in the verified module created by &lt;Race&gt; typeID
        EXPECTED: Only one selection is shown for this event
        EXPECTED: 'Unnamed Favourite' selections are excluded from the module created by &lt;Race&gt; typeID
        """
        pass
