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
class Test_C15830107_Feature_Toggle_for_Racing_Data_Hub_on_UI_for_Horse_Racing_Switched_off(Common):
    """
    TR_ID: C15830107
    NAME: Feature Toggle for Racing Data Hub on UI for Horse Racing (Switched off)
    DESCRIPTION: This test case verifies that information from Racing Data Hub (Horse Racing HR) on UI can be switched off in CMS
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Horse Racing (HR) Racing Data Hub toggle is turned off** : System-configuration > RacingDataHub > isEnabledForHorseRacing = false
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: ----------------
    PRECONDITIONS: **Racing Data Hub link:**
    PRECONDITIONS: Coral DEV : https://sb-api.coral.co.uk (old one:cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com)
    PRECONDITIONS: Ladbrokes DEV : https://sb-api.ladbrokes.com (old one: ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com)
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: categoryKey : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: eventKey : OB Event id
    PRECONDITIONS: i.e. Racing Post information on Ladbrokes Digital for OB event id 229312956:
    PRECONDITIONS: https://sb-api.ladbrokes.com/v4/sportsbook-api/categories/21/events/229312956/content?locale=en-GB&api-key=LD755f5f6b195b4688969e7e976df86855
    PRECONDITIONS: **Open bet link:** http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: --------------------
    PRECONDITIONS: **2 Featured tab modules with 'Select Events by' "RaceTypeID" and "MarketID" should be set**
    PRECONDITIONS: Featured tab modules setting:
    PRECONDITIONS: CMS > Featured Tab Modules > Create Featured Tab Module
    PRECONDITIONS: --------------------
    PRECONDITIONS: **2 Event Hubs featured modules with 'Select Events by' "RaceTypeID" and "MarketID" should be set**
    PRECONDITIONS: Event hub setting:
    PRECONDITIONS: 1. CMS > Sport pages > Event hub (choose or create a new one) > Featured events > Create featured Tab module (e.g, RaceTypeID/MarketID for horses)
    PRECONDITIONS: 2. CMS > Module Ribbon Tab > Add new module ribbon tab  (Directive Name = "Event hub", Event Hub Name - choose the event hub that was created or used in previous step, fill in other fields)
    PRECONDITIONS: For Featured functionality, try to find events that have different elements depending on RacingDataHub is switched on/off. Look at attached screenshot
    PRECONDITIONS: -------------------------
    PRECONDITIONS: **Next races should be set:**
    PRECONDITIONS: CMS > System-configuration > NextRaces
    PRECONDITIONS: CMS > Module Ribbon Tab > NEXT RACES
    PRECONDITIONS: ---------------------
    PRECONDITIONS: **Load Sportsbook App**
    PRECONDITIONS: **Log in as a user with a positive balance (e.g., mincyua/password)**
    """
    keep_browser_open = True

    def test_001_tap_on_horse_racing_icon_from_the_sports_menu_ribbon__open_1_event(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' icon from the Sports Menu Ribbon > Open 1 event
        EXPECTED: * HR Event Details Page is opened
        EXPECTED: * Data are displayed from Openbet
        EXPECTED: (Dev tool > Network > type [eventid] in search field > find request https://backoffice-tst2.coral.co.uk > data on UI correspond to data from the response)
        EXPECTED: In openbet request for event, there are 'racingForm: outcome' and 'racingForm: events' parameters
        """
        pass

    def test_002__tap_on_one_selection__add_to_betslip__place_a_betcoraltap_on_my_bets_button_at_the_header__open_bets_tabsettled_bets_tabladbrokestap_the_balance_button_at_the_header__my_bets_menu_item(self):
        """
        DESCRIPTION: * Tap on one selection > Add to betslip > Place a bet
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on 'My bets' button at the header > 'Open bets' tab/'Settled bets' tab
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap the balance button at the header > 'My bets' menu item
        EXPECTED: * Bet is placed successfully
        EXPECTED: * 'My bets' section is opened
        EXPECTED: * Data in all tabs are displayed from Openbet
        """
        pass

    def test_003_homepage__featured__find_featured_tab_module_with_events_selected_by_racetypeid(self):
        """
        DESCRIPTION: Homepage > Featured > Find Featured Tab Module with events selected by RaceTypeID
        EXPECTED: Data are displayed from Openbet
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > data in **racingFormEvent** module is taken from Openbet
        """
        pass

    def test_004_homepage__featured__find_featured_tab_module_with_events_selected_by_marketid(self):
        """
        DESCRIPTION: Homepage > Featured > Find Featured Tab Module with events selected by MarketID
        EXPECTED: Data are displayed from Openbet
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > data in **racingFormEvent** module is taken from Openbet
        """
        pass

    def test_005_homepage_tap_on_event_hub_tab_created_in_preconditions(self):
        """
        DESCRIPTION: Homepage. Tap on event hub tab created in preconditions
        EXPECTED: Tab with available featured modules is opened
        """
        pass

    def test_006_check_module_with_events_selected_by_racetypeid(self):
        """
        DESCRIPTION: Check module with events selected by RaceTypeID
        EXPECTED: Data are displayed from Openbet
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > data in **racingFormEvent** module is taken from Openbet
        """
        pass

    def test_007_check_module_with_events_selected_by_marketid(self):
        """
        DESCRIPTION: Check module with events selected by MarketID
        EXPECTED: Data are displayed from Openbet
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > data in **racingFormEvent** module is taken from Openbet
        """
        pass

    def test_008_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * The 'Next Races' tab is opened
        EXPECTED: * Data are displayed from Openbet
        """
        pass

    def test_009_tap_on_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: * GH Event Details Page is opened
        EXPECTED: * Data are displayed from GH Racing Data Hub
        EXPECTED: (Dev tool > Network > type [eventid] in search field > find '%sb-api%' request > data on UI correspond to data from the response)
        """
        pass
