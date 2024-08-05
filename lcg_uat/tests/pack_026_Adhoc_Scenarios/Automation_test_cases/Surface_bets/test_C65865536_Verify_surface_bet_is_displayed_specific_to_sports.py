import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string
from voltron.utils.waiters import wait_for_result, wait_for_haul, wait_for_cms_reflection
from datetime import datetime
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.js_functions import click
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from collections import OrderedDict


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.surface_bets
@vtest
class Test_C65865536_Verify_surface_bet_is_displayed_specific_to_sports(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C65865536
    NAME: Verify surface bet is displayed specific to sports
    DESCRIPTION: This test case verifies surface bet is displayed specific to sports
    """
    keep_browser_open = True

    def get_or_create_event_hub(self):
        # getting tabs of module ribbon tab from cms and checking if any of them are event hub
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                    tab['visible'] is True and
                    tab['directiveName'] == 'EventHub' and
                    (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                        time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        self.__class__.event_hub_tab_name = next((tab.upper() for tab in tabs_cms if tab.upper() == 'US SPORTS'),
                                                 None)
        # getting index of the US SPORT event hub
        self.__class__.index_number = None
        if self.event_hub_tab_name:
            self.__class__.index_number = next((tab['hubIndex'] for tab in module_ribbon_tabs if
                                                tab['title'].upper() == self.event_hub_tab_name.upper()), None)
        if self.event_hub_tab_name is None or self.index_number is None:
            # Creating the eventhub
            existing_event_hubs = self.cms_config.get_event_hubs()
            existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
            # need a unique non-existing index for new Event hub
            self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)
            # Create the event hub name
            self.cms_config.create_event_hub(index_number=self.index_number)
            # Adding event hub to module ribbon tab
            internal_id = f'tab-eventhub-{self.index_number}'
            event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                               internal_id=internal_id,
                                                                               hub_index=self.index_number,
                                                                               display_date=True)
            self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    def verify_surface_bet(self, surface_bets_container):
        # reading the surface bets
        surface_bets_reference = surface_bets_container.items_as_ordered_dict
        surface_bets_reference = OrderedDict((key.upper(), value) for key, value in surface_bets_reference.items())
        self.assertTrue(surface_bets_reference, msg='No created Surface Bets found in FE')

        self.assertIn(self.surface_bet_title, surface_bets_reference,
                      f'surface bet : "{self.surface_bet_title}" is not found in {surface_bets_reference}')

        # getting the surface bet which is created among the surface bets in FE
        surface_bet_content = surface_bets_reference.get(self.surface_bet_title)
        surface_bet_content.scroll_to()

        # asserting all the values in the FE surface bet with the expected data set in CMS
        actual_title = surface_bet_content.header.title.upper()
        self.assertEqual(actual_title, self.surface_bet_title,
                         f'Actual title : "{actual_title}" is not same as '
                         f'Expected title : "{self.surface_bet_title}"')

        actual_svg_icon = surface_bet_content.header.icontext.replace('#', '')
        expected_svg_icon = self.sb_cms_configurations['svgId'].replace('#', '')
        self.assertEqual(actual_svg_icon, f'{expected_svg_icon}',
                         f'Actual SVG icon: "{actual_svg_icon}", '
                         f'Expected SVG icon: "{expected_svg_icon}"')

        if tests.settings.backend_env != 'prod':
            self.assertEqual(surface_bet_content.get_attribute('style'), self.svgBg,
                             f'svg Background is not same as cms config')

        actual_content = surface_bet_content.content.strip().upper()
        expected_content = self.sb_cms_configurations['content'].strip().upper()
        self.assertEqual(actual_content, expected_content,
                         f'Actual Content : "{actual_content}" is not same as '
                         f'Expected Content : "{expected_content}"')
        self.verify_surface_bet_content_header(surface_bets_container=surface_bets_container,
                                               expected_content_header=self.sb_cms_configurations[
                                                   'contentHeader'].upper())

    def verify_surface_bet_content_header(self, surface_bets_container, expected_content_header):
        # reading the surface bets
        surface_bets_reference = surface_bets_container.items_as_ordered_dict
        surface_bets_reference = OrderedDict((key.upper(), value) for key, value in surface_bets_reference.items())
        self.assertTrue(surface_bets_reference, msg='No created Surface Bets found in FE')

        self.assertIn(self.surface_bet_title, surface_bets_reference,
                      f'surface bet : "{self.surface_bet_title}" is not found in {surface_bets_reference}')

        # getting the surface bet which is created among the surface bets
        surface_bet_content = surface_bets_reference.get(self.surface_bet_title)
        wait_for_haul(5)
        surface_bet_content.scroll_to()
        actual_content_header = wait_for_result(lambda: surface_bet_content.content_header.upper(), timeout=10,
                                                expected_result=True)
        self.assertEqual(actual_content_header, expected_content_header,
                         f'Actual Content Header :"{actual_content_header}" is not same as'
                         f'Expected Content Header : "{expected_content_header}"')

    def verify_surface_bets_previous_and_next_scroll_buttons(self, surface_bets_container):
        # Verifying Surface bets left and right scroll in home page, only applicable for desktop
        if self.device_type != 'mobile':
            self.assertTrue(surface_bets_container.has_scroll_button(),
                            msg="Slider button is not displayed even if there are more than 2 surface bets")
            # reading the surface bets
            surface_bets_reference = surface_bets_container.items_as_ordered_dict
            self.assertTrue(surface_bets_reference, msg='No Surface Bets found')

            surface_bets_name_list = [item.upper() for item in list(surface_bets_reference.keys())]
            self.assertIn(self.surface_bet_title, surface_bets_name_list,
                          f'surface bet : "{self.surface_bet_title}" is not found in {surface_bets_name_list}')

            # Verifying Surface bets left and right scroll functionality
            surface_bets_list = list(surface_bets_reference.items())
            first_surface_bet_name, first_surface_bet = surface_bets_list[0]
            self.assertTrue(first_surface_bet.is_displayed(),
                            msg=f'First surface bet with name {first_surface_bet_name} is not displayed '
                                f'even if next scroll action is not performed')

            # clicking on the next arrow
            next_arrow = surface_bets_container.scroll_next_button
            click(next_arrow._we)
            third_surface_bet_name, third_surface_bet = surface_bets_list[2]
            is_third_surface_bet_diaplayed = wait_for_result(lambda: third_surface_bet.is_displayed(), timeout=10,
                                                             expected_result=True)
            self.assertTrue(is_third_surface_bet_diaplayed,
                            msg=f'fourth surface bet with name {third_surface_bet_name} is not displayed '
                                f'even after next scroll action is  performed')

            # clicking on the previous arrow
            prev_arrow = surface_bets_container.scroll_previous_button
            click(prev_arrow._we)
            self.assertTrue(first_surface_bet.is_displayed(),
                            msg=f'First surface bet with name {third_surface_bet_name} is not displayed '
                                f'even if previous scroll action is  performed')

    def get_status_of_surface_bet(self, surface_bet_name, time=1, expected_result=True):
        if time > 180:
            return [not expected_result, []]
        wait_for_haul(1)
        if not self.site.football.tab_content.has_surface_bets(expected_result=True):
            surface_bets_names = []
        else:
            surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
            surface_bets_names = []
            for name, sb_obj in surface_bets.items():
                sb_obj.scroll_to_we()
                surface_bets_names.append(sb_obj.name)
        alive = True
        if surface_bet_name not in surface_bets_names:
            alive = False
        if alive == expected_result:
            return alive, surface_bets_names
        else:
            return self.get_status_of_surface_bet(surface_bet_name=surface_bet_name, time=time + 1,
                                                  expected_result=expected_result)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create a event in OB
        PRECONDITIONS: Surface bet Creation in CMS:
        PRECONDITIONS: 1.Login to Environment specific CMS
        PRECONDITIONS: 2.Navigate to Home Page -->Surface bets
        PRECONDITIONS: 3.Click 'Create Surface bet'
        PRECONDITIONS: 4.Check the checkbox 'Enabled','Display on Highlights tab','Display on EDP' and 'Display in Desktop'
        PRECONDITIONS: 5.Enter All fields like
        PRECONDITIONS: Active Checkbox
        PRECONDITIONS: Title as 'Featured - Ladies Matches '
        PRECONDITIONS: EventIds (Create with EventId)
        PRECONDITIONS: Show on Sports select mutliple sports 'Tennis,Gaming,Fanzone'
        PRECONDITIONS: Show on EventHub
        PRECONDITIONS: Content Header
        PRECONDITIONS: Content
        PRECONDITIONS: Was Price
        PRECONDITIONS: Selection ID
        PRECONDITIONS: Display From
        PRECONDITIONS: Display To
        PRECONDITIONS: SVG Icon
        PRECONDITIONS: SVG Background
        PRECONDITIONS: 6.Check segment as 'Universal' or 'Segment'
        PRECONDITIONS: 7.Click Save Changes
        PRECONDITIONS: Check the Sort Order of Surface bet Module
        PRECONDITIONS: Navigate to Home Page-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
        """
        category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        if tests.settings.backend_env == 'prod':
            event_ids_with_selection_ids = []  # Initialize an empty list to store the event ids and selection ids for creating surface bet
            cms_selection_ids_list = []  # Create an empty list to store selectionId values
            second_third_selection_ids = []  # This is stores selection id for creating surface bet on EDP

            def filtered_event_with_unique_selection_id():
                """
                This method returns the event_id, selection_id of a particular event
                for which the surface bet is not created already
                """
                all_surface_bets_cms = self.cms_config.get_all_surface_bets()
                # Iterate through each data object and extract selectionId values
                for item in all_surface_bets_cms:
                    if 'selectionId' in item:
                        cms_selection_ids_list.append(item["selectionId"])

                def process_event(event):
                    """
                    returns the event id and selection id of a particular event

                    :param event: (dict)
                    the whole event data fetched from Back Office(OB) response
                    """
                    event_id = event['event']['id']

                    outcomes = [market['market']['children'] for market in event['event']['children'] if
                                market['market'].get('children')]

                    event_selections = {i['outcome']['name']: i['outcome']['id'] for sub_outcome in outcomes for i in
                                        sub_outcome}
                    selection_id = list(event_selections.values())[0]
                    if len(second_third_selection_ids) == 0:
                        second_third_selection_ids.append(list(event_selections.values())[1])
                        second_third_selection_ids.append(list(event_selections.values())[2])
                    return event_id, selection_id

                # if a unique selectionId of the active event is found returning it, at maximum look up for only 20 events.
                for _ in range(20):
                    event_id, responce_selection_id = process_event(
                        self.get_active_events_for_category(category_id=category_id, number_of_events=1)[0])
                    if responce_selection_id not in cms_selection_ids_list and responce_selection_id not in event_ids_with_selection_ids:
                        cms_selection_ids_list.append(responce_selection_id)
                        return event_id, responce_selection_id
                else:
                    raise VoltronException(
                        'No events found in football for which the surface bet is not already created')

            while len(event_ids_with_selection_ids) < 3:
                event_id, responce_selection_id = filtered_event_with_unique_selection_id()
                event_ids_with_selection_ids.append(
                    (event_id, responce_selection_id))  # Append the tuple to the event_ids_with_selection_ids

        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = event.selection_ids[event.team1]
            self.__class__.eventID = event.event_id

        self.get_or_create_event_hub()

        surface_bet_modules_cms = None
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(self.index_number)
        for module in sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_modules_cms = module
                break
        if surface_bet_modules_cms is None:
            self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='SURFACE_BET')
        else:
            surface_bet_module_status = [module['disabled'] for module in sports_module_event_hub
                                         if module['moduleType'] == 'SURFACE_BET']
            if surface_bet_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=surface_bet_modules_cms)

        # creation of Surface bets
        created_surface_bets = []
        #  below we are iterating over the elements of the event_ids_with_selection_ids,
        #  and building up the configurations for the creation of surface bet.
        #  ones configurations are built, we are creating surface bets
        i = 1
        for event_id, selection_id in event_ids_with_selection_ids:
            config = {
                "title": f"Autotest C65865536-{i}",
                "selection_id": selection_id,
                "eventIDs": [event_id],
                "highlightsTabOn": True,
                "edp_on": True,
                "svg_icon": "Football",
                "eventHubsIndexes": [self.index_number],
                "displayOnDesktop": True,
                "categoryIDs": [16],
                "on_homepage": True,
                "all_sports": True
            }
            created_surface_bet = self.cms_config.add_surface_bet(**config)
            created_surface_bets.append(created_surface_bet)
            i += 1
            wait_for_haul(3)

        # Set the first_eventID attribute
        self.__class__.first_eventID = event_ids_with_selection_ids[0][0]

        # Create surface bet only on EDP configurations
        # Loop through the configurations to create surface bets only on Desktop
        if self.device_type != 'mobile':
            for selectionID in second_third_selection_ids:
                config = {
                    "title": f"Autotest C65865536-{i}",
                    "selection_id": selectionID,
                    "eventIDs": [self.first_eventID],
                    "edp_on": True,
                    "displayOnDesktop": True,
                    "categoryIDs": [],
                }
                self.cms_config.add_surface_bet(**config)
                i += 1
                wait_for_haul(3)

        # Assign specific surface bet IDs and titles
        self.__class__.sb_cms_configurations = created_surface_bets[0]
        self.__class__.surface_bet_title = self.sb_cms_configurations.get('title').upper()

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        wait_for_haul(time_interval=5)
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_observe_the_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Observe the surface bet created on homepage
        EXPECTED: Surface bet created in CMS should be reflected on homepage
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        if self.device_type == 'mobile':
            # checking whether there are surface bets in home page
            surface_bet_content = self.site.home.tab_content.has_surface_bets(expected_result=True)
            self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on home page")

            # reading the surface bets in home page
            surface_bets_container = self.site.home.tab_content.surface_bets
        else:
            # getting the featured tab in home page
            home_featured_tab = self.site.home.get_module_content(vec.SB.HOME_FEATURED_NAME)
            self.assertTrue(home_featured_tab, msg='No module found on Home Page')

            # checking whether there are surface bets in home page
            surface_bet_content = home_featured_tab.has_surface_bets(expected_result=True)
            self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on home page")

            # reading the surface bets in home page
            surface_bets_container = home_featured_tab.surface_bets
        self.verify_surface_bet(surface_bets_container)
        self.verify_surface_bets_previous_and_next_scroll_buttons(surface_bets_container)

    def test_003_validate_the_surface_bet_is_displayed_in_the_event_hub_selected(self):
        """
        DESCRIPTION: Validate the surface bet is displayed in the event hub selected
        EXPECTED: Surface bet created should reflect in the 'eventhub' selected as per CMS config
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # evnet hub is only for mobile devices validation of the surface bet content
        if self.device_type == 'mobile':
            # getting tabs in home page for mobile
            home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
            self.event_hub_tab_name = next(
                (tab.upper() for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name), None)
            # navigating to the event hub tab which is created
            home_page_tabs.get(self.event_hub_tab_name).click()
            self.assertEqual(self.site.home.tabs_menu.current,
                             self.event_hub_tab_name,
                             f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')
            # checking whether there are surface bets in event hub tab
            has_surface_bet_content = self.site.home.tab_content.has_surface_bets(expected_result=True)
            self.assertTrue(has_surface_bet_content, "Surface Bets Content is not Shown on event hub tab")
            self.verify_surface_bet(surface_bets_container=self.site.home.tab_content.surface_bets)
        else:
            # Verifying Surface bets left and right scroll on EDP, only applicable for desktop
            self.navigate_to_edp(self.first_eventID)
            self.verify_surface_bets_previous_and_next_scroll_buttons(
                surface_bets_container=wait_for_result(lambda: self.site.sport_event_details.tab_content.surface_bets))

    def test_004_validate_the_surface_bet_is_displayed_on_specific_sportstennisgamingfanzone(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on Specific Sports:'Tennis,Gaming,Fanzone'
        EXPECTED: Surface bet created should reflect on specific sports pages as per CMS config
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # navigating to the slp page and then checking that surface bet content is displayed
        self.navigate_to_page('sport/football')
        # checking whether there are surface bets in slp
        surface_bet_content = self.site.football.tab_content.has_surface_bets(expected_result=True)
        self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on foot ball")
        # reading the surface bets in slp
        self.verify_surface_bet(surface_bets_container=self.site.football.tab_content.surface_bets)

    def test_005_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config enddate
        """
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now,
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'  # formatting the now time as CMS time format
        display_from = self.sb_cms_configurations['displayFrom']
        display_to = self.sb_cms_configurations['displayTo']
        status = display_from < now < display_to
        self.assertTrue(status,
                        'Surface Bet is not displayed as per CMS configurations in between start time and end time')

    def test_006_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # covered in above step number 005
        pass

    def test_007_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        # covered in C65866505
        pass

    def test_008_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: Surface bet should disappear in FE
        """
        # covered in C65866505
        pass

    def test_009_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        # covered in C65866505
        pass

    def test_010_verify_surface_bets_display_if_there_are_more_no_of_surfaces_bets_created_in_homepage(self):
        """
        DESCRIPTION: Verify Surface bets display if there are more no of surfaces bets created in homepage
        EXPECTED: Surface bet with Right or Left arrow should display
        """
        if self.device_type != 'mobile':
            self.assertTrue(self.site.football.tab_content.surface_bets.has_scroll_button(),
                            msg="Slider button is not displayed even if there are more than 2 surface bets")

    def test_011_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        self.verify_surface_bets_previous_and_next_scroll_buttons(
            surface_bets_container=self.site.football.tab_content.surface_bets)

    def test_012_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        surface_bet = next((sb_obj for name, sb_obj in surface_bets.items() if
                            name.upper() == self.sb_cms_configurations['title'].upper()), None)
        bet_button = surface_bet.bet_button
        bet_button.click()
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            wait_for_haul(5)
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = wait_for_result(lambda: quick_bet.wait_for_bet_receipt_displayed())
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.bet_receipt.reuse_selection_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.reuse_selection_button.click()
        bet_button.scroll_to()
        self.assertTrue(bet_button.is_enabled(),
                        f'bet button is not selected after clicking on reuse selection')
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_013_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        self.cms_config.update_surface_bet(self.sb_cms_configurations.get('id'),
                                           contentHeader="modified content header")
        # reading the surface bets in slp
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, surface_bets,
                      f'surface bet : "{self.surface_bet_title}" is not found in {surface_bets}')
        # getting the surface bet which is created among the surface bets in slp
        surface_bet_content = surface_bets.get(self.surface_bet_title)
        surface_bet_content.scroll_to()
        wait_for_result(lambda: surface_bet_content.content_header.upper() == "MODIFIED CONTENT HEADER", expected_result=True)
        wait_for_haul(5)
        surface_bet_content_header = wait_for_result(lambda: surface_bet_content.content_header.upper(), timeout=10, expected_result=True)
        self.assertEqual(surface_bet_content_header,
                         "MODIFIED CONTENT HEADER",
                         f'Actual Content Header :"{surface_bet_content_header}" is not same as'
                         f'Expected Content Header : "MODIFIED CONTENT HEADER"')

    def test_014_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        self.cms_config.delete_surface_bet(self.sb_cms_configurations.get('id'))
        self.cms_config._created_surface_bets.remove(self.sb_cms_configurations.get('id'))

        alive, surface_bets_names = self.get_status_of_surface_bet(self.sb_cms_configurations.get('title'),
                                                                   expected_result=False)
        self.assertFalse(alive,
                         msg=f'Surface bet: {self.surface_bet_title} did not disappear in FE upon deletion in CMS')
