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
class Test_C60075242_Verify_displaying_of_Total_Goals_Over_Under_in_the_Market_Selector_dropdown_list(Common):
    """
    TR_ID: C60075242
    NAME: Verify displaying of 'Total Goals Over/Under' in the 'Market Selector' dropdown list
    DESCRIPTION: This test case verifies displaying of 'Total Goals Over/Under' in the 'Market Selector' dropdown list with different "rawHandicapValue" values
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The market with the following parameters should be created in OB system for a particular event:
    PRECONDITIONS: **'templateMarketName' = Over/Under Total Goals** and **'rawHandicapValue' = 2.5**
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_total_goals_overunder_market_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName' attribute for 'Total Goals Over/Under' market in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * templateMarketName='Over/Under Total Goals'
        EXPECTED: * rawHandicapValue='2.5'
        """
        pass

    def test_002_verify_if_the_option_is_present_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify if the option is present in the 'Market Selector' dropdown list
        EXPECTED: 'Total Goals Over/Under 2.5' option is present in the 'Market Selector' dropdown list
        """
        pass

    def test_003_in_ob_system_edit_the_rawhandicapvalue_value_to_25_for_example_35_and_save_the_changes(self):
        """
        DESCRIPTION: In OB system edit the 'rawHandicapValue' value to **=!2.5** (for example 3.5) and save the changes
        EXPECTED: 
        """
        pass

    def test_004_back_to_the_app_and_refresh_the_page(self):
        """
        DESCRIPTION: Back to the app and refresh the page
        EXPECTED: 
        """
        pass

    def test_005_go_to_network___all___preview_and_find_templatemarketname_attribute_for_total_goals_overunder_market_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName' attribute for 'Total Goals Over/Under' market in SS response
        EXPECTED: The following values are displayed in the SS response for the edited event:
        EXPECTED: * templateMarketName='Over/Under Total Goals'
        EXPECTED: * rawHandicapValue='3.5' (edited value in the step 3)
        """
        pass

    def test_006_verify_if_the_option_is_present_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify if the option is present in the 'Market Selector' dropdown list
        EXPECTED: 'Total Goals Over/Under 3.5' option is NOT present in the 'Market Selector' dropdown list
        """
        pass
