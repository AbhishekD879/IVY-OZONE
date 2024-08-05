import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C832537_Verify_parameter_deliveryPlatform(Common):
    """
    TR_ID: C832537
    NAME: Verify parameter deliveryPlatform
    DESCRIPTION: This test case verifies  display of delivery platform  when navigating from OXYGEN app to Casino Games Lobby:
    DESCRIPTION: When calling mcasino.coral.co.uk from the Oxygen HTML5 client then a deliveryPlatform parameter should be applied to link with the value of HTML5
    DESCRIPTION: Link in HTML5 app: http://mcasino.coral.co.uk/?ref=bma&deliveryPlatform=HTML5
    DESCRIPTION: When calling mcasino.coral.co.uk from the Oxygen Wrapped iOS or Android client then a deliveryPlatform parameter should be applied to link with the value of Wrapper
    DESCRIPTION: Link in Wrapper app: http://mcasino.coral.co.uk/?ref=bma&deliveryPlatform=Wrapper
    PRECONDITIONS: Note: should be checked for all items that navigate  users to Casino Games Lobby:
    PRECONDITIONS: - Sports Menu Logged In /Logged Out User;
    PRECONDITIONS: - All Sports (A-Z) page Logged In /Logged Out User;
    PRECONDITIONS: - Banners Logged In /Logged Out User;
    PRECONDITIONS: - Promotions: buttons, links Logged In /Logged Out User;
    PRECONDITIONS: - Footer Menu Logged In /Logged Out User;
    PRECONDITIONS: - Right side User Menu Logged In User;
    PRECONDITIONS: - Offers Logged In /Logged Out User  [Tablet/Desktop mode only];
    PRECONDITIONS: All navigation URI in CMS are configured as following: http://mcasino-<env>.coral.co.uk/?ref=bma
    PRECONDITIONS: **JIRA ticket **:
    PRECONDITIONS: BMA-17210
    PRECONDITIONS: As a WPL3 PO I want to append the Delivery Platform in the HTTP Header in order to distinguish between a HTML client and Wrapped client so that the correct games lobby can be served to the user.
    """
    keep_browser_open = True

    def test_001_open_oxygen_app_in_html5_or_wrapper(self):
        """
        DESCRIPTION: Open Oxygen App in HTML5 or Wrapper
        EXPECTED: 
        """
        pass

    def test_002_tap_on_gaming_icon_in_sports_menu__in_html5__in_wrapper(self):
        """
        DESCRIPTION: Tap on Gaming icon in Sports Menu
        DESCRIPTION: - in HTML5
        DESCRIPTION: - in Wrapper
        EXPECTED: User is Navigated to Casino Games Lobby by URL:
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=HTML5
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=Wrapper
        """
        pass

    def test_003_go_back_to_oxygen_app(self):
        """
        DESCRIPTION: Go Back to Oxygen app
        EXPECTED: User is navigated back to Oxygen app without parameter deliveryPlatform in URL
        """
        pass

    def test_004_in_cms_change_uri_to_following_and_repeat_steps_2_3__httpmcasino_envcoralcoukrefbmatest__httpmcasino_envcoralcoukrefbma__httpmcasino_envcoralcoukrefbmaspaces(self):
        """
        DESCRIPTION: In CMS Change URI to following and Repeat Steps #2-#3:
        DESCRIPTION: - http://mcasino-<env>.coral.co.uk/?ref=bma&test
        DESCRIPTION: - http://mcasino-<env>.coral.co.uk/?ref=bma&&
        DESCRIPTION: - http://mcasino-<env>.coral.co.uk/?ref=bma<spaces>
        EXPECTED: User is Navigated to Casino Games Lobby by URL:
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&test&deliveryPlatform=<HTML5 or Wrapper>
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&&&deliveryPlatform=<HTML5 or Wrapper>
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=<HTML5 or Wrapper>
        """
        pass

    def test_005_in_cms_change_uri_to_following_and_repeat_steps_2_3__httpmcasino_envcoralcoukrefbmadeliveryplatformhtml5___httpmcasino_envcoralcoukrefbmadeliveryplatformwrapper__httpmcasino_envcoralcoukrefbmadeliveryplatform__httpmcasino_envcoralcoukrefbmadeliveryplatformsometext(self):
        """
        DESCRIPTION: In CMS Change URI to following and Repeat Steps #2-#3:
        DESCRIPTION: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=HTML5
        DESCRIPTION: -  http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=Wrapper
        DESCRIPTION: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=
        DESCRIPTION: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=sometext
        EXPECTED: User is Navigated to Casino Games Lobby by URL(parameter deliveryPlatform is NOT doubled but will remain same as specified in CMS):
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=HTML5
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=Wrapper
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=
        EXPECTED: - http://mcasino-<env>.coral.co.uk/?ref=bma&deliveryPlatform=sometext
        """
        pass

    def test_006_repeat_steps_2_5_for_places_mentioned_in_preconditions_for_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps #2-#5 for places mentioned in preconditions for Logged Out User
        EXPECTED: 
        """
        pass

    def test_007_login_to_oxygen_app(self):
        """
        DESCRIPTION: Login to Oxygen app
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_5_for_places_mentioned_in_preconditions_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-#5 for places mentioned in preconditions for Logged In User
        EXPECTED: 
        """
        pass
