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
class Test_C15830113_Verify_displaying_data_on_UI_when_no_information_is_gotten_from_Racing_Data_Hub_GH(Common):
    """
    TR_ID: C15830113
    NAME: Verify displaying data on UI when no information is gotten from Racing Data Hub (GH)
    DESCRIPTION: This test case verifies that app pages are properly displayed when data from Racing Data Hub is unavailable or partially missing (GH)
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Greyhounds (GH) Racing Data Hub toggle is turned on:**  System-configuration > RacingDataHub > isEnabledForGreyhound = true
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
    PRECONDITIONS: -------------------------
    PRECONDITIONS: **Next races should be set:**
    PRECONDITIONS: CMS > System-configuration > NextRaces
    PRECONDITIONS: CMS > Module Ribbon Tab >  NEXT RACES
    PRECONDITIONS: ---------------------
    PRECONDITIONS: **Load Sportsbook App**
    PRECONDITIONS: **Log in as a user with a positive balance (e.g., mincyua/password)**
    """
    keep_browser_open = True

    def test_001_tap_on_greyhounds_icon_from_the_sports_menu_ribbon_gt_open_1_event(self):
        """
        DESCRIPTION: Tap on 'Greyhounds' icon from the Sports Menu Ribbon &gt; Open 1 event
        EXPECTED: * GH Event Details Page is opened
        EXPECTED: * Data are displayed from GH Data Hub (Dev tool &gt; Network &gt; type [eventid] in search field &gt; find '%-dev1.api.datafabric.dev.%' reques &gt; data on UI correspond to data from the response)
        EXPECTED: * If no data is available, no data is displayed
        """
        pass

    def test_002__tap_on_one_selection_gt_add_to_betslip_gt_place_a_betcoraltap_on_my_bets_button_at_the_header_gt_open_bets_tabsettled_bets_tabladbrokestap_the_balance_button_at_the_header_gt_my_bets_menu_item(self):
        """
        DESCRIPTION: * Tap on one selection &gt; Add to betslip &gt; Place a bet
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on 'My bets' button at the header &gt; 'Open bets' tab/'Settled bets' tab
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap the balance button at the header &gt; 'My bets' menu item
        EXPECTED: * Bet is placed successfully
        EXPECTED: * 'My bets' section is opened
        EXPECTED: * Data in all tabs are displayed from GH Data Hub. If no data is available, no data is displayed
        """
        pass

    def test_003_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: **should be changed**
        EXPECTED: * The 'Next Races' tab is opened
        EXPECTED: * Data are displayed from GH Data Hub
        EXPECTED: If no data is available, no data is displayed
        EXPECTED: (Dev tool &gt; Network &gt; type .. in search field &gt; data on UI correspond to data from the response)
        """
        pass
