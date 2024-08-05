import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C60090038_Verify_Bet_Receipt_page_skeleton(Common):
    """
    TR_ID: C60090038
    NAME: Verify Bet Receipt page skeleton
    DESCRIPTION: This test case verifies the loading skeleton (instead of spinners) for Bet Receipt pages.
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - User is logged in and has positive balance
    PRECONDITIONS: Note:
    PRECONDITIONS: Bet Receipt Skeleton for Quick bet is not in scope
    """
    keep_browser_open = True

    def test_001_add_few_selections_to_betslip_and_open_it(self):
        """
        DESCRIPTION: Add few selections to Betslip and open it
        EXPECTED: - Betslip is opened with selections added
        """
        pass

    def test_002_enter_stake_into_stake_field_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter stake into stake field and click on place bet
        EXPECTED: - Skeleton is displayed for few seconds before Bet Receipt is displayed
        EXPECTED: - Skeleton fades away and Bet Receipt becomes available
        """
        pass

    def test_003_check_the_skeleton_appearance(self):
        """
        DESCRIPTION: Check the skeleton appearance
        EXPECTED: - Skeleton does not jump up and down and appears smoothly
        EXPECTED: - There is no extra space/area below/beneath the skeleton
        EXPECTED: Skeleton animation:
        EXPECTED: ![](index.php?/attachments/get/122259034)
        """
        pass

    def test_004_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: - There is a smooth transition from the skeleton to page content
        EXPECTED: - All content is available and displayed
        EXPECTED: - No additional spinners are displayed on the page
        """
        pass

    def test_005_verify_for_all_types_of_bets(self):
        """
        DESCRIPTION: Verify for all types of Bets
        EXPECTED: 
        """
        pass
