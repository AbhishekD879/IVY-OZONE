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
class Test_C28856_Verify_Price_Odds_Buttons_for_Race_with_LP_price_type(Common):
    """
    TR_ID: C28856
    NAME: Verify Price/Odds Buttons for <Race> with LP price type
    DESCRIPTION: Verify Price/Odds Buttons for <Race> with LP price type
    PRECONDITIONS: There is <Race> event with LP prices available, there are some selections with the same Price/Odds
    """
    keep_browser_open = True

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: Event Details page is opened
        """
        pass

    def test_002_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify Price/Odds buttons
        EXPECTED: Prices are correct for each selection, values correspond to the **'priceNum'** and **'priceDec'** attributes
        """
        pass

    def test_003_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: *  Selections are ordered by price in ascending order (lowest to highest)
        EXPECTED: *  If odds of selections are the same then horses should be sorted by card number in ascending order
        """
        pass
