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
class Test_C65948327_Verify_GA_tracking_for_Add_to_Betslip(Common):
    """
    TR_ID: C65948327
    NAME: Verify GA tracking for  Add to Betslip
    DESCRIPTION: This test case verifies GA tracking for clicks on Add to Betslip
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        pass

    def test_000_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        pass

    def test_000_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        pass

    def test_000_click_on_add_to_betslip__observe_ga_tracking(self):
        """
        DESCRIPTION: Click on Add to betslip  ,Observe GA tracking
        EXPECTED: Note: Don't duplicate if tracking is exists please add Highlighted Values
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: eventCategory: betslip,
        EXPECTED: eventLabel: success ,
        EXPECTED: eventAction: add to betslip,
        EXPECTED: ecommerce : object,
        EXPECTED: add:object,
        EXPECTED: products: array,
        EXPECTED: 0:object,
        EXPECTED: name :  HVBD Nutifood U21 v Sanna Khanh Hoa U21,
        EXPECTED: dimension60: 238271291,
        EXPECTED: dimension61: 1815133198,
        EXPECTED: dimension62: 1,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension64: {popular bets} ,
        EXPECTED: dimension65: '{betmodule}'
        EXPECTED: category: 16,
        EXPECTED: variant:1935,
        EXPECTED: brand : Match Betting,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension86: 0,
        EXPECTED: dimension88: null,
        EXPECTED: }]
        EXPECTED: });
        """
        pass
