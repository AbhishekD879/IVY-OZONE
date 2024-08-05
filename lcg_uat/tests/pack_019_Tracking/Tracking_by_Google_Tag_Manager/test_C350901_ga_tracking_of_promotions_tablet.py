import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.tablet
@pytest.mark.google_analytics
@pytest.mark.promotions
@pytest.mark.cms
@pytest.mark.tablet_only
@pytest.mark.other
@pytest.mark.low
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C350901_GA_Tracking_Of_Promotion_Tablet_Mode(BaseDataLayerTest):
    """
    TR_ID: C350901
    VOL_ID: C30929734
    NAME: Verify tracking on 'Promotion' page tablet mode
    PRECONDITIONS: For this test was created specific promotion
    'Autotest GA - Tracking on Promotions page' with configured image, buttons and links,
    this promotion should be active and not expired
    """
    keep_browser_open = True
    device_name = tests.tablet_default
    expected_static_parameters = {
        'event': 'trackEvent',
        'eventCategory': 'promotions'
    }

    promotion_name = promo_key = promo_id = promotion = None
    link = 'lotto'.format(host=tests.HOSTNAME)
    link_name = 'autotest_link'
    link_configs = {'link': link,
                    'link_name': link_name}
    blue_button_name = 'In-Play'
    blue_button_link = 'in-play'.format(host=tests.HOSTNAME)
    blue_button_configs = {'button_name': blue_button_name,
                           'button_link': blue_button_link,
                           'button_width': 'half',
                           'button_color': 'blue'}
    green_button_name = 'Home'
    green_button_link = 'home'
    green_button_configs = {'button_name': green_button_name,
                            'button_link': green_button_link,
                            'button_width': 'half',
                            'button_color': 'green'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test promotion in CMS
        EXPECTED: Test promotion created
        """
        if self.brand == 'ladbrokes':
            self.__class__.vip_level_users = {
                tests.settings.bronze_user_vip_level_11: ['10'],
                tests.settings.silver_user_vip_level_12: ['60', '64'],
                tests.settings.gold_user_vip_level_13: ['62', '76'],
                tests.settings.platinum_user_vip_level_14: ['77', '79', '81']
            }
        else:
            self.__class__.vip_level_users = {
                tests.settings.bronze_user_vip_level_11: ['11'],
                tests.settings.silver_user_vip_level_12: ['12'],
                tests.settings.gold_user_vip_level_13: ['13'],
                tests.settings.platinum_user_vip_level_14: ['14']
            }
        promotion = self.cms_config.add_promotion(promo_description=[self.link_configs,
                                                                     self.blue_button_configs,
                                                                     self.green_button_configs])
        self.__class__.promotion_name, self.__class__.promo_key, self.__class__.promo_id =\
            promotion.title, promotion.key, promotion.id

    def test_001_navigate_to_promotions_page(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page
        EXPECTED: 'Promotions' page is opened
        """
        self.navigate_to_page('promotions')
        sleep(1)

    def test_002_click_on_banner_image(self):
        """
        DESCRIPTION: Click banner image on page for tested promotion
        EXPECTED: There is no GA tracking object for not clickable banner within 'Promotions' page
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotion_name.upper() in promotions.keys(),
                        msg=f'Test promotion: "{self.promotion_name.upper()}" was not found in {promotions.keys()}')
        self.__class__.promotion = promotions[self.promotion_name.upper()]
        self.promotion.scroll_to()
        self.assertTrue(self.promotion.has_image(), msg='Image for promotion is not displayed')
        sleep(1)
        self.promotion.image.click()
        try:
            self.get_data_layer_specific_object(object_key='eventCategory', object_value='promotions')
        except Exception as err:
            self.assertTrue('Required object with key: "eventCategory" value "promotions" was not found'
                            in str(err),
                            msg='GA tracking object was found for not clickable banner within "Promotions" page')

    def test_003_click_more_information_button(self, vip_level=''):
        """
        DESCRIPTION: Select any promotion (for this case created
        DESCRIPTION: "Autotest GA - Tracking on Promotions page" promotion) and click 'More information' button
        EXPECTED: Page for selected promotion is opened
        """
        self.promotion.more_info_button.click()
        static_parameters = self.get_data_layer_specific_object(object_key='eventCategory', object_value='promotions')
        self.__class__.expected_static_parameters['vipLevel'] = vip_level
        self.__class__.expected_static_parameters['eventAction'] = 'cta click'
        self.__class__.expected_static_parameters['eventLabel'] = self.promotion_name
        self.__class__.promo_action = 'More Info' if self.brand != 'ladbrokes' else 'See more'
        self.__class__.expected_static_parameters['promoAction'] = self.promo_action
        self.compare_json_response(static_parameters, self.expected_static_parameters)

    def test_004_click_on_in_play_promotion_button(self, vip_level=''):
        """
        DESCRIPTION: Click In-Play button on page for selected promotion
        EXPECTED: Verify dataLayer response match with required
        """
        details_section = self.site.promotion_details.tab_content.promotion.detail_description
        self.assertTrue(details_section, msg='Promotion: "%s" details section was not found'
                                             % self.promotion_name)
        # need to use sleep 0.5 second before each click because of
        # implementation of this functionality with explicit wait 300 milliseconds
        sleep(0.5)
        details_section.in_play_button.click()
        self.site.wait_content_state('InPlay')
        self.__class__.expected_static_parameters['vipLevel'] = vip_level
        self.__class__.expected_static_parameters['eventAction'] = 'link click'
        self.__class__.expected_static_parameters['promoAction'] = 'In-Play'
        static_parameters = self.get_data_layer_specific_object(object_key='eventCategory', object_value='promotions')
        self.compare_json_response(static_parameters, self.expected_static_parameters)
        self.navigate_to_promotion(promo_key=self.promo_key)

    def test_005_click_on_home_promotion_button(self, vip_level=''):
        """
        DESCRIPTION: Click Home button on page for selected promotion
        EXPECTED: Verify dataLayer response match with required
        """
        details_section = self.site.promotion_details.tab_content.promotion.detail_description
        self.assertTrue(details_section, msg=f'Promotion: "{self.promotion_name.upper()}" details section was not found')
        # need to use sleep 0.5 second before each click because of
        # implementation of this functionality with explicit wait 300 milliseconds
        sleep(0.5)
        details_section.home_button.click()
        self.site.wait_content_state('HomePage')
        self.__class__.expected_static_parameters['vipLevel'] = vip_level
        self.__class__.expected_static_parameters['promoAction'] = 'Home'
        static_parameters = self.get_data_layer_specific_object(object_key='eventCategory', object_value='promotions')
        self.compare_json_response(static_parameters, self.expected_static_parameters)
        self.navigate_to_promotion(promo_key=self.promo_key)

    def test_006_click_on_promotion_link(self, vip_level=''):
        """
        DESCRIPTION: Click link on page for selected promotion
        EXPECTED: Verify dataLayer response match with required
        """
        details_section = self.site.promotion_details.tab_content.promotion.detail_description
        self.assertTrue(details_section, msg=f'Promotion: "{self.promotion_name.upper()}" details section was not found')
        self.__class__.expected_static_parameters['promoAction'] = details_section.link_url

        # need to use sleep 0.5 second before each click because of
        # implementation of this functionality with explicit wait 300 milliseconds
        sleep(0.5)
        details_section.link.click()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Lotto')
        self.__class__.expected_static_parameters['vipLevel'] = vip_level
        self.__class__.expected_static_parameters['promoAction'] = "lotto"
        static_parameters = self.get_data_layer_specific_object(object_key='eventCategory', object_value='promotions')
        self.compare_json_response(static_parameters, self.expected_static_parameters)
        self.navigate_to_promotion(promo_key=self.promo_key)

    def test_007_click_on_promotion_for_different_users(self):
        """
        DESCRIPTION: Login as users with different vip level and repeat steps 1-6
        EXPECTED: Verify dataLayer response match with required
        """
        global vip_level
        self.site.back_button_click()
        for user, vip_level_range in self.vip_level_users.items():
            self.site.wait_content_state('HomePage')
            self.site.login(username=user)
            self.test_001_navigate_to_promotions_page()
            self.test_002_click_on_banner_image()
            self.promotion.more_info_button.click()
            static_parameters = self.get_data_layer_specific_object(object_key='eventCategory',
                                                                    object_value='promotions')
            actual_vip_level = static_parameters['vipLevel']
            self.assertIn(actual_vip_level, vip_level_range,
                          msg=f'Actual vip level "{actual_vip_level}" is not equal to any of expected vip levels "{vip_level_range}"')
            for vip_level in vip_level_range:
                if vip_level == actual_vip_level:
                    self.__class__.expected_static_parameters['vipLevel'] = vip_level
                    break
            self.__class__.expected_static_parameters['eventAction'] = 'cta click'
            self.__class__.expected_static_parameters['eventLabel'] = self.promotion_name
            self.__class__.promo_action = 'More Info' if self.brand != 'ladbrokes' else 'See more'
            self.__class__.expected_static_parameters['promoAction'] = self.promo_action
            self.compare_json_response(static_parameters, self.expected_static_parameters)
            self.test_004_click_on_in_play_promotion_button(vip_level=vip_level)
            self.test_005_click_on_home_promotion_button(vip_level=vip_level)
            self.test_006_click_on_promotion_link(vip_level=vip_level)
            self.site.logout()
