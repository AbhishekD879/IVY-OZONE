import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C14253862_Event_hub_Verify_module_created_by_Sport_Primary_market_ID(Common):
    """
    TR_ID: C14253862
    NAME: Event hub: Verify module created by <Sport> Primary market ID
    DESCRIPTION: This test case verifies featured events module created by <Sport> Primary Market ID on Event hub
    DESCRIPTION: Autotest: [C58428336] cannot configure Event hub module on prod cms
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Event created in TI with Primary market available. Markets supported:
    PRECONDITIONS: -  Match Betting,
    PRECONDITIONS: -  Match Results,
    PRECONDITIONS: -  Extra Time Result,
    PRECONDITIONS: -  Extra-Time Result,
    PRECONDITIONS: -  Penalty Shoot-Out Winner,
    PRECONDITIONS: -  To Qualify
    PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 4. Featured module by Primary Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 5. Appropriate Module Ribbon Tab should be created for Event Hub
    PRECONDITIONS: 6. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_001_navigate_to_module_from_preconditions_make_sure_its_expanded_and_verify_its_contents(self):
        """
        DESCRIPTION: Navigate to Module from preconditions. Make sure it's expanded and verify it's contents
        EXPECTED: * Module name corresponds to Name set in CMS
        """
        pass

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: * Event name corresponds to name attribute
        EXPECTED: * Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        pass

    def test_003_verify_fixture_header_and_price_buttons(self):
        """
        DESCRIPTION: Verify Fixture header and price buttons
        EXPECTED: * Fixture header depends on Market template:
        EXPECTED: - Home/Draw/Away
        EXPECTED: - 1/2
        EXPECTED: * Price buttons contain prices set in TI
        """
        pass

    def test_004_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: Event start time corresponds to startTime attribute:
        EXPECTED: - 'Live' label is shown for in-play event
        EXPECTED: - For events that occur Today date format is 24 hours: HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: - For events that occur in the future (including tomorrow) date format is 24 hours: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        pass

    def test_005_verify_watch_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch' icon and label
        EXPECTED: 'Watch' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        pass

    def test_006_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        pass

    def test_007_verify__more_link(self):
        """
        DESCRIPTION: Verify '№ more' link
        EXPECTED: * '№ more' link present under price buttons in case there are more than 1 market in this event
        """
        pass

    def test_008_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        pass
