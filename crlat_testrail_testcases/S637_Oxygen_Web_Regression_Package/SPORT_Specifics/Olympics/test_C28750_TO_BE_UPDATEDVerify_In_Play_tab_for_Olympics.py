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
class Test_C28750_TO_BE_UPDATEDVerify_In_Play_tab_for_Olympics(Common):
    """
    TR_ID: C28750
    NAME: [TO BE UPDATED]Verify In-Play tab for Olympics
    DESCRIPTION: This Test Case verified In-Play tab for Olympics
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-10037 Olympics: In Play
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
        EXPECTED: [TO BE UPDATED] -'Events (Fights/Games/Races/Tournaments)'  tab is selected by default (if configured as ON in the CMS)
        """
        pass

    def test_004_in_play_tab_is_configured_as_on_in_the_cms(self):
        """
        DESCRIPTION: In-Play tab is configured as ON in the CMS
        EXPECTED: In-Play tab is present
        """
        pass

    def test_005_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap  'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_006_verify_sorting_types(self):
        """
        DESCRIPTION: Verify sorting types
        EXPECTED: -Two sorting type buttons are visible: 'Live Now' and 'Upcoming'
        EXPECTED: -'Live Now is selected by default
        """
        pass

    def test_007_verify_live_now_view(self):
        """
        DESCRIPTION: Verify 'Live Now' view
        EXPECTED: -Type header is displayed
        EXPECTED: -Events for relevant Type is displayed
        EXPECTED: -First Type header is expanded by default
        """
        pass

    def test_008_verify_upcoming_view(self):
        """
        DESCRIPTION: Verify 'Upcoming' view
        EXPECTED: -Type header is displayed
        EXPECTED: -Events for relevant Type is displayed
        EXPECTED: -First Type header is expanded by default
        """
        pass

    def test_009_verify_type_headers_titles(self):
        """
        DESCRIPTION: Verify Type header's titles
        EXPECTED: The Type header titles are in the format:
        EXPECTED: **Category-League** **Name**
        """
        pass

    def test_010_verify_sections_collapsingexpanding(self):
        """
        DESCRIPTION: Verify section's collapsing/expanding
        EXPECTED: It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_011_verify_live_event_section_when_live_now_is_selected(self):
        """
        DESCRIPTION: Verify Live event section when 'Live Now' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        EXPECTED: *   **Elapsed time + ****Score **(if commentaries are available)
        EXPECTED: *   '**LIVE'** label (if commentaries are not available)
        EXPECTED: *   Link** '(+ <markets number>)'** if event has more than one market
        EXPECTED: *   **Stream icon **(if event has streaming available)
        EXPECTED: *   **Price/Odd** buttons (disabled "S" is shown in case of suspended event/market/outcome)
        """
        pass

    def test_012_verify_outright_event_section_when_live_now_is_selected(self):
        """
        DESCRIPTION: Verify Outright event section when 'Live Now' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        EXPECTED: *   '**LIVE'** label
        """
        pass

    def test_013_verify_in_play_event_section_when_upcoming_is_selected(self):
        """
        DESCRIPTION: Verify In-Play event section when 'Upcoming' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Start time**
        EXPECTED: *   **Event Name**
        EXPECTED: *   Link** '(+ <markets number>)'** if event has more than one market
        EXPECTED: *   **Stream icon **(if event has streaming available)
        EXPECTED: *   **Price/Odd** buttons (disabled "S" is shown in case of suspended event/market/outcome)
        """
        pass

    def test_014_verify_outright_event_section_when_upcoming_is_selected(self):
        """
        DESCRIPTION: Verify Outright event section when 'Upcoming' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        """
        pass

    def test_015_tap_on_event(self):
        """
        DESCRIPTION: Tap on Event
        EXPECTED: Event Details page is opened
        """
        pass

    def test_016_in_play_tab_is_configured_as_off_in_the_cms(self):
        """
        DESCRIPTION: In-Play tab is configured as OFF in the CMS
        EXPECTED: In-Play tab is not present
        """
        pass

    def test_017_repeat_steps_1_16_for(self):
        """
        DESCRIPTION: Repeat steps 1-16 for:
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

    def test_018_navigate_to_the_sport_from_the_left_hand_a_z_menu(self):
        """
        DESCRIPTION: Navigate to the <Sport> From the Left Hand A-Z menu
        EXPECTED: <Sport> page is opened
        """
        pass

    def test_019_repeat_steps_4_17(self):
        """
        DESCRIPTION: Repeat steps 4-17
        EXPECTED: 
        """
        pass
