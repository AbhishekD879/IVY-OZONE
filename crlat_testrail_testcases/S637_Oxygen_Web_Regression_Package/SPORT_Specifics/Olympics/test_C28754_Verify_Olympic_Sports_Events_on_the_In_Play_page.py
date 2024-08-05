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
class Test_C28754_Verify_Olympic_Sports_Events_on_the_In_Play_page(Common):
    """
    TR_ID: C28754
    NAME: Verify Olympic Sports Events on the In-Play page
    DESCRIPTION: This Test Case verified Olympic Sports Events on the In-Play page
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-10266 In Play: Olympic Sports
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_in_play_page(self):
        """
        DESCRIPTION: Navigate to the In-Play page
        EXPECTED: -'**In-Play**' Landing Page is opened
        EXPECTED: -'**All Sports**' icon is selected by default
        EXPECTED: -Olympic <Sport> icon is present in the Sports Menu Ribbon
        EXPECTED: -Olympic <Sport> header is present on the 'All Sports' page
        """
        pass

    def test_003_verify_sorting_types(self):
        """
        DESCRIPTION: Verify sorting types
        EXPECTED: -Two sorting type buttons are visible: 'Live Now' and 'Upcoming'
        EXPECTED: -'Live Now is selected by default
        """
        pass

    def test_004_verify_live_now_view(self):
        """
        DESCRIPTION: Verify 'Live Now' view
        EXPECTED: -Olympic <Sport> Category header is displayed
        EXPECTED: -Events for relevant Type is displayed
        """
        pass

    def test_005_verify_upcoming_view(self):
        """
        DESCRIPTION: Verify 'Upcoming' view
        EXPECTED: -Olympic <Sport> Category header is displayed
        EXPECTED: -Events for relevant Type is displayed
        """
        pass

    def test_006_verify_categoryheader_title(self):
        """
        DESCRIPTION: Verify Category header title
        EXPECTED: The Category header titles are in the format:
        EXPECTED: **Category  Name**
        """
        pass

    def test_007_verify_type_headers_titles(self):
        """
        DESCRIPTION: Verify Type header's titles
        EXPECTED: The Type header titles are in the format:
        EXPECTED: **League** **Name**
        """
        pass

    def test_008_verify_sections_collapsingexpanding(self):
        """
        DESCRIPTION: Verify section's collapsing/expanding
        EXPECTED: It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_009_verify_olympic_live_events_when_live_now_is_selected(self):
        """
        DESCRIPTION: Verify Olympic Live events when 'Live Now' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        EXPECTED: *   **Elapsed time + ****Score **(if commentaries are available)
        EXPECTED: *   '**LIVE'** label (if commentaries are not available)
        EXPECTED: *   Link** '(+ <markets number>)'** if event has more than one market
        EXPECTED: *   **Stream icon **(if event has streaming available)
        EXPECTED: *   **Price/Odd** buttons (disabled "S" is shown in case of suspended event/market/outcome)
        """
        pass

    def test_010_verify_olympics_outright_events_when_live_now_is_selected(self):
        """
        DESCRIPTION: Verify Olympics Outright events when 'Live Now' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        EXPECTED: *   '**LIVE'** label
        """
        pass

    def test_011_verify_olympics_in_play_events_when_upcoming_is_selected(self):
        """
        DESCRIPTION: Verify Olympics In-Play events when 'Upcoming' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Start time**
        EXPECTED: *   **Event Name**
        EXPECTED: *   Link** '(+ <markets number>)'** if event has more than one market
        EXPECTED: *   **Stream icon **(if event has streaming available)
        EXPECTED: *   **Price/Odd** buttons (disabled "S" is shown in case of suspended event/market/outcome)
        """
        pass

    def test_012_verify_olympics_outright_events_when_upcoming_is_selected(self):
        """
        DESCRIPTION: Verify Olympics Outright events when 'Upcoming' is selected
        EXPECTED: Event section consists of:
        EXPECTED: *   **Event Name**
        """
        pass

    def test_013_tap_on_event(self):
        """
        DESCRIPTION: Tap on Event
        EXPECTED: Event Details page is opened
        """
        pass

    def test_014_repeat_steps_2_13_for(self):
        """
        DESCRIPTION: Repeat steps 2-13 for:
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
