import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C66039859_Verify_the_display_of_the_Onboarding_tutorial_for_a_user_for_the_first_time_when_user_navigates_to_the_Horse_racing_event_details_page(Common):
    """
    TR_ID: C66039859
    NAME: Verify the display of the Onboarding tutorial for a user for the first time when user navigates to the Horse racing event details page.
    DESCRIPTION: This test case evaluates the display of the onboarding tutorial for My Stable when user will access the Horse racing event details page (Win or Each Way market tab)
    PRECONDITIONS: CMS configurations
    PRECONDITIONS: My Stable Menu item
    PRECONDITIONS: My Stable Configurations
    PRECONDITIONS: Checkbox against ‘Active Mystable’ - Should be checked in
    PRECONDITIONS: Checkbox against ‘Mystable Horses Running Today Carousel’ - Should be checked in
    PRECONDITIONS: Checkbox against ‘Active Antepost’ - Should be checked in
    PRECONDITIONS: Checkbox against ‘Active My Bets’ (Phase 2)
    PRECONDITIONS: My Stable Entry Point
    PRECONDITIONS: Entry Point SVG Icon - (Mystable-Entry-Point-White)
    PRECONDITIONS: Entry Point Label  - Ladbrokes (Stable Mates)/ Coral (My Stable)
    PRECONDITIONS: Edit Or Save My Stable
    PRECONDITIONS: Edit Stable Svg Icon - (Mystable-Entry-Point-Dark)
    PRECONDITIONS: Edit Stable Label - (Edit Stable)
    PRECONDITIONS: Save Stable Svg Icon - ( Mystable-Entry-Point-White)
    PRECONDITIONS: Save Stable Label -(Done)
    PRECONDITIONS: Edit Note Svg Icon - (Mystable-Edit-Note)
    PRECONDITIONS: Bookmark Svg Icon -(bookmarkfill)
    PRECONDITIONS: InProgress Bookmark Svg icon -(Mystable-Inprogress-Bookmark)
    PRECONDITIONS: Unbookmark Svg Icon -(bookmark)
    PRECONDITIONS: Empty My Stable
    PRECONDITIONS: Empty Stable Sag Icon - Mystable-Stable-Signposting
    PRECONDITIONS: Empty Stable Header Label - Empty Stable
    PRECONDITIONS: Empty Stable Message Label - Tap on ‘Edit Stable’ on the Race Card to add a horse
    PRECONDITIONS: Empty Stable CTA Label - View my horses
    PRECONDITIONS: My Stable Signposting
    PRECONDITIONS: Signposting Svg Icon - Mystable-Stable-Signposting
    PRECONDITIONS: Notes Signposting Svg Icon-Mystable-Note-Signposting
    PRECONDITIONS: Your Horses Running Today Carousel
    PRECONDITIONS: Carousel Icon - Mystable-Entry-Point-Dark
    PRECONDITIONS: Carousel Name - Your horses running today!
    PRECONDITIONS: Error Message Popups
    PRECONDITIONS: Maximum Horses Exceed Message - Maximum number of  selections reached. To add more, remove horses from your stable.
    """
    keep_browser_open = True

    def test_000_navigate_to_the_horse_racing_landing_page_without_logging_in(self):
        """
        DESCRIPTION: Navigate to the Horse racing landing page without logging in.
        EXPECTED: The Stream and bet pop should be displayed first.My Stable On-boarding tutorial should not show up in this instance.
        """
        pass

    def test_000_login_to_the_application_and_navigate_to_the_horse_racing_event_details_page_and_check_for_the_my_stable_on_boarding_tutorial(self):
        """
        DESCRIPTION: Login to the application and navigate to the Horse racing event details page and check for the My Stable On-boarding tutorial.
        EXPECTED: 1. The My Stable On-boarding tutorial should show up in the first instance when user navigates to the HR EDP(Win or Each way tab).
        EXPECTED: 2. If the user views the Stream and Bet tutorial then he will be not be able to view the My Stable tutorial unless he navigates to any other tab or page and comes back to the HR EDP (Each Way tab) if the user hasn't viewed the My Stable Onboarding before.
        EXPECTED: ![](index.php?/attachments/get/891e32b4-f3d4-456f-8da9-ea54997cadd0)
        EXPECTED: Note: The other existing pop up's will continue to show up like the current existing behaviour.(Odd's boost, Free bets etc)
        """
        pass
