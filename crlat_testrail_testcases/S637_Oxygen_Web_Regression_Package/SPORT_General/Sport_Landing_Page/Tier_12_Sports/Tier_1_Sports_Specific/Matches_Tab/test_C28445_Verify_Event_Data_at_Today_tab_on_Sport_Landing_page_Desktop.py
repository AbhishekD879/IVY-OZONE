import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28445_Verify_Event_Data_at_Today_tab_on_Sport_Landing_page_Desktop(Common):
    """
    TR_ID: C28445
    NAME: Verify Event Data at 'Today' tab on <Sport> Landing page: Desktop
    DESCRIPTION: This test case verifies event data at 'Today' tab on <Sport> Landing page for Desktop/tablet
    DESCRIPTION: AUTOTEST [C9698719]
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sport_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page from the 'Left Navigation' menu
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches': Today tab is opened by default
        """
        pass

    def test_003_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to **name** attribute
        EXPECTED: *   Event name is displayed in the following format:
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        EXPECTED: **For Desktop:**
        EXPECTED: <Team1/Player1> v <Team2/Player2>
        """
        pass

    def test_004_verify_favourite_icon(self):
        """
        DESCRIPTION: Verify 'Favourite' icon
        EXPECTED: 'Favourite' icon is displayed on the left side, before event name
        """
        pass

    def test_005_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start Time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   Event Start Time is shown below event name
        EXPECTED: *   For events that occur Today date format is 24 hours:
        EXPECTED: **HH:MM, Today** (e.g. "14:00 or 05:00, Today")
        """
        pass

    def test_006_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: * EVFLAG_AVA
        EXPECTED: * EVFLAG_IVM
        EXPECTED: * EVFLAG_PVM
        EXPECTED: * EVFLAG_RVA
        EXPECTED: * EVFLAG_RPM
        EXPECTED: * EVFLAG_GVM
        EXPECTED: * 'Watch live' icon/text is displayed next to event start time
        EXPECTED: * 'Watch live' icon and text are displayed for mobile/tablet, icon only is shown for desktop
        """
        pass

    def test_007_clicktapanywhere_on_event_section_except_priceodds_button(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section (except 'Price/Odds' button)
        EXPECTED: Event Details Page is opened
        """
        pass
