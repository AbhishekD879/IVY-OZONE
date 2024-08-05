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
class Test_C44870170_Verify_User_navigation_for_In_Play_tab(Common):
    """
    TR_ID: C44870170
    NAME: Verify User navigation for In-Play tab
    DESCRIPTION: User is on the
    DESCRIPTION: mobile: Homepage > In-play
    DESCRIPTION: Desktop: Homepage > In-play
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouk_app(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/ App
        EXPECTED: App is loaded and user is on Home page
        """
        pass

    def test_002_select_in_play_tab_from_home_page_menu(self):
        """
        DESCRIPTION: Select In-Play tab from Home page menu
        EXPECTED: Mobile & Tablet : In-Play page is loaded with 'Live Now' section is displayed with top 4 competitions are expanded in the list followed by other LIVE sports and 'UPCOMING' events at the bottom.
        EXPECTED: Desktop : Page is displayed with "In-play" & "Live Stream"
        EXPECTED: Events from first sport on the In-Play Carousal are listed with top 4 competitions expanded.
        """
        pass

    def test_003_on_the_in_play_tab_for_mobiletablet_click_on_see_all_sport_on_the_right_of_live_now(self):
        """
        DESCRIPTION: On the In-Play tab for Mobile/Tablet: Click on 'SEE ALL <sport>' on the right of LIVE NOW
        EXPECTED: All the live events for the corresponding sport / competition are expanded.
        """
        pass

    def test_004_on_the_in_play_for_desktop__click_on_each_sport_icon_from_the_carousel(self):
        """
        DESCRIPTION: On the In-play for Desktop : Click on each sport icon from the carousel.
        EXPECTED: All the live events for the corresponding sport / competition are displayed with In-play & Live stream options.
        """
        pass
