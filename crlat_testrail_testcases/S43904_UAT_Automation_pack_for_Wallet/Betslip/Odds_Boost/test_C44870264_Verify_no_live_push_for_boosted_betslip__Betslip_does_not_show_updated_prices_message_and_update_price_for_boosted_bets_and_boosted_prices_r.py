import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870264_Verify_no_live_push_for_boosted_betslip__Betslip_does_not_show_updated_prices_message_and_update_price_for_boosted_bets_and_boosted_prices_returns_remains_same_Verify_system_shows_updated_price_messaging_and_prices_when_betslip_gets_refresh_only(Common):
    """
    TR_ID: C44870264
    NAME: "Verify no live push for boosted betslip - Betslip does not show updated prices message and update price for boosted bets, and boosted prices/returns remains same -Verify system shows updated price messaging and prices when betslip gets refresh only
    DESCRIPTION: "Verify no live push for boosted betslip
    DESCRIPTION: User should have odds boost assigned
    DESCRIPTION: Add the selections that has odds boost available
    PRECONDITIONS: Load application and Login into the application
    """
    keep_browser_open = True

    def test_001_verify_no_live_push_for_boosted_betslip(self):
        """
        DESCRIPTION: Verify no live push for boosted betslip
        EXPECTED: Betslip does not show updated prices message and update price for boosted bets, and boosted prices/returns remains same
        """
        pass

    def test_002_verify_system_shows_updated_price_messaging_and_prices_when_betslip_gets_refresh_only(self):
        """
        DESCRIPTION: Verify system shows updated price messaging and prices when betslip gets refresh only
        EXPECTED: updated price is shown only after refresh
        """
        pass

    def test_003_verify_betslip_gets_grey_out_for_boosted_bets_when_getting_suspension_only_that_time_livepush_works_for_boosted_bets(self):
        """
        DESCRIPTION: Verify betslip gets grey out for boosted bets when getting suspension (only that time livepush works for boosted bets)
        DESCRIPTION: "
        EXPECTED: only that time livepush works for boosted bets
        """
        pass
