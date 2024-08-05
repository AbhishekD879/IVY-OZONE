import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C65968981_Verify_the_display_of_the_Golf_Matches_tab(Common):
    """
    TR_ID: C65968981
    NAME: Verify the display of the Golf  Matches tab
    DESCRIPTION: This test case verifies the display of the Golf Matches tab when events are available.
    PRECONDITIONS: 1. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf
    PRECONDITIONS: 2. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration
    PRECONDITIONS: 3. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration-&gt; Active/Inactive sport
    PRECONDITIONS: 4. There should be events available with 2 Ball Betting and 3 Ball Betting Markets present.
    """
    keep_browser_open = True

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application.
        EXPECTED: The application should be launched successfully.
        """
        pass

    def test_002_select_the_golf_sport_either_from_the_sports_ribbon_or_through_the_a_z_menu(self):
        """
        DESCRIPTION: Select the Golf Sport either from the sports ribbon or through the A-Z menu.
        EXPECTED: User should be redirected to the Golf sport landing page.
        """
        pass

    def test_003_select_the_matches_tab(self):
        """
        DESCRIPTION: Select the Matches tab
        EXPECTED: The Matches tab should be loaded successfully.
        EXPECTED: Events with 2 ball &amp; 3 ball betting markets should be displayed in this tab.
        EXPECTED: Outright events should not be displayed in the Matches tab.
        """
        pass

    def test_004_verify_that_the_matches_tab_is_not_displayed_in_the_fe_when_there_are_no_events_with_2_ball_or_3_ball_markets(self):
        """
        DESCRIPTION: Verify that the Matches tab is not displayed in the FE when there are no events with 2 Ball or 3 Ball markets.
        EXPECTED: The Matches tab should not be displayed in FE if there are no events with 2 Ball or 3 Ball markets.
        """
        pass

    def test_005_add_the_selections_from_the_matches_tab_and_place_the_bets(self):
        """
        DESCRIPTION: Add the selections from the Matches tab and place the bets.
        EXPECTED: User should be able to add selections to bet slip and place bets successfully.
        """
        pass
