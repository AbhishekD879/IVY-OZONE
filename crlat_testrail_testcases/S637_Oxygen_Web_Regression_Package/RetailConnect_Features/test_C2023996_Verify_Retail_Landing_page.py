import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2023996_Verify_Retail_Landing_page(Common):
    """
    TR_ID: C2023996
    NAME: Verify Retail Landing page
    DESCRIPTION: This test case verifies Connect Landing page in sportsbook app
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: BMA-30799 Connect landing page with menu
    DESCRIPTION: BMA-35064 Menu items in RHM/LP/A-Z
    PRECONDITIONS: To configure Retail Page content use CMS:
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: https://CMS_ENDPOINT -> Chose 'sportsbook' channel -> 'Menus' -> Retail Menus (obsolete 'Connect Menus')
    PRECONDITIONS: **Note that on UI Retail page should be named as 'Connect' for Coral App **
    PRECONDITIONS: 1. Load SportsBook App
    PRECONDITIONS: 2. Chose 'Connect' from header ribbon
    """
    keep_browser_open = True

    def test_001_check_the_structure_of_retail_landing_page(self):
        """
        DESCRIPTION: Check the structure of Retail landing page
        EXPECTED: - '< Connect'  back button
        EXPECTED: - Banners carousel
        EXPECTED: - Features that were set up in CMS (in Retail Menus) (One exception is 'Use Connect Online' item, it's shown only for logged in In-Shop user)
        EXPECTED: - Each feature is represented with the icon, title, and a brief description
        EXPECTED: - Link to each feature '>'
        """
        pass

    def test_002_open_link__to_each_feature(self):
        """
        DESCRIPTION: Open link '>' to each feature
        EXPECTED: A user can access each feature and navigate back to Landing page using the back button
        """
        pass

    def test_003_go_to_cms_and_change_title_subtitle_icon_for_any_retail_landing_page_item(self):
        """
        DESCRIPTION: Go to CMS and change Title/ Subtitle/ icon for any Retail landing page item
        EXPECTED: All changes are mirrored on interface respectively
        """
        pass
