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
class Test_C60092716_Verify_displaying_Olympic_Sports_based_on_data_received_from_CMS(Common):
    """
    TR_ID: C60092716
    NAME: Verify displaying Olympic Sports based on data received from CMS
    DESCRIPTION: This test case verifies that configured in CMS Olympic Sports are received in /api/bma/initial-data response within  'sportCategories:'
    DESCRIPTION: ![](index.php?/attachments/get/122293278)
    DESCRIPTION: **Note:*** after BMA-55202 Configuration of Olympics will be done in Sports Categories by checkbox "isOlympic".
    DESCRIPTION: Before that Olympics are configured in 'Olympic Sports' and received in /api/bma/initial-data response within sports:
    PRECONDITIONS: 1. There is at least one Olympic Sport created in CMS
    PRECONDITIONS: 2. Events for Olympic Sport are available in OB
    PRECONDITIONS: List of all OpenBet systems: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: List of all CMS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001__go_to_app_open_devtools_search_for_apibmainitial_data_response_expande_response_verify_olympic_sport_in_sportcategories(self):
        """
        DESCRIPTION: * Go to app, open devTools, search for /api/bma/initial-data response
        DESCRIPTION: * Expande response, verify Olympic sport in "sportCategories:'
        EXPECTED: Olympic Sport is received. All data is available ()additional parameters will be described later)
        """
        pass

    def test_002_navigate_to_olympic_sport_page_in_the_app(self):
        """
        DESCRIPTION: Navigate to Olympic sport page in the app
        EXPECTED: Sport Landing Page is opened.
        EXPECTED: Available Events are shown
        """
        pass

    def test_003__in_cms_delete_any_olympic_sport_refresh_an_app_verify_if_deleted_sport_is_available_in_app(self):
        """
        DESCRIPTION: * In CMS, delete any Olympic Sport
        DESCRIPTION: * Refresh an App, verify if deleted Sport is available in App
        EXPECTED: User is redirected to Home Page
        EXPECTED: Olympic Sport disappeared from Left Menu
        """
        pass

    def test_004_in_devtools_verify_apibmainitial_data_response(self):
        """
        DESCRIPTION: In devtools verify /api/bma/initial-data response
        EXPECTED: Deleted Olympic Sport is not received "sportCategories:'
        """
        pass
