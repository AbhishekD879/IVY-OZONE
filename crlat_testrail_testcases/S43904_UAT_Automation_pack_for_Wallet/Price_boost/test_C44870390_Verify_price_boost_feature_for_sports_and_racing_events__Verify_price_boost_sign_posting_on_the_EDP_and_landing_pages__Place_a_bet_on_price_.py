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
class Test_C44870390_Verify_price_boost_feature_for_sports_and_racing_events__Verify_price_boost_sign_posting_on_the_EDP_and_landing_pages__Place_a_bet_on_price_boost_selection_and_verify_bet_receipt_and_my_bets_Configure_price_boost_through_CMS_on_sports_and_verify(Common):
    """
    TR_ID: C44870390
    NAME: "Verify price boost feature for sports and racing events, - Verify price boost sign posting on the EDP and landing pages - Place a bet on price boost selection and verify bet receipt and my bets -Configure price boost through CMS on sports and verify
    DESCRIPTION: "Verify price boost feature for sports and racing events,
    DESCRIPTION: - Verify price boost sign posting on the EDP and landing pages
    DESCRIPTION: - Place a bet on price boost selection and verify bet receipt and my bets
    DESCRIPTION: -Configure price boost through CMS/OB on sports and verify on FE"
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_event_with_price_boost_flag_ticked_at_market_level(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag ticked at market level
        EXPECTED: Price Boost icon is displayed on the right side of market header
        """
        pass

    def test_002_navigate_to_edp_of_event_with_price_boost_flag_ticked_at_market_level__cashout_flag_available(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag ticked at market level & cashout flag available
        EXPECTED: Cashout icon is present
        EXPECTED: Price Boost icon is displayed after Cashout icon
        """
        pass

    def test_003_expandcollapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: Price Boost icon remains displayed on the right side of market heade
        """
        pass

    def test_004_navigate_to_edp_of_event_with_price_boost_flag_not_ticked(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag not ticked
        EXPECTED: Price Boost icon is not displayed
        """
        pass

    def test_005_place_any_bet_with_price_boost_bet_and_verify_the_signposting_on_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Place any bet with Price boost bet and verify the signposting on bet receipt and my bets
        EXPECTED: Bet placed successfully and the signposting is displayed
        """
        pass
