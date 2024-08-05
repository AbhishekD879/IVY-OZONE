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
class Test_C44870203_Verify_that_user_is_able_to_see_the_next_races_carousel_that_is_scrollable_Each_event_displays_the_venue_time_and_name_and_three_selections_with_statistics_silks_names_and_odds_the_elapsed_time_link_to_EDP_and_all_data_is_updated_Check_that(Common):
    """
    TR_ID: C44870203
    NAME: "Verify that user is able to see the next races carousel that is scrollable. Each event displays the venue (time and name and three selections with statistics, silks, names and odds) the elapsed time, link to EDP and all data is updated. Check that
    DESCRIPTION: "Verify that user is able to see the next races carousel that is scrollable. Each event displays the venue (time and name and three selections with statistics, silks, names and odds) the elapsed time, link to EDP and all data is updated. Check that  Event drop off when starts.
    DESCRIPTION: Verify that user is able to see Surface Bet as per backend settings, ll data is correct and complete, and link navigates user to EDP. User is able to click on navigation arrow and its scrollable"
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_race_landing_page_and_verify(self):
        """
        DESCRIPTION: Navigate to Horse Race Landing page and verify.
        EXPECTED: The Next races carousel is displayed and it is scroll-able.
        """
        pass

    def test_002_verify_for_each_event_displayed_in_the_next_races_carousel(self):
        """
        DESCRIPTION: Verify for each event displayed in the next races carousel.
        EXPECTED: Each event displays the venue (time and name and three selections with statistics, silks, names and odds) the elapsed time and link to EDP.
        """
        pass

    def test_003_verify_when_an_event_starts(self):
        """
        DESCRIPTION: Verify when an event starts.
        EXPECTED: The event drops off from the next races carousel.
        """
        pass

    def test_004_configure_a_surface_bet_in_cms_and_verify(self):
        """
        DESCRIPTION: Configure a surface bet in CMS and verify.
        EXPECTED: User is able to see Surface Bet as per backend settings, all data is correct and complete, and link navigates user to EDP. User is able to click on navigation arrow and its scrollable
        """
        pass

    def test_005_repeat_steps_1_4_for_greyhounds(self):
        """
        DESCRIPTION: Repeat steps 1-4 for Greyhounds.
        EXPECTED: The result is same as in steps 1-4
        """
        pass
