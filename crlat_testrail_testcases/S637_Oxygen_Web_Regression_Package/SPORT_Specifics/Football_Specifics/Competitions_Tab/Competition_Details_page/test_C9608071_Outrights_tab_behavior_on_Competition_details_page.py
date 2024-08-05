import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C9608071_Outrights_tab_behavior_on_Competition_details_page(Common):
    """
    TR_ID: C9608071
    NAME: Outrights tab behavior on Competition details page
    DESCRIPTION: Test case verifies Outrights tab display on Competition details page depending on outrights availability
    PRECONDITIONS: Competitions tab on Football is opened
    PRECONDITIONS: How to create Outrights:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+create+Outrights
    """
    keep_browser_open = True

    def test_001_navigate_to_details_page_of_a_competition_without_outrightsverify_tabs(self):
        """
        DESCRIPTION: Navigate to details page of a competition without outrights.
        DESCRIPTION: Verify tabs
        EXPECTED: - Outrights tab is not displayed
        EXPECTED: - Matches and Results tab are present
        """
        pass

    def test_002_navigate_to_details_page_of_a_competition_with_outrightsverify_tabs(self):
        """
        DESCRIPTION: Navigate to details page of a competition with outrights.
        DESCRIPTION: Verify tabs
        EXPECTED: 3 tabs are displayed on Competition details page
        EXPECTED: - Matches
        EXPECTED: - Outrights
        EXPECTED: - Results
        """
        pass

    def test_003_tap_on_outrights_tab_inside_competition_details_page(self):
        """
        DESCRIPTION: Tap on Outrights tab inside Competition details page
        EXPECTED: - Outrights tab is opened
        EXPECTED: - Outrights are displayed as quick links with arrow
        """
        pass

    def test_004_tap_on_the_outright(self):
        """
        DESCRIPTION: Tap on the outright
        EXPECTED: - Outright page with markets is opened
        """
        pass
