import pytest
from faker import Faker
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.opt_in_promotion
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@pytest.mark.login
@vtest
class Test_C50047_Verify_display_Opt_In_button_on_relevant_Promotions_page(Common):
    """
    TR_ID: C50047
    NAME: Verify display Opt In button on relevant Promotions page
    DESCRIPTION: This test case verifies display Opt In button on relevant Promotion's page for logged out User
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+setup+and+use+Promotional+Opt+In+trigger
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True
    fake = Faker()
    button_name = 'Unique Opt In ' + fake.city()

    def test_001_make_sure_promotion_with_opt_in_is_configured_in_cms(self):
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

    def test_002_open_promotions_page(self):
        """
        DESCRIPTION: Open 'Promotions' page
        EXPECTED: 'Promotions' landing page is opened
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_003_check_promotions_landing_page(self):
        """
        DESCRIPTION: Check 'Promotions' landing page
        EXPECTED: Opt In button is NOT displayed on 'Promotions' landing page
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotion_title in promotions.keys(),
                        msg=f'Test promotion: "{self.promotion_title}" was not found in "{promotions.keys()}"')

        promotion = promotions[self.promotion_title]
        promotion.scroll_to()
        self.assertFalse(promotion.short_description.has_button(expected_result=False),
                         msg='There is button present in short description of opt-in promo, it should not')

    def test_004_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: Promotion page is opened
        """
        self.navigate_to_promotion(promo_key=self.promo_key)

    def test_005_check_a_promotion_page(self):
        """
        DESCRIPTION: Check a Promotion page
        EXPECTED: Opt In button is displayed on relevant Promotion page
        """
        details_section = self.site.promotion_details.tab_content.promotion.detail_description
        actual_button_name = details_section.button.name
        self.assertEqual(actual_button_name, self.button_name,
                         msg=f'Actual button name: "{actual_button_name}" '
                             f'is not equal to expected: "{self.button_name}"')

    def test_006_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        self.site.login(async_close_dialogs=False)

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        """
        self.test_002_open_promotions_page()
        self.test_003_check_promotions_landing_page()
        self.test_004_find_a_configured_promotion_with_opt_in()
        self.test_005_check_a_promotion_page()
