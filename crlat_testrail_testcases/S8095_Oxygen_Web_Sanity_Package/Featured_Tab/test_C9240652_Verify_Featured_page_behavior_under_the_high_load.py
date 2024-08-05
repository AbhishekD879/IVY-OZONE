import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C9240652_Verify_Featured_page_behavior_under_the_high_load(Common):
    """
    TR_ID: C9240652
    NAME: Verify  'Featured'  page behavior under the high load
    DESCRIPTION: This test case verifies front end behavior of 'Featured' page during high load times
    PRECONDITIONS: This test case should be run during high load on 'Featured' page on 3g network:
    PRECONDITIONS: - big number of users connected to Featured MS
    PRECONDITIONS: - big number of Featured events (e.g. 10  modules of all types, 100 events on the page - TO BE CLARIFIED)
    PRECONDITIONS: - big number of Live updates for Featured events (price updates, suspensions)
    PRECONDITIONS: On TEST2/STG end points: Featured load to be requested from the Automation team
    PRECONDITIONS: On PROD end points: test case to be run during Performance tests or busy weekends
    """
    keep_browser_open = True

    def test_001_load_the_homepage___featured_tabsection(self):
        """
        DESCRIPTION: Load the Homepage -> 'Featured' tab/section
        EXPECTED: - 'Featured' page is loaded smoothly
        EXPECTED: - There is not long loading spinner while content is not shown yet
        EXPECTED: - Content is displayed correctly
        EXPECTED: - The page is rendered correctly
        """
        pass

    def test_002_expandcollapse_accordions(self):
        """
        DESCRIPTION: Expand/collapse accordions
        EXPECTED: - 'Accordions' can be expanded/collapsed
        EXPECTED: - No issues with delays of showing content or rendering of the page
        """
        pass

    def test_003_swipe_to_the_bottomto_the_top(self):
        """
        DESCRIPTION: Swipe to the bottom/to the top
        EXPECTED: - Page can be swiped to the top/to the bottom
        EXPECTED: - No issues with delays of showing content or rendering of the page
        """
        pass

    def test_004_verify_live_updates(self):
        """
        DESCRIPTION: Verify live updates
        EXPECTED: - Live updates are displayed on 'Featured' page
        EXPECTED: - No issues with delays of showing content or rendering of the page
        """
        pass
