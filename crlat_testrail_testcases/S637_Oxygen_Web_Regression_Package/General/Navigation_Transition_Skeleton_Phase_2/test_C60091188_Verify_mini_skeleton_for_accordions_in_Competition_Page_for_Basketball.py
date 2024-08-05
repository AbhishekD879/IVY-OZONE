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
class Test_C60091188_Verify_mini_skeleton_for_accordions_in_Competition_Page_for_Basketball(Common):
    """
    TR_ID: C60091188
    NAME: Verify mini skeleton for accordions in Competition Page for Basketball
    DESCRIPTION: This test case verifies mini loading skeleton inside accordions in Basketball Competitions page while content loads so that user gets feedback that something is happening when expanding accordions.
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Story related: https://jira.egalacoral.com/browse/50254
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - User is on Basketball Competitions page where accordions can be expanded
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_tap_on_any_collapsed_accordion_on_the_competition_page(self):
        """
        DESCRIPTION: Tap on any collapsed accordion on the Competition Page.
        EXPECTED: - No spinner is displayed inside the accordion
        EXPECTED: - User sees mini loading skeleton
        EXPECTED: - Content loads inside the accordion
        """
        pass

    def test_002_expand_all_accordion_on_the_same_page_one_by_one(self):
        """
        DESCRIPTION: Expand all accordion on the same page one by one
        EXPECTED: - No spinner is displayed inside the accordion
        EXPECTED: - User sees mini loading skeleton
        EXPECTED: - Content loads inside the accordion
        EXPECTED: ![](index.php?/attachments/get/122292752)
        EXPECTED: Note: If there are one or more than one events only one skeleton will display
        """
        pass

    def test_003_check_the_skeleton_animation_while_it_is_displayed_to_the_user(self):
        """
        DESCRIPTION: Check the skeleton animation while it is displayed to the user
        EXPECTED: - Skeleton does not jump up and down and appears smoothly
        EXPECTED: - There is no extra space/area below/beneath the skeleton
        """
        pass

    def test_004_verify_the_skeleton_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the skeleton transition when content becomes available
        EXPECTED: When content becomes available within accordion user sees a smooth transition from the loading skeleton to the content
        """
        pass
