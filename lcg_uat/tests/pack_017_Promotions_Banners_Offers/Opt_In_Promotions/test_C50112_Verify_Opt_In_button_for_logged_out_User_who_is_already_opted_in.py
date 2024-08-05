import pytest
from faker import Faker

from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.opt_in_promotion
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C50112_Verify_Opt_In_button_for_logged_out_User_who_is_already_opted_in(BaseUserAccountTest):
    """
    TR_ID: C50112
    NAME: Verify Opt In button for logged out User who is already opted in
    DESCRIPTION: This test case verifies Opt In button for logged out User who is already opted in
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+setup+and+use+Promotional+Opt+In+trigger
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True
    fake = Faker()
    button_name = 'Auto Opt In ' + fake.city()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Make sure Promotion with Opt In is configured in CMS
        """
        opt_in_promo_request_id = self.ob_config.backend.ob.opt_in_offer.default_offer.id
        promotion = self.cms_config.add_promotion(requestId=opt_in_promo_request_id,
                                                  promo_description=[{'button_name': f'{self.button_name}',
                                                                      'button_link': '',
                                                                      'is_it_opt_in_button': True}])
        self.__class__.promotion_title, self.__class__.promo_id, self.__class__.promo_key = \
            promotion.title.upper(), promotion.id, promotion.key
        opt_in_messagging = self.get_initial_data_system_configuration().get('OptInMessagging', {})
        if not opt_in_messagging:
            opt_in_messagging = self.cms_config.get_system_configuration_item('OptInMessagging')
        self.__class__.successful_opt_in_text = opt_in_messagging.get('successMessage')
        if not self.successful_opt_in_text:
            raise CmsClientException('Successful Opt-in messages not configured in CMS')

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username

    def test_001_go_to_promotions_from_sports_ribbon(self):
        """
        DESCRIPTION: Go to 'Promotions' from sports ribbon
        EXPECTED: 'Promotions' landing page is opened
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_002_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Promotion page is opened
        EXPECTED: - Opt In button is displayed as per CMS configuration
        EXPECTED: - Relevant request Opt In ID is NOT sent
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotion_title in promotions.keys(),
                        msg=f'Test promotion: "{self.promotion_title}" was not found in "{promotions.keys()}"')

    def test_003_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Log in pop-up appears
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        self.__class__.opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertTrue(self.opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')
        self.assertEqual(self.opt_in_button.name, self.button_name,
                         msg=f'Actual button name: "{self.opt_in_button.name}"'
                             f'is not equal to expected: "{self.button_name}"')
        self.opt_in_button.click()

    def test_004_enter_valid_name_and_password(self):
        """
        DESCRIPTION: Enter valid name and password
        EXPECTED: User is logged in on relevant Promotion page
        """
        self.site.login(username=self.username, timeout_wait_for_dialog=2)

    def test_005_check_opt_in_button_on_relevant_promotion_page_once_after_logging_in(self):
        """
        DESCRIPTION: Check 'Opt In' button on relevant Promotion page once after logging in
        EXPECTED: - Opt In button appears
        EXPECTED: - Opt In button contains already opted in message
        EXPECTED: - 'fired': 'true' is sent in the Request ID response
        """
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        result = wait_for_result(lambda: opt_in_button.name == self.successful_opt_in_text,
                                 name='Opt-in button text changed')
        # TODO bug https://jira.egalacoral.com/browse/BMA-49437
        self.assertTrue(result,
                        msg=f'Actual button text: "{opt_in_button.name}" is not equal to taken '
                            f'from CMS: "{self.successful_opt_in_text}"')
