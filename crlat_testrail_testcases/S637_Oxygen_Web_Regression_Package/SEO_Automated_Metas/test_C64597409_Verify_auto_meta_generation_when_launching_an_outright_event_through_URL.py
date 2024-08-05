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
class Test_C64597409_Verify_auto_meta_generation_when_launching_an_outright_event_through_URL(Common):
    """
    TR_ID: C64597409
    NAME: Verify auto meta generation when launching an outright event through URL.
    DESCRIPTION: Verify auto meta generation when launching an outright event through URL.
    PRECONDITIONS: * Outrights template is added in CMS &gt; SEO &gt; Automated Tags page.
    PRECONDITIONS: * Choose an event for which Manual SEO page is not set.
    PRECONDITIONS: NOTE: Applicable only to web in Mobile platforms.
    """
    keep_browser_open = True

    def test_001_navigate_to_any_outright_event_for_which_manual_seo_page_is_not_setcopy_the_url(self):
        """
        DESCRIPTION: Navigate to any outright event for which Manual SEO page is not set.
        DESCRIPTION: Copy the Url
        EXPECTED: Url is taken for the outright event.
        """
        pass

    def test_002_launch_the_url_in_a_different_window_preferred_incognito_hover_the_cursor_over_the_browser_tab_of_the_launched_url(self):
        """
        DESCRIPTION: Launch the url in a different window (preferred incognito). Hover the cursor over the Browser tab of the launched url.
        EXPECTED: Auto generated SEO tittle is displayed.
        EXPECTED: ![](index.php?/attachments/get/12fa1051-5817-4658-9bbd-e9a9a48f8d86) ![](index.php?/attachments/get/ddb5d941-1900-4de8-a9e4-0600bd3c484f)
        """
        pass

    def test_003_check_for_the_meta_tittle_and_description_in_inspection_window_gt_elements_tab_under_header___head_call(self):
        """
        DESCRIPTION: Check for the meta tittle and description in Inspection Window &gt; Elements tab under header - 'head' call.
        EXPECTED: Autogenerated Meta tittle and description are displayed.
        EXPECTED: ![](index.php?/attachments/get/32063298-95a2-4c10-bb69-9137ae180216) ![](index.php?/attachments/get/dbe7b82a-6af1-4838-86f7-dd23f9a890ef)
        """
        pass