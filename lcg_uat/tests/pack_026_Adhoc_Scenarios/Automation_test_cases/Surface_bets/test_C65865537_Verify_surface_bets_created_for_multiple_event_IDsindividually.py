import random
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.surface_bets
@pytest.mark.adhoc_suite
@pytest.mark.homepage_featured
@pytest.mark.last
@vtest
@pytest.mark.timeout(900)
class Test_C65865537_Verify_surface_bets_created_for_multiple_event_IDsindividually(BaseBetSlipTest):
    """
    TR_ID: C65865537
    NAME: Verify surface bets created for multiple event ID's(individually)
    DESCRIPTION: Verify surface bet is displayed for different event hubs
    PRECONDITIONS: Create a event in OB
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Navigate to Home Page -->Surface bets
    PRECONDITIONS: 3.Click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled','Display on Highlights tab','Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title as 'Featured - Ladies Matches '
    PRECONDITIONS: EventIds (Create multiple surface bets with respective EventId's)
    PRECONDITIONS: Show on Sports select 'All Sports'
    PRECONDITIONS: Show on EventHub select any event hub
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
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        surface_bet_module = cms_config.get_sport_module(sport_id=0, module_type='SURFACE_BET')[0]
        cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

    def get_status_of_surface_bet_module(self, time=1, expected_result=True):
        if time > 180:
            return not expected_result
        wait_for_haul(1)
        if self.device_type == 'mobile':
            status = self.site.home.tab_content.has_surface_bets()
        else:
            try:
                status = self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(
                    self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).has_surface_bets(
                    expected_result=True)
            except VoltronException:
                status = None
        if (status is not None and expected_result == True) or (status is None and expected_result == False):
            return expected_result
        else:
            return self.get_status_of_surface_bet_module(time=time + 1, expected_result=expected_result)

    def get_status_of_surface_bet(self, surface_bet_name, time=1, expected_result=True):
        if time > 120:
            return [not expected_result, []]
        wait_for_haul(1)
        if self.device_type == 'mobile':
            if not self.site.home.tab_content.has_surface_bets(expected_result=True):
                surface_bets_names = []
            else:
                surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                surface_bets_names = []
                for name, sb_obj in surface_bets.items():
                    sb_obj.scroll_to_we()
                    surface_bets_names.append(sb_obj.name)
        else:
            if not self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(
                    self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).has_surface_bets(
                    expected_result=True):
                surface_bets_names = []
            else:
                surface_bets = self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(
                    self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).surface_bets.items_as_ordered_dict
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
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Home Page > Surface bets
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            self.__class__.eventID_1 = events[-1]['event']['id']
            self.__class__.eventID_2 = events[-2]['event']['id']
            outcomes1 = next(((market['market']['children']) for market in events[-1]['event']['children'] if
                              market['market'].get('children')), None)
            event_selection1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes1}

            outcomes2 = next(((market['market']['children']) for market in events[-2]['event']['children'] if
                              market['market'].get('children')), None)
            event_selection2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2}
            self.__class__.selection_id_1 = list(event_selection1.values())[0]
            self.__class__.selection_id_2 = list(event_selection2.values())[0]
            self.__class__.selection_id_3 = list(event_selection2.values())[1]
            svg_bg_id = 'surface-bet-bg-bigc'
        else:
            event1 = self.ob_config.add_football_event_to_england_premier_league()
            self.__class__.selection_id_1 = event1.selection_ids[event1.team1]
            self.__class__.eventID_1 = event1.event_id
            event2 = self.ob_config.add_football_event_to_england_premier_league()
            self.__class__.selection_id_2 = event2.selection_ids[event2.team1]
            self.__class__.eventID_2 = event2.event_id
            self.__class__.selection_id_3 = event2.selection_ids[event2.team2]
            svg_bg_id = 'surface-bet-bg-bigc'
        self.__class__.surface_bet_1 = self.cms_config.add_surface_bet(selection_id=self.selection_id_1,
                                                                       categoryIDs=[0, 16],
                                                                       eventIDs=self.eventID_1,
                                                                       highlightsTabOn=True,
                                                                       svg_icon='football',
                                                                       svg_bg_id=svg_bg_id,
                                                                       displayOnDesktop=True)
        surface_bet_title_1 = self.surface_bet_1.get('title').upper()
        self.__class__.surface_bet_2 = self.cms_config.add_surface_bet(selection_id=self.selection_id_2,
                                                                       categoryIDs=[0, 16],
                                                                       eventIDs=self.eventID_2,
                                                                       highlightsTabOn=True,
                                                                       svg_icon='football',
                                                                       svg_bg_id=svg_bg_id,
                                                                       displayOnDesktop=True)
        surface_bet_title_2 = self.surface_bet_2.get('title').upper()
        self.cms_config.add_surface_bet(selection_id=self.selection_id_3,
                                        title=f"Dummy SB{random.randint(1, 100000)}",
                                        categoryIDs=[0, 16],
                                        eventIDs=[self.eventID_2],
                                        highlightsTabOn=True,
                                        svg_icon='football',
                                        displayOnDesktop=True)
        self.__class__.sb_cms_configurations = [self.surface_bet_1, self.surface_bet_2]
        self.__class__.created_surface_bet_titles = [surface_bet_title_1, surface_bet_title_2]

    def test_001_login_to_ladscoral_ltenvironmentgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &lt;Environment&gt;
        EXPECTED: User should be logged in
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_observe_the_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Observe the surface bet created on homepage
        EXPECTED: Surface bet created in CMS should be reflected on homepage
        """

        self.device.refresh_page()
        if self.device_type == 'mobile':
            fe_surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        else:
            fe_surface_bets = self.site.home.get_module_content \
                (module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)). \
                surface_bets.items_as_ordered_dict

        fe_surface_bets_names = list(fe_surface_bets.keys())
        for sb in self.created_surface_bet_titles:
            self.assertIn(sb, fe_surface_bets_names, f'surface bet {sb} not in {fe_surface_bets_names}')

    def test_003_validate_the_order_of_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Validate the Order of surface bet created on homepage
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        # Covered in another test case
        pass

    def test_004_change_the_order_of_surface_bet_created(self):
        """
        DESCRIPTION: Change the Order of surface bet created
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        # Covered in another test case
        pass

    def test_005_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        # Covered in test_002_observe_the_surface_bet_created_on_homepage
        pass

    def test_006_validate_multiple_surface_bets_for_different_events(self):
        """
        DESCRIPTION: Validate multiple surface bets for different events
        EXPECTED: Multiple Surface bets created should reflect on as per CMS config
        """
        # Covered in test_002_observe_the_surface_bet_created_on_homepage
        pass

    def test_007_validate_multiple_surface_bets_for_different_events_specific_to_few_sports(self):
        """
        DESCRIPTION: Validate multiple surface bets for different events specific to few sports
        EXPECTED: Multiple Surface bets created should reflect on specific sports as per CMS config
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        for sb_title in self.created_surface_bet_titles:
            surface_bet = self.site.football.tab_content.surface_bets.items_as_ordered_dict.get(sb_title)
            surface_bet.scroll_to_we()
            self.assertTrue(surface_bet, f'Surface bet "{sb_title}" not found on FE')

            sb_config = next((config for config in self.sb_cms_configurations if config['title'].upper() == sb_title),
                             None)
            self.assertIsNotNone(sb_config, f'Configuration not found for surface bet "{sb_title}"')

            expected_title = sb_config['title']
            self.assertEqual(surface_bet.header.title.upper(), expected_title.upper(),
                             f'Expected title: "{expected_title}", Actual title: "{surface_bet.header.title}"')

            expected_content_header = sb_config['contentHeader']
            self.assertEqual(surface_bet.content_header.upper(), expected_content_header.upper(),
                             f'Expected content header: "{expected_content_header}", '
                             f'Actual content header: "{surface_bet.content_header}"')

            expected_content = sb_config['content'].strip()
            self.assertEqual(surface_bet.content.strip().upper(), expected_content.upper(),
                             f'Expected content: "{expected_content}", Actual content: "{surface_bet.content.strip()}"')

            expected_svg_icon = sb_config['svgId']
            self.assertEqual(surface_bet.header.icontext, f'#{expected_svg_icon}',
                             f'Expected SVG icon: "{expected_svg_icon}", '
                             f'Actual SVG icon: "{surface_bet.header.icontext}"')

            if tests.settings.backend_env != 'prod':
                self.assertEqual(surface_bet.get_attribute('style'), self.svgBg,
                                 f'svg Background is not same as cms config')

    def test_008_validate_the_surface_bet_content_header(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        """
        #  covered in test_007_validate_multiple_surface_bets_for_different_events_specific_to_few_sports
        pass

    def test_009_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        # test_007_validate_multiple_surface_bets_for_different_events_specific_to_few_sports
        pass

    def test_010_validate_the_surface_bet_was_price(self):
        """
        DESCRIPTION: Validate the surface bet 'Was Price'
        EXPECTED: Was Price' should be displayed as per config in the OB
        """
        # Covered in pre_conditions
        pass

    def test_011_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config enddate
        """
        # covered in test_013_verify_surface_bet_display_from_and_display_to_date_has_set_to_past_future_in_cms
        pass

    def test_012_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # test_007_validate_multiple_surface_bets_for_different_events_specific_to_few_sports
        pass

    def test_013_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        # covered in test case : C65865505
        pass

    def test_014_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: Surface bet should disappear in FE
        """
        # Covered in test case : C65865505
        pass

    def test_015_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        # Covered in test case : C65865505
        pass

    def test_016_verify_surface_bets_display_if_there_are_more_no_of_surfaces_bets_created_in_homepage(self):
        """
        DESCRIPTION: Verify Surface bets display if there are more no of surfaces bets created in homepage
        EXPECTED: Surface bet with Right or Left arrow should display
        """
        # Covered in test case : C65865536
        pass

    def test_017_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should be able to scroll from left to right &amp; from right to left
        """
        # Covered in test case : C65865536
        pass

    def test_018_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        sb = self.site.football.tab_content.surface_bets.items_as_ordered_dict.get(self.created_surface_bet_titles[0])
        sb.scroll_to_we()
        bet_button = sb.bet_button
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), f'unable to select bet button')

        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.bet_receipt.reuse_selection_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.reuse_selection_button.click()
        bet_button.scroll_to_we()
        self.assertTrue(bet_button.is_selected(), f'bet button is not selected after clicking on reuse selection')
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_019_activatedeactivate_the_whole_surface_bet_module_on_homepage(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on homepage
        EXPECTED: Surface bet should display on Home page if it is activated
        EXPECTED: Surface bet should not display on Home page if it is deactivated
        """

        self.navigate_to_page(name='/')
        self.site.wait_content_state('HomePage')
        surface_bet_module = self.cms_config.get_sport_module(sport_id=0, module_type='SURFACE_BET')[0]
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=False)

        surface_bet_visible_status = self.get_status_of_surface_bet_module(expected_result=False)
        self.assertFalse(surface_bet_visible_status, f'surface bet module still visible even though surface bet '
                                                     f'module deactivated')

        surface_bet_module = self.cms_config.get_sport_module(sport_id=0, module_type='SURFACE_BET')[0]
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

        surface_bet_visible_status = self.get_status_of_surface_bet_module(expected_result=True)
        self.assertTrue(surface_bet_visible_status, f'surface bet module is not visible even though surface bet '
                                                    f'module activated')

    def test_020_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        # deleting in test_021_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet
        pass

    def test_021_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        # validating for only one surface bet
        surface_bet_data = self.cms_config.update_surface_bet(self.sb_cms_configurations[0].get('id'),
                                           contentHeader="modified content header")
        wait_for_haul(5)
        # reading the surface bets in homepage
        if self.device_type == 'mobile':
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        else:
            surface_bets = self.site.home.get_module_content \
                (module_name=self.get_ribbon_tab_name(
                    self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)).surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertIn(self.created_surface_bet_titles[0], surface_bets,
                      f'surface bet : "{self.created_surface_bet_titles[0]}" is not found in {surface_bets}')
        # getting the surface bet which is created among the surface bets in homepage
        surface_bet_content = surface_bets.get(self.created_surface_bet_titles[0])
        surface_bet_content.scroll_to()
        surface_bet_content_header = wait_for_result(lambda: surface_bet_content.content_header.upper(), timeout=10,
                                                     expected_result=True)
        for i in range(5):
            if surface_bet_content.content_header.upper() == surface_bet_data['contentHeader'].upper():
                break
            else:
                self.device.refresh_page()
                wait_for_haul(5)
        self.assertEqual(surface_bet_content_header,
                         surface_bet_data['contentHeader'].upper(),
                         f'Actual Content Header :"{surface_bet_content_header}" is not same as'
                         f'Expected Content Header : "{surface_bet_data["contentHeader"].upper()}"')
        # Deleting surface bet in cms and verifying in front end
        self.cms_config.delete_surface_bet(self.surface_bet_1.get('id'))
        self.cms_config._created_surface_bets.remove(self.surface_bet_1.get('id'))
        result, fe_surface_bets = self.get_status_of_surface_bet(surface_bet_name=self.created_surface_bet_titles[0],
                                                                 expected_result=False)
        self.assertFalse(result, f'{self.created_surface_bet_titles[0]} is not disappeared in frontend after deletion')
