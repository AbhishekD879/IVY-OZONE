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
class Test_C44870180_Verify_user_can_navigate_to_in_play_sports_by_clicking_on_in_play_on_the_quick_carousel_And_In_play_events_are_available_on_page_Verify_navigation_to_Multiple_sports_pages_from_Quick_Carousel_say_Cricket_GH_Rugby_Union_(Common):
    """
    TR_ID: C44870180
    NAME: "Verify user can navigate to in-play sports by clicking on in-play on the quick carousel And In -play events are available on page  Verify navigation to Multiple sports pages from Quick Carousel say Cricket, GH , Rugby Union "
    DESCRIPTION: "Verify user can navigate to in-play sports by clicking on in-play on the quick carousel
    DESCRIPTION: And In -play events are available on page
    DESCRIPTION: Verify navigation to Multiple sports pages from Quick Carousel say Cricket, GH , Rugby Union
    DESCRIPTION: "
    PRECONDITIONS: Roxanne app is loaded
    """
    keep_browser_open = True

    def test_001_on_the_home_page_tap_on_in_play_from_footer_menu(self):
        """
        DESCRIPTION: On the Home page, tap on 'In-Play' from footer menu
        EXPECTED: In-Play page is loaded and In-Play events of the first sport in the header menu are displayed.
        """
        pass

    def test_002_click_on_any_other_sport_from_the_header_menu(self):
        """
        DESCRIPTION: Click on any other sport from the header menu.
        EXPECTED: All the In-Play events of the sport are displayed. User is able to switch between sports and should be able to view all In-Play events for the corresponding sport.
        """
        pass

    def test_003_verify_the_content_for_each_sport(self):
        """
        DESCRIPTION: Verify the content for each sport
        EXPECTED: All the In-Play events for each sport are grouped according to competitions and user is able to expand/ collapse by clicking on the accordion.
        """
        pass
