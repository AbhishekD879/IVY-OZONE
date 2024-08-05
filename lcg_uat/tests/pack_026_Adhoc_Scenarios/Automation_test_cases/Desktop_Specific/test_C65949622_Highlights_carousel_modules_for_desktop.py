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
class Test_C65949622_Highlights_carousel_modules_for_desktop(Common):
    """
    TR_ID: C65949622
    NAME: Highlights carousel modules for desktop
    DESCRIPTION: This test case is to validate Highlights carousel modules for desktop
    PRECONDITIONS: 1. User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Login with valid credentials
    PRECONDITIONS: 3.CORAL - Navigate to sports pages>Homepage>Highlight Carousel Module
    PRECONDITIONS: LADS - Navigate to Homepage>Highlight Carousels Module
    PRECONDITIONS: 4.Create one Highlight Carousels Module with active event Id/Type Id
    PRECONDITIONS: 5.Check checkbox "Display on Desktop" while creating Highlight Carousels
    PRECONDITIONS: 6.'Highlights Carousel' module should be enabled in CMS > Sports Configs > Structure > Highlight Carousel
    PRECONDITIONS: 7.'Highlights Carousel' module should be be 'Active' in CMS > Sports Pages > Homepage > Highlights Carousel module
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_scroll_the_page_down_to_view_highlights_carousel_section(self):
        """
        DESCRIPTION: Scroll the page down to view 'Highlights Carousel' section
        EXPECTED: User able to see all Highlighst Carousels which are configured in CMS
        """
        pass

    def test_003_verify_displaying_of_the_event_type_idevent_id_in_highlights_carousel_module(self):
        """
        DESCRIPTION: Verify displaying of the event (Type Id/Event Id) in 'Highlights Carousel' module
        EXPECTED: User will be displayed no. of events as configured data in CMS
        """
        pass

    def test_004_verify_right_scroll_bar_is_displayed_when_there_are_more_no_of_events(self):
        """
        DESCRIPTION: Verify Right scroll bar is displayed when there are more no. of events
        EXPECTED: Right scroll bar is seen and able to scroll right side
        EXPECTED: Events on the right side will be displayed
        """
        pass

    def test_005_verify_left_scroll_bars_are_displayed_when_there_are_more_no_of_events(self):
        """
        DESCRIPTION: Verify Left scroll bars are displayed when there are more no. of events
        EXPECTED: Left scroll bar is seen and able to scroll Left side
        EXPECTED: Events on the Left side will be displayed
        """
        pass

    def test_006_verify_right_chevron_is_displayed_for_each_event(self):
        """
        DESCRIPTION: Verify right chevron is displayed for each event
        EXPECTED: clicking on that chevron user can able to navigate to particular event
        """
        pass

    def test_007_click_on_any_selection_from_the_highlight_carousel_events(self):
        """
        DESCRIPTION: Click on any selection from the Highlight carousel events
        EXPECTED: Selection is successfully added to Betslip
        """
        pass

    def test_008_place_a_bet_for_added_selection(self):
        """
        DESCRIPTION: Place a bet for added selection
        EXPECTED: Bet is placed successfully
        """
        pass
