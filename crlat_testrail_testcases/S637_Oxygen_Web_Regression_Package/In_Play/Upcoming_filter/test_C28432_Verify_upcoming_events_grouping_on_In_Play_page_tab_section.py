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
class Test_C28432_Verify_upcoming_events_grouping_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C28432
    NAME: Verify upcoming events grouping on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies upcoming events grouping on 'In-Play' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Upcoming events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: *To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::UPCOMING_EVENT::XXX"
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40803)
    """
    keep_browser_open = True

    def test_001_verify_upcoming_events_grouping_by_category(self):
        """
        DESCRIPTION: Verify upcoming events grouping by category
        EXPECTED: * The &lt;Category&gt; accordions are displayed
        EXPECTED: * Types are grouped by 'categoryID' &gt; 'classID' within expanded &lt;Category&gt; accordion
        """
        pass

    def test_002_verify_upcoming_events_grouping_by_types(self):
        """
        DESCRIPTION: Verify upcoming events grouping by Types
        EXPECTED: * The &lt;Type&gt; accordions/odds headers are displayed
        EXPECTED: * Events are grouped by 'typeID' within &lt;Type&gt; expanded accordions/odds headers
        """
        pass

    def test_003_repeat_steps_1_2_onhome_page_gt_in_play_tab_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: *Home page &gt; 'In-Play' tab **Mobile/Tablet**
        EXPECTED: 
        """
        pass

    def test_004_repeat_step_2_onsports_landing_page_gt_in_play_tabin_play_page_gt_sport_tab(self):
        """
        DESCRIPTION: Repeat step 2 on:
        DESCRIPTION: *Sports Landing Page &gt; 'In-Play' tab
        DESCRIPTION: *'In-Play' page &gt; 'Sport' tab
        EXPECTED: 
        """
        pass
