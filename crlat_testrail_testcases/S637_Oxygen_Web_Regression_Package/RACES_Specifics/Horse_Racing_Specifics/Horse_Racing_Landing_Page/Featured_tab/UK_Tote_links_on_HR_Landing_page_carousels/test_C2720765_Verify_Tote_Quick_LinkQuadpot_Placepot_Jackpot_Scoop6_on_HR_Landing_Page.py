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
class Test_C2720765_Verify_Tote_Quick_LinkQuadpot_Placepot_Jackpot_Scoop6_on_HR_Landing_Page(Common):
    """
    TR_ID: C2720765
    NAME: Verify Tote Quick Link(Quadpot/Placepot/Jackpot/Scoop6) on HR Landing Page
    DESCRIPTION: Verify when clicking on **Quadpot/Placepot/Jackpot/Scoop6** Quick Link(indicator) for HR Landing Page it takes user directly to the **Totepool tab > Quadpot/Placepot/Jackpot/Scoop6>LEG1**
    PRECONDITIONS: **CMS configuration**:
    PRECONDITIONS: - Enable **UK Tote feature** (System configuration > Enable_ UK_ Totepools > True) and save changes
    PRECONDITIONS: **Request on Horse Racing Landing page**: PoolForEvent/ *{events_ids}* ?simpleFilter=pool.type:intersects:UPLP,UQDP,UJKP,USC6&translationLang=en
    PRECONDITIONS: **User is on Horse Racing Page landing page with Tote Pool ***Quadpot/Placepot/Jackpot/Scoop6*** Quick Link for UK & IRE Races**
    """
    keep_browser_open = True

    def test_001_tap_on__any_quadpot__placepot__jackpot__scoop6_indicator(self):
        """
        DESCRIPTION: Tap on  any **Quadpot / Placepot / Jackpot / Scoop6** indicator
        EXPECTED: - User should be taken on appropriate Horse Racing Event Detail Page with UK Tote (Quadpot / Placepot / Jackpot / Scoop6) pool type
        EXPECTED: - User should be taken directly to the Totepool tab > Quadpot / Placepot / Jackpot / Scoop6 > LEG1
        EXPECTED: - URL should be changed according to the respective pool (e.g **/totepool/quadpot**)
        EXPECTED: - Event time tab is highlighted
        EXPECTED: - Event details are displayed
        EXPECTED: - Totepool Tab is highlighted
        EXPECTED: - Quadpot subtab is selected
        EXPECTED: - Leg1 is selected by default and content is loaded
        """
        pass

    def test_002_switch_from_totepool_to_win_or_ew_tab_and_back(self):
        """
        DESCRIPTION: Switch from 'Totepool' to 'Win Or E/W' tab and back
        EXPECTED: User should be taken to the the first available Tote pool type
        """
        pass
