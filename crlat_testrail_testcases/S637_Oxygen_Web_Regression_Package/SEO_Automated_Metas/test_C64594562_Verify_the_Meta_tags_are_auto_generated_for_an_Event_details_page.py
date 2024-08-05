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
class Test_C64594562_Verify_the_Meta_tags_are_auto_generated_for_an_Event_details_page(Common):
    """
    TR_ID: C64594562
    NAME: Verify the Meta tags are auto generated for an Event details page.
    DESCRIPTION: Verify the Meta tittle and description are auto generated for an Event details page.
    PRECONDITIONS: * Create an event in OB.
    PRECONDITIONS: * No SEO page is created in CMS &gt; SEO &gt; Manual section for the chosen event.
    """
    keep_browser_open = True

    def test_001_add_the_event_template_in_cms_gt_seo_gt_automated_tags_pageeg__page_url___event_page_tittle___bet_on_lteventgt__ltcompetitiongt_ltsportgt__ltbrandgt_page_description___betting__odds_on_lteventgt__ltcompetitiongt_______ltsportgt__ltbrandgtmake_sure_that_variables_or_the_content_within_the_angular_braces_is_not_changed(self):
        """
        DESCRIPTION: Add the event template in CMS &gt; SEO &gt; Automated Tags page.
        DESCRIPTION: Eg :
        DESCRIPTION: * Page Url - /event
        DESCRIPTION: * Page Tittle - Bet on &lt;event&gt; | &lt;competition&gt; &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: * Page Description - Betting & Odds on &lt;event&gt; | &lt;competition&gt;       &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: (Make sure that variables or the content within the angular braces is not changed.)
        EXPECTED: Template is added successfully.
        """
        pass

    def test_002_navigate_to_tier_1_sport_slp_page_gt_event_details_page_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to Tier-1 sport SLP page &gt; Event details page. Hover the cursor over the Browser tab.
        EXPECTED: The meta tittle is auto generated for the event as per the template set in the CMS.
        EXPECTED: ![](index.php?/attachments/get/163bf1de-0ed7-4244-adfa-22eb785c77fe) ![](index.php?/attachments/get/2db3af1b-7aca-471d-b4df-2aa20dd8c586)
        """
        pass

    def test_003_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_callwhere_the_event_competition_sport_and_brand_should_contain_the_currently_opened_sport_event_details(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        DESCRIPTION: where the 'event', 'competition', 'sport' and 'brand' should contain the currently opened sport event details.
        EXPECTED: Meta tittles and description are displayed as per the template set in the CMS &gt; SEO &gt; Automated Tags.
        EXPECTED: ![](index.php?/attachments/get/432fa3ee-510e-4e2d-b495-3ef6fc268160) ![](index.php?/attachments/get/cf4674f9-07db-423f-a590-dbb1ee02d553)
        """
        pass

    def test_004_repeat_the_steps_23_for_all_the_tier_12_virtual_sports_horse_and_greyhound_races(self):
        """
        DESCRIPTION: Repeat the Steps 2&3 for all the Tier-1&2, Virtual sports, Horse and Greyhound races.
        EXPECTED: Meta tittles and description are displayed as per the template set in the CMS &gt; SEO &gt; Automated Tags.
        """
        pass
