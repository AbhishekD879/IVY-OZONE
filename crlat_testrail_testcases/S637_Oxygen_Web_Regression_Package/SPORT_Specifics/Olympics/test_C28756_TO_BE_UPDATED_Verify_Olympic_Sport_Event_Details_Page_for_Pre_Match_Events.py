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
class Test_C28756_TO_BE_UPDATED_Verify_Olympic_Sport_Event_Details_Page_for_Pre_Match_Events(Common):
    """
    TR_ID: C28756
    NAME: [TO BE UPDATED] Verify Olympic <Sport> Event Details Page for Pre-Match Events
    DESCRIPTION: This Test Case verified Olympic <Sport> Event Details Page for Pre-Match Events
    PRECONDITIONS: 1. To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: *
    PRECONDITIONS: **JIRA Ticket:**
    PRECONDITIONS: BMA-10264 Olympics: Event Detail Page
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
        EXPECTED: -'Events (Fights/Games/Races/Tournaments)' tab is selected by default (if configured as ON in the CMS)
        """
        pass

    def test_004_tapevent_name_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event name on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify back button
        EXPECTED: Back button is displayed on the top of Event Details Page
        """
        pass

    def test_006_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: -It is displayed below the back button
        EXPECTED: -Event name corresponds to '**name**' attribute
        EXPECTED: -Event name matches with event name on the event section we navigated from
        """
        pass

    def test_007_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify event start date/time
        EXPECTED: -It is displayed below the event name
        EXPECTED: -Event start date corresponds to '**startTime**' attribute
        EXPECTED: -Event start date is shown in** '<name of the day>, DD-MMM-YY. 12 hours AM/PM'** format
        EXPECTED: -Event start date/time matches with date/time on the event section we navigated from
        """
        pass

    def test_008_verify_market_tabs(self):
        """
        DESCRIPTION: Verify market tabs
        EXPECTED: -They are displayed below the event details
        EXPECTED: -It is possible to navigate between all market tabs
        EXPECTED: -The 'All markets' tab is first in the list of tabs
        """
        pass

    def test_009_verify_priceodds_buttons_for_selections(self):
        """
        DESCRIPTION: Verify Price/Odds buttons for selections
        EXPECTED: -Price/Odds buttons are shown for every selection
        EXPECTED: -Disabled "S" is shown in case of suspended event/market/outcome
        """
        pass

    def test_010_place_a_bet_on_the_event_from_event_details_page(self):
        """
        DESCRIPTION: Place a bet on the event from Event Details page
        EXPECTED: -Bet is placed successfully
        EXPECTED: -'My Bets' tab is appeared on Event Details page
        EXPECTED: -'Markets' tab is appeared on Event Details page
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
