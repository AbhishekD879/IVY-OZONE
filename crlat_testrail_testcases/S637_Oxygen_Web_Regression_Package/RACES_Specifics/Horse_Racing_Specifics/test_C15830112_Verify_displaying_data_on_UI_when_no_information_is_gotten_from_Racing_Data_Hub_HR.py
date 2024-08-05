import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C15830112_Verify_displaying_data_on_UI_when_no_information_is_gotten_from_Racing_Data_Hub_HR(Common):
    """
    TR_ID: C15830112
    NAME: Verify displaying data on UI when no information is gotten from Racing Data Hub (HR)
    DESCRIPTION: This test case verifies that app pages are properly displayed when data from Racing Data Hub is unavailable or partially missing (HR)
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Horse Racing (HR) Racing Data Hub toggle is turned on** : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: ----------------
    PRECONDITIONS: **Racing Data Hub link:**
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com
    PRECONDITIONS: Ladbrokes DEV : ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: categoryKey : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: eventKey : OB Event id
    PRECONDITIONS: i.e. Racing Post information on Ladbrokes Digital for OB event id 5227306:
    PRECONDITIONS: https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/5227306/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: **Data, that should be displayed on UI, is empty (values can be mocked)**
    PRECONDITIONS: --------------------
    PRECONDITIONS: **2 Featured tab modules with 'Select Events by' "RaceTypeID" and "MarketID" should be set**
    PRECONDITIONS: Featured tab modules setting:
    PRECONDITIONS: CMS > Featured Tab Modules > Create Featured Tab Module
    PRECONDITIONS: --------------------
    PRECONDITIONS: **2 Event Hubs featured modules with 'Select Events by' "RaceTypeID" and "MarketID" should be set**
    PRECONDITIONS: Event hub setting:
    PRECONDITIONS: 1. CMS > Sport pages > Event hub (choose or create a new one) > Featured events > Create featured Tab module (e.g, RaceTypeID/MarketID for horses)
    PRECONDITIONS: 2. CMS > Module Ribbon Tab > Add new module ribbon tab  (Directive Name = "Event hub", Event Hub Name - choose the event hub that was created or used in previous step, fill in other fields)
    PRECONDITIONS: -------------------------
    PRECONDITIONS: **Next races should be set:**
    PRECONDITIONS: CMS > System-configuration > NextRaces
    PRECONDITIONS: CMS > Module Ribbon Tab >  NEXT RACES
    PRECONDITIONS: ---------------------
    PRECONDITIONS: **Load Sportsbook App**
    PRECONDITIONS: **Log in as a user with a positive balance (e.g., mincyua/password)**
    """
    keep_browser_open = True

    def test_001_tap_on_horse_racing_icon_from_the_sports_menu_ribbon__open_1_event(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' icon from the Sports Menu Ribbon > Open 1 event
        EXPECTED: * HR Event Details Page is opened
        EXPECTED: * Data are displayed from Horse Racing Data Hub (Dev tool > Network > type [eventid] in search field > find '%-dev1.api.datafabric.dev.%' reques > data on UI correspond to data from the response)
        EXPECTED: * If no data is available, no data is displayed
        """
        pass

    def test_002_tap_on_one_selection__add_to_betslip__place_a_bet(self):
        """
        DESCRIPTION: Tap on one selection > Add to betslip > Place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_003_tap_on_my_bets_button_at_the_header__open_bets_tabsettled_bets_tab(self):
        """
        DESCRIPTION: Tap on 'My bets' button at the header > 'Open bets' tab/'Settled bets' tab
        EXPECTED: * 'My bets' section is opened
        EXPECTED: * 'Cash out' tab is opened by default
        EXPECTED: * Data in all tabs are displayed from Horse Racing Data Hub. If no data is available, no data is displayed
        EXPECTED: (Dev tool > Network > type .. in search field > data on UI correspond to data from the response)
        """
        pass

    def test_004_homepage__featured__find_featured_tab_module_with_events_selected_by_racetypeid(self):
        """
        DESCRIPTION: Homepage > Featured > Find Featured Tab Module with events selected by RaceTypeID
        EXPECTED: Data are displayed from Horse Racing Data Hub. If no data is available, no data is displayed
        EXPECTED: Data are displayed from Racing Data Hub
        EXPECTED: (Check WS)
        """
        pass

    def test_005_homepage__featured__find_featured_tab_module_with_events_selected_by_marketid(self):
        """
        DESCRIPTION: Homepage > Featured > Find Featured Tab Module with events selected by MarketID
        EXPECTED: Data are displayed from Horse Racing Data Hub. If no data is available, no data is displayed
        EXPECTED: Data are displayed from Racing Data Hub
        EXPECTED: (Check WS)
        """
        pass

    def test_006_homepage_tap_on_event_hub_tab_created_in_preconditions(self):
        """
        DESCRIPTION: Homepage. Tap on event hub tab created in preconditions
        EXPECTED: Tab with available featured modules is opened
        """
        pass

    def test_007_check_module_with_events_selected_by_racetypeid(self):
        """
        DESCRIPTION: Check module with events selected by RaceTypeID
        EXPECTED: Data are displayed from Horse Racing Data Hub. If no data is available, no data is displayed
        EXPECTED: Data are displayed from Racing Data Hub
        EXPECTED: (Check WS)
        """
        pass

    def test_008_check_module_with_events_selected_by_marketid(self):
        """
        DESCRIPTION: Check module with events selected by MarketID
        EXPECTED: Data are displayed from Horse Racing Data Hub. If no data is available, no data is displayed
        EXPECTED: Data are displayed from Racing Data Hub
        EXPECTED: (Check WS)
        """
        pass

    def test_009_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: **should be changed**
        EXPECTED: * The 'Next Races' tab is opened
        EXPECTED: * Data are displayed from Horse Racing Data Hub
        EXPECTED: If no data is available, no data is displayed
        EXPECTED: (Dev tool > Network > type .. in search field > data on UI correspond to data from the response)
        """
        pass
