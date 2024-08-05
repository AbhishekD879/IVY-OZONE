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
class Test_C14253856_Event_Hub_Verify_Event_Data_inside_module_created_by_Event_ID(Common):
    """
    TR_ID: C14253856
    NAME: Event Hub: Verify Event Data inside module created by Event ID.
    DESCRIPTION: This test case verifies Event Data inside the created module
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Active Featured module is created in CMS by Sport Event ID (not Outright Event with primary market) for Event Hub.
    PRECONDITIONS: 3. Module Ribbon Tab is created for Event Hub
    PRECONDITIONS: 4. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: In order to check event data use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_001_navigate_to_the_configured_event_hub_module_and_event_inside_the_module(self):
        """
        DESCRIPTION: Navigate to the configured Event Hub module and Event inside the module
        EXPECTED: Configured Event is shown inside the created module.
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

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: * Event start time corresponds to startTime attribute
        EXPECTED: * For events that occur Today date format is 24 hours: HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: * For events that occur in the future (including tomorrow) date format is 24 hours: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        pass

    def test_004_verify_watch_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch' icon and label
        EXPECTED: * 'Watch' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: * EVFLAG_AVA
        EXPECTED: * EVFLAG_IVM
        EXPECTED: * EVFLAG_PVM
        EXPECTED: * EVFLAG_RVA
        EXPECTED: * EVFLAG_RPM
        EXPECTED: * EVFLAG_GVM
        """
        pass

    def test_005_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        pass

    def test_006_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        pass
