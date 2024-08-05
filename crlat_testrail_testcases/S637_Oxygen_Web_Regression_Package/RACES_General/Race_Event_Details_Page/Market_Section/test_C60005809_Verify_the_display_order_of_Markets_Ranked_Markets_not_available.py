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
class Test_C60005809_Verify_the_display_order_of_Markets_Ranked_Markets_not_available(Common):
    """
    TR_ID: C60005809
    NAME: Verify the display order of Markets- Ranked Markets not available
    DESCRIPTION: Verify that if a Market is ranked but unavailable next ranked market will take the position and unavailable market will not be displayed in EDP
    PRECONDITIONS: 1: Horse Racing and Grey Hound racing events should be available
    PRECONDITIONS: 2: Markets order should be configured in CMS
    PRECONDITIONS: 3: Few Markets which are configured in CMS should not be available in EDP
    """
    keep_browser_open = True

    def test_001_1launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        pass

    def test_003_click_on_any_events_which_does_not_have_all_markets_configured_in_cms(self):
        """
        DESCRIPTION: Click on any events which does not have all markets configured in CMS
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_004_validate_the_display_order_of_markets(self):
        """
        DESCRIPTION: Validate the display order of Markets
        EXPECTED: 1: Market tabs should be displayed as per CMS ranking
        EXPECTED: 2: The market is ranked in CMS but unavailable should not be displayed
        EXPECTED: 3: The Next ranked market should take the position
        EXPECTED: Example: 1:Win or Each Way, 2:Win Only, 3:Betting without are configured in CMS
        EXPECTED: Win Only is not available in EDP for an event then the order should be displayed as Win or Each way, Betting without
        """
        pass

    def test_005_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        EXPECTED: 
        """
        pass
