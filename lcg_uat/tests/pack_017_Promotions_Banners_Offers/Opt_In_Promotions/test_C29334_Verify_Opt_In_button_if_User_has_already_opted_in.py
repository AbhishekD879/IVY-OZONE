import pytest
from faker import Faker

from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.opt_in_promotion
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29334_Verify_Opt_In_button_if_User_has_already_opted_in(BaseUserAccountTest):
    """
    TR_ID: C29334
    NAME: Verify Opt In button if User has already opted in
    DESCRIPTION: This test case verifies Opt In button if User revisits a Promotion page and has already opted in
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14803: Opt In Promotion Functionality
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    PRECONDITIONS: * Make sure Promotion with Opt In is configured in CMS
    PRECONDITIONS: * User is logged in
    """
    keep_browser_open = True
    fake_name = Faker()
    button_name = 'Unique Opt In' + fake_name.city()
    username = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Storing opt-in success message from CMS into variable
        DESCRIPTION: Creating new user
        DESCRIPTION: Make sure Promotion with Opt In is configured in CMS
        DESCRIPTION: User is logged in
        """
        opt_in_messagging_config = self.get_initial_data_system_configuration().get('OptInMessagging', {})
        if not opt_in_messagging_config:
            opt_in_messagging_config = self.cms_config.get_system_configuration_item('OptInMessagging')
        self.__class__.successful_opt_in_text = opt_in_messagging_config.get('successMessage')
        self.__class__.already_opt_in_text = opt_in_messagging_config.get('alreadyOptedInMessage')
        if not self.successful_opt_in_text or not self.already_opt_in_text:
            raise CmsClientException('Opt-in messages not configured in CMS')

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        opt_in_promo_request_id = self.ob_config.backend.ob.opt_in_offer.default_offer.id
        promotion = self.cms_config.add_promotion(requestId=opt_in_promo_request_id,
                                                  promo_description=[{'button_name': f'{self.button_name}',
                                                                      'button_link': '',
                                                                      'is_it_opt_in_button': True}])

        self.__class__.promotion_title, self.__class__.promo_id, self.__class__.promo_key = \
            promotion.title.upper(), promotion.id, promotion.key

        self.site.login(username=self.username, async_close_dialogs=False)

    def test_001_go_to_promotions_page(self):
        """
        DESCRIPTION: Go to 'Promotions' page
        EXPECTED: 'Promotions' page with configured Promotion is opened
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_002_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Opt In button is displayed on relevent Promotion page
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotion_title in list(promotions.keys()),
                        msg=f'Test promotion: "{self.promotion_title}" was not found in "{list(promotions.keys())}"')

    def test_003_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Opt In option was successful
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertTrue(opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')
        self.assertEqual(opt_in_button.name, self.button_name,
                         msg=f'Actual button name: "{opt_in_button.name}"'
                             f'is not equal to expected: "{self.button_name}"')
        opt_in_button.click()
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        result = wait_for_result(lambda: opt_in_button.name == self.successful_opt_in_text,
                                 name='Opt-in button text changed')
        self.assertTrue(result, msg=f'Actual button text: "{opt_in_button.name}" '
                                    f'is not equal to taken from CMS: "{self.successful_opt_in_text}"')

    def test_004_navigate_from_promotion_page(self):
        """
        DESCRIPTION: Navigate from Promotion page
        """
        self.test_001_go_to_promotions_page()

    def test_005_revisit_the_same_configured_promotion(self):
        """
        DESCRIPTION: Revisit the same configured Promotion
        EXPECTED: Opt In button is dispalyed on relevant Promotion page
        EXPECTED: - 'fired': 'true' is sent in the Request ID response
        """
        self.test_002_find_a_configured_promotion_with_opt_in()

    def test_006_make_sure_there_is_no_buttons_blink_once_promotion_page_is_opened(self):
        """
        DESCRIPTION: Make sure there is no button's blink once Promotion page is opened
        EXPECTED: Opt In button can appears spinner of loading.
        EXPECTED: There is no blink of previous message once Promotion page is opened.
        """
        pass

    def test_007_check_the_opt_in_button(self):
        """
        DESCRIPTION: Check the Opt In button
        EXPECTED: - Opt In button contains the message 'You're already opted in'.
        EXPECTED: - This message is configurable within CMS.
        EXPECTED: - Opt In button contains the icon.
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        self.site.wait_content_state(state_name='PromotionDetails')
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertEqual(opt_in_button.name, self.already_opt_in_text,
                         msg=f'Button name "{opt_in_button.name}" is not'
                             f'equal to expected "{self.already_opt_in_text}"')

    def test_008_click_on_opt_in_button_again(self):
        """
        DESCRIPTION: Click on Opt In button again
        EXPECTED: - Opt In button is not clickable.
        EXPECTED: - Actions are not triggered.
        """
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertFalse(opt_in_button.is_enabled(expected_result=False), msg='Opt-in button is not disabled')
