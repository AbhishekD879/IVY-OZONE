import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58665683_Verify_the_view_of_the_Race_card(Common):
    """
    TR_ID: C58665683
    NAME: Verify the view of the Race card
    DESCRIPTION: This test case verifies the view of the Race card.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_the_virtual_sport_page(self):
        """
        DESCRIPTION: Navigate to the Virtual sport page.
        EXPECTED: The next available event is loaded.
        EXPECTED: The Race card is displayed as per the design with next options:
        EXPECTED: - The event being displayed should be highlighted
        EXPECTED: - Time of the event with the name of the event
        EXPECTED: - Count down timer if the race isn't off yet
        EXPECTED: - Switcher for the Win/EW market, Forecast and Tricast markets
        EXPECTED: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa/screen/5dee3f51be0bb316723dcf29
        """
        pass

    def test_002_observe_the_winew_market(self):
        """
        DESCRIPTION: Observe the 'Win/EW' market.
        EXPECTED: There are next options displayed under the Win/EW market:
        EXPECTED: - Display the terms of the EW
        EXPECTED: - List of runners with the display order as per OB
        EXPECTED: - Runner number
        EXPECTED: - Silks
        EXPECTED: - Name of the runner
        EXPECTED: - Odds button with the odds
        EXPECTED: - CTA, with the text and the link (if configured)
        """
        pass

    def test_003_select_the_forecast_market(self):
        """
        DESCRIPTION: Select the 'Forecast' market.
        EXPECTED: There are next options displayed under the Forecast market:
        EXPECTED: - Text asking the User to pick the order of the first two runners.
        EXPECTED: - List of the runners sorted by runner number and the option to choose the position of the horse (from 1st, 2nd or Any).
        EXPECTED: - The 'Add to Betslip' CTA is disabled.
        """
        pass

    def test_004_select_the_tricast_market(self):
        """
        DESCRIPTION: Select the 'Tricast' market.
        EXPECTED: There are next options displayed under the Tricast market:
        EXPECTED: - Text asking the user to pick the order of the first three runners
        EXPECTED: - List of the runners sorted by runner number and the option to choose the position of the horse (from 1st, 2nd, 3rd or Any).
        EXPECTED: - The 'Add to Betslip' CTA is disabled.
        """
        pass
