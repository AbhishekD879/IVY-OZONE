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
class Test_C3019572_Verify_Navigation_to_Competition_Page_through_See_all_link_on_Tier_1_Sport_Landing_page(Common):
    """
    TR_ID: C3019572
    NAME: Verify Navigation to Competition Page through 'See all' link on Tier 1 Sport Landing page
    DESCRIPTION: This test case verifies navigation from Matches tab of sport landing page to Competitions page when user clicks on 'See all' link in the type header.
    PRECONDITIONS: The list of sports that are tier I/II/III is available here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: Upcoming events are available for sports Tier 1
    PRECONDITIONS: User is on Sport landing page that is tier 1
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: Football Matches tab is opened
        """
        pass

    def test_002_in_the_upcoming_module_click_on_see_all_link_in_any_type_header(self):
        """
        DESCRIPTION: In the 'Upcoming' module click on 'See all' link in any type header
        EXPECTED: User is redirected to Football Competitions page to the exact league where the 'See all' link was placed
        """
        pass

    def test_003_navigate_to_baseball_landing_page_that_is_tier_3(self):
        """
        DESCRIPTION: Navigate to Baseball landing page (that is tier 3)
        EXPECTED: Baseball Matches tab is opened
        """
        pass

    def test_004_in_the_upcoming_module_find_see_all_link(self):
        """
        DESCRIPTION: In the 'Upcoming' module find 'See all' link
        EXPECTED: There is no 'See all' link for sports that are tier 3
        """
        pass

    def test_005_repeat_above_steps_1_2_for_other_sports_that_are_tier_1(self):
        """
        DESCRIPTION: Repeat above steps (1-2) for other sports that are tier 1
        EXPECTED: On Basketball/Tennis landing pages each time user clicks on 'See all' link he is always redirected to Competition page: exact league
        """
        pass
