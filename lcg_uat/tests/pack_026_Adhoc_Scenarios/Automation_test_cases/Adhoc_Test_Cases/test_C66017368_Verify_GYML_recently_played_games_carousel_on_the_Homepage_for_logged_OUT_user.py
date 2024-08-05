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
class Test_C66017368_Verify_GYML_recently_played_games_carousel_on_the_Homepage_for_logged_OUT_user(Common):
    """
    TR_ID: C66017368
    NAME: Verify  GYML/recently played games  carousel on the Homepage for logged OUT user.
    DESCRIPTION: This test case verifies GYML/recently played games  carousel
    DESCRIPTION: on the Homepage for logged OUT user.
    PRECONDITIONS: 1.Login to CMS.
    PRECONDITIONS: 2 Navigate to Hompage-&gt; Module Order-&gt;   'Recently Played Games Module' should be Active  and configure 'Game Count'  with positive value
    PRECONDITIONS: Note: To view the RPG/GYML module in home page user must play at least one game.
    """
    keep_browser_open = True

    def test_000_launch_the__application(self):
        """
        DESCRIPTION: Launch the  application
        EXPECTED: User should be able to launch the app should be see the Homepage is loaded successfully.
        """
        pass

    def test_000_verify_the_recently_played_gamesgames_you_might_likerpggyml_module_in_the_homepage(self):
        """
        DESCRIPTION: Verify the Recently Played Games/Games You Might Like(RPG/GYML) module in the homepage
        EXPECTED: RPG/GYML module is not displayed  when user is not logged in
        """
        pass
