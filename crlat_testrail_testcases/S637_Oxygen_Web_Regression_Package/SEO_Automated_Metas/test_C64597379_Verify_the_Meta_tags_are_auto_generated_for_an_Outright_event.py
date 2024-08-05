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
class Test_C64597379_Verify_the_Meta_tags_are_auto_generated_for_an_Outright_event(Common):
    """
    TR_ID: C64597379
    NAME: Verify the Meta tags are auto generated for an Outright event.
    DESCRIPTION: Verify that meta tittle and Description (Page tittle and Description) are auto generated for an Outright event.
    PRECONDITIONS: * Choose an outright event for which no SEO page is set in CMS &gt; SEO &gt; Manual section.
    PRECONDITIONS: * Create an outright event in OB. (If there are no existing outrights.)
    PRECONDITIONS: ** Note: Applicable to only web in mobile platforms
    """
    keep_browser_open = True

    def test_001_add_an_outright_template_in_cms_gt_seo_gt_automated_tags_if_not_availableegpage_tittle___bet_on_ltcompetitiongt_winner__ltsportgt_odds__ltbrandgtpage_description___betting__odds_on_ltcompetitiongt_outright_winner_or_find_the_latest_odds__ltsportgt__ltbrandgt_important_note_content_in_the_angular_braces_should_not_be_changed(self):
        """
        DESCRIPTION: Add an Outright template in CMS &gt; SEO &gt; Automated Tags (if not available)
        DESCRIPTION: Eg:
        DESCRIPTION: Page tittle - Bet on &lt;competition&gt; winner | &lt;sport&gt; Odds | &lt;brand&gt;
        DESCRIPTION: Page Description - Betting & Odds on &lt;competition&gt; outright winner or find the latest odds  &lt;sport&gt; | &lt;brand&gt;
        DESCRIPTION: ** Important Note: Content in the angular braces should not be changed.
        EXPECTED: Template is added successfully.
        """
        pass

    def test_002_navigate_to_any_outright_in_the_front_end_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Navigate to any outright in the front end. Hover the cursor over the browser tab.
        EXPECTED: Auto generated meta tittle is displayed with the specific details of the event.
        EXPECTED: ![](index.php?/attachments/get/d9a4242e-8f4b-4ac1-a409-9df957081b30) ![](index.php?/attachments/get/fce48698-d3cf-43e1-a35a-5c58fc8b9328)
        """
        pass

    def test_003_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_callwhere_the_event_competition_sport_and_brand_should_contain_the_currently_opened_sport_event_details(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        DESCRIPTION: where the 'event', 'competition', 'sport' and 'brand' should contain the currently opened sport event details.
        EXPECTED: Auto generated meta tittles are displayed as per the template set in CMS.
        EXPECTED: ![](index.php?/attachments/get/3d1fcbe1-691f-46e0-80bb-5e5f4e6c5365) ![](index.php?/attachments/get/42d1610b-b305-4883-91bd-03258e651a96)
        """
        pass

    def test_004_repeat_the_above_steps_for_horse_greyhound_racesfor_races_check_for_the_antepost_events(self):
        """
        DESCRIPTION: Repeat the above Steps for Horse, Greyhound races.
        DESCRIPTION: For Races check for the Antepost events.
        EXPECTED: 
        """
        pass
