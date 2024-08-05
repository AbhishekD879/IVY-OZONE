import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C44870190_Verify_tennis_journey(Common):
    """
    TR_ID: C44870190
    NAME: Verify tennis journey
    DESCRIPTION: 
    PRECONDITIONS: "Site is loaded,
    """
    keep_browser_open = True

    def test_001_tapclick_on_tennis_button_from_the_main_menu(self):
        """
        DESCRIPTION: Tap/Click on Tennis button from the Main Menu
        EXPECTED: Tennis Page is loaded
        EXPECTED: The 'Matches' tab is selected by default
        EXPECTED: The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: All events which are available are displayed for the League
        EXPECTED: Enhanced Multiple events (if available) are displayed on the top of the list and is expanded (**For Mobile/Tablet**) Enhanced Multiple events (if available) are displayed as carousel above tabs (**For Desktop**)
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel (**For Desktop**)
        """
        pass

    def test_002_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: The 'In-Play' tab is loaded with the 'Live Now'/'Upcoming' sections
        EXPECTED: The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content (**For Desktop**)
        """
        pass

    def test_003_tapclick_on_the_competition_tab(self):
        """
        DESCRIPTION: Tap/Click on the Competition tab
        EXPECTED: Event types are displayed.
        EXPECTED: Click any event type, Matches/ Outright tabs are displayed.
        """
        pass

    def test_004_tapclick_on_back_button_and_then_tapclick_on_outright_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Back' button and then tap/click on 'Outright' tab
        EXPECTED: The 'Outrights' tab is loaded
        EXPECTED: Leagues and Competitions are all collapsed by default
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content (**For Desktop**)
        """
        pass
