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
class Test_C64594507_Verify_that_manual_Meta_tags_are_not_overwritten_by_the_Auto_generation(Common):
    """
    TR_ID: C64594507
    NAME: Verify that manual Meta tags are not overwritten by the Auto generation.
    DESCRIPTION: Verify that the existing Meta tittles and description in Manual SEO section is not over written for a competition by auto generation.
    PRECONDITIONS: * User should have access to CMS.
    PRECONDITIONS: * Note: Applicable to Mobile web.
    """
    keep_browser_open = True

    def test_001_log_into_cms_and_navigate_to_seo_gt_cms_gt_manual_section(self):
        """
        DESCRIPTION: Log into CMS and navigate to SEO &gt; CMS &gt; Manual section.
        EXPECTED: Available SEO pages are displayed.
        """
        pass

    def test_002_create_an_seo_page_for_a_competition_with_tittle_and_description_and_set_it_active(self):
        """
        DESCRIPTION: Create an SEO page for a competition with Tittle and Description and set it active.
        EXPECTED: SEO page is created for the competition.
        """
        pass

    def test_003_navigate_to_same_created_page_in_the_front_end_and_hover_the_cursor_over_the_browser_tabindexphpattachmentsgetf17d96e6_bd3c_41cd_b645_1b8524f2d7d0indexphpattachmentsget3a64bef1_74ea_414d_a10a_04e52be90cb5(self):
        """
        DESCRIPTION: Navigate to same created page in the front end and hover the cursor over the browser tab.
        DESCRIPTION: ![](index.php?/attachments/get/f17d96e6-bd3c-41cd-b645-1b8524f2d7d0) ![](index.php?/attachments/get/3a64bef1-74ea-414d-a10a-04e52be90cb5)
        EXPECTED: Manually input Page Tittle (Meta Tittle) is visible.
        """
        pass

    def test_004_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header_head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header 'head' call.
        EXPECTED: Manual SEO page tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/090a5119-32e0-4d7c-96df-f2df882961a2) ![](index.php?/attachments/get/25b7ec40-4482-4a91-90c5-842ac1bdcc34)
        """
        pass

    def test_005_repeat_steps_34_for_horse_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat Steps 3&4 for Horse, Greyhound races and Virtual sports.
        EXPECTED: Manual SEO page tittle and description are displayed.
        """
        pass

    def test_006_add_a_competition_template_in_the_cms_gt_seo_gt_automated_tags_page_if_not_availableeg_page_url___competitions_page_tittle___bet_on_ltcompetitiongt__ltsportgt_odds__ltbrandgt_page_description___betting__odds_on_ltcompetitiongt_or_find_the_latest_odds_ltsportgt__ltbrandgtcontent_in_the_angular_braces_should_not_be_changed(self):
        """
        DESCRIPTION: Add a competition template in the CMS &gt; SEO &gt; Automated Tags page. (if not available)
        DESCRIPTION: Eg:
        DESCRIPTION: * Page Url - /competitions
        DESCRIPTION: * Page tittle - Bet on &lt;competition&gt; | &lt;sport&gt; Odds | &lt;brand&gt;
        DESCRIPTION: * Page Description - Betting & Odds on &lt;competition&gt; or find the latest odds &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: (Content in the angular braces should not be changed)
        EXPECTED: Competition template is added successfully.
        """
        pass

    def test_007_launch_ladbrokescoral_url_and_navigate_to_the_competition_for_which_manual_seo_page_is_createdhover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Launch ladbrokes/Coral url and navigate to the competition for which Manual SEO page is created.
        DESCRIPTION: Hover the cursor over the browser tab.
        EXPECTED: Manual SEO page title is displayed.
        EXPECTED: ![](index.php?/attachments/get/5a1b0117-90dc-4f6d-aa0a-3c7c30e8fedc) ![](index.php?/attachments/get/2141faf8-b7ea-4d2d-a2bd-57d219016180)
        """
        pass

    def test_008_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header_head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header 'head' call.
        EXPECTED: Manual SEO page tittle and description should be displayed.
        EXPECTED: ![](index.php?/attachments/get/dbc7abb7-e1be-45a8-9c1a-6a023391f715) ![](index.php?/attachments/get/bb1b12d4-6394-43fc-a9ad-4768f3554ecc)
        """
        pass

    def test_009_repeat_steps_78_for_horse_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat Steps 7&8 for Horse, Greyhound races and Virtual sports.
        EXPECTED: Manual SEO page tittle and description should be displayed.
        """
        pass

    def test_010_choose_a_competition_for_which_no_seo_page_is_present_in_cms_gt_seo_gt_manual_section_navigate_to_that_competition_and_check_for_the_meta_tittle_in_the__front_end(self):
        """
        DESCRIPTION: Choose a Competition for which No SEO page is present in CMS &gt; SEO &gt; Manual section. Navigate to that competition and Check for the Meta tittle in the  front end.
        EXPECTED: Autogenerated Meta tittle is displayed.
        EXPECTED: ![](index.php?/attachments/get/1db75c43-ceee-4ef1-947e-7315385a5689) ![](index.php?/attachments/get/13d87550-783e-410c-8937-22271ea48159)
        """
        pass

    def test_011_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header_head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header 'head' call.
        EXPECTED: Autogenerated Meta Tags are displayed.
        EXPECTED: ![](index.php?/attachments/get/13c962c3-4df1-41b7-b768-7583e5aedeb6) ![](index.php?/attachments/get/eb203c1a-f8e6-43ee-b84a-c9bed031eaad)
        """
        pass

    def test_012_repeat_steps_1011_for_horse_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat Steps 10&11 for Horse, Greyhound races and Virtual sports.
        EXPECTED: Autogenerated Meta Tags are displayed.
        """
        pass

    def test_013_create_a_manual_seo_page_for_the_same_competition_in_cms(self):
        """
        DESCRIPTION: Create a manual SEO page for the same competition in CMS.
        EXPECTED: Manual SEO Page is created.
        """
        pass

    def test_014_navigate_to_the_same_in_the_front_end_and_reload_the_page_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to the same in the front end and reload the page. Hover the cursor over the browser tab.
        EXPECTED: Manual SEO Page tittle is displayed.
        EXPECTED: ![](index.php?/attachments/get/a6745bb0-6d38-45e3-bd78-b7100d7fb637) ![](index.php?/attachments/get/d73df89b-32a2-4fa4-89d7-e40ca61fec1f)
        """
        pass

    def test_015_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header_head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header 'head' call.
        EXPECTED: Manual Tags i.e. Tittle and Description are displayed.
        EXPECTED: ![](index.php?/attachments/get/3b0d7c8f-7956-43db-8522-84db08cb3ef5) ![](index.php?/attachments/get/03c8af01-b381-4bea-9330-22dd4e64977b)
        """
        pass

    def test_016_repeat_steps_1415_for_horse_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat Steps 14&15 for Horse, Greyhound races and Virtual sports.
        EXPECTED: Manual Tags i.e. Tittle and Description are displayed.
        """
        pass
