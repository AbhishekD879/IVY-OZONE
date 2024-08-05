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
class Test_C64597404_Verify_that_auto_generated_meta_tags_can_be_updated(Common):
    """
    TR_ID: C64597404
    NAME: Verify that auto generated meta tags can be updated
    DESCRIPTION: Verify that the tittle and description auto generated can be updated.
    PRECONDITIONS: * Outrights template should be added in CMS &gt; SEO &gt; Automated Tags if not available
    PRECONDITIONS: * Choose an outright event for which Manual SEO page is not set.
    PRECONDITIONS: * Revert the changes after the execution is done.
    PRECONDITIONS: Eg:
    PRECONDITIONS: Page Url - /outrights
    PRECONDITIONS: Page Tittle - Bet on &lt;competition&gt; winner | &lt;sport&gt; Odds | &lt;brand&gt;
    PRECONDITIONS: Page Description - Betting & Odds on &lt;competition&gt; outright winner or find the latest odds  &lt;sport&gt; | &lt;brand&gt;
    PRECONDITIONS: The content in the angular braces should not be changed.
    PRECONDITIONS: Note: Applicable only to web in Mobile platform.
    """
    keep_browser_open = True

    def test_001_navigate_to_any_outright_event_in_front_end_for_which_no_manual_seo_page_is_set_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to any outright event in front end for which no Manual SEO page is set. Hover the cursor over the browser tab.
        EXPECTED: Auto Generated Meta/Page tittle is displayed.
        EXPECTED: ![](index.php?/attachments/get/2181f7ad-ec6d-4fab-8e85-eea835253cd4) ![](index.php?/attachments/get/8da09856-b03c-4e8f-be66-fa5256c22775)
        """
        pass

    def test_002_update_the_template_for_outrights_in_cms_gt_seo_gt_automated_tags_sectionmake_sure_that_content_in_the_angular_braces_is_not_changed(self):
        """
        DESCRIPTION: Update the template for Outrights in CMS &gt; SEO &gt; Automated tags section.
        DESCRIPTION: (Make sure that content in the angular braces is not changed)
        EXPECTED: Template updated successfully.
        """
        pass

    def test_003_navigate_to_any_outright_event_for_which_no_manual_seo_page_is_set_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to any outright event for which no Manual SEO page is set. Hover the cursor over the Browser tab.
        EXPECTED: Updated Tittle with the specific details of the event opened is displayed.
        EXPECTED: ![](index.php?/attachments/get/ae10ebc0-bb63-4c97-be31-3258c0ed1a0d) ![](index.php?/attachments/get/e0bd1253-ed8c-4cb3-89b7-7e203577ddfb)
        """
        pass

    def test_004_repeat_step_3_for_horse_and_greyhounds_races(self):
        """
        DESCRIPTION: Repeat Step-3 for Horse and Greyhounds races.
        EXPECTED: 
        """
        pass
