import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2605957_SSR_is_not_applied_anywhere_except_app_Home_page(Common):
    """
    TR_ID: C2605957
    NAME: SSR is not applied anywhere except app Home page
    DESCRIPTION: Test case verifies SSR is not applied anywhere except app Home page
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: Clear site data (Dev tools> Application > Clear Storage) before each step
    """
    keep_browser_open = True

    def test_001_paste_the_following_link_in_browserhomefeatured(self):
        """
        DESCRIPTION: Paste the following link in browser:
        DESCRIPTION: home/featured
        EXPECTED: SSR is applied (Splash screen is shown for a few seconds and then substituted with rendered snapshot)
        """
        pass

    def test_002_paste_the_following_link_in_browserhorse_racing(self):
        """
        DESCRIPTION: Paste the following link in browser:
        DESCRIPTION: /horse-racing
        EXPECTED: SSR is not applied
        """
        pass

    def test_003_paste_the_following_link_in_browserbetslipaddselection_id(self):
        """
        DESCRIPTION: Paste the following link in browser:
        DESCRIPTION: /betslip/add/selection_id
        EXPECTED: SSR is not applied
        """
        pass

    def test_004_paste_the_following_link_in_browseraz_sports(self):
        """
        DESCRIPTION: Paste the following link in browser:
        DESCRIPTION: /az-sports
        EXPECTED: SSR is not applied
        """
        pass

    def test_005_paste_the_following_link_in_browserin_play(self):
        """
        DESCRIPTION: Paste the following link in browser:
        DESCRIPTION: /in-play
        EXPECTED: SSR is not applied
        """
        pass
