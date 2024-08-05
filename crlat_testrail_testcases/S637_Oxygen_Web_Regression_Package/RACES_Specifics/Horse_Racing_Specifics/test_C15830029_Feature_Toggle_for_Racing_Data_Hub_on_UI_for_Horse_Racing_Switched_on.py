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
class Test_C15830029_Feature_Toggle_for_Racing_Data_Hub_on_UI_for_Horse_Racing_Switched_on(Common):
    """
    TR_ID: C15830029
    NAME: Feature Toggle for Racing Data Hub on UI for Horse Racing (Switched on)
    DESCRIPTION: This test case verifies that information from Racing Data Hub (Horse Racing HR) on UI can be switched on in CMS
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Horse Racing (HR) Racing Data Hub toggle is turned on** : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned off: System-configuration > RacingDataHub > isEnabledForGreyhound = false
    PRECONDITIONS: CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT** via **devlog** function)
    PRECONDITIONS: ----------------
    PRECONDITIONS: **Racing Data Hub link:**
    PRECONDITIONS: - ___Coral DEV___ : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: - ___Ladbrokes DEV___ : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: https://sb-api-stg.coral.co.uk/v4/sportsbook-api/categories/21/events/13137995/content?locale=en-GB&api-key=CDd2396372409341029e905faba611713
    PRECONDITIONS: - ___Vanila___: https://sb-api-stg.coral.co.uk/v4/sportsbook-api/categories/21/events/13137995/content?locale=en-GB&api-key=CDd2396372409341029e905faba611713
    PRECONDITIONS: - ___URI___ : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: **Open bet link:**
    PRECONDITIONS: - ___VANILLA___: - BETA: https://ss-aka-ori-dub.coral.co.uk/openbet-ssviewer/Drilldown/2.31/Class?translationLang=en&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: - ___TST2___: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: --------------------
    PRECONDITIONS: **Two Featured tab modules with 'Select Events by' "RaceTypeID" and "MarketID" should be set**
    PRECONDITIONS: Make Featured tab modules setting:
    PRECONDITIONS: CMS > Featured Tab Modules > Create Featured Tab Module
    PRECONDITIONS: Featured events enabled on Home page:
    PRECONDITIONS: sports pages > homepage > featured events > active
    PRECONDITIONS: --------------------
    PRECONDITIONS: **Two Event Hubs featured modules with 'Select Events by' "RaceTypeID" and "MarketID" should be created and set**
    PRECONDITIONS: ___How to create Event hub and make the right setting___:
    PRECONDITIONS: 1. Go to and create: CMS > Sport pages > Event hub (choose or create a new one) > Featured events > Create featured Tab module (e.g, RaceTypeID/MarketID for horses)
    PRECONDITIONS: 2. Go to and create: CMS > Module Ribbon Tab > Add new module ribbon tab  (Directive Name = "Event hub", Event Hub Name - choose the event hub that was created or used in previous step, fill in other fields)
    PRECONDITIONS: -------------------------
    PRECONDITIONS: **Next races should be set:**
    PRECONDITIONS: CMS > System-configuration > NextRaces
    PRECONDITIONS: CMS > System-configuration > NextRacesToggle (if available)
    PRECONDITIONS: CMS > Module Ribbon Tab >  NEXT RACES
    PRECONDITIONS: ---------------------
    PRECONDITIONS: **Load Sportsbook App**
    PRECONDITIONS: **Log in as a user with a positive balance (e.g., mincyua/password)**
    """
    keep_browser_open = True

    def test_001_tap_on_horse_racing_icon_from_the_sports_menu_ribbon__open_any_event_open_any_resulted_event(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' icon from the Sports Menu Ribbon >
        DESCRIPTION: * Open any event
        DESCRIPTION: * Open any resulted event
        EXPECTED: * HR Event Details Page is opened
        EXPECTED: * Data are displayed from Horse Racing Data Hub
        EXPECTED: (Dev tool > Network > type [eventid] in search field > find "sb-api"/"datafabric" request (via search) > data on UI correspond to data from the response):
        EXPECTED: ***Coral:***
        EXPECTED: **Mobile, Desktop**
        EXPECTED: - Header area: Distance; Going; Racing Post Verdict.
        EXPECTED: - Runner area: Silks; Jockey; Trainer; Form; Runner Number; Draw; Option to see more details (when expanded: RPR, Age, Weight, Spotlight are displayed)
        EXPECTED: For resulted event: Silks; Jockey; Trainer; Runner Number
        EXPECTED: Note: if Aggregational MS is not available, Generic Silks (Greyed Out Silks) are displayed
        EXPECTED: ***Ladbrokes:***
        EXPECTED: - Header area: Race Title, Race Type, Going (Soft / Heavy /Good / Standard etc), Distance, Racing Post Verdict (Desktop: Course map (Desktop Map))
        EXPECTED: - Runner area: The 'SHOW MORE ⋁':
        EXPECTED: **Mobile:** Runner Age, Runner Weight, RPR, Runner Comment, CD/C/BF (if a course winner and/or if a beaten favorite), Star Rating
        EXPECTED: **Desktop:**
        EXPECTED: Runner Age, Runner Weight, RPR, Runner Comment, CD/C/BF (if a course winner and/or if a beaten favorite), Star Rating (aligned to the right), Detailed Form
        EXPECTED: * In openbet request for event there are no 'racingForm: outcome' and 'racingForm: events' parameters (Query String Parameters) and such info is absent in the response (look attachment EDP.DF)
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
        EXPECTED: * Data in all tabs are displayed from Horse Racing Data Hub
        """
        pass

    def test_003_homepage__featured__find_featured_tab_module_with_events_selected_by_racetypeid(self):
        """
        DESCRIPTION: Homepage > Featured > Find Featured Tab Module with events selected by RaceTypeID
        EXPECTED: Data are displayed from Horse Racing Data Hub:
        EXPECTED: -Jockey Name
        EXPECTED: -Trainer Name
        EXPECTED: -Silks
        EXPECTED: -Forms
        EXPECTED: -Runner Number
        EXPECTED: -Draw
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > racingFormEvent module is present (in case event has Distance or Going attributes in DF response)
        """
        pass

    def test_004_homepage__featured__find_featured_tab_module_with_events_selected_by_marketid(self):
        """
        DESCRIPTION: Homepage > Featured > Find Featured Tab Module with events selected by MarketID
        EXPECTED: Data are displayed from Horse Racing Data Hub:
        EXPECTED: -Jockey Name
        EXPECTED: -Trainer Name
        EXPECTED: -Silks
        EXPECTED: -Forms
        EXPECTED: -Runner Number
        EXPECTED: -Draw
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > racingFormEvent module is present (in case event has Distance or Going attributes in DF response)
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
        EXPECTED: Data are displayed from Horse Racing Data Hub:
        EXPECTED: -Jockey Name
        EXPECTED: -Trainer Name
        EXPECTED: -Silks
        EXPECTED: -Forms
        EXPECTED: -Runner Number
        EXPECTED: -Draw
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > racingFormEvent module is present (in case event has Distance or Going attributes in DF response)
        """
        pass

    def test_007_check_module_with_events_selected_by_marketid(self):
        """
        DESCRIPTION: Check module with events selected by MarketID
        EXPECTED: Data are displayed from Horse Racing Data Hub:
        EXPECTED: -Jockey Name
        EXPECTED: -Trainer Name
        EXPECTED: -Silks
        EXPECTED: -Forms
        EXPECTED: -Runner Number
        EXPECTED: -Draw
        EXPECTED: In Devtools WebSocket > Featured MS in FEATURED_STRUCTURE_CHANGED message > modules > EventsModule > data > racingFormEvent module is present (in case event has Distance or Going attributes in DF response)
        """
        pass

    def test_008_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * The 'Next Races' tab is opened
        EXPECTED: * Data are displayed from Racing Data Hub
        """
        pass

    def test_009_tap_on_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: * GH Event Details Page is opened
        EXPECTED: * Data are displayed from Openbet
        EXPECTED: * In openbet link for event there are 'racingForm: outcome' and 'racingForm: events' parameters (Query String Parameters) and such info is present in the response
        EXPECTED: * Racing Data Hub request ('%-dev1.api.datafabric.dev.%') is absent
        """
        pass
