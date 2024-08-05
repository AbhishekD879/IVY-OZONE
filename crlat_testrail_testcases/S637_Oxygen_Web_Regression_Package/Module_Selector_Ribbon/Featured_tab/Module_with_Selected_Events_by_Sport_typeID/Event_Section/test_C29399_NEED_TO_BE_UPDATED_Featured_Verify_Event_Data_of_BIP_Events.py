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
class Test_C29399_NEED_TO_BE_UPDATED_Featured_Verify_Event_Data_of_BIP_Events(Common):
    """
    TR_ID: C29399
    NAME: [NEED TO BE UPDATED] Featured: Verify Event Data of BIP Events
    DESCRIPTION: This test case verifies Event Data of BIP events.
    DESCRIPTION: AUTOTEST: [C2855485]
    PRECONDITIONS: 1. Active Featured module is created in CMS and is displayed on Featured tab. Make sure you have retrieved BIP events in this module.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    PRECONDITIONS: Note: there are no BIP events on Desktop
    """
    keep_browser_open = True

    def test_001_go_to_event_section_of_bip_event(self):
        """
        DESCRIPTION: Go to event section of BIP event
        EXPECTED: **For mobile/tablet:**
        EXPECTED: BIP event is shown within Module just if it has:
        EXPECTED: **Not Outright event:**
        EXPECTED: *   **isMarketBetInRun="true" **(on the Primary Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStarted="true"** AND **rawIsOffCode="-")**
        EXPECTED: **Outright event:**
        EXPECTED: *   **eventSortCode="TNMT"**
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStarted="true"** AND **rawIsOffCode="-")**
        """
        pass

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: *   Event name corresponds to '**name**' attribute OR to <name> set in CMS if name was overridden
        EXPECTED: *   Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        pass

    def test_003_verify_live_label(self):
        """
        DESCRIPTION: Verify LIVE label
        EXPECTED: * LIVE label is shown
        EXPECTED: * Start time of event is not shown
        """
        pass

    def test_004_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: * 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: *   EVFLAG_AVA
        EXPECTED: *   EVFLAG_IVM
        EXPECTED: *   EVFLAG_PVM
        EXPECTED: *   EVFLAG_RVA
        EXPECTED: *   EVFLAG_RPM
        EXPECTED: *   EVFLAG_GVM
        """
        pass

    def test_005_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        pass

    def test_006_tapanywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        pass
