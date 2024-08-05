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
class Test_C28757_TO_BE_UPDATEDVerify_Matches_tab_for_Olympic_Sport(Common):
    """
    TR_ID: C28757
    NAME: [TO BE UPDATED]Verify Matches tab for Olympic Sport
    DESCRIPTION: This Test Case verified Events tab for Olympic Sport
    PRECONDITIONS: **JIRA Ticket:**
    PRECONDITIONS: BMA-10039 Olympics: Events/Matches
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_olympics_page(self):
        """
        DESCRIPTION: Navigate to the Olympics page
        EXPECTED: -Olympics page is opened
        EXPECTED: -Olympics Sports Menu Ribbon is present
        """
        pass

    def test_003_tapsport_icon_on_the_olympics_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Olympics Sports Menu Ribbon
        EXPECTED: -<Sport> page is opened
        """
        pass

    def test_004_events_tab_is_configured_as_on_in_the_cms(self):
        """
        DESCRIPTION: Events tab is configured as ON in the CMS
        EXPECTED: -'Events (Fights/Games/Races/Tournaments)' tab is present
        EXPECTED: -'Events (Fights/Games/Races/Tournaments)' tab is opened by default
        EXPECTED: -'Events (Fights/Games/Races/Tournaments)' tab include Daily slider
        EXPECTED: -Type headers is displayed
        EXPECTED: -Events for relevant Type is displayed
        EXPECTED: -First three Type headers is expanded by default
        """
        pass

    def test_005_verify_daily_slider(self):
        """
        DESCRIPTION: Verify 'Daily slider'
        EXPECTED: Daily Slider is displayed with the following options:
        EXPECTED: *   Today (selected by default)
        EXPECTED: *   Tomorrow
        EXPECTED: *   Future
        """
        pass

    def test_006_verify_content_of_todaytomorrowfuture_tabs_on_daily_slider(self):
        """
        DESCRIPTION: Verify content of Today/Tomorrow/Future tabs on Daily Slider
        EXPECTED: When the user selects an option from the daily slider, the system will display the relevant events for the time period selected
        """
        pass

    def test_007_verify_type_headers_titles(self):
        """
        DESCRIPTION: Verify Type header's titles
        EXPECTED: The Type header titles are in the format:
        EXPECTED: **Category-League** **Name**
        """
        pass

    def test_008_verify_sections_collapsingexpanding(self):
        """
        DESCRIPTION: Verify section's collapsing/expanding
        EXPECTED: It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_009_verify_event_section(self):
        """
        DESCRIPTION: Verify Event section
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        EXPECTED: *   **Event Start Time**
        EXPECTED: *   Link** '(+ <markets number>)'** if event has more than one market
        EXPECTED: *   **Stream icon **(if event has streaming available)
        EXPECTED: *   **Price/Odd** buttons (disabled "S" is shown in case of suspended event/market/outcome)
        """
        pass

    def test_010_place_a_bet_on_the_event(self):
        """
        DESCRIPTION: Place a bet on the event
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_011_verify_events_tab_if_no_events_are_available(self):
        """
        DESCRIPTION: Verify 'Events' tab if no Events are available
        EXPECTED: 'No events found' message is displayed
        """
        pass

    def test_012_eventstab_is_configured_as_off_in_the_cms(self):
        """
        DESCRIPTION: 'Events' tab is configured as OFF in the CMS
        EXPECTED: 'Events' tab is not present
        """
        pass

    def test_013_repeat_steps_3_12_for(self):
        """
        DESCRIPTION: Repeat steps 3-12 for:
        EXPECTED: *   Archery
        EXPECTED: *   Athletics
        EXPECTED: *   Badminton
        EXPECTED: *   Basketball
        EXPECTED: *   Beach Volleyball
        EXPECTED: *   Boxing
        EXPECTED: *   Canoeing
        EXPECTED: *   Cycling
        EXPECTED: *   Diving
        EXPECTED: *   Equestrian
        EXPECTED: *   Fencing
        EXPECTED: *   Football
        EXPECTED: *   Golf
        EXPECTED: *   Gymnastics
        EXPECTED: *   Handball
        EXPECTED: *   Hockey
        EXPECTED: *   Judo
        EXPECTED: *   Pentathlon
        EXPECTED: *   Rowing
        EXPECTED: *   Rugby Sevens
        EXPECTED: *   Sailing
        EXPECTED: *   Shooting
        EXPECTED: *   Swimming
        EXPECTED: *   Syn Swimming
        EXPECTED: *   Table Tennis
        EXPECTED: *   Taekwondo
        EXPECTED: *   Tennis
        EXPECTED: *   Triathlon
        EXPECTED: *   Volleyball
        EXPECTED: *   Water Polo
        EXPECTED: *   Weight Lifting
        EXPECTED: *   Wrestling
        """
        pass

    def test_014_navigate_to_the_sport_from_the_left_hand_a_z_menu(self):
        """
        DESCRIPTION: Navigate to the <Sport> From the Left Hand A-Z menu
        EXPECTED: <Sport> page is opened
        """
        pass

    def test_015_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps 4-13
        EXPECTED: 
        """
        pass
