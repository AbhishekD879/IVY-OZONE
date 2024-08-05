import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest, generate_highlights_carousel_name
from crlat_cms_client.utils.date_time import get_date_time_as_string
from datetime import datetime


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create highlight carousels and event in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C9726410_Event_Hub_Highlights_Carousel_displaying_based_on_active_option_for_particular_highlights_carousel(BaseHighlightsCarouselTest):
    """
    TR_ID: C9726410
    NAME: Event Hub: Highlights Carousel displaying based on "active" option for particular highlights carousel
    DESCRIPTION: This test case verifies Highlights Carousel displaying based on "Active" option for particular Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True
    highlights_carousels_titles = [generate_highlights_carousel_name(), generate_highlights_carousel_name()]
    now = datetime.now()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    def test_001_verify_highlights_carousels_displaying(self, **featured):
        """
        DESCRIPTION: Verify Highlights Carousels displaying
        EXPECTED: 2 Highlights Carousels are displayed
        """
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                                   tab['visible'] is True and
                                   tab['directiveName'] == 'EventHub' and
                                   (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                       time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]

        self.__class__.event_hub_tab_name = self.tabs_cms[0]
        self.__class__.event_hub_index = [tab['hubIndex'] for tab in module_ribbon_tabs if
                                          tab['title'].upper() == self.event_hub_tab_name]

        self.__class__.sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(self.event_hub_index[0])

        featured['events_time_from_hours_delta'] = -10
        featured['module_time_from_hours_delta'] = -10
        featured['date_from'] = get_date_time_as_string(date_time_obj=self.now, time_format=self.time_format,
                                                        url_encode=False, hours=-5, days=-1)[:-3] + 'Z'
        hc_module_cms = None
        for module in self.sports_module_event_hub:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break
        if hc_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL')
        else:
            highlights_module_status = [module['disabled'] for module in self.sports_module_event_hub
                                        if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL']
            if highlights_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms)

        event_1 = self.ob_config.add_autotest_premier_league_football_event()
        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        event_id_1 = event_1.event_id
        event_id_2 = event_2.event_id

        self.__class__.highlights_carousel_1 = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                                                          events=[event_id_1],
                                                                                          page_type='eventhub',
                                                                                          sport_id=self.event_hub_index[0],
                                                                                          **featured)
        self.__class__.highlights_carousel_2 = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[1],
                                                                                          events=[event_id_2],
                                                                                          page_type='eventhub',
                                                                                          sport_id=self.event_hub_index[0],
                                                                                          **featured)

        self.__class__.highlights_carousel_name_1 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_2 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[1])

        self.site.wait_content_state('homepage')
        module_tab = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.keys()
        if self.event_hub_tab_name in module_tab:
            self.site.home.module_selection_ribbon.tab_menu.click_button(self.event_hub_tab_name)
        else:
            self.device.refresh_page()
            self.site.wait_content_state_changed()

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_1}')

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_2}')

    def test_002___in_cms__sport_pages__event_hub__highlights_carousel_deactivate_one_of_the_displayed_highlights_carousels__in_application_refresh_the_page_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Event hub > Highlights Carousel deactivate one of the displayed Highlights Carousels
        DESCRIPTION: - In Application refresh the page and verify Highlights Carousel displaying
        EXPECTED: Only 1 active Highlights Carousel is displayed and deactivated Highlights Carousel is not displayed
        """
        self.cms_config.change_highlights_carousel_state(self.highlights_carousel_1, active=False)
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_1, expected_result=False)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertNotIn(self.highlights_carousel_name_1, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named "{self.highlights_carousel_name_1}" should disappear')
        self.assertIn(self.highlights_carousel_name_2, highlight_carousels.keys(),
                      msg=f'Highlights Carousel named "{self.highlights_carousel_name_2}" was not found in {highlight_carousels.keys()}')
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named "{self.highlights_carousel_name_1}"')

    def test_003___in_cms__sport_pages__event_hub__highlights_carousel_deactivate_another_highlights_carousels_that_is_still_displayed__in_application_refresh_the_page_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Event hub > Highlights Carousel deactivate another Highlights Carousels that is still displayed
        DESCRIPTION: - In Application refresh the page and verify Highlights Carousel displaying
        EXPECTED: None Highlights Carousels are displayed
        """
        self.cms_config.change_highlights_carousel_state(self.highlights_carousel_2, active=False)
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_2, expected_result=False)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertNotIn(self.highlights_carousel_name_1, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named {self.highlights_carousel_name_1} should disappear')
        self.assertNotIn(self.highlights_carousel_name_2, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named {self.highlights_carousel_name_2} should disappear')
