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
class Test_C44870320_Verify_user_sees_all_in_play_sports_tabs_in_the_in_play_page_(Common):
    """
    TR_ID: C44870320
    NAME: "Verify user sees all in-play sports tabs in the in-play page.  "
    DESCRIPTION: This test case verify inplay sports available in In-Play tab
    PRECONDITIONS: sport should be in in-play to appear in In-Play tab
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

    def test_003_for_mobiletabletverify_sport_tabs_filteringfor_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_verify_sport_tabs_filtering(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Verify Sport tabs filtering
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play & Live Stream' section on Homepage and verify Sport tabs filtering
        EXPECTED: Each sport tab is tappable
        EXPECTED: -If there are any live events available for the particular sport then, number of Live events is displayed on sport icon (example: 3,2 etc)
        EXPECTED: -sports ribbon is scrollable from right to left
        EXPECTED: -Selected sport is highlighted
        EXPECTED: ![](index.php?/attachments/get/106815423)
        """
        pass
