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
class Test_C2351716_Coral_Only_Oxygen_Connect_Page(Common):
    """
    TR_ID: C2351716
    NAME: [Coral Only] Oxygen Connect Page
    DESCRIPTION: This test case verifies Connect Landing page in sportsbook app
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: To configure Connect Landing Page content use CMS:
    PRECONDITIONS: https://CMS_ENDPOINT -> Chose 'sportsbook' channel -> 'Menus' -> 'Connect Menus'
    PRECONDITIONS: Make sure AEM banners are enabled: System-configuration -> DYNAMICBANNERS -> enabled
    PRECONDITIONS: Contact GVC (Venugopal Rao Joshi / Abhinav Goel) and/or Souparna Datta + Oksana Tkach in order to generate In-Shop users
    """
    keep_browser_open = True

    def test_001_chose_connect_from_header_ribbon(self):
        """
        DESCRIPTION: Chose 'Connect' from header ribbon
        EXPECTED: Connect landing page is opened
        """
        pass

    def test_002_check_page_structure(self):
        """
        DESCRIPTION: Check page structure
        EXPECTED: * '< Connect' back button
        EXPECTED: * Banners carousel
        EXPECTED: * Features that were set up in CMS
        EXPECTED: * Link to each feature '>'
        EXPECTED: * Features have descriptions (subtitles) according to CMS:
        EXPECTED: * Use Connect Online (for the in-shop user only)
        EXPECTED: * Shop Exclusive Promos
        EXPECTED: * Shop Bet Tracker
        EXPECTED: * Football Bet Filter
        EXPECTED: * Shop Locator
        """
        pass

    def test_003_go_to_cms_and_change_title_subtitle_icon_for_any_connect_landing_page_item(self):
        """
        DESCRIPTION: Go to CMS and change Title/ Subtitle/ icon for any Connect landing page item
        EXPECTED: All changes are mirrored on interface respectively
        """
        pass

    def test_004_open_link__to_each_feature(self):
        """
        DESCRIPTION: Open link '>' to each feature
        EXPECTED: A user can access each feature and navigate back to Landing page using back button
        """
        pass

    def test_005_verify_that_aem_banners_are_displayed_correctly_for_the_logged_out_user(self):
        """
        DESCRIPTION: Verify that AEM banners are displayed correctly for the logged out user
        EXPECTED: * Banners images and sequence correspond to JSON received from the link **endpoint/bin/lc/coral/offers.json/locale/en-gb/channels/connect/pages/homepage/userType/anonymous/response.json**
        EXPECTED: * After tapping banner user is redirected to target Url (from JSON)
        """
        pass
