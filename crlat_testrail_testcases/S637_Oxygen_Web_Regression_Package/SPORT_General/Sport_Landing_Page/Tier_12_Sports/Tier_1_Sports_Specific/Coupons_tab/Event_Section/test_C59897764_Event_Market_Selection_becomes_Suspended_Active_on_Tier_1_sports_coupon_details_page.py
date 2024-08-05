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
class Test_C59897764_Event_Market_Selection_becomes_Suspended_Active_on_Tier_1_sports_coupon_details_page(Common):
    """
    TR_ID: C59897764
    NAME: Event/Market/Selection becomes Suspended/Active on Tier 1 sports coupon details page
    DESCRIPTION: This test case verifies suspension/unsuspension of Event on Tier 1 sports coupon details page
    PRECONDITIONS: **To see what CMS and TI is in use type "devlog" over opened application or go to URL:** https://your_environment/buildInfo.json
    PRECONDITIONS: **CMS:** https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: **TI:** https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **How to create a coupon:** https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. Find or create two events with two markets for each of them.
    PRECONDITIONS: 2. Create coupon with this two events
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Open Basketball/Tennis Lading page
    PRECONDITIONS: **NOTE:** On Basketball/Tennis coupon details page only events from expaned module should be received in push > Request Payload
    PRECONDITIONS: On Football coupon details page all the events should be received in push > Request Payload (from collapsed and expanded accordions)
    """
    keep_browser_open = True

    def test_001_go_to_the_coupon_page_accas(self):
        """
        DESCRIPTION: Go to the Coupon Page (ACCAS)
        EXPECTED: Coupon page is loaded
        """
        pass

    def test_002_open_coupon_details_page_footballexpand_one_accordion_basketballtennis(self):
        """
        DESCRIPTION: Open coupon details page (Football)
        DESCRIPTION: Expand one accordion (Basketball/Tennis)
        EXPECTED: Coupon details page is loaded. Events are displayed
        EXPECTED: Accourdion is expanded. Events are displayed
        """
        pass

    def test_003_trigger_the_following_situation_for_eventeventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for event:
        DESCRIPTION: **eventStatusCode="S"**
        EXPECTED: Update is received
        """
        pass

    def test_004_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds buttons of this event are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        pass

    def test_005_change_attribute_for_this_eventeventstatuscodea(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: eventStatusCode="A"
        EXPECTED: * Update is received
        EXPECTED: * All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        pass

    def test_006_collapse_competition_and_trigger_suspension_for_event_basketballtennis(self):
        """
        DESCRIPTION: Collapse competition and trigger suspension for event (Basketball/Tennis)
        EXPECTED: Event suspension update is NOT received
        """
        pass

    def test_007_expand_competition_and_verify_event_suspension(self):
        """
        DESCRIPTION: Expand competition and verify event suspension
        EXPECTED: * Event suspension update is received
        EXPECTED: * Price/Odds buttons of this event are displayed immediately as greyed out
        """
        pass

    def test_008_repeat_steps_2_6_for_suspension_on_market_levelmarketstatuscodesmarketstatuscodea(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Suspension on Market level:
        DESCRIPTION: marketStatusCode="S"
        DESCRIPTION: marketStatusCode="A"
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_6_for_suspension_on_outcome_leveloutcomestatuscodesoutcomestatuscodea(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Suspension on Outcome level:
        DESCRIPTION: outcomeStatusCode="S"
        DESCRIPTION: outcomeStatusCode="A"
        EXPECTED: 
        """
        pass
