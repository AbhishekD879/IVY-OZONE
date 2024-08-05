import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C64055799_GALAXY_S9_Featured_Verify_Event_Data_of_Pre_Match_Events(Common):
    """
    TR_ID: C64055799
    NAME: [GALAXY S9] Featured: Verify Event Data of Pre-Match Events
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001___________create_test_prematch_event(self):
        """
        DESCRIPTION: *          Create test prematch event
        EXPECTED: *          Football event and featured module were created
        """
        pass

    def test_002___________go_to_event_section_of_pre_match_event(self):
        """
        DESCRIPTION: *          Go to event section of Pre-Match event
        EXPECTED: *          Event is shown
        """
        pass

    def test_003___________verify_event_name(self):
        """
        DESCRIPTION: *          Verify Event name
        EXPECTED: *          * Event name corresponds to **name** attribute OR to **name** set in CMS if it was overridden
        EXPECTED: *          * Event name is displayed in two lines:
        EXPECTED: *          <Team1/Player1>
        EXPECTED: *          <Team2/Player2>
        """
        pass

    def test_004___________verify_event_start_time(self):
        """
        DESCRIPTION: *          Verify Event Start time
        EXPECTED: *          *   Event start time corresponds to **startTime** attribute
        EXPECTED: *          *   Event Start Time is shown below event name
        EXPECTED: *          *   For events that occur Today date format is 24 hours: for Coral: HH:MM, Today (e.g. "14:00 or 05:00, Today"), for Ladbrokes: HH:MM Today (e.g. "14:00 or 05:00 Today")
        EXPECTED: *          *   For events that occur in the future (including tomorrow) date format is 24 hours: for Coral: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov), for Ladbrokes: HH:MM DD MMM (e.g. 14:00 or 05:00 24 Nov or 02 Nov)
        """
        pass

    def test_005___________verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: *          Verify 'Watch Live' icon and label
        EXPECTED: *          * 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: *          *   EVFLAG_AVA
        EXPECTED: *          *   EVFLAG_IVM
        EXPECTED: *          *   EVFLAG_PVM
        EXPECTED: *          *   EVFLAG_RVA
        EXPECTED: *          *   EVFLAG_RPM
        EXPECTED: *          *   EVFLAG_GVM
        """
        pass

    def test_006___________verify_cash_out_label(self):
        """
        DESCRIPTION: *          Verify 'CASH OUT' label
        EXPECTED: *          'CASH OUT' label is not shown on module header
        """
        pass

    def test_007___________verify_favourites_icon(self):
        """
        DESCRIPTION: *          Verify 'Favourites' icon
        EXPECTED: *          'Favourites' icon is displayed only for Football events within Module section
        """
        pass

    def test_008___________tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: *          Tap anywhere on Event section (except for price buttons)
        EXPECTED: *          Event Details Page is opened
        """
        pass
