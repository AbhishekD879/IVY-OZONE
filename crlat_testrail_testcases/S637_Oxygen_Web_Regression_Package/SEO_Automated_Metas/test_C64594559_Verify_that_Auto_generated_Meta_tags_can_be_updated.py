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
class Test_C64594559_Verify_that_Auto_generated_Meta_tags_can_be_updated(Common):
    """
    TR_ID: C64594559
    NAME: Verify that Auto generated Meta tags can be updated.
    DESCRIPTION: Verify the reflection in the FE for update functionality of the Meta tittles and descriptions from CMS for Automated tags section.
    PRECONDITIONS: * User should have access to the CMS.
    PRECONDITIONS: * Competition template should be set in CMS &gt; SEO &gt; Automated tags. (If not available)
    PRECONDITIONS: Eg:
    PRECONDITIONS: *Page Url - /competitions
    PRECONDITIONS: *Page tittle - Bet on &lt;competition&gt; | &lt;sport&gt; Odds | &lt;brand&gt;
    PRECONDITIONS: *Page Description - Betting & Odds on &lt;competition&gt; or find the latest odds &lt;sport&gt; | &lt;brand&gt;
    PRECONDITIONS: (Content in the angular braces should not be changed)
    PRECONDITIONS: * Note: Applicable only to mobile web
    """
    keep_browser_open = True

    def test_001_log_into_cms_and_navigate_to_seo_gt_automated_tags_page_(self):
        """
        DESCRIPTION: Log into CMS and navigate to SEO &gt; Automated Tags page .
        EXPECTED: Competition template is present.
        """
        pass

    def test_002_check_for_a_competition_where_the_meta_tittle_and_description_are_auto_generated_in_the_front_end(self):
        """
        DESCRIPTION: Check for a competition where the Meta tittle and description are auto generated in the front end.
        EXPECTED: Autogenerated Meta tags are displayed.
        EXPECTED: ![](index.php?/attachments/get/9cee2955-cf3c-4b67-b67b-d393b1e4ef68) ![](index.php?/attachments/get/d7fbe605-c42f-465a-91bf-89793ea334ea)
        """
        pass

    def test_003_modify_the_existing_competition_template_make_sure_that_variables_or_the_content_within_the_angular_braces_is_not_changed(self):
        """
        DESCRIPTION: Modify the existing Competition template. (Make sure that variables or the content within the angular braces is not changed.)
        EXPECTED: Template updated successfully.
        """
        pass

    def test_004_navigate_to_the_same_competition_in_the_front_endreload_the_page_if_necessaryhover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to the same competition in the front end.
        DESCRIPTION: Reload the page if necessary.
        DESCRIPTION: Hover the cursor over the Browser tab.
        EXPECTED: Updated meta tittle as per the template set should be displayed.
        EXPECTED: ![](index.php?/attachments/get/ed3b7353-0b8e-4311-8d9f-71e040ad35c5) ![](index.php?/attachments/get/19550e5f-a8f2-4e56-8fdc-82278f337de7)
        """
        pass

    def test_005_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header_head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header 'head' call.
        EXPECTED: The updated Meta tags are displayed.
        EXPECTED: ![](index.php?/attachments/get/fdd5c0b7-cf9e-4a2a-87b3-dcf71ebbbe66) ![](index.php?/attachments/get/93e78bec-e275-4740-8578-b3c6ba1de47f)
        """
        pass

    def test_006_repeat_steps__4__5_for_horse_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat Steps- 4 & 5 for Horse, Greyhound races and Virtual sports.
        EXPECTED: The updated Meta tags are displayed.
        """
        pass
