import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C874371_Verify_Featured_Module_adding_by_Race_Type_ID_HL_TEST2(Common):
    """
    TR_ID: C874371
    NAME: Verify Featured Module adding by Race Type ID [HL/TEST2]
    DESCRIPTION: AUTOTESTS [C9698181] [C9690230]
    DESCRIPTION: **LADBROKES Design (MOBILE)**
    DESCRIPTION: ![](index.php?/attachments/get/31784991)
    DESCRIPTION: **CORAL Design (MOBILE)**
    DESCRIPTION: ![](index.php?/attachments/get/31784992)
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Featured' tab/section
    PRECONDITIONS: **Configurations**
    PRECONDITIONS: 1) For creating the module in the 'Featured' tab/section by HR/Greyhound Type ID (Race Type Id) via CMS use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=126685715
    PRECONDITIONS: 2) For reaching the appropriate CMS per env use the following link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "EventsModule" an choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32612728)
    PRECONDITIONS: 2) Cashout icon is displayed only on CORAL Desktop
    PRECONDITIONS: 3) Virtual sports (HR, HR Jumps, Grand National, GH) are also applicable to be displayed within featured module created by RaceTypeID, so this test case should check them as well.
    PRECONDITIONS: **Pay attention:**
    PRECONDITIONS: - Agreed with Adam Smith that Previous Odds functionality is not applied for Featured module for now (user can see previous odds appears under Price/Odds button if during live price update Feature module was active but in all other cases previous odds won't be displayed)
    PRECONDITIONS: - To implement Previous Odd to be displayed on Featured module changes should be made for featured microservice (no an issue according to comment in https://jira.egalacoral.com/browse/BMA-19508)
    """
    keep_browser_open = True

    def test_001_verify_created_module_on_featured_tabsection(self):
        """
        DESCRIPTION: Verify created module on 'Featured' tab/section
        EXPECTED: The created module is displayed and contains the following elements:
        EXPECTED: * Featured module header with module name set in CMS and 'SEE ALL' link(mobile only) that redirects the user to 'Horse Racing/Greyhounds' landing page
        EXPECTED: * Number of retrieved events corresponds to Max Events to Display value set in CMS
        EXPECTED: * All events within Module are in date/time range set in CMS
        EXPECTED: * It is possible to move between events using swiping ( **Mobile** ) / navigation arrow ( **Desktop** )
        EXPECTED: * Events are sorted by 'start time': the first event to start is shown first
        """
        pass

    def test_002_verify_event_section_header_of_racing_events_carousel(self):
        """
        DESCRIPTION: Verify event section header of Racing events carousel
        EXPECTED: - Header consists of:
        EXPECTED: * Time
        EXPECTED: * Event name
        EXPECTED: * Countdown timer (when available),
        EXPECTED: * Type of race, going ( **Ladbrokes Only** ) ![](index.php?/attachments/get/11473525)
        EXPECTED: * 'More >' link navigating the user to the specific race card (for CORAL DESKTOP - 'FULL RACE CARD >' link at the bottom of the race card)
        EXPECTED: * E/W terms ( **CORAL Mobile** )/ for **CORAL Desktop** E/W terms are not implemented
        EXPECTED: - **LADBROKES ONLY** Below header goes E/W terms and watch icon (if the stream is available) at the top of the race card
        """
        pass

    def test_003_verify_silksrunner_numberjockeytrainer_information(self):
        """
        DESCRIPTION: Verify silks/runner number/jockey/trainer information
        EXPECTED: Corresponding elements are present in case data is available
        """
        pass
