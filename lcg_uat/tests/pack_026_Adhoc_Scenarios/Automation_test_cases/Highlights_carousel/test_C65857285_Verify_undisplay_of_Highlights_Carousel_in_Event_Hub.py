import pytest
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name, BaseHighlightsCarouselTest
from voltron.utils.waiters import wait_for_haul, wait_for_result, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.cms
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@vtest
class Test_C65857285_Verify_undisplay_of_Highlights_Carousel_in_Event_Hub(BaseHighlightsCarouselTest):
    """
    TR_ID: C65857285
    NAME: Verify undisplay of Highlights Carousel in Event Hub
    DESCRIPTION: This test case verifies  undisplay of Highlights Carousel in Event Hub
    PRECONDITIONS: Create Event hub and tag this event hub to Module ribbon tab,
    PRECONDITIONS: Event Hub - Highlights Carousel Creation in CMS:
    PRECONDITIONS: 1. Login to Environment specific CMS
    PRECONDITIONS: 2. Navigate to Sports Pages -->Event Hub
    PRECONDITIONS: 3. Click on Create Event Hub
    PRECONDITIONS: 4. Enter title and click on Create button
    PRECONDITIONS: 5. Click on Add Sport Module --> Select option from dropdown as Highlights Carousel
    PRECONDITIONS: 6. Click on Create button
    PRECONDITIONS: 7. Click on Highlights Carousel module in newly created Event Hub --> Click on Create Highlight Carousel button
    PRECONDITIONS: 8. Enter All fields like
    PRECONDITIONS: - Active Checkbox
    PRECONDITIONS: - Title as 'Featured - Ladies Matches '
    PRECONDITIONS: - TypeId/EventId
    PRECONDITIONS: - Select market and Market Type will be auto selected
    PRECONDITIONS: - Display From
    PRECONDITIONS: - Display To
    PRECONDITIONS: - SVG Icon
    PRECONDITIONS: - No.Of Events
    PRECONDITIONS: - Display Inplay
    PRECONDITIONS: 9. Click on Create button
    PRECONDITIONS: 10. Unselect Active checkbox for Highlight Carosel in Event hub and save the changes
    PRECONDITIONS: Module Ribbon Tab Creation(MRT) in CMS :
    PRECONDITIONS: 1. Navigate to Module Ribbon tab
    PRECONDITIONS: 2. Click on Create Module Ribbon tab and enter below fields
    PRECONDITIONS: - Module Ribbon tab Title
    PRECONDITIONS: - Directive name as Event Hub
    PRECONDITIONS: - Select Event Hub name(Which we created above)
    PRECONDITIONS: - Visible from,Visible To(User can change accordingly)
    PRECONDITIONS: 3. Click on Create button
    PRECONDITIONS: 4. Select Active checkbox,IOS,Android checkboxes
    PRECONDITIONS: 5. Select Show Tab on field and click on Save Changes button
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create Event hub and tag this event hub to Module ribbon tab,
        PRECONDITIONS: Event Hub - Highlights Carousel Creation in CMS:
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_ID = event.ss_response['event']['id']
        else:
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            event_ID = events[0]['event']['id']
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_numbers = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_numbers)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='HIGHLIGHTS_CAROUSEL')
        highlights_carousel_title_name = generate_highlights_carousel_name()
        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(
                                                                         title=highlights_carousel_title_name,
                                                                         events=[event_ID],
                                                                         page_type='eventhub',
                                                                         inplay=True,
                                                                         limit=1,
                                                                         sport_id=index_number)
        self.__class__.highlights_carousel_title = highlights_carousel_title_name if self.brand == 'bma' else \
            highlights_carousel_title_name.upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           title='AutoTest_C65857285',
                                                                           hub_index=index_number,
                                                                           display_date=True,
                                                                           devices_wp=False)
        self.assertTrue(event_hub_tab_data, msg=f'event hub tab is not configured')
        self.__class__.module_ribbon_tab = event_hub_tab_data['title'].upper()

    def test_001_1_login_to_ladscoral_ltenvironmentgt(self):
        """
        DESCRIPTION: 1. Login to Lads/Coral &lt;Environment&gt;
        EXPECTED: User should be logged in
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage')
        for i in range(20):
            module_ribbon_tabs = wait_for_result(
                lambda: self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict, timeout=10)
            module_ribbon_tab = next((tab for tab in module_ribbon_tabs if tab.upper() == self.module_ribbon_tab), None)
            if module_ribbon_tab:
                break
            else:
                self.device.refresh_page()
                wait_for_haul(6)
        self.assertIn(self.module_ribbon_tab, module_ribbon_tabs,
                      msg=f'{self.module_ribbon_tab} not found in {module_ribbon_tabs}')
        featured_module_ribbon_tab = module_ribbon_tabs.get(self.module_ribbon_tab)
        featured_module_ribbon_tab.click()
        highlight_carousels_items = self.site.home.tab_content.highlight_carousels
        self.assertTrue(highlight_carousels_items, msg=f'Highlights Carousels is not displayed in Event Hub')
        highlight_carousel_item = highlight_carousels_items.get(self.highlights_carousel_title)
        if not highlight_carousel_item:
            wait_for_haul(3)
            self.device.refresh_page()
            highlight_carousels_items = self.site.home.tab_content.highlight_carousels
            self.assertTrue(highlight_carousels_items, msg=f'Highlights Carousels is not displayed in Event Hub')
            highlight_carousel_item = highlight_carousels_items.get(self.highlights_carousel_title)
        self.assertTrue(highlight_carousel_item, msg=f'{highlight_carousel_item} highlight carousel not is displayed')

    def test_002_2_navigate_to_module_ribbon_tab_which_is_created_in_cms(self):
        """
        DESCRIPTION: 2. Navigate to Module Ribbon tab which is created in CMS
        EXPECTED: 2. Highlight Carousel should not be displayed in Module Ribbon tab
        """
        self.cms_config.change_highlights_carousel_state(self.highlights_carousel, active=False)
        highlights_carousel_is_displayed = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(self.highlights_carousel_title),
            expected_result=False,
            timeout=10,
            refresh_count=5, ref=self
        )
        self.assertFalse(highlights_carousel_is_displayed, msg='Highlights Carousel section still shown on the screen')
