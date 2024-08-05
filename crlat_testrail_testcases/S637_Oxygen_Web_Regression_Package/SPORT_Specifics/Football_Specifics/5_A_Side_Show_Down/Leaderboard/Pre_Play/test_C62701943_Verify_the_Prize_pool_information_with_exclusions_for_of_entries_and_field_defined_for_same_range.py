import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62701943_Verify_the_Prize_pool_information_with_exclusions_for_of_entries_and_field_defined_for_same_range(Common):
    """
    TR_ID: C62701943
    NAME: Verify the Prize pool information with exclusions for # of entries and % field defined for same range.
    DESCRIPTION: This test case verifies the accuracy of position ranges divided when both % of field and # of entries are configured.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: 4: Event should be in Pre-Play
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: Contest Criteria
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: Asset Management
    PRECONDITIONS: 1: Team Flags can be configured in CMS &gt; BYB &gt; ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_configure_one_of_the_prize_in_prize_pool_information_as_followsprize_type__freebetprize_value__1_of_field__201_10000_of_entries__1001_1100other_prizes_should_be_configured_till_1000click_on_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS, configure one of the prize in prize pool information as follows.
        DESCRIPTION: Prize Type   : FreeBet
        DESCRIPTION: Prize value  : 1
        DESCRIPTION: % of field   : 20,*1-10000
        DESCRIPTION: "#" of entries : 1001-1100
        DESCRIPTION: Other prizes should be configured till 1000.
        DESCRIPTION: Click on save changes.
        EXPECTED: Changes should be saved with the updated information.
        """
        pass

    def test_002_navigate_to_pre_leaderboard_and_verify_if_all_the_prizes_configured_are_visible(self):
        """
        DESCRIPTION: Navigate to Pre-Leaderboard and verify if all the prizes configured are visible.
        EXPECTED: All the prizes configured in CMS, should be available in Pre-leaderboard.
        EXPECTED: The Freebet prize should be as follows
        EXPECTED: # FreeBet - 1001-1100
        """
        pass

    def test_003_verify_the_behaviour_till_there_are_1100plus_entries_in_contest(self):
        """
        DESCRIPTION: Verify the behaviour till there are 1100+ entries in contest.
        EXPECTED: When there are more than 1000 entries the FE should be as follows.
        EXPECTED: for  1105 entries :
        EXPECTED: # FreeBet - 1001-1105.
        """
        pass
