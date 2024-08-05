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
class Test_C28752_TO_BE_UPDATEDVerify_Outright_tab_for_Olympic_Sport(Common):
    """
    TR_ID: C28752
    NAME: [TO BE UPDATED]Verify Outright tab for Olympic Sport
    DESCRIPTION: This Test Case verified Outright tab for Olympic Sport
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: *   BMA-10041 Olympics: Outrights
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
        EXPECTED: *   Olympics page is opened
        EXPECTED: *   Olympics Sports Menu Ribbon is present
        """
        pass

    def test_003_tapsport_icon_on_the_olympics_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Olympics Sports Menu Ribbon
        EXPECTED: *   <Sport> page is opened
        EXPECTED: *  'Events (Fights/Games/Races/Tournaments)'  tab is selected by default (if configured as ON in the CMS)
        """
        pass

    def test_004_outright_tab_is_configured_as_on_in_the_cms(self):
        """
        DESCRIPTION: Outright tab is configured as ON in the CMS
        EXPECTED: 'Outright' tab is present
        """
        pass

    def test_005_tap_outright_tab(self):
        """
        DESCRIPTION: Tap  'Outright' tab
        EXPECTED: *   'Outright' tab is opened
        EXPECTED: *   Type header is displayed
        EXPECTED: *   Events for relevant Type is displayed
        EXPECTED: *   All Type headers is collapsed by default
        """
        pass

    def test_006_verify_sections_collapsingexpanding(self):
        """
        DESCRIPTION: Verify section's collapsing/expanding
        EXPECTED: It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_007_verify_event_section_content(self):
        """
        DESCRIPTION: Verify event section content
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        EXPECTED: *   Label "**LIVE**", if Outright is In-Play
        """
        pass

    def test_008_tap_on_event(self):
        """
        DESCRIPTION: Tap on Event
        EXPECTED: Event Details page is opened
        """
        pass

    def test_009_verify_tab_if_there_are_no_events(self):
        """
        DESCRIPTION: Verify tab if there are no events
        EXPECTED: Message 'No events found' is shown
        """
        pass

    def test_010_place_a_bet_on_outright_event(self):
        """
        DESCRIPTION: Place a bet on Outright event
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_011_outrighttab_is_configured_as_off_in_the_cms(self):
        """
        DESCRIPTION: Outright tab is configured as OFF in the CMS
        EXPECTED: Outright tab is not present
        """
        pass

    def test_012_repeat_steps_3_11_for(self):
        """
        DESCRIPTION: Repeat steps 3-11 for:
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

    def test_013_navigate_to_the_sport_from_the_left_hand_a_z_menu(self):
        """
        DESCRIPTION: Navigate to the <Sport> From the Left Hand A-Z menu
        EXPECTED: <Sport> page is opened
        """
        pass

    def test_014_repeat_steps_4_13(self):
        """
        DESCRIPTION: Repeat steps 4-13
        EXPECTED: 
        """
        pass
