import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.mobile_only
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
        self.site.home.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
        self.site.wait_content_state_changed(timeout=10)

    def test_002_verify_upcoming_events_section(self):
        """
        DESCRIPTION: Verify Upcoming events section
        EXPECTED: - Upcoming events section is located at the very bottom of the page below the Live events module
        EXPECTED: - Upcoming section has header 'Upcoming events' with the events count (which is updated accordingly to events availability)
        EXPECTED: - Upcoming events section contains Sports accordions (with the events) all in a collapsed state
        """
        upcoming = self.site.home.tab_content.upcoming
        upcoming_events = upcoming.items_as_ordered_dict
        self.assertTrue(upcoming_events, msg='No upcoming events found')
        upcoming_header = upcoming.upcoming_header
        self.assertEqual(upcoming_header.text_label, vec.inplay.UPCOMING_EVENTS_SECTION,
                         msg=f'Actual section name "{upcoming_header.text_label}" is not same as'
                             f' Expected section name "{vec.inplay.UPCOMING_EVENTS_SECTION}"')
        self.assertTrue(upcoming_header.events_count_label.is_displayed(),
                        msg='Upcoming section counter is not displayed')
        for sport_name, sport in upcoming_events.items():
            self.assertFalse(sport.is_expanded(), msg=f'{sport.name} sport accordion is not collapsed')
            sport.expand()
            sleep(2)
            self.assertTrue(sport.is_expanded(), msg=f'{sport.name} sport accordion is not expanded')
            # Sport Should Be Expanded
            if sport.is_expanded():
                events = sport.items_as_ordered_dict
                self.assertTrue(events, msg='no events found under sport')
            # Event Name Contains String "SEE ALL" which does not match expected
            # Removed String "SEE ALL" From Event Name
            actual_sport = sport.name.replace('SEE ALL', "").strip()
            self.assertEqual(sport_name.strip(), actual_sport, msg=f'Actual title "{actual_sport}" '
                                                         f'is not same as Expected title "{sport_name}"')
            if sport.name in ['FOOTBALL', 'TENNIS', 'BASKETBALL']:
                self.assertTrue(sport.has_show_more_leagues_button(),
                                msg=f'see all link is not present for the sport {sport.name}')

    def test_003_click_on_any_sport_accordion_within_this_upcoming_section(self):
        """
        DESCRIPTION: Click on any sport accordion within this Upcoming section
        EXPECTED: Accordion becomes expanded with all the upcoming events of this sport available
        """
        # covered in step 002

    def test_004_verify_the_content_of_expanded_accordion(self):
        """
        DESCRIPTION: Verify the content of expanded accordion
        EXPECTED: The container has the following components:
        EXPECTED: - Name of the sport as the header
        EXPECTED: - 'SEE ALL' link in the header navigating the user to competition page of that sport - Only for tier 1 sports (Football, Tennis and Basket ball)
        EXPECTED: - Events grouped by type (to be displayed as per the OB display order)
        """
        # covered in step 002

    def test_005_expand_other_sports_accordions_in_the_upcoming_section(self):
        """
        DESCRIPTION: Expand other sports accordions in the Upcoming section
        EXPECTED: - All sport accordions are expandable with the events of that sport grouped by type
        EXPECTED: - If no events within certain sports are available then no <sport> accordion is displayed in upcoming section
        """
        # covered in step 002
