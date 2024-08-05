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
class Test_C28753_TO_BE_UPDATED_no_date_filter_for_specials_clickable_event_with_one_selection_live_is_presentVerify_Specials_tab_for_Olympic_Sports(Common):
    """
    TR_ID: C28753
    NAME: [TO BE UPDATED] (no date filter for specials, clickable event with one selection, live is present):Verify Specials tab for Olympic Sports
    DESCRIPTION: This Test Case verified Specials tab for Olympics
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-10417 Olympics: Specials
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
        EXPECTED: -'Events (Fights/Games/Races/Tournaments)'  tab is selected by default (if configured as ON in the CMS)
        """
        pass

    def test_004_specials_tab_is_configured_as_on_in_the_cms(self):
        """
        DESCRIPTION: Specials tab is configured as ON in the CMS
        EXPECTED: 
        """
        pass

    def test_005_sport_specials_are_not_available(self):
        """
        DESCRIPTION: <Sport> Specials are not available
        EXPECTED: Specials tab hidden
        """
        pass

    def test_006_sport_specials_are_available(self):
        """
        DESCRIPTION: <Sport> Specials are available
        EXPECTED: Specials tab is present
        """
        pass

    def test_007_tap_on_specials_tab(self):
        """
        DESCRIPTION: Tap on 'Specials' tab
        EXPECTED: -Specials tab is opened
        EXPECTED: -Specials tab is displayed all available <Sport> Specials
        EXPECTED: -'Specials' events is displayed within Competition header
        EXPECTED: -Each Event within a Competition header is ordered by Start date and time
        EXPECTED: -Specials tab contain a Date Filter (Today, Tomorrow, Future) header
        """
        pass

    def test_008_verify_sections_collapsingexpanding(self):
        """
        DESCRIPTION: Verify section's collapsing/expanding
        EXPECTED: -The first header is expanded by default
        EXPECTED: -The remaining headers are collapsed by default
        EXPECTED: -‘+’ icon is present on Competitions (Type ID) header
        EXPECTED: -It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_009_sport_special_event_contains_only_one_selection(self):
        """
        DESCRIPTION: <Sport> Special Event contains only one selection
        EXPECTED: -Selection name is displayed with odds
        EXPECTED: -Special Event is not clickable
        """
        pass

    def test_010_sport_special_event_is_in_play(self):
        """
        DESCRIPTION: <Sport> Special Event is In-Play
        EXPECTED: In-Play Special Event isn't displayed within Specials tab
        """
        pass

    def test_011_tap_on_the_selection_name(self):
        """
        DESCRIPTION: Tap on the selection name
        EXPECTED: Event details page of that Special is opened
        """
        pass

    def test_012_place_a_bet_on_special_event(self):
        """
        DESCRIPTION: Place a bet on Special event
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_013_specials_tab_is_configured_as_offin_the_cms(self):
        """
        DESCRIPTION: Specials tab is configured as OFF in the CMS
        EXPECTED: Specials tab is not present
        """
        pass

    def test_014_repeat_steps_3_14_for(self):
        """
        DESCRIPTION: Repeat steps 3-14 for:
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

    def test_015_navigate_to_the_sport_from_the_left_hand_a_z_menu(self):
        """
        DESCRIPTION: Navigate to the <Sport> From the Left Hand A-Z menu
        EXPECTED: <Sport> page is opened
        """
        pass

    def test_016_repeat_steps_4_14(self):
        """
        DESCRIPTION: Repeat steps 4-14
        EXPECTED: 
        """
        pass
