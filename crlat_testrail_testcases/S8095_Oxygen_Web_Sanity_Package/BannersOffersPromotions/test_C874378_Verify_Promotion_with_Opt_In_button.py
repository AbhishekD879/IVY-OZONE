import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C874378_Verify_Promotion_with_Opt_In_button(Common):
    """
    TR_ID: C874378
    NAME: Verify Promotion with Opt In button
    DESCRIPTION: For configuration Opt In offers, please, use the following instruction:
    DESCRIPTION: https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Promotional+Opt+In+trigger
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_order=asc&group_id=739526
    DESCRIPTION: AUTOTEST [C49803162]
    PRECONDITIONS: Make sure Promotion with Opt In button is configured within CMS and contains following settings:
    PRECONDITIONS: 1) OPTIN button contains following source code:
    PRECONDITIONS: <p class="MsoNoSpacing"><strong><a class="btn full-width btn-style2 handle-opt-in hidden" target=""><span class="btn-label">#####</span></a></strong></p>  , where ##### is the 'Text to display' set during the creation of a button.
    PRECONDITIONS: ![](index.php?/attachments/get/107907219)
    PRECONDITIONS: 1.1) No need to use 'Insert Link' option for the created button.
    PRECONDITIONS: 2) 'Opt In Request ID'![](index.php?/attachments/get/107907202) value should be valid and taken from real(active/up-to-date) OpenBet offer with 'Trigger ID'![](index.php?/attachments/get/107907209) (without ',')
    PRECONDITIONS: **Messages which are shown within the OPT-IN button after the click, are configured in System Configuration -> Structure -> 'OptInMessagging' section.**
    PRECONDITIONS: ![](index.php?/attachments/get/107907233)
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_promotions_page(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page
        EXPECTED: 'Promotions' page with configured Promotion is opened
        """
        pass

    def test_003_check_a_promotion_page(self):
        """
        DESCRIPTION: Check a Promotion page
        EXPECTED: 'Opt In' button is displayed on relevant Promotion page
        """
        pass

    def test_004_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: - The text which is contained within Opt In button is changed
        EXPECTED: - Opt In button contains the message 'Thanks, you're already opted in'
        EXPECTED: - This message is configurable within CMS
        """
        pass

    def test_005_go_to_my_freebetsbonuses_page_and_check_whether_user_is__received_bonus_for_the_relevant_promotion(self):
        """
        DESCRIPTION: Go to My Freebets/Bonuses page and check whether user is  received bonus for the relevant promotion
        EXPECTED: User is received bonus for relevant promotion once promotion criteria is met
        """
        pass

    def test_006_revisit_the_same_configured_promotion_and_check_the_opt_in_button(self):
        """
        DESCRIPTION: Revisit the same configured Promotion and check the 'Opt In' button
        EXPECTED: - Opt In button contains the message 'You're already opted in'
        EXPECTED: - Opt In button is not clickable
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_008_go_to_promotions_page_and_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Go to 'Promotions' page and find a configured Promotion with Opt In
        EXPECTED: - Promotion page is opened
        EXPECTED: - Opt In button is displayed as per CMS configuration
        """
        pass

    def test_009_tap_on_opt_in_button_and_log_in(self):
        """
        DESCRIPTION: Tap on 'Opt In' button and log in
        EXPECTED: User is logged in on relevant Promotion page
        """
        pass

    def test_010_check_opt_in_button_once_after_logging_in(self):
        """
        DESCRIPTION: Check Opt In button once after logging in
        EXPECTED: - Opt In button contains the message 'You're already opted in'
        EXPECTED: - Opt In button is disabled
        """
        pass
