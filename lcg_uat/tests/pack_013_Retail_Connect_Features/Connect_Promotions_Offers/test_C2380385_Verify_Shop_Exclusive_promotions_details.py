import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


#@pytest.mark.crl_tst2  # Coral only
#@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.desktop
@pytest.mark.promotions
@pytest.mark.connect
@pytest.mark.retail
@pytest.mark.medium
@vtest
@pytest.mark.connect_descoped
class Test_C2380385_Verify_Shop_Exclusive_promotions_details(Common):
    """
    TR_ID: C2380385
    NAME: Verify 'Shop Exclusive' promotions details
    DESCRIPTION: This test case verifies 'Connect Exclusive' tab details
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: CMS:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ -> Pick 'sportsbook' brand from the drop-down -> 'Promotions'  :
    PRECONDITIONS: Active promotions are created with current validity period and Category equal 'Connect promotions'
    PRECONDITIONS: 'Shop Exclusive' tab should be opened (Header ribbon menu -> Promotions -> 'Shop Exclusive' tab)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test promotion in CMS
        EXPECTED: Test promotion created
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('promotions'):
            raise CmsClientException('"Connect Promotions" is disabled')
        category_ids = self.cms_config.get_sport_categories()
        connect_promotions = list(filter(lambda param: param['imageTitle'] == 'Connect Promotions', category_ids))
        if not connect_promotions:
            raise CmsClientException('No "Connect Promotions" exist')
        category_id = connect_promotions[0].get('id')
        promotion = self.cms_config.add_promotion(category_id=[category_id])
        self.__class__.promotion_title, self.__class__.promo_id = \
            promotion.title.upper(), promotion.id
        self.__class__.promotion_cms = self.cms_config.get_promotion(promotion_id=self.promo_id)
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_RETAIL)
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions, vec.promotions.TABS_RETAIL,
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL}"')

    def test_001_verify_promotion_view(self):
        """
        DESCRIPTION: Verify promotion view
        EXPECTED: List of CMS configurable promotion content:
        EXPECTED: * Banner
        EXPECTED: * Promotion title (White text on a blue area)
        EXPECTED: * Short Description (Grey text on a grey area)
        EXPECTED: * green 'More info' button on a grey area
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='Can not find any promotions on page')
        self.assertIn(self.promotion_title, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title}" not found in promotions list: '
                          f'{list(promotions.keys())}')
        self.__class__.promotion = promotions.get(self.promotion_title.upper())
        self.promotion.scroll_to()
        self.assertTrue(self.promotion.has_image(), msg='Image for promotion is not displayed')
        self.assertTrue(self.promotion.name, msg='Promo name is empty')
        self.assertTrue(self.promotion.short_description.text, msg='Short description is not found')
        self.assertTrue(self.promotion.more_info_button.is_displayed(),
                        msg=f'"More Info" button for Promotion {self.promotion_title} is not shown')

    def test_002_tap_click_more_info_button_on_any_promotion(self):
        """
        DESCRIPTION: Tap/Click 'More info' button on any promotion
        EXPECTED: Promotion page is opened
        """
        self.promotion.more_info_button.click()
        self.site.wait_content_state('PromotionDetails')
        self.__class__.promotion_details = self.site.promotion_details.tab_content.promotion
        self.assertTrue(self.promotion_details, msg=f'Promotion: "{self.promotion_title}" details page was not found')

    def test_003_verify_the_promotion_details_page(self):
        """
        DESCRIPTION: Verify the promotion details page
        EXPECTED: * Promotion title
        EXPECTED: * Banner (according to CMS configuration)
        EXPECTED: * Description (according to CMS configuration)
        EXPECTED: * 'T&C's' section (according to CMS configuration)
        """
        sections = self.site.promotion_details.tab_content.promotion
        self.assertTrue(sections, msg='Can not find any section on Promotion details page')
        self.assertEqual(sections.name, self.promotion_title,
                         msg=f'Promotion title "{sections.name}" is not equal to expected "{self.promotion_title}"')
        image_url_cms = self.promotion_cms.get('directFileUrl')
        self.assertIn(image_url_cms, self.promotion_details.image, msg=f'Promotion image in CMS: "{image_url_cms}"'
                                                                       f'is not equal to UI: "{self.promotion_details.image}"')

        description = self.promotion_cms.get('description')
        promotion_description_cms = description.replace('\n', ' ').replace('\\n', ' ')
        self.assertEqual(self.promotion_details.detail_description.text, promotion_description_cms,
                         msg=f'Promotion text in UI: "{self.promotion_details.detail_description.text}"'
                             f'is not equal to expected CMS: "{promotion_description_cms}"')

        terms_and_conditions_cms = self.promotion_cms.get('htmlMarkup')
        terms_and_conditions_ui = self.site.promotion_details.tab_content.terms_and_conditions.details
        self.assertEqual(terms_and_conditions_ui.replace('amp;', ''), terms_and_conditions_cms,
                         msg=f'Terms and conditions text in UI: "{terms_and_conditions_ui}" '
                             f'is not equal to "{terms_and_conditions_cms}"')
