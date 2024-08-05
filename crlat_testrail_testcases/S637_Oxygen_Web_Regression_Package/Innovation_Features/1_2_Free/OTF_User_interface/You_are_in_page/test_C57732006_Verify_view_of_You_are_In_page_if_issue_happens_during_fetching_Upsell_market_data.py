import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732006_Verify_view_of_You_are_In_page_if_issue_happens_during_fetching_Upsell_market_data(Common):
    """
    TR_ID: C57732006
    NAME: Verify view of You are In page if issue happens during fetching Upsell market data
    DESCRIPTION: This test case verifies **view** of page if issue happens during fetching Upsell market data
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    """
    keep_browser_open = True

    def test_001_user_submit_predictions_and_there_is_an_issue_with_fetching_the_upsell_market_data_for_any_of_the_markets_match_result_over_under_25_goals__or_btts(self):
        """
        DESCRIPTION: User 'Submit' predictions and there is an issue with fetching the upsell market data for any of the markets (Match result, Over/ Under 2.5 goals , or BTTS)
        EXPECTED: - 'You are in' page opened successfully
        EXPECTED: - Upsell Market options NOT displayed
        EXPECTED: - All data retrieved from CMS and correctly designed according: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c61a5e263ad7b1235e17741*
        """
        pass
