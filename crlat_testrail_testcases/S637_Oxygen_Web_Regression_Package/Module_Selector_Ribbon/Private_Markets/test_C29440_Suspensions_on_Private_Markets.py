import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29440_Suspensions_on_Private_Markets(Common):
    """
    TR_ID: C29440
    NAME: Suspensions on Private Markets
    DESCRIPTION: This test case verifies Suspensions on Private Markets.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Your Enhanced Markets' is present
        """
        pass

    def test_002_trigger_suspension_for_event_private_market_belongs_to(self):
        """
        DESCRIPTION: Trigger suspension for event private market belongs to
        EXPECTED: All Price/Odds buttons of this market immediately start displaying as greyed out and become disabled on 'Your Enhanced Markets' tab/section
        """
        pass

    def test_003_trigger_unsuspension_for_event_private_market_belongs_to(self):
        """
        DESCRIPTION: Trigger unsuspension for event private market belongs to
        EXPECTED: All Price/Odds buttons of this market immediately start displaying as active and become unsuspended on 'Your Enhanced Markets' tab/section
        """
        pass

    def test_004_trigger_suspension_for_event_private_market_belongs_to_and_refresh_the_page(self):
        """
        DESCRIPTION: Trigger suspension for event private market belongs to and refresh the page
        EXPECTED: *   Verified suspended private market is no more shown within 'Your Enhanced Markets' tab/section (in case there were two or more markets available)
        EXPECTED: *   'Your Enhanced Markets' tab/section is no more shown (in case verified private market was the only one to be shown)
        """
        pass

    def test_005_trigger_unsuspension_for_event_private_market_belongs_to(self):
        """
        DESCRIPTION: Trigger unsuspension for event private market belongs to
        EXPECTED: All Price/Odds buttons of this market immediately start displaying as active and become unsuspended on 'Your Enhanced Markets' tab/section
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: *   Verified suspended private market is shown again within 'Your Enhanced Markets' tab/section (in case there were two or more markets available)
        EXPECTED: *   'Your Enhanced Markets' tab/section is shown again (in case verified private market was the only one to be shown)
        EXPECTED: *   All selections are active
        """
        pass

    def test_007_repeat_steps_2_5_but_suspendunsuspend_one_of_private_markets(self):
        """
        DESCRIPTION: Repeat steps #2-5 but suspend/unsuspend one of private markets
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_5_but_suspendunsuspend_all_outcomes_of_private_markets(self):
        """
        DESCRIPTION: Repeat steps #2-5 but suspend/unsuspend all outcomes of private markets
        EXPECTED: 
        """
        pass

    def test_009_trigger_suspension_of_one_outcome_of_private_markets(self):
        """
        DESCRIPTION: Trigger suspension of one outcome of private markets
        EXPECTED: Outcome becomes suspended
        """
        pass

    def test_010_verify_selected_outcome(self):
        """
        DESCRIPTION: Verify selected outcome
        EXPECTED: Outcome immediately start displaying as greyed out and becomes disabled on 'Your Enhanced Markets' tab/section
        """
        pass

    def test_011_trigger_unsuspension_of_one_outcome_of_private_markets(self):
        """
        DESCRIPTION: Trigger unsuspension of one outcome of private markets
        EXPECTED: Outcome becomes unsuspended
        """
        pass

    def test_012_verify_selected_outcome(self):
        """
        DESCRIPTION: Verify selected outcome
        EXPECTED: Outcome is no more disabled and starts displaying as active immediately on 'Your Enhanced Markets' tab/section
        """
        pass
