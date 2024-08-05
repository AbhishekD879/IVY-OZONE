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
class Test_C10397574_Verify_a_proper_URL_is_opened_when_follow_the_See_more_link(Common):
    """
    TR_ID: C10397574
    NAME: Verify a proper URL is opened when follow the "See more" link
    DESCRIPTION: Test case verifies the functionality of See more link
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user with some playing history
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_in_the_cms_set_a_see_more_link_to_the_appropriate_gaming_link_e_g_httpsgamingcoralcouk_and_save(self):
        """
        DESCRIPTION: In the CMS set a "See more link" to the appropriate gaming link (e. g. https://gaming.coral.co.uk) and save.
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_follow_the_see_more_link(self):
        """
        DESCRIPTION: In the application follow the "See more" link
        EXPECTED: User is redirected to the Gaming section
        EXPECTED: User is logged in
        """
        pass

    def test_003_in_the_cms_set_a_see_more_link_to_the_any_location_e_g_httpswwwgooglecom(self):
        """
        DESCRIPTION: In the CMS set a "See more link" to the any location (e. g. https://www.google.com)
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_follow_the_see_more_link(self):
        """
        DESCRIPTION: In the application follow the "See more" link
        EXPECTED: User is redirected to the defined URL
        """
        pass
