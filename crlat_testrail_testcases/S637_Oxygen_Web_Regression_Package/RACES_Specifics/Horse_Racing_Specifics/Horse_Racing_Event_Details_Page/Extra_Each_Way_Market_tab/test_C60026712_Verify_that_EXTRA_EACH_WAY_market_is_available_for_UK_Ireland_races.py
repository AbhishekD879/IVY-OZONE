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
class Test_C60026712_Verify_that_EXTRA_EACH_WAY_market_is_available_for_UK_Ireland_races(Common):
    """
    TR_ID: C60026712
    NAME: Verify that "EXTRA EACH WAY" market is available for UK & Ireland races
    DESCRIPTION: Verify "EXTRA EACH WAY" market is displayed in Event Details page for all UK & Ireland races.
    PRECONDITIONS: 1: Horse racing event should be available.
    PRECONDITIONS: 2: "EXTRA EACH WAY" market should be available for the event.
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

    def test_003_click_on_any_uk_and_ireland_race_which_has_extra_each_way_market_available(self):
        """
        DESCRIPTION: Click on any UK and Ireland race which has "EXTRA EACH WAY" market available
        EXPECTED: User should be navigated to Event details page.
        """
        pass

    def test_004_validate_extra_each_way_market(self):
        """
        DESCRIPTION: Validate "EXTRA EACH WAY" market
        EXPECTED: 1: User should be displayed "EXTRA EACH WAY"
        EXPECTED: 2: Selections should be displayed
        """
        pass
