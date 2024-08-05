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
class Test_C28755_TO_BE_UPDATED_stream_icon_S_is_not_shown_for_suspension_Verify_Olympic_Sport_Event_Details_Page_for_In_Play_Events(Common):
    """
    TR_ID: C28755
    NAME: [TO BE UPDATED] (stream icon, S is not shown for suspension): Verify Olympic <Sport> Event Details Page for In-Play Events
    DESCRIPTION: This Test Case verified Olympic <Sport> Event Details Page
    PRECONDITIONS: 1. To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. Event is **In-Play **(live) when:
    PRECONDITIONS: *   **drilldownTagNames="EVFLAG_BL" **(on the Event level)** **
    PRECONDITIONS: *   AND **isMarketBetInRun="true" **(on the any Market level)
    PRECONDITIONS: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
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
        EXPECTED: -It is displayed below the 'Back' button
        EXPECTED: -Event name corresponds to '**name**' attribute
        EXPECTED: -Event name matches with event name on the event section we navigated from
        """
        pass

    def test_007_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify event start date/time
        EXPECTED: -It is displayed below the event name
        EXPECTED: -Event start date corresponds to '**startTime**' attribute
        EXPECTED: -Event start time is shown in** "<name of the day>, DD-Month****-YY. 12 hours AM/PM" **format
        EXPECTED: -Event start date/time matches with date/time on the event section we navigated from
        """
        pass

    def test_008_verify_live_label_or_score(self):
        """
        DESCRIPTION: Verify 'LIVE' label or Score
        EXPECTED: 'LIVE'/Score is displayed next to the Event Start Time if event is live now:
        EXPECTED: 1.  rawIsOffCode="Y"
        EXPECTED: 2.  rawIsOffCode="-" AND isStarted="true"
        """
        pass

    def test_009_verify_stream_label(self):
        """
        DESCRIPTION: Verify 'Stream' label
        EXPECTED: -Stream icon is shown
        EXPECTED: -'Watch Live' tab is present
        EXPECTED: when **'drilldownTagNames'** attribute has one of the following flags: EVFLAG\_AVA, EVFLAG\_PVM, EVFLAG\_IVM, EVFLAG\_RVA, EVFLAG_RPM
        """
        pass

    def test_010_verify_market_tabs(self):
        """
        DESCRIPTION: Verify market tabs
        EXPECTED: -They are displayed below the event details
        EXPECTED: -It is possible to navigate between all market tabs
        EXPECTED: -The 'All markets' tab is first in the list of tabs
        """
        pass

    def test_011_verify_present_market_type_sections(self):
        """
        DESCRIPTION: Verify present market type sections
        EXPECTED: -The first **two **market type sections are expanded by default
        EXPECTED: -The remaining sections are collapsed by default
        EXPECTED: -It is possible to collapse/expand  market type sections by clicking the section's header
        """
        pass

    def test_012_verify_priceodds_buttons_for_selections(self):
        """
        DESCRIPTION: Verify Price/Odds buttons for selections
        EXPECTED: -Price/Odds buttons are shown for every selection
        EXPECTED: -Disabled "S" is shown in case of suspended event/market/outcome
        """
        pass

    def test_013_place_a_bet_on_the_event_from_event_details_page(self):
        """
        DESCRIPTION: Place a bet on the event from Event Details page
        EXPECTED: -Bet is placed successfully
        EXPECTED: -'My Bets' tab is appeared on Event Details page
        EXPECTED: -'Markets' tab is appeared on Event Details page
        """
        pass

    def test_014_repeat_steps_3_13_for(self):
        """
        DESCRIPTION: Repeat steps 3-13 for:
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
