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
class Test_C28441_Old_FunctionalityVerify_Sticky_Header_on_Event_View(Common):
    """
    TR_ID: C28441
    NAME: [Old Functionality]Verify Sticky Header on Event View
    DESCRIPTION: This test case verifies sticky header on event view according the story **BMA-4501** Implement sticky headers on Event View and Market View
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-9146 'Apply new design to Outrights and Enhanced Multiples'
    PRECONDITIONS: **NOTE** :
    PRECONDITIONS: *   for Football Sport only, Outright' tab is removed from the module header into 'Competition Module Header' within 'Matches' tab
    PRECONDITIONS: *   make sure that there is enough quantity of events within the sections to execute this test case
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is selected by default
        """
        pass

    def test_003_go_to_the_expanded_section_or_expand_collapsed_one(self):
        """
        DESCRIPTION: Go to the expanded section or expand collapsed one
        EXPECTED: 
        """
        pass

    def test_004_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: 
        """
        pass

    def test_005_verify_section_header(self):
        """
        DESCRIPTION: Verify section header
        EXPECTED: The section header is always stuck on the top of the page until the next header reaches the top and sticks instead
        """
        pass

    def test_006_go_tooutrighs_events_page(self):
        """
        DESCRIPTION: Go to **'Outrighs' **Events page
        EXPECTED: **'Outrighs' **Events page is opened
        """
        pass

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: 
        """
        pass

    def test_008_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap **'In-Play' **tab
        EXPECTED: **'In-Play' **tab is opened
        """
        pass

    def test_009_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: 
        """
        pass
