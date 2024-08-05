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
class Test_C28429_Verify_live_events_grouping_on_In_Play_pages(Common):
    """
    TR_ID: C28429
    NAME: Verify live events grouping on 'In-Play' pages
    DESCRIPTION: This test case verifies live events grouping on 'In-Play' pages
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
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40725)
    """
    keep_browser_open = True

    def test_001_verify_grouping_by_categories_in_live_now_section(self):
        """
        DESCRIPTION: Verify grouping by Categories in 'Live Now' section
        EXPECTED: * The &lt;Category&gt; accordions are displayed
        EXPECTED: * Types are grouped by 'categoryID' &gt; 'classID' within expanded &lt;Category&gt; accordion
        """
        pass

    def test_002_verify_live_events_grouping_by_types(self):
        """
        DESCRIPTION: Verify live events grouping by Types
        EXPECTED: * The &lt;Type&gt; accordions/odds headers are displayed
        EXPECTED: * Events are grouped by 'typeID' within &lt;Type&gt; expanded accordions/odds headers
        """
        pass

    def test_003_repeat_steps_1_2_on_home_page_gt_in_play_tab_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: * Home page &gt; 'In-Play' tab **Mobile/Tablet**
        EXPECTED: 
        """
        pass

    def test_004_repeat_step_2_on_sports_landing_page_gt_in_play_tab_in_play_page_gt_sport_tab_home_page_for_in_play__live_stream_section_for_both_switchers_desktop(self):
        """
        DESCRIPTION: Repeat step 2 on:
        DESCRIPTION: * Sports Landing Page &gt; 'In-Play' tab
        DESCRIPTION: * 'In-Play' page &gt; 'Sport' tab
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers **Desktop**
        EXPECTED: 
        """
        pass
