import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C2538042_Your_Enhanced_Markets__Odds_Format(Common):
    """
    TR_ID: C2538042
    NAME: Your Enhanced Markets - Odds Format
    DESCRIPTION: 
    PRECONDITIONS: User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: **For mobile/tablet:**
    PRECONDITIONS: Go to Setting and change Odds format to decimal
    PRECONDITIONS: **For desktop:**
    PRECONDITIONS: Change Odds format to decimal using 'Price Format' dropdown at the 'Universal Header'
    """
    keep_browser_open = True

    def test_001_select_decimal_odds_format(self):
        """
        DESCRIPTION: Select Decimal Odds format
        EXPECTED: 
        """
        pass

    def test_002_verify_odds_format_for_selections_within_the_private_market(self):
        """
        DESCRIPTION: Verify Odds format for selections within the private market
        EXPECTED: Price/Odds are displayed in Decimal format
        """
        pass

    def test_003_select_fractional_odds_format(self):
        """
        DESCRIPTION: Select Fractional Odds format
        EXPECTED: 
        """
        pass

    def test_004_verify_odds_format_for_selections_within_the_private_market(self):
        """
        DESCRIPTION: Verify Odds format for selections within the private market
        EXPECTED: Price/Odds are displayed in Fractional format
        """
        pass
