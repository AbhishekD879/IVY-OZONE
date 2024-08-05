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
class Test_C10687849_Verify_In_Play_page_behavior_with_slow_network_connection(Common):
    """
    TR_ID: C10687849
    NAME: Verify In-Play page behavior with slow network connection
    DESCRIPTION: This Test Case verifies In-Play page behavior with slow network connection.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * Slow network connection (Edge/Slow 3G) is turned on in device preference
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    """
    keep_browser_open = True

    def test_001_trigger_liveserve_update_suspension_price_change_etc(self):
        """
        DESCRIPTION: Trigger LiveServe update (suspension, price change etc.)
        EXPECTED: All updates triggered during slow network connection are received in WS connection and are displayed on FE
        """
        pass

    def test_002_trigger_completionexpiration_of_the_event(self):
        """
        DESCRIPTION: Trigger completion/expiration of the event
        EXPECTED: Completed/expired event is removed from the front-end automatically
        """
        pass

    def test_003_start_new_event_within_sport_section_that_is_not_present_on_current_page(self):
        """
        DESCRIPTION: Start new event within <Sport> section that is not present on current page
        EXPECTED: * <Sport> icon is appeared in In Play ribbon immediately
        EXPECTED: * <Sport> section appears at the bottom of the page in collapsed stated state disregarding it's Display Order
        """
        pass

    def test_004_choose_upcoming_sorting_type_on_in_play_page_and_repeat_steps_1_3(self):
        """
        DESCRIPTION: Choose 'Upcoming' sorting type on 'In-Play' page and repeat steps 1-3
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_1_3_on_home_page__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play__module_for_mobiletablet_homepage__in_play__live_stream_section_for_desktop_sports_landing_page__in_play_widget_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 on:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play'  module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section **For Desktop**
        DESCRIPTION: * Sports Landing page > 'In-play' widget **For Desktop:**
        EXPECTED: 
        """
        pass
