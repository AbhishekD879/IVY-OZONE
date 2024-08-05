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
class Test_C64594482_Verify_the_Auto_generated_meta_tittle_and_description_for_a_competition(Common):
    """
    TR_ID: C64594482
    NAME: Verify the Auto generated meta tittle and description for a competition.
    DESCRIPTION: Verify the Auto generated meta tittle and description for a competition according to the template set in the Automated tags section in CMS.
    PRECONDITIONS: * Choose a competition for which meta tittle and description are not predefined in the CMS &gt; SEO &gt; Manual section. (Create a competition in OB.
    PRECONDITIONS: Add Events, Markets and selections to the created competition if not available)
    PRECONDITIONS: * Launch the Ladbrokes/Coral url.
    PRECONDITIONS: Note: Applicable to Mobile Web.
    """
    keep_browser_open = True

    def test_001_add_a_competition_template_in_the_cms_gt_seo_gt_automated_tags_page_if_not_availableegpage_url___competitionspage_tittle___bet_on_ltcompetitiongt__ltsportgt_odds__ltbrandgtpage_description___betting__odds_on_ltcompetitiongt_or_find_the____latest_odds_ltsportgt__ltbrandgt_important_note_content_in_the_angular_braces_should_not_be_changed(self):
        """
        DESCRIPTION: Add a competition template in the CMS &gt; SEO &gt; Automated Tags page. (if not available)
        DESCRIPTION: Eg:
        DESCRIPTION: *Page Url - /competitions
        DESCRIPTION: *Page tittle - Bet on &lt;competition&gt; | &lt;sport&gt; Odds | &lt;brand&gt;
        DESCRIPTION: *Page Description - Betting & Odds on &lt;competition&gt; or find the    latest odds &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: ** Important Note: Content in the angular braces should not be changed.
        EXPECTED: Template created successfully.
        """
        pass

    def test_002_navigate_to_the_competition_created_or_chosen(self):
        """
        DESCRIPTION: Navigate to the competition created or chosen.
        EXPECTED: Landed on to the competition page.
        """
        pass

    def test_003_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Hover the cursor over the browser tab.
        EXPECTED: The tittle is in the format defined in CMS &gt; SEO auto
        EXPECTED: page with the specific details of the opened competition.
        EXPECTED: ![](index.php?/attachments/get/498ccc6a-8723-4e6a-bba9-a18f7932b59d)
        EXPECTED: ![](index.php?/attachments/get/dc9a3299-a6f2-4775-b05b-dbc54f412e92)   ![](index.php?/attachments/get/b8b986ca-d4b9-4ca5-a69a-52140292d419)
        """
        pass

    def test_004_check_for_the_meta_tittle_and_description_in_the_inspection_window_gt_elements_tab_under_header_head_callwhere_competition_sport_and_brand_should_contain_the_currently_opened_competition_details_as_per_the_template_set_in_the_cms_gt_seo_gt_automated_tagsindexphpattachmentsgetda2bd03e_7405_4861_a3c1_3819828d756cindexphpattachmentsgetefcc7eb5_d70d_4bb4_ab6b_1f4661bd4a3a(self):
        """
        DESCRIPTION: Check for the meta tittle and description in the Inspection Window &gt; Elements tab under header 'head' call.
        DESCRIPTION: where 'competition', 'sport' and 'brand' should contain the currently opened competition details. (As per the template set in the CMS &gt; SEO &gt; Automated Tags.)
        DESCRIPTION: ![](index.php?/attachments/get/da2bd03e-7405-4861-a3c1-3819828d756c)![](index.php?/attachments/get/efcc7eb5-d70d-4bb4-ab6b-1f4661bd4a3a)
        EXPECTED: The tittle and description are as per the template set with the specific details of the Competition page opened.
        """
        pass

    def test_005_repeat_steps1_4_for_horse_and_greyhound_races_and_virtual_sports(self):
        """
        DESCRIPTION: Repeat Steps:1-4 for Horse and Greyhound races and Virtual sports.
        EXPECTED: The Meta tittle and description should be auto generated.
        """
        pass
