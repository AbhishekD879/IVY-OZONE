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
class Test_C28751_TO_BE_UPDATEDVefiry_In_Play_tab_for_Olympics_if_there_are_no_events(Common):
    """
    TR_ID: C28751
    NAME: [TO BE UPDATED]Vefiry In-Play tab for Olympics if there are no events
    DESCRIPTION: This Test Case verified In-Play tab for Olympics if there are no events
    PRECONDITIONS: There are no events to show on Olympics '<Sport>' In-Play tab.
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
        EXPECTED: -'Events (Fights/Games/Races/Tournaments)'  tab is selected by default (if configured as ON in the CMS)
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

    def test_006_verify_selected_by_default_sorting_type(self):
        """
        DESCRIPTION: Verify selected by default sorting type
        EXPECTED: -'Live Now' filter is selected by default if there are available Live Now events
        EXPECTED: -'Upcoming' filter is selected by default if there are no Live Now events, but there are available Upcoming events
        """
        pass

    def test_007_verify_message_presence_on_live_now_view(self):
        """
        DESCRIPTION: Verify message presence on 'Live Now' view
        EXPECTED: **'There are currently no Live events available' **message is shown if there are no Live Now events
        """
        pass

    def test_008_verify_message_presence_on_upcoming_view(self):
        """
        DESCRIPTION: Verify message presence on 'Upcoming' view
        EXPECTED: **'There are currently no upcoming Live events available' **message is shown if there are no Upcoming events
        """
        pass

    def test_009_verify_message_presence_on_in_play_page(self):
        """
        DESCRIPTION: Verify message presence on 'In-Play' page
        EXPECTED: -'Upcoming' filter is selected by default if there are no events at all
        EXPECTED: **-'**There are currently no upcoming Live events available**' **message is shown if there are no events at all
        """
        pass

    def test_010_in_play_tab_is_configured_as_off_in_the_cms(self):
        """
        DESCRIPTION: In-Play tab is configured as OFF in the CMS
        EXPECTED: In-Play tab is not present
        """
        pass

    def test_011_repeat_steps_3_10_for(self):
        """
        DESCRIPTION: Repeat steps 3-10 for:
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

    def test_012_navigate_to_the_sport_from_the_left_hand_a_z_menu(self):
        """
        DESCRIPTION: Navigate to the <Sport> From the Left Hand A-Z menu
        EXPECTED: <Sport> page is opened
        """
        pass

    def test_013_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps 4-11
        EXPECTED: 
        """
        pass
