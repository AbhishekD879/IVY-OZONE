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
class Test_C9770238_Archived_from_102_Coral_and_Ladbrokes_Single_view_of_landing_page(Common):
    """
    TR_ID: C9770238
    NAME: [Archived from 102 Coral and Ladbrokes] Single view of landing page
    DESCRIPTION: This test case verifies the Tier 3 Sport landing page content
    DESCRIPTION: **It will be archived from 102 Coral and Ladbrokes**
    PRECONDITIONS: The list of sports that are tier I/II/III is available here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: User is on home page
    """
    keep_browser_open = True

    def test_001_click_on_sport_icon_of_tier_3_type_sport_in_menu_ribbon(self):
        """
        DESCRIPTION: Click on sport icon of Tier 3 type sport in menu ribbon
        EXPECTED: User is redirected to &lt;sport&gt; single view page
        """
        pass

    def test_002_check_the_view_of_landing_page(self):
        """
        DESCRIPTION: Check the view of landing page
        EXPECTED: - No sub tabs 'Today/Tomorrow/Future'
        EXPECTED: - All events are displayed in separate modules like: In-Play/Upcoming/Outright/Specials/Coupons/etc. (if available)
        EXPECTED: - Types accordions (Each Type should act as a separate header i.e. La Liga below last Premier league event)
        EXPECTED: - Events with standard event cards
        EXPECTED: - If no events are available for the definite section than message 'No events found' is displayed
        EXPECTED: - No 'See all' links are displayed on the single view page as user should see all the available events on one page.
        """
        pass

    def test_003_navigate_to_another_tier_3_sport(self):
        """
        DESCRIPTION: Navigate to another tier 3 sport
        EXPECTED: Same view is displayed as described above
        """
        pass
