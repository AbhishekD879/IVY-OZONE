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
class Test_C28428_Verify_data_ordering_in_Live_Now_section_on_In_Play_pages(Common):
    """
    TR_ID: C28428
    NAME: Verify data ordering in  'Live Now' section on 'In-Play' pages
    DESCRIPTION: This test case verifies data ordering in  'Live Now' section on 'In-Play' pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify category/class/type ordering check received data using Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::XX::LIVE_EVENT" - where XX - Sport/Category Id
    PRECONDITIONS: ![](index.php?/attachments/get/40682)
    """
    keep_browser_open = True

    def test_001_verify_ltcategorygt_title_on_the_first_level_accordion_within_live_now_section(self):
        """
        DESCRIPTION: Verify &lt;Category&gt; title on the first level accordion within 'Live Now' section
        EXPECTED: 'Sport' name is displayed at the &lt;Category&gt; accordion within 'Live Now' section
        """
        pass

    def test_002_verify_ltcategorygt_accordions_order(self):
        """
        DESCRIPTION: Verify &lt;Category&gt; accordions order
        EXPECTED: &lt;Category&gt; accordions are ordered by:
        EXPECTED: * Category 'displayOrder' in ascending where minus ordinals are displayed first
        """
        pass

    def test_003_verify_lttypegt_title_on_accordionsodds_headers_within_live_now_section(self):
        """
        DESCRIPTION: Verify &lt;Type&gt; title on accordions/odds headers within 'Live Now' section
        EXPECTED: **Mobile/Tablet**
        EXPECTED: * 'Type' name is displayed at the &lt;Type&gt; accordions/odds headers
        EXPECTED: **Desktop**
        EXPECTED: * 'Type' name if the section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: * 'Class' - 'Type' name if the section is named Class Name (sport name should not be displayed) + Type Name on Pre-Match pages
        """
        pass

    def test_004_verify_lttypegt_accordionsodds_headers_order(self):
        """
        DESCRIPTION: Verify &lt;Type&gt; accordions/odds headers order
        EXPECTED: &lt;Type&gt; accordions/odds headers are ordered by:
        EXPECTED: * Class 'displayOrder' in ascending where minus ordinals are displayed first
        EXPECTED: * Type 'displayOrder' in ascending where minus ordinals are displayed first
        """
        pass

    def test_005_verify_events_order_within_the_lttypegt_accordionsodds_headers(self):
        """
        DESCRIPTION: Verify events order within the &lt;Type&gt; accordions/odds headers
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * 'startTime' - chronological order in the first instance
        EXPECTED: * Event 'displayOrder' in ascending
        EXPECTED: * Alphabetical order
        """
        pass

    def test_006_repeat_steps_1_5_on_home_page_gt_in_play_tab_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Home page &gt; 'In-Play' tab **Mobile/Tablet**
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_5_on_sports_landing_page_gt_in_play_tab_in_play_page_gt_sport_tab_home_page_for_in_play__live_stream_section_for_both_switchers_desktop(self):
        """
        DESCRIPTION: Repeat steps 3-5 on:
        DESCRIPTION: * Sports Landing Page &gt; 'In-Play' tab
        DESCRIPTION: * 'In-Play' page &gt; 'Sport' tab
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers **Desktop**
        EXPECTED: 
        """
        pass
