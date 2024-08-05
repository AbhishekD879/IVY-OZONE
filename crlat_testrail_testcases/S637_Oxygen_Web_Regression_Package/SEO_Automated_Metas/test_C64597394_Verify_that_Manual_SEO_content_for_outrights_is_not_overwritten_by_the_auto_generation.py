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
class Test_C64597394_Verify_that_Manual_SEO_content_for_outrights_is_not_overwritten_by_the_auto_generation(Common):
    """
    TR_ID: C64597394
    NAME: Verify that Manual SEO content for outrights is not overwritten by the auto generation.
    DESCRIPTION: Verify that manually given Meta tittles (Page tittle and description) in CMS are not over written by the auto generated tittles.
    PRECONDITIONS: * Choose an Outright  for which tags are predefined in CMS &gt; SEO &gt; Manual section. (Create a manual SEO page for the outright if not available)
    PRECONDITIONS: Note: Applicable to web in Mobile platform.
    """
    keep_browser_open = True

    def test_001_navigate_to_an_outright_event_in_the_front_for_which_seo_page_is_set_in_cms_gt_seo_gt_manual_sectionhover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to an outright event in the front for which SEO page is set in CMS &gt; SEO &gt; Manual section.
        DESCRIPTION: Hover the cursor over the browser tab.
        EXPECTED: Landed on to the outright page.
        EXPECTED: Meta tittle is displayed same as set in Manual SEO page.
        """
        pass

    def test_002_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Manual SEO page tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/da1c6af9-9768-419c-b95b-c5810285993d) ![](index.php?/attachments/get/7372fc54-7f21-4f4c-878e-94a5367ef6fc)
        """
        pass

    def test_003_add_outright_template_in__cms_gt_seo_gt_automated_tags_pageeg_page_tittle___bet_on_ltcompetitiongt_winner__ltsportgt_odds__ltbrandgtpage_description___betting__odds_on_ltcompetitiongt_outright_winner_or_find_the_latest_odds__ltsportgt__ltbrandgtcontent_in_angular_braces_should_not_be_changed(self):
        """
        DESCRIPTION: Add Outright template in  CMS &gt; SEO &gt; Automated Tags page.
        DESCRIPTION: eg :
        DESCRIPTION: Page tittle - Bet on &lt;competition&gt; winner | &lt;sport&gt; Odds | &lt;brand&gt;
        DESCRIPTION: Page Description - Betting & Odds on &lt;competition&gt; outright winner or find the latest odds  &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: (Content in angular braces should not be changed.)
        EXPECTED: Template added successfully.
        """
        pass

    def test_004_navigate_to_the_competition_for_which_manual_seo_page_is_setcheck_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Navigate to the competition for which Manual SEO page is set.
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Manual SEO page tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/15d2fc74-adeb-4592-86fb-4a5070921239)  ![](index.php?/attachments/get/99363137-c082-424f-9bf3-d1ede61f4b64)
        """
        pass

    def test_005_remove_the_manual_seo_page_in_cms_for_the_outright_page(self):
        """
        DESCRIPTION: Remove the Manual SEO page in CMS for the outright page.
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_the_same_event_in_the_front_end_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to the same event in the front end. Hover the cursor over the browser tab.
        EXPECTED: Auto generated tittle is visible.
        EXPECTED: ![](index.php?/attachments/get/efcdf2e0-8b95-4eab-a25e-8c7fd93db703) ![](index.php?/attachments/get/44979de8-c072-4624-b986-2f385198dd65)
        """
        pass

    def test_007_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Auto generated tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/8e646701-a15e-4388-9661-a982cab16041) ![](index.php?/attachments/get/1b9f62e4-6307-4798-a3ba-3e5df9176130)
        """
        pass

    def test_008_remove_the_outright_template_from_cms_gt_seo_gt_automated_tags(self):
        """
        DESCRIPTION: Remove the Outright template from CMS &gt; SEO &gt; Automated tags.
        EXPECTED: Template removed successfully.
        """
        pass

    def test_009_navigate_to_any_competition_for_which_manual_seo_page_is_set(self):
        """
        DESCRIPTION: Navigate to any competition for which Manual SEO page is set.
        EXPECTED: Manual SEO page tittle is displayed.
        EXPECTED: ![](index.php?/attachments/get/20ed1a5b-e00f-4c06-b6d7-ebdc56cbda20) ![](index.php?/attachments/get/b39b896e-e4a6-4fef-8af5-8f68c238b3d2)
        """
        pass

    def test_010_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Manually set SEO page tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/6b497f44-008b-444e-b54e-fef2369b9e66) ![](index.php?/attachments/get/be0afd7a-d635-421d-8ada-a55bcbc955c3)
        """
        pass

    def test_011_create_an_seo_page_with_only_page_tittle_in_cms_gt_seo_gt_manual_sectionindexphpattachmentsget776e706b_e2b1_485b_a59b_34acedc15e70(self):
        """
        DESCRIPTION: Create an SEO page with only Page tittle in CMS &gt; SEO &gt; Manual section.
        DESCRIPTION: ![](index.php?/attachments/get/776e706b-e2b1-485b-a59b-34acedc15e70)
        EXPECTED: SEO page created successfully.
        """
        pass

    def test_012_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Manual SEO page tittle with no empty description content is visible.
        EXPECTED: ![](index.php?/attachments/get/c0fa2717-4661-4c5a-a31f-5a4d9fb045c3) ![](index.php?/attachments/get/d2c0a78c-167d-4cfe-830c-dd6a7fe747a4)
        """
        pass

    def test_013_add_outright_template_in__cms_gt_seo_gt_automated_tags_pageeg_page_tittle___bet_on_ltcompetitiongt_winner__ltsportgt_odds__ltbrandgtpage_description___betting__odds_on_ltcompetitiongt_outright_winner_or_find_the_latest_odds__ltsportgt__ltbrandgtcontent_in_angular_braces_should_not_be_changed(self):
        """
        DESCRIPTION: Add Outright template in  CMS &gt; SEO &gt; Automated Tags page.
        DESCRIPTION: eg :
        DESCRIPTION: Page tittle - Bet on &lt;competition&gt; winner | &lt;sport&gt; Odds | &lt;brand&gt;
        DESCRIPTION: Page Description - Betting & Odds on &lt;competition&gt; outright winner or find the latest odds  &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: (Content in angular braces should not be changed.)
        EXPECTED: Template added successfully
        """
        pass

    def test_014_set_the_manual_seo_page_for_the_outrights_event_to_inactive(self):
        """
        DESCRIPTION: Set the manual SEO page for the outrights event to inactive.
        EXPECTED: SEO page is deactivated.
        """
        pass

    def test_015_navigate_to_the_competition_for_which_manual_seo_page_is_set_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to the competition for which Manual SEO page is set. Hover the cursor over the browser tab.
        EXPECTED: Page tittle is auto generated.
        EXPECTED: ![](index.php?/attachments/get/9e30c092-34ff-4793-ba9f-b27c8461959a) ![](index.php?/attachments/get/76d69afd-5b54-405c-bc93-ecb9e017b04b)
        """
        pass

    def test_016_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Auto generated tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/be864840-cab7-43d8-b4a1-3feb3b923784) ![](index.php?/attachments/get/8ba03a86-55fb-4b8b-9cd3-216d23a3b207)
        """
        pass

    def test_017_repeat_the_above_steps_for_horse_and_greyhound_races(self):
        """
        DESCRIPTION: Repeat the above steps for Horse and greyhound races.
        EXPECTED: 
        """
        pass
