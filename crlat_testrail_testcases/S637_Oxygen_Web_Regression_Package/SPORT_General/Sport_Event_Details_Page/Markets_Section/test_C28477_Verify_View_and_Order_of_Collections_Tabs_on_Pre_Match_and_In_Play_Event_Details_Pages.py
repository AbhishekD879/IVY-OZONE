import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28477_Verify_View_and_Order_of_Collections_Tabs_on_Pre_Match_and_In_Play_Event_Details_Pages(Common):
    """
    TR_ID: C28477
    NAME: Verify View and Order of Collections (Tabs) on Pre-Match and In-Play Event Details Pages
    DESCRIPTION: This test case verifies view and order of Market tabs on Pre-Match and In-Play Event Details Pages.
    PRECONDITIONS: * Few market collections are added in CMS -> edp-markets
    PRECONDITIONS: * Market Collections are taken from http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/SportToCollection?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: [How to set up order of tabs on sport event details page (EDP)][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?pageId=62551321
    PRECONDITIONS: [How to create a New Collection][2]
    PRECONDITIONS: [2]:https://confluence.egalacoral.com/display/SPI/How+to+create+a+New+Collection
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to event details page
    """
    keep_browser_open = True

    def test_001_verify_tab_selected_by_default(self):
        """
        DESCRIPTION: Verify tab selected by default
        EXPECTED: **Coral:**
        EXPECTED: *   **'Main Markets'** collection (Tab) is selected by default
        EXPECTED: * All Markets is selected if markets don't have collectionNames="Main Markets"
        EXPECTED: **Ladbrokes:**
        EXPECTED: *   **'All Markets'** collection (Tab) is selected by default
        """
        pass

    def test_002_verify_name_of_collections_tabs(self):
        """
        DESCRIPTION: Verify Name of Collections (Tabs)
        EXPECTED: Name of Market Collections (Tabs) corresponds to the **'name**' attribute on Collection level
        """
        pass

    def test_003_verify_present_collections_tabs(self):
        """
        DESCRIPTION: Verify present Collections (Tabs)
        EXPECTED: *   Only collections (Tabs) with attribute **drilldownTagNames="COLLFLAG_EP" **are displayed
        EXPECTED: *   Only Collections (Tabs) that have Markets are displayed
        EXPECTED: *   Collections (Tabs) are NOT displayed if there are no Markets belonging to them
        """
        pass

    def test_004_verify_order_of_collections_tabs(self):
        """
        DESCRIPTION: Verify order of Collections (Tabs)
        EXPECTED: * Order is the same as in EDP-Markets response from CMS
        EXPECTED: * Collection (Tab) with 'lastItem: true' is displayed the last one
        EXPECTED: * In case some collection (Tab) is not added in CMS is displayed before collection (Tab) with 'lastItem: true' value
        EXPECTED: * In case there are several not added to CMS collections (Tabs) they are displayed before collection (Tab) with 'lastItem: true' value, displayed according to collection displayOrder in ascending taken from 'SportToCollection' response
        EXPECTED: Old removed logic:
        EXPECTED: *   '**Main Markets**' collection (Tab) is ordered second
        EXPECTED: *   All other Collections (Tabs) are ordered  **Alphabetically**
        EXPECTED: *   **'Other Markets' **is displayed in the end of Markets Ribbon if it is available
        EXPECTED: *   '**All Markets**' is displayed first of Markets Ribbon
        """
        pass

    def test_005__change_order_of_collections_tabs_in_cms_by_dragdrop(self):
        """
        DESCRIPTION: * Change order of Collections (Tabs) in CMS by drag&drop
        EXPECTED: 
        """
        pass

    def test_006_refresh_the_event_details_page_and_verify_order_of_collections_tabs(self):
        """
        DESCRIPTION: Refresh the Event Details Page and verify order of Collections (Tabs)
        EXPECTED: * Updated EDP-Markets response is received
        EXPECTED: * Order is changed accordingly
        """
        pass

    def test_007_coral_onlynavigate_to_football_edp_with_new_yourcall_tab_phase_2_available_and_with_yourcall_collection_received_in_response_phase_1(self):
        """
        DESCRIPTION: **Coral Only**
        DESCRIPTION: Navigate to Football EDP with new YourCall tab (Phase 2) available and with #YourCall collection received in response (Phase 1)
        EXPECTED: * Only new YourCall tab from Phase 2 is displayed
        EXPECTED: * #YourCall tab from Phase 1 is hidden
        """
        pass
