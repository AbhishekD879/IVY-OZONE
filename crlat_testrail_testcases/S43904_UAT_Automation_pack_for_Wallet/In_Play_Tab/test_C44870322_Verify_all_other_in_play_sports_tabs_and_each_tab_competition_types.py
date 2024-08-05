import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870322_Verify_all_other_in_play_sports_tabs_and_each_tab_competition_types(Common):
    """
    TR_ID: C44870322
    NAME: Verify all other in-play sports tabs and each tab competition types
    DESCRIPTION: This test case verify inplay sports available in In-Play tab
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' Landing Page is opened
        EXPECTED: Sports Menu Ribbon is shown with Categories where In-Play events are available
        EXPECTED: First <Sport> tab is opened by default
        EXPECTED: Two filter switchers are visible: 'Live Now' and 'Upcoming'
        """
        pass

    def test_003_verify_live_now__upcoming_filter_switchers_are_visible_for_all_other_in_play_sports_tab_and_each_tab_competition_types_are_expandablecollapsible(self):
        """
        DESCRIPTION: Verify 'Live Now & Upcoming' filter switchers are visible for all other In-play sports tab and each tab competition types are expandable/collapsible.
        EXPECTED: 'Live Now & Upcoming' filter switchers are visible for all other In-play sports tab and each tab competition types are expandable/collapsible.
        """
        pass
