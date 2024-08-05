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
class Test_C29421_Exclude_Non_Runners_selections_from_the_Race_events_carousel(Common):
    """
    TR_ID: C29421
    NAME: Exclude Non-Runners selections from the <Race> events carousel
    DESCRIPTION: This test case verifies how 'Non-Runners' will be excluded from the <Race> events carousel
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on outcome level to see horse name
    PRECONDITIONS: **'outcomeStatusCode' **to see outcome status
    PRECONDITIONS: 'Non-Runners' is a selection which contains **'N/R'** text next to it's name
    PRECONDITIONS: All those selections should be suspended 'outcomeStatusCode'='S'
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon__gt_module_created_by_ltracegt_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -&gt; Module created by &lt;Race&gt; type ID
        EXPECTED: 1.  'Feature' tab is selected by default
        EXPECTED: 2.  Module created by &lt;Race&gt; type ID is shown
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

    def test_004_on_the_ltracegt_events_carousel_find_an_event_which_contains_non_runner_selection(self):
        """
        DESCRIPTION: On the &lt;Race&gt; events carousel find an event which contains 'non-runner' selection
        EXPECTED: Event is displayed in the &lt;Race&gt; events carousel
        """
        pass

    def test_005_verify_selections_in_the_event(self):
        """
        DESCRIPTION: Verify selections in the event
        EXPECTED: 1.  'Non-Runners' won't appear in the &lt;Race&gt; events carousel
        EXPECTED: 2.  'Non-Runners' are excluded by **outcomeStatusCode **attribute (suspended selections are not shown in the &lt;Race&gt; events carousel )
        """
        pass

    def test_006_find_an_event_which_contains_3_or_less_selection_and_one_of_those_selections_is_non_runners(self):
        """
        DESCRIPTION: Find an event which contains 3 or less selection and one of those selections is 'non-runners'
        EXPECTED: Event is shown
        """
        pass

    def test_007_verify_selections_in_the_ltracegt_events_carousel(self):
        """
        DESCRIPTION: Verify selections in the &lt;Race&gt; events carousel
        EXPECTED: 'Non- Runner' selections still are not displayed
        """
        pass
