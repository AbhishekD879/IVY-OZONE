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
class Test_C60026713_Verify_that_EXTRA_EACH_WAY_market_is_not_available_for_any_races_other_than_UK_Ireland(Common):
    """
    TR_ID: C60026713
    NAME: Verify that "EXTRA EACH WAY" market is not available for any races other than UK & Ireland
    DESCRIPTION: Verify that "EXTRA EACH WAY" market is not available for any Horse races other than UK & Ireland
    PRECONDITIONS: 1: Horse racing event other than UK & Ireland should be available.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_click_on_any_race_other_than_uk__ireland(self):
        """
        DESCRIPTION: Click on any race other than UK & Ireland
        EXPECTED: User should be navigated to Event details page.
        """
        pass

    def test_004_validate_extra_each_way_market(self):
        """
        DESCRIPTION: Validate "EXTRA EACH WAY" market
        EXPECTED: "EXTRA EACH WAY" market should not be displayed.
        """
        pass
