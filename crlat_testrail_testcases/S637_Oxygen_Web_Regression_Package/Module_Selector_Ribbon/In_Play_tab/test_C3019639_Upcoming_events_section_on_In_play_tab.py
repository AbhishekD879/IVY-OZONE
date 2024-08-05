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
class Test_C3019639_Upcoming_events_section_on_In_play_tab(Common):
    """
    TR_ID: C3019639
    NAME: Upcoming events section on In-play tab
    DESCRIPTION: This test case verifies the Upcoming section of sports events on In-Play module tab on Homepage.
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: User is on Featured Home page (for example)
    """
    keep_browser_open = True

    def test_001_click_on_in_play_module_ribbon_tab_on_homepage(self):
        """
        DESCRIPTION: Click on In-Play module ribbon tab on Homepage
        EXPECTED: In-Play tab content is loaded
        """
        pass

    def test_002_verify_upcoming_events_section(self):
        """
        DESCRIPTION: Verify Upcoming events section
        EXPECTED: - Upcoming events section is located at the very bottom of the page below the Live events module
        EXPECTED: - Upcoming section has header 'Upcoming events' with the events count (which is updated accordingly to events availability)
        EXPECTED: - Upcoming events section contains Sports accordions (with the events) all in a collapsed state
        """
        pass

    def test_003_click_on_any_sport_accordion_within_this_upcoming_section(self):
        """
        DESCRIPTION: Click on any sport accordion within this Upcoming section
        EXPECTED: Accordion becomes expanded with all the upcoming events of this sport available
        """
        pass

    def test_004_verify_the_content_of_expanded_accordion(self):
        """
        DESCRIPTION: Verify the content of expanded accordion
        EXPECTED: The container has the following components:
        EXPECTED: - Name of the sport as the header
        EXPECTED: - 'SEE ALL' link in the header navigating the user to competition page of that sport - Only for tier 1 sports (Football, Tennis and Basket ball)
        EXPECTED: - Events grouped by type (to be displayed as per the OB display order)
        """
        pass

    def test_005_expand_other_sports_accordions_in_the_upcoming_section(self):
        """
        DESCRIPTION: Expand other sports accordions in the Upcoming section
        EXPECTED: - All sport accordions are expandable with the events of that sport grouped by type
        EXPECTED: - If no events within certain sports are available then no &lt;sport&gt; accordion is displayed in upcoming section
        """
        pass
