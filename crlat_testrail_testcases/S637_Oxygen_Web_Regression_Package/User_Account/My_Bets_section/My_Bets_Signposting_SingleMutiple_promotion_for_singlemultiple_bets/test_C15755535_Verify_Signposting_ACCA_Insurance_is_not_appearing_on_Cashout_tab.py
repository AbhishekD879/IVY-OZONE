import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C15755535_Verify_Signposting_ACCA_Insurance_is_not_appearing_on_Cashout_tab(Common):
    """
    TR_ID: C15755535
    NAME: Verify Signposting ACCA Insurance is not appearing on Cashout tab
    DESCRIPTION: 
    PRECONDITIONS: n OB(back office) signposting ACCA Insurance promo flag is configured.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User placed Single/ Multiple bets where Cash Out offer and Extra ACCA Insurance Promo is available on Events/Event levels.
    """
    keep_browser_open = True

    def test_001_1navigate_to_my_bets____go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets --> Go to Cash out tab
        EXPECTED: Cash Out tab should be opened
        """
        pass

    def test_002_2verify_signposting_acca_insurance_promo(self):
        """
        DESCRIPTION: 2.Verify SignPosting ACCA Insurance Promo
        EXPECTED: The Signposting ACCA Insurance promo should not displayed in cash out tab
        """
        pass
