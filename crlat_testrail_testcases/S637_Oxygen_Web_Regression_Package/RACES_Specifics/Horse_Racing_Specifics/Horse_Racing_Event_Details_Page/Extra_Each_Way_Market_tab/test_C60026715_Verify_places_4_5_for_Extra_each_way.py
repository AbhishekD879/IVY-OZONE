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
class Test_C60026715_Verify_places_4_5_for_Extra_each_way(Common):
    """
    TR_ID: C60026715
    NAME: Verify places 4 & 5 for Extra each way
    DESCRIPTION: Verify that "EXTRA EACH WAY" market displays 4 PLACES & 5 PLACES when WIN OR E/W market is for 2 Places i.e. "Places 1-2-3 "
    PRECONDITIONS: 1: Horse racing event should be available.
    PRECONDITIONS: 2: "EXTRA EACH WAY" market should be available for the event.
    PRECONDITIONS: 3: Win Or Each way market should be available
    PRECONDITIONS: 4: Each way market should be for only places 1 , 2 & 3
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

    def test_003_click_on_any_uk_and_ireland_race_which_has_extra_each_way_market_available_and_each_way_market_has_only_places_1_2__3(self):
        """
        DESCRIPTION: Click on any UK and Ireland race which has "EXTRA EACH WAY" market available and Each way market has only places 1 ,2 & 3
        EXPECTED: User should be navigated to Event details page.
        """
        pass

    def test_004_navigate_to_win_or_each_way_market_and_validate_places(self):
        """
        DESCRIPTION: Navigate to Win or Each Way market and validate places
        EXPECTED: 1: User should be displayed odds for Each way.
        EXPECTED: 2: Places should be displayed as "Places 1-2-3"
        """
        pass

    def test_005_navigate_to_extra_each_way_market_and_validate_places(self):
        """
        DESCRIPTION: Navigate to Extra Each Way market and validate places
        EXPECTED: 1: User should be displayed selections
        EXPECTED: 2: Odds should be tabulated under headers
        EXPECTED: "4 PLACES" "5 PLACES"
        """
        pass
