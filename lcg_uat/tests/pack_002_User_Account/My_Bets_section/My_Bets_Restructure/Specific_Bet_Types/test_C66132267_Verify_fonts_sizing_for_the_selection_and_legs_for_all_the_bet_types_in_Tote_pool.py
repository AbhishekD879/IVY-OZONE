import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66132267_Verify_fonts_sizing_for_the_selection_and_legs_for_all_the_bet_types_in_Tote_pool(Common):
    """
    TR_ID: C66132267
    NAME: Verify fonts, sizing for the selection and legs for all the bet types in Tote pool
    DESCRIPTION: This test case verify fonts, sizing for the selection and legs for all the bet types in Tote pool
    PRECONDITIONS: User should have a Horse Racing event
    PRECONDITIONS: Tote Pool market should be available
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_000_navigate_to__horse_racing_page(self):
        """
        DESCRIPTION: Navigate to  Horse racing page
        EXPECTED: Horse racing page is opened with all the available meetings
        """
        pass

    def test_000_check_for_the_events_which_has_tote_pools(self):
        """
        DESCRIPTION: Check for the events which has Tote Pools
        EXPECTED: Totepool market should be available with (WIN,Place,Exacta,Trifacta,Placepot,jackpot,ITV7placepot)
        """
        pass

    def test_000_place_bet_on_the_below_marketswinplaceexactatrifactaplacepotjackpotitv7placepot(self):
        """
        DESCRIPTION: Place bet on the below markets
        DESCRIPTION: WIN
        DESCRIPTION: Place
        DESCRIPTION: Exacta
        DESCRIPTION: Trifacta
        DESCRIPTION: Placepot
        DESCRIPTION: Jackpot
        DESCRIPTION: ITV7placepot
        EXPECTED: Bets should be placed successfully on all the mention markets
        """
        pass

    def test_000_navigate_to_my_bets_openpool_bets(self):
        """
        DESCRIPTION: Navigate to my bets-open(Pool bets)
        EXPECTED: Open tab should be available with the tote  bets placed
        """
        pass

    def test_000_check_the_font_and_size_of_the_lines_for_all_the_bets_placed(self):
        """
        DESCRIPTION: Check the Font and Size of the lines for all the bets placed
        EXPECTED: Lines should be as per the Figma deign
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/a807961d-2923-418a-bb46-cc2149626e4d)
        EXPECTED: ![](index.php?/attachments/get/20388ded-d9ac-4d30-b1a1-c7dec0b75ff7)
        EXPECTED: ![](index.php?/attachments/get/c67b37ee-32c1-43de-a9f3-46013d62c958)
        EXPECTED: ![](index.php?/attachments/get/d4c235cd-17df-4d42-8f35-b468ecd7b4cb)
        EXPECTED: **Coral**
        EXPECTED: ![](index.php?/attachments/get/c3147af9-0f3b-47cb-b2f0-7a257e7e8518)
        EXPECTED: ![](index.php?/attachments/get/9716f60c-7416-47a5-82d2-5dd655525dd4)
        EXPECTED: ![](index.php?/attachments/get/3dd1385a-190b-4bb3-8c7f-d66334cdbb79)
        EXPECTED: ![](index.php?/attachments/get/f53a2e06-9fad-496b-af9b-6fb68a156bf1)
        """
        pass

    def test_000_go_to_settle_bets_after_the_pool_bets_got_settle(self):
        """
        DESCRIPTION: Go to settle bets after the pool bets got settle
        EXPECTED: settle tab should be available with settled pool bets
        """
        pass

    def test_000_check_the_font_and_size_of_the_lines_and_race(self):
        """
        DESCRIPTION: Check the Font and Size of the lines and Race
        EXPECTED: Lines and race should be as per the Figma deign
        """
        pass
