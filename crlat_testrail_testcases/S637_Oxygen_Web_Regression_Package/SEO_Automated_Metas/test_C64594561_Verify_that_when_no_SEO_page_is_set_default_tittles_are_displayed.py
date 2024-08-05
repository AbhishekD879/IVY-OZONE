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
class Test_C64594561_Verify_that_when_no_SEO_page_is_set_default_tittles_are_displayed(Common):
    """
    TR_ID: C64594561
    NAME: Verify that when no SEO page is set default tittles are displayed.
    DESCRIPTION: Verify that when no SEO page is set in both manual and Automated tags section default tittles are displayed.
    PRECONDITIONS: * Choose a competition for no SEO page is set in manual SEO section in CMS.
    PRECONDITIONS: * Make sure that no Competition template is present in CMS &gt; SEO &gt; Automated tags section.
    PRECONDITIONS: ** Note: Applicable only to Mobile Web **
    """
    keep_browser_open = True

    def test_001_navigate__to_the_competition_for_which_no_manual_seo_page_is_set_in_the_front_end(self):
        """
        DESCRIPTION: Navigate  to the competition for which no manual SEO page is set in the front end.
        EXPECTED: Landed on to the competition page.
        """
        pass

    def test_002_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under 'head' call.
        EXPECTED: Default Meta tittle and Description are displayed.
        EXPECTED: ![](index.php?/attachments/get/66868824-8061-4429-96ac-3b4619d11eb3) ![](index.php?/attachments/get/1e806a3a-ce21-4753-8e4b-78b81c2831ac)
        """
        pass

    def test_003_repeat_the_step_2_for_horse_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat the Step-2 for Horse, Greyhound races and Virtual Sports.
        EXPECTED: Default Meta tittle and Description are displayed.
        """
        pass
