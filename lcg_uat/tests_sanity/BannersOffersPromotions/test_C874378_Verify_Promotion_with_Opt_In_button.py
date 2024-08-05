import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from faker import Faker


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # we can not create promotions on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.login
@pytest.mark.opt_in_promotion
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@pytest.mark.safari
@vtest
class Test_C874378_Verify_Promotion_with_Opt_In_button(BaseUserAccountTest):
    """
    TR_ID: C874378
    NAME: Verify Promotion with Opt In button
    DESCRIPTION: For configuration Opt In offers, please, use the following instruction:
    DESCRIPTION: https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Promotional+Opt+In+trigger
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_order=asc&group_id=739526
    PRECONDITIONS: Make sure Promotion with Opt In button is configured within CMS (Please see TC C29336 how to add Opt In to Promotion within CMS)
    """
    keep_browser_open = True
    fakename = Faker()
    button_name = 'Unique Opt In' + fakename.city()
    optin_offer_name = 'Automation OptIn offer'
    currency, amount = '£', '1.00'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Make sure Promotion with Opt In is configured in CMS
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

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_002_go_to_promotions_page_from_sports_ribbon(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page
        EXPECTED: 'Promotions' page with configured Promotion is opened
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        self.assertTrue(self.promotion_title in promotions.keys(),
                        msg=f'Test promotion: "{self.promotion_title}" was not found in "{promotions.keys()}"')

    def test_003_check_a_promotion_page(self):
        """
        DESCRIPTION: Check a Promotion page
        EXPECTED: 'Opt In' button is displayed on relevant Promotion page
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        self.__class__.opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertTrue(self.opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')
        self.assertEqual(self.opt_in_button.name, self.button_name,
                         msg=f'Actual button name: "{self.opt_in_button.name}"'
                             f'is not equal to expected: "{self.button_name}"')

    def test_004_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: - The text which is contained within Opt In button is changed
        EXPECTED: - Opt In button contains the message 'Thanks, you're already opted in'
        EXPECTED: - This message is configurable within CMS
        """
        self.opt_in_button.click()
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        result = wait_for_result(lambda: opt_in_button.name == self.successful_opt_in_text,
                                 name='Opt-in button text changed')
        self.assertTrue(result,
                        msg=f'Actual button text: "{opt_in_button.name}" is not equal to taken '
                            f'from CMS: "{self.successful_opt_in_text}"')

    def test_005_go_to_my_freebets_bonuses_page_and_check_whether_user_is__received_bonus(self):
        """
        DESCRIPTION: Go to My Freebets/Bonuses and check whether user is received bonus for the relevant promotion
        EXPECTED: User is received bonus for relevant promotion once promotion criteria is met
        """
        # Navigate to promotions for triggering optIn offer on right menu
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

        self.navigate_to_page(name='freebets')
        self.site.wait_content_state('Freebets')
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items, msg='No Free Bets found on page')
        if self.brand == 'ladbrokes':
            free_bet_value = f'{vec.bma.FREE_BET.upper()}: {self.currency}{self.amount}'
            auto_freebet = list(freebet_items.values())[-1]
            self.assertEqual(auto_freebet.name, free_bet_value,
                             msg=f'Freebet name "{auto_freebet.name}" is not the same as expected "{free_bet_value}"')

            self.assertEqual(auto_freebet.freebet_text, self.optin_offer_name,
                             msg=f'Freebet text "{auto_freebet.freebet_text}" '
                                 f'is not the same as expected "{self.optin_offer_name}"')
        else:
            free_bet_value = f'{self.currency}{self.amount} {vec.bma.FREE_BETS.upper()}'
            free_bet = self.site.freebets.freebets_content.section_header
            auto_freebet = f'{free_bet.total_balance_with_currency} {free_bet.header_title}'
            self.assertEqual(auto_freebet, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')

    def test_006_revisit_the_same_configured_promotion_and_check_the_opt_in_button(self):
        """
        DESCRIPTION: Revisit the same configured Promotion and check the 'Opt In' button
        EXPECTED: - Opt In button contains the message 'You're already opted in'
        EXPECTED: - Opt In button is not clickable
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertEqual(opt_in_button.name, self.already_opt_in_text,
                         msg=f'Button name "{opt_in_button.name}" is not'
                             f'equal to expected "{self.already_opt_in_text}"')
        self.assertFalse(self.opt_in_button.is_enabled(expected_result=False), msg='Opt-in button is not disabled')

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        self.site.logout()

    def test_008_go_to_promotions_page_and_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Go to 'Promotions' page and find a configured Promotion with Opt In
        EXPECTED: - Promotion page is opened
        EXPECTED: - Opt In button is displayed as per CMS configuration
        """
        self.navigate_to_promotion(promo_key=self.promo_key)
        self.__class__.opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertTrue(self.opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')

    def test_009_tap_on_opt_in_button_and_log_in(self):
        """
        DESCRIPTION: Tap on 'Opt In' button and log in
        EXPECTED: User is logged in on relevant Promotion page
        """
        self.opt_in_button.click()
        self.site.login(username=self.username, timeout_wait_for_dialog=2)
        self.site.wait_content_state(state_name='PromotionDetails')

    def test_010_check_opt_in_button_once_after_logging_in(self):
        """
        DESCRIPTION: Check Opt In button once after logging in
        EXPECTED: - Opt In button contains the message 'You're already opted in'
        EXPECTED: - Opt In button is disabled
        """
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertEqual(opt_in_button.name, self.already_opt_in_text,
                         msg=f'Button name "{opt_in_button.name}" is not'
                             f'equal to expected "{self.already_opt_in_text}"')
        self.assertFalse(opt_in_button.is_enabled(expected_result=False), msg='Opt-in button is not disabled')
