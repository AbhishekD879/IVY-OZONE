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
class Test_C64597371_Verify_that_manually_given_Meta_tittles_in_CMS_are_not_over_written_by_the_auto_generated_tittles(Common):
    """
    TR_ID: C64597371
    NAME: Verify that manually given Meta tittles  in CMS are not over written by the auto generated tittles.
    DESCRIPTION: Verify that manually given Meta tittles in CMS are not over written by the auto generated tittles.
    PRECONDITIONS: * Choose an event  for which tags are predefined in CMS &gt; SEO &gt; Manual section (Create a manual SEO page for an event if not available).
    PRECONDITIONS: * Note: Applicable for Mobile Web.
    """
    keep_browser_open = True

    def test_001_open_cms_navigate_to_seo_gt_manual_page_check_for_the_meta_tittle_per_defined_for_a_tier_1_sport_edp_page_if_not_available_create_with_tittle_and_description(self):
        """
        DESCRIPTION: Open CMS, navigate to SEO &gt; Manual page, check for the meta tittle per-defined for a Tier-1 sport EDP page. (If not available create with Tittle and Description.)
        EXPECTED: Manual SEO page is present for an event.
        """
        pass

    def test_002_navigate_to_the_same_event_in_the_front_end_to_the_event_details_page_hover_the_cursor_over_the_browser_tab_opened(self):
        """
        DESCRIPTION: Navigate to the same event in the front end to the event details page. Hover the cursor over the Browser tab opened.
        EXPECTED: EDP is opened.
        EXPECTED: Meta tittle of the page is displayed same as set in CMS.
        EXPECTED: ![](index.php?/attachments/get/5e01b579-37e8-44d0-9406-cb871ae3e4bb) ![](index.php?/attachments/get/04f63f70-1f01-4cd8-bd76-40fb67d1be4f)
        """
        pass

    def test_003_check_for_the_meta_tittle_and_description_in_the_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in the Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Manual SEO page Meta tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/7fab3622-0642-4da8-bf48-0dbe8b7cbd31) ![](index.php?/attachments/get/0b74cb4e-6a8a-4a01-b8f1-70119a062a99)
        """
        pass

    def test_004_choose_an_event_for_which_no_seo_page_is_set_in_cms_gt_seo_gt_manual_section_check_for_the_meta_tittles_in_the_inspection_windowprovided_no_edp_template_is_added_in_cms_gt_seo_gt_automated_tags(self):
        """
        DESCRIPTION: Choose an event for which no SEO page is set in CMS &gt; SEO &gt; Manual section. Check for the Meta tittles in the inspection window.
        DESCRIPTION: (Provided no EDP template is added in CMS &gt; SEO &gt; Automated Tags)
        EXPECTED: Default Meta tittle and Description are visible.
        EXPECTED: ![](index.php?/attachments/get/2eb3d0ab-f882-4f5f-acad-f656aced32a1) ![](index.php?/attachments/get/98d4669a-1f50-41dc-b8b0-d37021530c1c)
        """
        pass

    def test_005_add_seo_page_in_cms_gt_seo_gt_manual_section(self):
        """
        DESCRIPTION: Add SEO page in CMS &gt; SEO &gt; Manual section.
        EXPECTED: SEO page added successfully.
        """
        pass

    def test_006_navigate_to_the_same_event_in_the_front_end_and_hover_the_cursor_over_the_browser_tab_check_for_the_same_in_the_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Navigate to the same event in the Front end and hover the cursor over the browser tab. Check for the same in the inspection window &gt; Elements tab under header - 'Head' call.
        EXPECTED: Manually set Meta Tags are displayed.
        EXPECTED: ![](index.php?/attachments/get/91c39df0-63e9-43c0-8363-34353a041c20) ![](index.php?/attachments/get/45f38a7a-7e1e-4c4a-be38-8a5a39895d50)
        """
        pass

    def test_007_add_event_template_in_the_cms_gt_seo_gt_automated_tags_page_url___event_page_tittle___bet_on_lteventgt__ltcompetitiongt_ltsportgt__ltbrandgt_page_description___betting__odds_on_lteventgt__ltcompetitiongt______ltsportgt__ltbrandgt(self):
        """
        DESCRIPTION: Add Event template in the CMS &gt; SEO &gt; Automated tags.
        DESCRIPTION: * Page Url - /event
        DESCRIPTION: * Page Tittle - Bet on &lt;event&gt; | &lt;competition&gt; &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: * Page Description - Betting & Odds on &lt;event&gt; | &lt;competition&gt;      &lt;sport&gt; | &lt;brand&gt;
        EXPECTED: Template added successfully.
        """
        pass

    def test_008_navigate_to_the_same_event_in_the_front_end_and_hover_the_cursor_over_the_browser_tabcheck_for_the_same_in_the_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Navigate to the same event in the Front end and hover the cursor over the browser tab.
        DESCRIPTION: Check for the same in the inspection window &gt; Elements tab under header - 'Head' call.
        EXPECTED: Landed on to the Event details page.
        EXPECTED: Manually SEO page tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/3a421386-45b1-4051-a607-b9c03bd11110) ![](index.php?/attachments/get/f07411c7-1290-4be2-bbb7-8fc0b2293652)
        """
        pass

    def test_009_create_a_manual_seo_page_in_cms_gt_seo_gt_manual_section_with_only_page_tittleindexphpattachmentsget54e48931_d078_4249_afec_e980cc579db0(self):
        """
        DESCRIPTION: Create a Manual SEO Page in CMS &gt; SEO &gt; Manual section with only Page tittle.
        DESCRIPTION: ![](index.php?/attachments/get/54e48931-d078-4249-afec-e980cc579db0)
        EXPECTED: Page successfully created.
        """
        pass

    def test_010_a_navigate_to_the_same_edp_in_the_front_end_and_hover_the_cursor_over_the_browser_tabb_check_for_the_same_in_the_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: a) Navigate to the Same EDP in the front end and hover the cursor over the browser tab.
        DESCRIPTION: b) Check for the same in the inspection window &gt; Elements tab under header - 'Head' call.
        EXPECTED: a) Manual SEO page tittle is visible.
        EXPECTED: ![](index.php?/attachments/get/919fdcb2-8ff1-40fd-9a9c-f0a17ec1e3f6) ![](index.php?/attachments/get/7d7aca5a-d95d-4b99-875f-45480929e898)
        EXPECTED: b) Manual page tittle is displayed and Description content is empty.
        EXPECTED: ![](index.php?/attachments/get/6795d15b-9c30-476b-a41d-350b8bb15528) ![](index.php?/attachments/get/54279611-c85e-4a02-b0e1-cf030fdbd32a)
        """
        pass

    def test_011_set_a_manual_seo_page_containing_both_tittle_and_description_defined_in_cms_gt_seo_gt_manual_to_inactive(self):
        """
        DESCRIPTION: Set a Manual SEO page containing both Tittle and description defined in CMS &gt; SEO &gt; Manual to inactive.
        EXPECTED: Manual SEO page is inactive.
        """
        pass

    def test_012_navigate_to_the_same_event_details_page_in_the_front_end_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to the same event details page in the front end. Hover the cursor over the browser tab.
        EXPECTED: Auto generated meta tittle is displayed.
        EXPECTED: ![](index.php?/attachments/get/52687840-4fb1-4e05-a0db-40a3f24a55a1) ![](index.php?/attachments/get/921bfad4-6848-4ae3-84e8-a179f9399028)
        """
        pass

    def test_013_check_for_the_same_in_the_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the same in the inspection window &gt; Elements tab under header - 'Head' call.
        EXPECTED: Auto generated Page tittle and description is visible with the specific details of the event.
        EXPECTED: ![](index.php?/attachments/get/a7803f9e-2af0-45f9-b17e-d89a72bacf26) ![](index.php?/attachments/get/9623514c-3295-4f9c-9257-cb09786e5c01)
        """
        pass

    def test_014_repeat_the_above_steps_for_tier2_sports(self):
        """
        DESCRIPTION: Repeat the above steps for Tier2 sports.
        EXPECTED: 
        """
        pass
