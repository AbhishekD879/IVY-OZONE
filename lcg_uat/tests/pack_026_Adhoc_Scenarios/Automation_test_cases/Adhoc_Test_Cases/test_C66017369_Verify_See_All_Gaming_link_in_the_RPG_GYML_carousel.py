import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C66017369_Verify_See_All_Gaming_link_in_the_RPG_GYML_carousel(Common):
    """
    TR_ID: C66017369
    NAME: Verify 'See All Gaming' link in the RPG/GYML carousel
    DESCRIPTION: This test case verifies See All Gaming' link in the RPG/GYML carousel
    DESCRIPTION: on the Homepage for logged IN user.
    PRECONDITIONS: 1.Login to CMS.
    PRECONDITIONS: 2 Navigate to Hompage-&gt; Module Order-&gt;   'Recently Played Games Module' should be Active  and configure 'Game Count'  with positive value
    PRECONDITIONS: 3.Log into the application with the user who has played casino games recently
    PRECONDITIONS: Note: To view the RPG/GYML module in home page user must play at least one game.
    """
    keep_browser_open = True

    def test_000_launch_the__application(self):
        """
        DESCRIPTION: Launch the  application
        EXPECTED: RPG/GYML module is not displayed  when user is not logged in
        """
        pass

    def test_000_click_on_see_all_gaming_ampgt_link(self):
        """
        DESCRIPTION: Click on 'See All Gaming &amp;gt;' link
        EXPECTED: User should be redirected to the gaming page.
        """
        pass
