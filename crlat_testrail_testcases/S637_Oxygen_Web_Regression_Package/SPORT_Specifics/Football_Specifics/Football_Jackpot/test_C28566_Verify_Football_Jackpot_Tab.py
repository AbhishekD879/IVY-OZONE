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
class Test_C28566_Verify_Football_Jackpot_Tab(Common):
    """
    TR_ID: C28566
    NAME: Verify Football 'Jackpot' Tab
    DESCRIPTION: This test case verifies Football 'Jackpot' tab
    PRECONDITIONS: **JIRA Ticket **: BMA-8911 'Football Jackpot tab - only display if Jackpot is active'
    PRECONDITIONS: To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: **any changes are applied **(displaying/removing of  'Jackpot' tab or changing Jackpot pool that is displayed to another) **on page refresh ONLY**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_003_verify_jackpot_tab_presence(self):
        """
        DESCRIPTION: Verify 'Jackpot' tab presence
        EXPECTED: *   'Jackpot' tab is shown after 'Outrights' tab if Siteserver returns Pool Data for Football Jackpot (see link to use in Preconditions)
        EXPECTED: *   'Jackpot' tab is not shown if no pools are returned in response
        """
        pass

    def test_004_verify_jackpot_tab_view_accessibility(self):
        """
        DESCRIPTION: Verify 'Jackpot' tab view accessibility
        EXPECTED: 'Jackpot' tab is available for both logged out and logged in users if Football Pool Data available
        """
        pass

    def test_005_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: *   Football Jackpot Page is opened
        EXPECTED: *   Navigation is carried out smoothly
        """
        pass
