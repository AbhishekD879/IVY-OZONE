import pytest
from faker import Faker

import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.promotions
@pytest.mark.opt_in_promotion
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C50111_Verify_Opt_In_button_for_logged_out_User_who_is_NOT_opted_in(Common):
    """
    TR_ID: C50111
    NAME: Verify Opt In button for logged out User who is NOT opted in
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+setup+and+use+Promotional+Opt+In+trigger
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True
    fake = Faker()
    button_name = 'New Opt In' + fake.city()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Promotion with Opt In button
        """
        opt_in_promo_request_id = self.ob_config.backend.ob.opt_in_offer.default_offer.id
        promotion = self.cms_config.add_promotion(requestId=opt_in_promo_request_id,
                                                  promo_description=[
                                                      {'button_name': f'{self.button_name}',
                                                       'button_link': '',
                                                       'is_it_opt_in_button': True}])

        self.__class__.promotion_title, self.__class__.promo_id, self.__class__.promo_key = \
            promotion.title.upper(), promotion.id, promotion.key

    def test_001_make_sure_promotion_with_opt_in_is_configured_in_cms(self):
        """
        DESCRIPTION: Make sure Promotion with Opt In is configured in CMS
        """
        if self.cms_config.get_promotion(self.promo_id):
            self._logger.debug('*** Promotion with Opt In is configured in CMS successfully')
        else:
            raise CmsClientException('Promotion with Opt In is not configured in CMS')

    def test_002_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: User is not logged in
        """
        self.site.wait_content_state('HomePage')

    def test_003_go_to_promotions_from_sports_ribbon(self):
        """
        DESCRIPTION: Go to 'Promotions' from sports ribbon
        EXPECTED: 'Promotions' landing page is opened
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_004_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Promotion page is opened
        EXPECTED: - Opt In button is displayed as per CMS configuration
        EXPECTED: - Relevant request Opt In ID is NOT sent
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        details_section = self.site.promotion_details.tab_content.promotion.detail_description
        actual_button_name = details_section.button.name
        self.assertEqual(actual_button_name, self.button_name,
                         msg=f'Actual button name: "{actual_button_name}" '
                         f'is not equal to expected: "{self.button_name}"')

    def test_005_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Log in pop-up appears
        """
        self.site.promotion_details.tab_content.promotion.detail_description.button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=5)
        self.assertTrue(dialog, msg='"LOG IN" dialog is not present on page')

    def test_006_enter_valid_name_and_password(self):
        """
        DESCRIPTION: Enter valid name and password
        EXPECTED: User is logged in on relevant Promotion page
        """
        self.site.login(username=tests.settings.betplacement_user, timeout_wait_for_dialog=2)
        self.site.wait_content_state(state_name='PromotionDetails')

    def test_007_check_opt_in_button_on_relevant_promotion_page_once_after_logging_in(self):
        """
        DESCRIPTION: Check 'Opt In' button on relevant Promotion page once after logging in
        EXPECTED: - Opt In button appears
        EXPECTED: - Opt In button contains success message
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        promo_page = self.site.promotion_details.tab_content.promotion.detail_description
        self.assertTrue(promo_page.has_opt_in_button, msg='There is button present on relevant Promotion page')
