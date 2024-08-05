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
class Test_C15392967_Verify_Signposting_ACCA_Insurance_on_Open_Settled_bets_tab(Common):
    """
    TR_ID: C15392967
    NAME: Verify Signposting ACCA Insurance on Open/Settled bets tab
    DESCRIPTION: 
    PRECONDITIONS: In OB(back office) signposting ACCA Insurance promo flag is configured.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User placed Single/ Multiple bets where Cash Out offer and Extra ACCA Insurance Promo is available on Events/Event levels.
    PRECONDITIONS: User should have some open and settled bets.
    """
    keep_browser_open = True

    def test_001_1navigate_to_my_bets__go_to_open_bets_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets-->Go to Open bets tab
        EXPECTED: Open bets tab should be Opened.
        """
        pass

    def test_002_2verify_signposting_acca_insurance_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting ACCA Insurance promo
        EXPECTED: The Signposting ACCA Insurance promo should be displayed in Open bets section at top level of the overall bet.
        """
        pass

    def test_003_3navigate_to_my_bets__go_to_settled_bet_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Go to Settled bet tab
        EXPECTED: Settled bets tab should be opened.
        """
        pass

    def test_004_4verify_signposting_acca_insurance_promo(self):
        """
        DESCRIPTION: 4.Verify SignPosting ACCA Insurance Promo
        EXPECTED: The Signposting ACCA Insurance promo should be displayed in Settled bets section at top level of the overall bet.
        """
        pass
