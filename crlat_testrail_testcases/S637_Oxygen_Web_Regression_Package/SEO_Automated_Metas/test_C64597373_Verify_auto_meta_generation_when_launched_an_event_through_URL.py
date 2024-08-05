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
class Test_C64597373_Verify_auto_meta_generation_when_launched_an_event_through_URL(Common):
    """
    TR_ID: C64597373
    NAME: Verify auto meta generation when launched an event through URL.
    DESCRIPTION: Verify the auto tittles are generated when launching an event through URL.
    PRECONDITIONS: * Choose an event for which no SEO page in set in CMS &gt; SEO &gt; Manual section.
    PRECONDITIONS: * Applicable to Mobile Web.
    """
    keep_browser_open = True

    def test_001_copy_the_url_of_an_edp_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Copy the url of an EDP. Hover the cursor over the browser tab.
        EXPECTED: Url is copied.
        """
        pass

    def test_002_launch_the_url_in_different_window_preferably_in_an_incognito_window_hover_the_cursor_over_the_browser_tab(self):
        """
        DESCRIPTION: Launch the Url in different window, preferably in an incognito window. Hover the cursor over the browser tab.
        EXPECTED: Meta tittle is auto generated.
        EXPECTED: ![](index.php?/attachments/get/b21dd89f-dd56-41a4-b7f0-01b961fa0498) ![](index.php?/attachments/get/09604057-2e53-4e88-a1fb-3122394a068b)
        """
        pass

    def test_003_check_for_the_meta_tittle_and_description_in_the_inspection_window_gt_elements_tab_under_header_head_callwhere_competition_sport_and_brand_should_contain_the_currently_opened_competition_details_as_per_the_template_set_in_the_cms_gt_seo_gt_automated_tags(self):
        """
        DESCRIPTION: Check for the meta tittle and description in the Inspection Window &gt; Elements tab under header 'head' call.
        DESCRIPTION: where 'competition', 'sport' and 'brand' should contain the currently opened competition details. (As per the template set in the CMS &gt; SEO &gt; Automated Tags.)
        EXPECTED: Automated page tittle and descriptions are visible.
        EXPECTED: ![](index.php?/attachments/get/a727a993-2e57-42b7-bb8f-2164cb899c0e)  ![](index.php?/attachments/get/a1bb8266-8037-4da1-88e9-9722206ddd19)
        """
        pass
