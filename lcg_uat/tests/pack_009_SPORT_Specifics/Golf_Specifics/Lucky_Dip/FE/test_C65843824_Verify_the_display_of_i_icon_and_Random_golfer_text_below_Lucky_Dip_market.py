import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from lxml.html import fromstring


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C65843824_Verify_the_display_of_i_icon_and_Random_golfer_text_below_Lucky_Dip_market(BaseGolfTest):
    """
    TR_ID: C65843824
    NAME: Verify the display of 'i' icon  and Random golfer text below Lucky Dip market
    DESCRIPTION: This testcase verifies the display of 'i' icon and Random golfer text below Lucky Dip Market.
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']
        self.__class__.market_description = self.get_lucky_dip_market_description_by_event(event=event).get(
            'market_description')
        cms_luckydip_configuaion = self.cms_config.get_lucky_dip_configuration()
        luckydip_fields_config = cms_luckydip_configuaion.get('luckyDipFieldsConfig')
        self.__class__.expected_market_title = luckydip_fields_config['title'] if luckydip_fields_config['title'] == ""\
            else fromstring(luckydip_fields_config['title']).text_content().strip('\n').strip()
        self.__class__.expected_market_desc = luckydip_fields_config['desc'] if luckydip_fields_config['desc'] == "" \
            else fromstring(luckydip_fields_config['desc']).text_content().strip('\n').strip()

    def test_001_log_in_to_ladbrokes_application_and_navigate_to_golf_event_to_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Log in to Ladbrokes application and Navigate to Golf event to which Lucky Dip Market is configured
        EXPECTED: User is Navigated to Golf EDP with Lucky Dip Market. Odds are displayed beside the Market
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_verify_the_display_of_i_icon_and_random_golfer_text_below_lucky_dip_market(self):
        """
        DESCRIPTION: Verify the display of 'i' icon and Random Golfer text below Lucky Dip market
        EXPECTED: 1.'i' icon is displayed below Lucky Dip Market
        EXPECTED: 2.Random golfer text is displayed beside 'i' icon (The text is displayed from the selection name which
                    is set to display - yes in OB)
        """
        self.__class__.expected_event_name = self.site.sport_event_details.event_name.strip()
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.assertTrue(self.lucky_dip_section.has_info_icon, f'Info Icon is Not Displayed in Lucky Dip Market Section')
        self.assertEqual(self.lucky_dip_section.market_discription, self.market_description,
                         f"Expected market description : '{self.market_description}' \
                         does not match with Actuall description : '{self.lucky_dip_section.market_discription}'")

    def test_003_verify_if_the_i_icon_is_clickable_and_the_lucky_dip_banner_is_displayed(self):
        """
        DESCRIPTION: Verify if the 'i' icon is clickable and the lucky dip banner is displayed
        EXPECTED: 1. 'i' icon should be clickable
        EXPECTED: 2. Lucky dip banner and the text below the banner should be displayed to the user
        (as configured in cms)upon clicking the icon
        """
        self.lucky_dip_section.info_icon.click()
        is_info_banner = self.lucky_dip_section.lucky_dip_info.has_lucky_dip_info_banner
        self.assertTrue(is_info_banner, "Lucky Dip Info Banner is Not Displayed")
        actual_info_market_title = self.lucky_dip_section.lucky_dip_info.info_market_title
        actual_info_market_description = self.lucky_dip_section.lucky_dip_info.info_market_description
        self.assertEqual(self.expected_market_title, actual_info_market_title,
                         f'Actual Market Title : "{actual_info_market_title}" is not same as Expected Market Title : "'
                         f'{self.expected_market_title}"')
        self.assertEqual(self.expected_market_desc, actual_info_market_description,
                         f'Actual Market Description : "{actual_info_market_description}'
                         f'" is not same as Expected Market Description : "{self.expected_market_desc}"')
        self.assertTrue(self.lucky_dip_section.lucky_dip_info.has_lucky_dip_info_close_button,
                         f'Close(X) Button is not displayed')
        self.lucky_dip_section.lucky_dip_info.info_close_button.click()
        actual_event_name = self.site.sport_event_details.event_name.strip()
        self.assertEqual(self.expected_event_name, actual_event_name,
                         f'Actual Event Name : "{actual_event_name}" is not same as Expected Event Name : '
                         f'"{self.expected_event_name}"')