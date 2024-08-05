import pytest
from faker import Faker

from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.opt_in_promotion
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.login
@pytest.mark.issue('(https://jira.egalacoral.com/browse/BMA-56146')
@vtest
class Test_C29332_Verify_Opt_In_button_if_Opt_In_option_was_SUCCESSFUL(BaseUserAccountTest):
    """
    TR_ID: C29332
    NAME: Verify Opt In button if Opt In option was SUCCESSFUL
    DESCRIPTION: This test case verifies Opt In button if Opt In option was successful
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True
    fakename = Faker()
    button_name = 'Unique Opt In' + fakename.city()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Storing opt-in success message from CMS into variable
        DESCRIPTION: Creating new user
        DESCRIPTION: Make sure Promotion with Opt In is configured in CMS
        DESCRIPTION: User is logged in
        DESCRIPTION: Navigate to Promotions page
        """
        opt_in_messagging_conf = self.get_initial_data_system_configuration().get('OptInMessagging', {})
        if not opt_in_messagging_conf:
            opt_in_messagging_conf = self.cms_config.get_system_configuration_item('OptInMessagging')
        self.__class__.successful_opt_in_text = opt_in_messagging_conf.get('successMessage')
        if not self.successful_opt_in_text:
            raise CmsClientException('Opt-in success message not configured in CMS')

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        opt_in_promo_request_id = self.ob_config.backend.ob.opt_in_offer.default_offer.id
        promotion = self.cms_config.add_promotion(requestId=opt_in_promo_request_id,
                                                  promo_description=[{'button_name': f'{self.button_name}',
                                                                      'button_link': '',
                                                                      'is_it_opt_in_button': True}])

        self.__class__.promotion_title, self.__class__.promo_id, self.__class__.promo_key = \
            promotion.title.upper(), promotion.id, promotion.key

        self.site.login(username=self.username, async_close_dialogs=False)

        # Verify current number of freebets
        self.navigate_to_page(name='freebets')
        self.site.wait_content_state(state_name='Freebets')
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertNotIn('Auto', str(freebet_items.keys()), msg=f'Fount Auto in "{freebet_items}"')
        self.__class__.num_of_freebets = len(freebet_items)

        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_001_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Opt In button is displayed on relevant Promotion page
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        self.__class__.opt_in_button = \
            self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertTrue(self.opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')
        self.assertEqual(self.opt_in_button.name, self.button_name,
                         msg=f'Actual button name: "{self.opt_in_button.name}" '
                             f'is not equal to expected: "{self.button_name}"')

    def test_002_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Opt In option was successful
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        self.__class__.opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.opt_in_button.click()

    def test_003_check_opt_in_button_after_successful_opt_in_option(self):
        """
        DESCRIPTION: Check 'Opt In' button after successful Opt In option
        EXPECTED: The text which is contained within Opt In button is changed
        EXPECTED: This message is configurable within CMS.
        EXPECTED: For e.g.: 'Thanks, you are now opted in'
        """
        result = wait_for_result(lambda: self.opt_in_button.name == self.successful_opt_in_text,
                                 name='Opt-in button text changed ',
                                 timeout=5)

        self.assertTrue(result, msg=f'Actual button text: "{self.opt_in_button.name}" '
                                    f'is not equal to taken from CMS: "{self.successful_opt_in_text}"')

    def test_004_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: - Opt In button is not clickable.
        EXPECTED: - Actions are not triggered.
        """
        self.assertFalse(self.opt_in_button.is_enabled(expected_result=False), msg='Opt-in button is not disabled')

    def test_005_check_whether_user_is_eligible_to_receive_bonus_for_the_relevant_promotion(self):
        """
        DESCRIPTION: Check whether User is eligible to receive bonus for the relevant promotion
        EXPECTED: User is eligible to receive bonus for relevant promotion once promotion criteria is met
        """
        self.navigate_to_page(name='freebets')
        self.site.wait_content_state(state_name='Freebets')
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        # We can not create offer by autotest so name of offer can changed
        self.assertIn('Auto', str(freebet_items.keys()), msg=f'Can not find configured "Auto" '
                                                             f'offer in "{freebet_items}"')
        self.assertEqual(len(freebet_items), self.num_of_freebets + 1,
                         msg=f'Current number of freebets "{len(freebet_items)}" '
                             f'is not increased got "{self.num_of_freebets + 1}"')
