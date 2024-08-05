import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C1684306_Verify_layout_of_Build_Your_Own_Racecard_page(Common):
    """
    TR_ID: C1684306
    NAME: Verify layout of 'Build Your Own Racecard' page
    DESCRIPTION: This test case verifies layout of 'Build Your Own Racecard' page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'Horse Racing' Landing page -> 'Featured' tab
    PRECONDITIONS: 3. Click on 'Build a Racecard' button in 'Build Your Own Racecard' section that is located at the top of the main view below tabs
    PRECONDITIONS: 4. Tick at least one checkbox before 'Event off time' tab
    PRECONDITIONS: 5. Click on 'Build Your Own Racecard' button (Selected Race card should be displayed on 'Build Your Own Racecard' page)
    PRECONDITIONS: To get info about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYY?translationLang=en&racingForm=outcome&racingForm=event
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - event ID
    """
    keep_browser_open = True

    def test_001_verify_races_subheader(self):
        """
        DESCRIPTION: Verify 'Races' subheader
        EXPECTED: * 'Back' button is displayed on the left side of subheader
        EXPECTED: * 'Horse Racing' inscription is displayed next to 'Back' button
        EXPECTED: * 'Meeting' selector is NOT displayed at the subheader
        EXPECTED: * 'Bet Filter' and 'New' icon is displayed at the right side of subheader
        """
        pass

    def test_002_verify_displaying_of_breadcrumbs_trail(self):
        """
        DESCRIPTION: Verify displaying of Breadcrumbs trail
        EXPECTED: * Breadcrumbs are located below the 'Races' subheader
        EXPECTED: * Breadcrumbs are displayed in the next format: 'Home' > 'Horse Racing' > 'Build Your Own Racecard'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined on mouse hover over
        """
        pass

    def test_003_verify_event_details_section(self):
        """
        DESCRIPTION: Verify 'Event details' section
        EXPECTED: Event details section contains:
        EXPECTED: * Event name (corresponds to attribute **'name'** in SS response)
        EXPECTED: * Event off time (taken from attribute **'name'** and corresponds to the race local time)
        EXPECTED: * Date (for tomorrow and future events only) in the format: 'Tuesday 22nd May' (attribute **'startTime'**)
        EXPECTED: * Race Event Status e.g. 'Going GOOD' (attribute **'going'** within **'racingFormEvent'** section)
        EXPECTED: * Distance in the format: 'Distance: Xm Yf Zy' (attribute **'distance'**)
        EXPECTED: * Countdown timer (shown only for events with Race start time less then or equal to 45 minutes)
        """
        pass

    def test_004_verify_displaying_of_markets_tabs(self):
        """
        DESCRIPTION: Verify displaying of Markets tabs
        EXPECTED: * Market tabs are displayed below 'Event details' section
        EXPECTED: * The next tabs are displayed in the following order:
        EXPECTED: * 'Win Or E/W' tab
        EXPECTED: * 'Forecast' tab
        EXPECTED: * 'Tricast' Tab
        EXPECTED: * 'Win Only' tab
        EXPECTED: * 'Betting WO' tab
        EXPECTED: * 'To Finish' tab
        EXPECTED: * 'Top Finish' tab
        EXPECTED: * 'Place Insurance' tab
        EXPECTED: * 'More Markets' tab
        EXPECTED: * 'Totepool' Tab
        EXPECTED: * Navigation arrows appear when hovering the mouse over Market tabs if they do not fit on the page
        """
        pass

    def test_005_verify_displaying_of_selected_race_card(self):
        """
        DESCRIPTION: Verify displaying of Selected Race card
        EXPECTED: Selected Race card is displayed below Market tabs
        """
        pass

    def test_006_verify_displying_of_watch_free_widget(self):
        """
        DESCRIPTION: Verify displying of 'Watch Free' widget
        EXPECTED: **For Coral:**
        EXPECTED: * 'Watch Free' widget is displayed in 3-rd column for >= 1280px resolution and below main content area for < 1280px resolution
        EXPECTED: * 'Watch Free' header is collapsible/expandable
        EXPECTED: **For Ladbrokes:**
        EXPECTED: * 'Watch Free' widget is NOT displayed
        """
        pass

    def test_007_repeat_steps_from_preconditions_and_verify_that_build_your_own_racecard_page_is_opened_but_tick_several_checkboxes_before_event_off_time_tab(self):
        """
        DESCRIPTION: Repeat steps from preconditions and verify that 'Build Your Own Racecard' page is opened but tick several checkboxes before 'Event off time' tab
        EXPECTED: * 'Build Your Own Racecard' page is opened
        EXPECTED: * Selected multiple race cards are displayed one after another,  separated by 'Event details' sections
        """
        pass

    def test_008_verify_order_of_selected_multiple_race_cards(self):
        """
        DESCRIPTION: Verify order of selected multiple race cards
        EXPECTED: * Selected multiple race cards are ordered by start date and time in ascending i.e. starting from earliest one
        EXPECTED: * In case start time is identical, alphabetically
        """
        pass

    def test_009_repeat_steps_5_7_for_each_selected_race_card(self):
        """
        DESCRIPTION: Repeat steps 5-7 for each selected race card
        EXPECTED: 
        """
        pass
