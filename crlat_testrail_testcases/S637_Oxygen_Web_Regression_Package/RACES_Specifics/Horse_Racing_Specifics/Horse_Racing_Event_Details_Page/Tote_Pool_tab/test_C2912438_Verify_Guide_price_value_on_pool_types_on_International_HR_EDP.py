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
class Test_C2912438_Verify_Guide_price_value_on_pool_types_on_International_HR_EDP(Common):
    """
    TR_ID: C2912438
    NAME: Verify Guide price value on pool types on International HR EDP
    DESCRIPTION: This test case verifies Guide price value on Win pool type on International HR EDP
    PRECONDITIONS: * User should have a International HR EDP open ("Tote" tab)
    PRECONDITIONS: * Event should have Win/Place/Exacta/Trifecta pool types available
    PRECONDITIONS: To retrieve data For pool info from the Site Server use the following links:
    PRECONDITIONS: * https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/PoolToPoolValue/<Pool_ID>
    PRECONDITIONS: * https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool/<Pool_ID>
    """
    keep_browser_open = True

    def test_001_select_win_tab(self):
        """
        DESCRIPTION: Select "Win" tab
        EXPECTED: * "Win" tab is selected
        EXPECTED: * Win racecard is shown
        """
        pass

    def test_002_verify_guide_price_value_for_win_pool_type_selections(self):
        """
        DESCRIPTION: Verify Guide price value for **'Win'** pool type selections
        EXPECTED: * Guide price values are shown on every 'Win' button/selection
        EXPECTED: * Guide price values are shown under 'Win' label
        EXPECTED: * Guide price values are displayed with 'Guide' label and a decimal number
        EXPECTED: * Guide price values correspond to the values, received in **openbet-ssviewer/Drilldown/2.26/PoolToPoolValue** request
        EXPECTED: (E.G.: <poolValue id="17830702" poolId="1369930" runnerNumber1="1" **value="6.8"**/> - this 'value' parameter is the Guide price for this pool)
        """
        pass

    def test_003_trigger_change_of_guide_price_and_refresh_the_page(self):
        """
        DESCRIPTION: Trigger change of Guide price and refresh the page
        EXPECTED: The updated Guide price is shown after page refresh
        """
        pass

    def test_004_repeat_steps_2_3_for_place_pool_type_exacta_pool_type_trifecta_pool_type(self):
        """
        DESCRIPTION: Repeat steps 2-3 for:
        DESCRIPTION: * Place pool type
        DESCRIPTION: * Exacta pool type
        DESCRIPTION: * Trifecta pool type
        EXPECTED: 
        """
        pass
