import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C47047436_Verify_content_of_5_A_Side_tab(Common):
    """
    TR_ID: C47047436
    NAME: Verify content of  '5-A-Side' tab
    DESCRIPTION: This test case verifies content displayed on '5-A-Side' tab
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that the '5-A-Side' tab should be switched off in case Static Block is disabled because it's part of path for reaching the '5-A-Side' overlay.
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    """
    keep_browser_open = True

    def test_001__clicktap_on_the_5_a_side_tab_verify_5_a_side_tab_content(self):
        """
        DESCRIPTION: * Click/Tap on the '5-A-Side' tab.
        DESCRIPTION: * Verify '5-A-Side' tab content
        EXPECTED: * Content corresponds to 'five-a-side-launcher' static block in CMS > Static Blocks
        EXPECTED: * 'five-a-side-launcher' response is received from CMS with data set in CMS
        """
        pass

    def test_002__edit_html_markupopen_source_code_for_editing_field_in_cms__static_blocks__five_a_side_launcher_save_changes(self):
        """
        DESCRIPTION: * Edit 'Html Markup'(open 'Source Code' for editing) field in CMS > Static Blocks > 'five-a-side-launcher'.
        DESCRIPTION: * Save changes.
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_003__back_to_the_app_refresh_event_details_page_clicktap_on_the_5_a_side_tab_and_verify_the_content(self):
        """
        DESCRIPTION: * Back to the app refresh event details page.
        DESCRIPTION: * Click/Tap on the '5-A-Side' tab and verify the content.
        EXPECTED: * Changes made for the static block in CMS are reflected
        EXPECTED: * 'five-a-side-launcher' response is received from CMS with data set in CMS
        """
        pass
