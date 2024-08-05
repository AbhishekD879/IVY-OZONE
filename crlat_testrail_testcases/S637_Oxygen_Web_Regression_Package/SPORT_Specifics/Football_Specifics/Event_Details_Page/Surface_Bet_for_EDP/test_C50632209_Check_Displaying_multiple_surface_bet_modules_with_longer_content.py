import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C50632209_Check_Displaying_multiple_surface_bet_modules_with_longer_content(Common):
    """
    TR_ID: C50632209
    NAME: [Check] Displaying multiple surface  bet modules with longer content.
    DESCRIPTION: This test case is a check for reocurring issue with Surface Bet Modules.
    PRECONDITIONS: Prepare 3 or more Surface Bet Modules with longer content that will be displayed together (eg. on one Event Details Page). Add Icons to each Surface Bet Module
    PRECONDITIONS: Example content:
    PRECONDITIONS: Title: Surface Bet Title Module
    PRECONDITIONS: Content: Ben Stokes to be Top Eng 1st Inns Runscorer end Engalnd to win the Match
    PRECONDITIONS: Content: Stokes to hit 2+ Sixes, take 2+ Wickets and take 2+ Catches in the Match
    PRECONDITIONS: Content: Stokes to score a Century and England to win Match
    PRECONDITIONS: or any other with similar amount of words
    """
    keep_browser_open = True

    def test_001__this_should_be_checked_on_different_screen_sizes__13_15_17go_to_the_edp_where_surface_bet_modules_are_displayed_and_check_if_they_are_displayed_correctly(self):
        """
        DESCRIPTION: _This should be checked on different screen sizes_: 13", 15", 17"
        DESCRIPTION: Go to the EDP where Surface Bet Modules are displayed and check if they are displayed correctly.
        EXPECTED: Titles and Content are displayed correctly, price button stays within Surface Bet Module borders
        """
        pass
