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
class Test_C2746137_Verify_suspension_for_Placepot_Quadpot_Jackpot_Scoop6_pool_types_on_HR_Landing_page(Common):
    """
    TR_ID: C2746137
    NAME: Verify suspension for Placepot/Quadpot/Jackpot/Scoop6 pool types on HR Landing page
    DESCRIPTION: This test case verifies suspension for Placepot/Quadpot/Jackpot/Scoop6 pool types on Horse Racing Landing page
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Enable UK Tote feature (System configuration > Enable_ UK_ Totepools > True) and save changes
    PRECONDITIONS: **Request on Horse Racing Landing page**: PoolForEvent/ *{events_ids}* ?simpleFilter=pool.type:intersects:UPLP,UQDP,UJKP,USC6&translationLang=en
    PRECONDITIONS: **User is on Horse Racing Page landing page with Tote Pool ***Quadpot/Placepot/Jackpot/Scoop6*** Quick Link for UK & IRE Races**
    """
    keep_browser_open = True

    def test_001_suspend_any_tote_pool_quadpotplacepotjackpotscoop6_in_backoffice_betting_setup__pools__select_pool__set_status___suspended(self):
        """
        DESCRIPTION: Suspend any Tote Pool (Quadpot/Placepot/Jackpot/Scoop6) in backoffice (Betting Setup > Pools > Select pool > Set status - Suspended)
        EXPECTED: - Tote Pool (Quadpot/Placepot/Jackpot/Scoop6) should be suspended in backoffice
        EXPECTED: - Quadpot/Placepot/Jackpot/Scoop6 indicator is still available on HR Landing page
        """
        pass

    def test_002_tap_on_any_quadpot__placepot__jackpot__scoop6_indicator(self):
        """
        DESCRIPTION: Tap on any Quadpot / Placepot / Jackpot / Scoop6 indicator
        EXPECTED: - User should be taken on appropriate Horse Racing Event Detail Page with UK Tote (Quadpot / Placepot / Jackpot / Scoop6) pool type
        EXPECTED: - User should be taken directly to the Totepool tab > Quadpot / Placepot / Jackpot / Scoop6 > LEG1 which should be greyed out
        """
        pass
