import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C28410_Verify_Expired_Events_Removing_from_In_Play_pages(Common):
    """
    TR_ID: C28410
    NAME: Verify Expired Events Removing from In-Play pages
    DESCRIPTION: This test case verifies which events are removed from displaying within In-Play pages on front-end
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sport Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_trigger_completionexpiration_of_verified_eventnote_eventcompletionexpiration_means_that_event_is_not_present_on_siteserver_anymore_attribute_displayedn_is_set_for_the_event(self):
        """
        DESCRIPTION: Trigger completion/expiration of verified event
        DESCRIPTION: NOTE: Event completion/expiration means that event is not present on SiteServer anymore (attribute 'displayed="N"' is set for the event )
        EXPECTED: Completed/expired event is removed from the front-end automatically
        """
        pass

    def test_002_repeat_step_1_for_upcoming_events(self):
        """
        DESCRIPTION: Repeat step 1 for upcoming events
        EXPECTED: Completed/expired event is removed from the front-end automatically
        """
        pass

    def test_003_navigate_to_sports_landing_page_gt_in_play_tab_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: Navigate to Sports Landing page &gt; 'In-Play' tab and repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_live_stream_page_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: Navigate to Live Stream page and repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_005_for_mobiletabletnavigate_to_homepage_gt_in_play_tab_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage &gt; 'In-Play' tab and repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_006_for_mobiletabletnavigate_to_homepage_gt_live_stream_tab_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage &gt; 'Live Stream' tab and repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_007_for_mobiletabletnavigate_to_homepage_gt_featured_tab_gt_in_play__module_and_repeat_step_1(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage &gt; 'Featured' tab &gt; 'In-play'  module and repeat step 1
        EXPECTED: 
        """
        pass

    def test_008_for_mobiletabletnavigate_to_sports_landing_page_gt_matches_tab_gt_in_play_module_and_repeat_step_1(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Sports Landing page &gt; 'Matches' tab &gt; 'In-play' module and repeat step 1
        EXPECTED: 
        """
        pass

    def test_009_for_desktopnavigate_to_in_play__live_stream_section_on_homepageand_repeat_step_1_for_both_in_play_and_live_stream_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage
        DESCRIPTION: and repeat step 1 for both 'In-Play' and 'Live Stream' filter switchers
        EXPECTED: 
        """
        pass

    def test_010_for_desktopnavigate_to_sports_landing_page_gt_in_play_widget_and_repeat_step_1(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page &gt; 'In-play' widget and repeat step 1
        EXPECTED: 
        """
        pass
