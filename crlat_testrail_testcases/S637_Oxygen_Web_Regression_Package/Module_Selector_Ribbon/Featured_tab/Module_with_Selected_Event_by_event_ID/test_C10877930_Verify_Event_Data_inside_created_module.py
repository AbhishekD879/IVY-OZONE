import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C10877930_Verify_Event_Data_inside_created_module(Common):
    """
    TR_ID: C10877930
    NAME: Verify Event Data inside created module
    DESCRIPTION: This test case verifies Event Data inside the created module
    PRECONDITIONS: 1. Active Featured module is created in CMS by sport Sport Event ID (not Outright Event with primary market) and displayed on Featured tab.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_001_navigate_to_the_configured_module_and_event_inside_module(self):
        """
        DESCRIPTION: navigate to the configured module and Event inside module
        EXPECTED: Configured Event is shown inside the created module.
        """
        pass

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: * Event name corresponds to **name** attribute
        EXPECTED: * Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        pass

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   For events that occur Today date format is 24 hours: for **Coral**: **HH:MM, Today** (e.g. "14:00 or 05:00, Today"), for **Ladbrokes**: **HH:MM Today** (e.g. "14:00 or 05:00 Today")
        EXPECTED: *   For events that occur in the future (including tomorrow) date format is 24 hours: for **Coral**: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov), for **Ladbrokes**: **HH:MM DD MMM** (e.g. 14:00 or 05:00 24 Nov or 02 Nov)
        """
        pass

    def test_004_verify_watch_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch' icon and label
        EXPECTED: * 'Watch' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: *   EVFLAG_AVA
        EXPECTED: *   EVFLAG_IVM
        EXPECTED: *   EVFLAG_PVM
        EXPECTED: *   EVFLAG_RVA
        EXPECTED: *   EVFLAG_RPM
        EXPECTED: *   EVFLAG_GVM
        """
        pass

    def test_005_for_coral_verify_favourites_icon(self):
        """
        DESCRIPTION: for **Coral**: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        pass

    def test_006_tapanywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        pass
