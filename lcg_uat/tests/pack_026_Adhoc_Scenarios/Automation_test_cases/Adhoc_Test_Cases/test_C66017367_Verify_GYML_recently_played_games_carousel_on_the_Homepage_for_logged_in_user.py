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
class Test_C66017367_Verify_GYML_recently_played_games_carousel_on_the_Homepage_for_logged_in_user(Common):
    """
    TR_ID: C66017367
    NAME: Verify  GYML/recently played games  carousel on the Homepage for logged in user.
    DESCRIPTION: This test case verifies GYML/recently played games  carousel on the Homepage for logged in user.
    PRECONDITIONS: 1.Login to CMS.
    PRECONDITIONS: 2 Navigate to Hompage-&gt; Module Order-&gt;   'Recently Played Games Module' should be Active  and configure 'Game Count'  with positive value
    PRECONDITIONS: 3.Log into the application with the user who has played casino games recently
    PRECONDITIONS: Note: To view the RPG/GYML module in home page user must play atleast one game.
    """
    keep_browser_open = True

    def test_000_launch_the__application(self):
        """
        DESCRIPTION: Launch the  application
        EXPECTED: User should be able to launch the app should be see the Homepage is loaded successfully.
        """
        pass

    def test_000_log_into_the_application_with_the_user_who_visited_casinoand_played_at_least_one_game_recently(self):
        """
        DESCRIPTION: Log into the application with the user who visited casino
        DESCRIPTION: and played at least one game recently.
        EXPECTED: User is logged in &amp; user is able to see RPG/GYML Module
        """
        pass

    def test_000_verify_the_recently_played_gamesgames_you_might_like_module_is_displayed_in_carousel_form(self):
        """
        DESCRIPTION: Verify the Recently Played Games/Games You Might Like module is displayed in carousel form.
        EXPECTED: User should be able to see module displays in Carousel form which consists of the games that user recently played &amp; Other Games that user may like.
        """
        pass

    def test_000_verify_the_scrolling_of_rpggyml_carousel(self):
        """
        DESCRIPTION: Verify the scrolling of RPG/GYML carousel.
        EXPECTED: User should be able to smooth scroll in the carousel.
        """
        pass

    def test_000_validate_the_count_of_games_in_the_carousel(self):
        """
        DESCRIPTION: Validate the count of games in the Carousel
        EXPECTED: User should be able to see the total number of games is matched with 'Games Count' which is configued in the CMS
        EXPECTED: Note:
        EXPECTED: If Game count is set as 10
        EXPECTED: 10 games are displayed in the carousel
        EXPECTED: If user played 4 casino games recently then the above 10 games are aligned in the form of 4 recently played games followed by other games that user may like
        EXPECTED: *If Game count is set as 5
        EXPECTED: 5 games are displayed in the carousel
        EXPECTED: If user played 5 casino games recently then the above 5 games are aligned only with 5 recently played games
        """
        pass

    def test_000_verify_the_game_name_in_the_carousel(self):
        """
        DESCRIPTION: Verify the game name in the carousel
        EXPECTED: If game name has one line of characters then the label/game name is displayed within one line under the image of game
        EXPECTED: If game name has two lines of characters then the label/game name is displayed within two lines under the image of game
        EXPECTED: If game name exceeds two lines of characters then the label/game name is displayed within two lines under the image of game even though the game name is more than two lines
        EXPECTED: And ellipses comes into the picture means three dots are shown at the end of second line
        """
        pass
