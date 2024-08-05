from datetime import datetime
import pytest
from crlat_cms_client.utils.exceptions import CMSException
import voltron.environments.constants as vec
from crlat_ob_client.utils.date_time import get_date_time_as_string
import tests
from tests.Common import Common
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name
from voltron.utils.waiters import wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.cms
@vtest
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
class Test_C65861232_Verify_Highlight_carousal_display_with_eventID_for_primary_market_Mobile_Homepage(
    Common):
    """
    TR_ID: C65861232
    NAME: Verify Highlight carousal display with eventID for primary market_Mobile Homepage
    DESCRIPTION: This test case is to verify Highlight carousal display with eventID for primary market_Mobile Homepage
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS Navigation:
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active & Display on Desktop" check boxes
    PRECONDITIONS: *Title=TENNIS - FEATURED MATCHES
    PRECONDITIONS: *Set events by=Event IDs
    PRECONDITIONS: *Event IDs= 240767310,240778313(pre-play)
    PRECONDITIONS: *Select Market & Market Type = Primary Market
    PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
    PRECONDITIONS: *SVG Icon=tennis
    PRECONDITIONS: *No. of Events = 2
    PRECONDITIONS: *Enable Display In-Play checkbox
    PRECONDITIONS: *Select Universal view
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def check_hc_module_status_and_create_hightlight_carousel(self, hc_title=None, events_list=[], events_count=1,
                                                              svg_icon=""):
        sports_module = self.cms_config.get_sport_module(module_type=None)
        hc_module_cms = None
        for module in sports_module:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break
        if hc_module_cms is None:
            raise CMSException("Highlight carousel module not found in CMS")
        else:
            highlights_module_status = next((module['disabled'] for module in sports_module
                                        if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL'), None)
            if highlights_module_status:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms)
        highlights_carousel = self.cms_config.create_highlights_carousel(
            title=hc_title,
            events=events_list, limit=events_count, svgId=svg_icon, displayOnDesktop=False)
        return highlights_carousel

    def check_sb_module_status_and_create_surface_bet(self, sb_title=None, selection_id: int = None,
                                                      eventID=0):
        sports_module = self.cms_config.get_sport_module(module_type=None)
        surface_bet_module_cms = None
        for module in sports_module:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_module_cms = module
                break
        if surface_bet_module_cms is None:
            raise CMSException("Surface bet module not found in CMS")
        else:
            surface_bet_module_status = next((module['disabled'] for module in sports_module
                                         if module['moduleType'] == 'SURFACE_BET'), None)
            if surface_bet_module_status:
                self.cms_config.change_sport_module_state(sport_module=surface_bet_module_cms)

        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0],
                                                      eventIDs=eventID,
                                                      edp_on=True,
                                                      highlightsTabOn=True,
                                                      svg_icon='tennis',
                                                      title=sb_title
                                                      )
        return surface_bet

    def check_ql_module_status_and_create_quick_link(self, ql_title=None, destination_url=None):
        sports_module = self.cms_config.get_sport_module(module_type=None)
        quick_link_module_cms = None
        for module in sports_module:
            if module['moduleType'] == 'QUICK_LINK':
                quick_link_module_cms = module
                break
        if quick_link_module_cms is None:
            raise CMSException("Quick Link module not found in CMS")
        else:
            quick_link_status = next((module['disabled'] for module in sports_module
                                 if module['moduleType'] == 'QUICK_LINK'), None)
            if quick_link_status:
                self.cms_config.change_sport_module_state(sport_module=quick_link_module_cms)
        quick_link = self.cms_config.create_quick_link(title=ql_title,
                                                       sport_id=0,
                                                       destination=destination_url,
                                                       )
        return quick_link

    def verify_highlight_carousel_on_fe(self, highlights_carousel_title=None, expected_result=True, refresh_count=3,
                                        timeout=1):
        if expected_result:
            HC = wait_for_cms_reflection(
                lambda: self.site.home.tab_content.highlight_carousels.get(highlights_carousel_title),
                refresh_count=refresh_count, ref=self, timeout=timeout, haul=5)
            self.assertTrue(HC,
                            msg=f'{highlights_carousel_title} is not available')
            return HC
        else:
            hcs = self.site.home.tab_content.highlight_carousels
            if hcs:
                section = wait_for_cms_reflection(
                    lambda: hcs.get(highlights_carousel_title),
                    refresh_count=3, ref=self, expected_result=False)
                self.assertFalse(section,
                                 msg=f'{highlights_carousel_title} is available')

    def changing_the_order_of_modules_in_cms(self, modules):
        modules = modules
        # getting the modules
        sports_module = self.cms_config.get_sport_module(module_type=None)
        # getting the ids of the module which we need to change the order
        drag_panel_ids = []
        for module in modules:
            for item in sports_module:
                if item.get('moduleType').upper() == module.upper():
                    drag_panel_ids.append(item.get('id'))
                    break
        order = [item['id'] for item in sports_module]
        i = 0
        for drag_panel_id in drag_panel_ids:
            order.remove(drag_panel_id)
            order.insert(i, drag_panel_id)
            self.cms_config.change_order_of_module_items(new_order=order, moving_item=drag_panel_id)
            i += 1

    def checking_ordering_of_modules(self):
        sports_module = self.cms_config.get_sport_module(module_type=None)
        if self.brand != 'bma':
            sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='ladbrokes')
        else:
            sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='bma')
        for section in sports_module[:3]:
            module_type = section.get('moduleType').upper()
            for count in range(3):
                if sections_names_with_order.get(module_type) != sports_module.index(section):
                    self.device.refresh_page()
                    self.device.driver.implicitly_wait(3)
                    if self.brand != 'bma':
                        sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='ladbrokes')
                    else:
                        sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='bma')
                else:
                    break
            self.assertEqual(sections_names_with_order.get(module_type), sports_module.index(section),
                             msg=f'the module of cms {module_type} order {sports_module.index(section)} is '
                                 f'not same as frontend {sections_names_with_order.get(module_type)} ')

    def changing_highlights_carousel_order(self, highlight_carousels_list=[]):
        all_hcs = self.cms_config.get_all_highlights_carousels()
        hc_ids = []
        for i in range(len(highlight_carousels_list)):
            for hc in all_hcs:
                if hc.get('title').upper() == highlight_carousels_list[i].upper():
                    hc_ids.append(hc.get('id'))
                    break
        all_hc_ids = [item['id'] for item in all_hcs]
        i = 0
        for hc_id in hc_ids:
            all_hc_ids.remove(hc_id)
            all_hc_ids.insert(i, hc_id)
            self.cms_config.set_highlight_courousel_ordering(new_order=all_hc_ids, moving_item=hc_id)
            i += 1

    def verify_ordering_of_highlight_carousels(self):
        hcs = self.cms_config.get_all_highlights_carousels()
        sections = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels,
            refresh_count=3, ref=self)
        actual_highlight_carousels = list(sections.keys())
        expected_highlight_carousels = [hc.get('title').upper() for hc in hcs]
        for i in range(2):
            self.assertEqual(actual_highlight_carousels[i].upper(), expected_highlight_carousels[i].upper(),
                             msg=f"expected highlight carousel is {expected_highlight_carousels[i].upper()} but {actual_highlight_carousels[i].upper()} ")

    def convert_highlights_carousel_title(self, title):
        return title if not self.brand == 'ladbrokes' else title.upper()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS Navigation:
        PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel and click on Create Highlights Carousel CTA.
        PRECONDITIONS: Configure HC as below by giving all the fields.
        """
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title=generate_highlights_carousel_name())
        self.__class__.surface_bet_title = "Autotest C65861232 Surface bet"
        self.__class__.quick_link_title = "Autotest C65861232 Quick link"
        self.__class__.svg_icon = "tennis"
        self.__class__.expected_highlights_carousel_events = []
        self.__class__.events_start_time = {}
        self.__class__.highlights_carousel_event_ids = []
        if tests.settings.backend_env == 'prod':
            # ******** Getting Events ********
            events = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id,
                                                         all_available_events=True)
            # ******** Getting event id  ********
            self.__class__.eventID1 = events[0]['event']['id']
            self.__class__.eventID2 = events[1]['event']['id']
            self.__class__.eventID3 = events[2]['event']['id']
            # ******** Getting Selection IDs ********
            outcomes = next(((market['market']['children']) for market in events[0]['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(event_selection.values())[0]
            # ******** Events list and Events start time ********
            for i in range(2):
                # ******** events list ********
                self.expected_highlights_carousel_events.append(events[i]['event']['name'].upper().strip())
                # ******** events start time list ********
                self.events_start_time[events[i]['event']['name'].upper()] = events[i]['event']['startTime']
        else:
            # ******** Getting Events ********
            event1 = self.ob_config.add_tennis_event_to_autotest_trophy()
            event2 = self.ob_config.add_tennis_event_to_autotest_trophy()
            event3 = self.ob_config.add_tennis_event_to_autotest_trophy()
            # ******** Getting Event id ********
            self.__class__.eventID1 = event1.event_id
            self.__class__.eventID2 = event2.event_id
            self.__class__.eventID3 = event3.event_id
            # ******** Getting Selection IDs ********
            self.__class__.selection_id = event1.selection_ids[event1.team1]
            # ******** Events list and Events start time ********
            event1_name = event1.team1 + ' v ' + event1.team2
            event2_name = event2.team1 + ' v ' + event2.team2
            self.__class__.expected_highlights_carousel_events = [event1_name.upper(), event2_name.upper()]
            self.events_start_time[0] = event1.event_date_time
            self.events_start_time[1] = event2.event_date_time

        self.__class__.highlights_carousel_event_ids = [self.eventID1, self.eventID2]
        # ******** Creation of Highlights Carousel *************************
        self.__class__.highlights_carousel = self.check_hc_module_status_and_create_hightlight_carousel(
            hc_title=self.highlights_carousel_title, events_list=self.highlights_carousel_event_ids, events_count=2,
            svg_icon=self.svg_icon)

    def test_001_launch_bma_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application
        EXPECTED: User should able to launch successfully
        """
        # ******** Home page navigation *************************
        self.site.login()

    def test_002_verify_created_highlight_carousal_displaying_on_fe(self):
        """
        DESCRIPTION: Verify Created Highlight carousal displaying on FE
        EXPECTED: Created HC should display on Homepage
        """
        # ******** Verification of Highlight Carousel *************************
        self.__class__.section = self.verify_highlight_carousel_on_fe(
            highlights_carousel_title=self.highlights_carousel_title)
        # ******** Verification of Highlight Carousel events *************************
        actual__highlights_carousel_events = [item_name.upper() for item_name in self.section.items_names]
        self.assertListEqual(self.expected_highlights_carousel_events, actual__highlights_carousel_events,
                             msg=f'actual highlights carousel events {actual__highlights_carousel_events} not equals to expected highlights carousel events {self.expected_highlights_carousel_events}')
        # ******** Verification of SVG icon *************************
        self.assertEqual(self.section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')
        # ******** Creation of Surface Bet *************************
        surface_bets_stauts = self.site.home.tab_content.has_surface_bets(expected_result=True)
        if not surface_bets_stauts:
            surface_bet = self.check_sb_module_status_and_create_surface_bet(sb_title=self.surface_bet_title,
                                                                             selection_id=self.selection_id,
                                                                             eventID=self.eventID1)
            created_surface_bet = surface_bet.get('title').upper()
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bet = surface_bets.get(created_surface_bet)
            self.assertTrue(surface_bet,
                            msg=f'Failed to display Surface Bets named {created_surface_bet} is not available in {surface_bets.keys()}')
        # ******** Creation of Quick Link *************************
        quick_links_status = self.site.home.tab_content.has_quick_links(expected_result=True)
        if not quick_links_status:
            destination_url = f'https://{tests.HOSTNAME}/home/'
            quick_link = self.check_ql_module_status_and_create_quick_link(ql_title=self.quick_link_title,
                                                                           destination_url=destination_url)
            created_quick_link = quick_link.get('title')
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            quick_link = quick_links.get(created_quick_link)
            self.assertTrue(quick_link, msg=f'{created_quick_link} quick link is not available in {quick_links.keys()}')

    def test_003_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        # setting the order of the module in CMS
        self.modules = ['SURFACE_BET', 'QUICK_LINK', 'HIGHLIGHTS_CAROUSEL']
        self.changing_the_order_of_modules_in_cms(modules=self.modules)
        self.checking_ordering_of_modules()

    def test_004_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        # setting the order of the module in CMS
        self.modules = ['HIGHLIGHTS_CAROUSEL', 'SURFACE_BET', 'QUICK_LINK']
        self.changing_the_order_of_modules_in_cms(modules=self.modules)
        self.checking_ordering_of_modules()

    def test_005_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_006_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Homepage as per cms changes
        """
        # ******** Updation of Highlight Carousel title and SVG icon *************************
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title=generate_highlights_carousel_name())
        self.svg_icon = "icon-tennis"
        self.cms_config.update_highlights_carousel(self.highlights_carousel, title=self.highlights_carousel_title,
                                                   svgId=self.svg_icon)
        # ******** Verification of Highlight Carousel title and SVG icon *************************
        section = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                                       refresh_count=10,
                                                       timeout=10)
        self.assertEqual(section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_007_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_008_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        # ******** Updation of Highlight Carousel Display dates to Past dates *************************
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-8.5)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-6.5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_009_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                             expected_result=False)

    def test_010_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        # ******** Updation of Highlight Carousel From date to Past and To date to Future *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-6.5)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=10)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_011_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Homepage
        """
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)

    def test_012_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes.
        EXPECTED: Changes are saved
        """
        # ******** Updation of Highlight Carousel Display dates to Future dates *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=2)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_013_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                             expected_result=False)
        # ******** Updation of Highlight Carousel From date to Past and To date to Future *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-10)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=5.5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)
        # ******** Verification of Highlight Carousel *************************
        self.__class__.section = self.verify_highlight_carousel_on_fe(
            highlights_carousel_title=self.highlights_carousel_title)

    def test_014_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # covered in C65861228 test case

    def test_015_verify_the_chevron_on_hc_event_card_amp_navigation(self):
        """
        DESCRIPTION: Verify the chevron on HC event card &amp; navigation
        EXPECTED: Chevron should be in blue color and aligned to right &amp; upon clicking on it should redirect to EDP of that event
        """
        # ******** Verification of Highlight Carousel Events Navigation *************************
        highlight_carousel_events = self.section.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')
        highlight_carousel_events = {key.upper(): value for key, value in highlight_carousel_events.items()}
        highlight_carousel_events.get(self.expected_highlights_carousel_events[0]).click()
        self.site.wait_content_state(state_name='EventDetails')
        current_url = self.device.get_current_url()
        self.assertIn(self.highlights_carousel_event_ids[0], current_url, msg="event details page not displayed")
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        section = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)
        self.__class__.highlight_carousel_events = section.items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')

    def test_016_verify_the_date_amp_time_of_event_on_hc_event_card(self):
        """
        DESCRIPTION: Verify the date &amp; time of event on HC event card
        EXPECTED: Date &amp; time should display on event card(eg:21:45 Today/00:30 10July)
        """
        # ******** Verification of Highlight Carousel events Date and Time *************************
        self.highlight_carousel_events = {key.upper(): value for key, value in self.highlight_carousel_events.items()}
        for event_name, event in self.highlight_carousel_events.items():
            actual_event_date_time = event.event_time
            future_datetime_format = '%H:%M, %d %b' if self.brand == 'bma' else '%H:%M %d %b'
            ui_format_pattern = '%H:%M, Today' if self.brand == 'bma' else '%H:%M Today'
            expected_event_start_date_time = self.convert_time_to_local(
                date_time_str=self.events_start_time.get(event_name.upper()),
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True, future_datetime_format=future_datetime_format,
                ui_format_pattern=ui_format_pattern)
            self.assertEqual(expected_event_start_date_time, actual_event_date_time,
                             msg=f"expected event start date time {expected_event_start_date_time} is not matched with actual event start date time {actual_event_date_time}")
        # ******** Verification of Highlight Carousel event odds header *************************
        bet_buttons = list(self.highlight_carousel_events.values())[0].get_all_prices()
        del bet_buttons['Draw']
        expected_list = ['1', '2']
        actual_list = [button.name.split('\n')[0].upper() for button_name, button in bet_buttons.items()]
        self.assertListEqual(expected_list, actual_list,
                             f'actual headers of odds is {actual_list} is not same as expected odds headers {expected_list}')
        bet_button = next(iter(bet_buttons.values()))
        bet_button.click()
        self.site.quick_bet_panel.close()
        self.assertTrue(bet_button.is_selected(), f'bet button is not selected')

    def test_017_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_018_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """
        # ******** Updation of Highlight Carousel Number of Events to 1 *************************
        updated_limit = 1
        self.cms_config.update_highlights_carousel(self.highlights_carousel, limit=updated_limit)
        # ******** Verification of Highlight Carousel events count *************************
        is_events_count_equal = wait_for_cms_reflection(
            lambda: len(self.site.home.tab_content.highlight_carousels.get(
                self.highlights_carousel_title).items_names) == updated_limit, timeout=5,
            refresh_count=2, ref=self, expected_result=True)
        self.assertTrue(is_events_count_equal,
                        msg=f"updated events limit count is not matched with expected events limit count {updated_limit} ")

    def test_019_verify_hc_display_as_per_cms_entry_as_per_comma_separation(self):
        """
        DESCRIPTION: Verify HC display as per CMS entry as per comma separation
        EXPECTED: HC events should display as per comma seperation (eg: if two event id's configured in cms, the first congigured event should display first in FE, second configured event should diplay in second place)
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_020_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # Covered in test_016_verify_the_date_amp_time_of_event_on_hc_event_card

    def test_021_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        # covered in test_004_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated

    def test_022_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        hc2_title = self.convert_highlights_carousel_title(
            title=generate_highlights_carousel_name())
        self.check_hc_module_status_and_create_hightlight_carousel(
            hc_title=hc2_title, events_list=[self.eventID3], events_count=1,
            svg_icon=self.svg_icon)
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=hc2_title)
        hc_titles = [self.highlights_carousel_title, hc2_title]
        self.changing_highlights_carousel_order(highlight_carousels_list=hc_titles)
        self.verify_ordering_of_highlight_carousels()

    def test_023_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can able to select the selections on HC
        EXPECTED: User should able to select &amp; selections should be highlighted
        """
        # covered in test_016_verify_the_date_amp_time_of_event_on_hc_event_card

    def test_024_verify_univeral_view_for_hc(self):
        """
        DESCRIPTION: Verify Univeral view for HC
        EXPECTED: HC should display for all  logged in &amp; logged out users
        """
        # ******** Verification of Highlight Carousel for logged out user *************************
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)

    def test_025_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(
            self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """
        # ******** Updation of Highlight Carousel to segment view *************************
        self.cms_config.update_highlights_carousel(self.highlights_carousel, inclusionList=[self.segment])
        # ******** Verification of Highlight Carousel for logged in user *************************
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)

    def test_026_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
        # covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_027_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        # Covered in test_015_verify_the_chevron_on_hc_event_card_amp_navigation

    def test_028_verify_team_kits_when_hc_is_configured_using_the_event_id_for_the_football_premier_or_champions_league(
            self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the event ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        # created event with tennis and this step is covered in test case C6587284

    def test_029_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        # Can't deactivate the whole highlight carousel module, It will impact other HC test cases

    def test_030_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on homepage
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_031_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        # Need resulted event

    def test_032_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(
            self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        # Need resulted event

    def test_033_go_back_to_the_same_highlights_carousel_in_cms_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel in CMS, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        # ******** Updation of Highlight Carousel to Inactive State *************************
        self.cms_config.update_highlights_carousel(self.highlights_carousel, disabled=True)

    def test_034_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                             expected_result=False)
        # ******** Updation of Highlight Carousel to Active State *************************
        self.cms_config.update_highlights_carousel(self.highlights_carousel, disabled=False)
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title, refresh_count=10,
                                             timeout=10)

    def test_035_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        # ******** Removing Highlight Carousel *************************
        highlight_carousel_id = self.highlights_carousel["id"]
        self.cms_config.delete_highlights_carousel(highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                             expected_result=False)
