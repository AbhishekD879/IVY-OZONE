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
class Test_C57732075_Verify_opening_different_pages_of_Correct_4(Common):
    """
    TR_ID: C57732075
    NAME: Verify opening different pages of Correct 4
    DESCRIPTION: This test case verifies opening different pages of Correct4 (e.g. directly to end page)
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. User NOT played Correct 4 before
    PRECONDITIONS: **NOTE: use your current domain name instead of 'https://phoenix-invictus.coral.co.uk/' and current source id instead of 'correct4' e.g. '/qe/survey1'**
    """
    keep_browser_open = True

    def test_001_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4splashhttpsphoenix_invictuscoralcoukcorrect4questionshttpsphoenix_invictuscoralcoukcorrect4afterlatest_quizhttpsphoenix_invictuscoralcoukcorrect4infoprizeshttpsphoenix_invictuscoralcoukcorrect4infofaqhttpsphoenix_invictuscoralcoukcorrect4infoterms(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/splash
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/questions
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/after/latest-quiz
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/prizes
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/faq
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/terms
        EXPECTED: - Links should be successfully opened
        """
        pass

    def test_002_make_prediction_to_active_quiz(self):
        """
        DESCRIPTION: Make prediction to active Quiz
        EXPECTED: Predictions successfully made
        """
        pass

    def test_003_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4questions(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/questions
        EXPECTED: - Access to questions page after making predictions should be closed
        EXPECTED: - User should be redirected to End page.
        """
        pass

    def test_004_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4splashhttpsphoenix_invictuscoralcoukcorrect4afterlatest_quizhttpsphoenix_invictuscoralcoukcorrect4infoprizeshttpsphoenix_invictuscoralcoukcorrect4infofaqhttpsphoenix_invictuscoralcoukcorrect4infoterms(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/splash
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/after/latest-quiz
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/prizes
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/faq
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/terms
        EXPECTED: - Links should be successfully opened
        """
        pass

    def test_005_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4infosadfasfsafdhttpsphoenix_invictuscoralcoukcorrect4afdasdfasf(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/sadfasfsafd
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/afdasdfasf
        EXPECTED: - User should be redirected on the homepage or get an error message with back button
        """
        pass

    def test_006_logout(self):
        """
        DESCRIPTION: Logout.
        EXPECTED: The User is successfully logged out.
        """
        pass

    def test_007_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4splashhttpsphoenix_invictuscoralcoukcorrect4infoprizeshttpsphoenix_invictuscoralcoukcorrect4infofaqhttpsphoenix_invictuscoralcoukcorrect4infoterms(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/splash
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/prizes
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/faq
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/terms
        EXPECTED: Links are successfully opened.
        """
        pass

    def test_008_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4questionshttpsphoenix_invictuscoralcoukcorrect4afterlatest_quiz(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/questions
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/after/latest-quiz
        EXPECTED: The User is redirected to Splash page.
        EXPECTED: The Login pop-up is opened.
        """
        pass
