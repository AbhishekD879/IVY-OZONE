import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C11482847_Racing_EDP_Coral_displaying_Place_Insurance_2_Place_Insurance_3_Place_Insurance_4_markets(Common):
    """
    TR_ID: C11482847
    NAME: Racing EDP [Coral]: displaying 'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4' markets
    DESCRIPTION: This test case verifies displaying of 'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4' markets on <Racing> EDP
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have <Race> event with active markets added from 'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places' templates and with selections
    PRECONDITIONS: - You should be on <Race> EDP
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_markets_tabs_displaying(self):
        """
        DESCRIPTION: Verify markets tabs displaying
        EXPECTED: 'PLACE INSURANCE' market tab is displayed
        """
        pass

    def test_002_tap_place_insurance_market_tab_and_verify_displaying_of_selections_and_columns(self):
        """
        DESCRIPTION: Tap 'PLACE INSURANCE' market tab and verify displaying of selections and columns
        EXPECTED: - Columns '2ND', '3RD', '4TH' are displayed
        EXPECTED: - Selections are displayed next to the respective runners and under respective column (selections from 'Insurance 2 Places' market are displayed under '2ND' column and so on)
        """
        pass

    def test_003___in_ti_tool_undisplay_one_of_the_markets_eg_insurance_2_places__in_application_refresh_the_page_and_verify_displaying_of_the_column_of_the_undisplayed_market(self):
        """
        DESCRIPTION: - In TI tool undisplay one of the markets (e.g. 'Insurance 2 Places')
        DESCRIPTION: - In application refresh the page and verify displaying of the column of the undisplayed market
        EXPECTED: Column of the undisplayed market is not displayed
        """
        pass
