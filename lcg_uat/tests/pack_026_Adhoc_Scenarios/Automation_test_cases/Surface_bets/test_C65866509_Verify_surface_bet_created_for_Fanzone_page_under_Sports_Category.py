from datetime import datetime
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tzlocal import get_localzone
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul, wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.surface_bets
@pytest.mark.adhoc_suite
@pytest.mark.reg167_fix
@pytest.mark.timeout(900)
@vtest
class Test_C65866509_Verify_surface_bet_created_for_Fanzone_page_under_Sports_Category(BaseBetSlipTest):
    """
    TR_ID: C65866509
    NAME: Verify surface bet created for Fanzone page under Sports Category
    DESCRIPTION: This test case verifies surface bet is displayed specific to sports

    """
    keep_browser_open = True
    svg_icon = "football"
    timezone = str(get_localzone())
    days = 20
    end_date = f'{get_date_time_as_string(days=days)}T00:00:00.000Z'
    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        surface_bet_module = cms_config.get_sport_module(sport_id=160, module_type='SURFACE_BET')[0]
        cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

    def get_status_of_surface_bet(self, surface_bet_name, time=1, expected_result=True):
        if time > 120:
            return [not expected_result, []]
        wait_for_haul(1)
        if not self.site.fanzone.tab_content.has_surface_bets(expected_result=True):
            surface_bets_names = []
        else:
            surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
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

    def handle_fanzone_popups(self):
        pop_ups = [vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN, vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES]
        for pop_up_name in pop_ups:
            try:
                wait_for_haul(3)
                dialog_alert = self.site.wait_for_dialog(dialog_name=pop_up_name)
                if pop_up_name == vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN and dialog_alert:
                    dialog_alert.remind_me_later.click()
                else:
                    dialog_alert.close_btn.click()
            except:
                continue

    def subscribe_FanZone_Team(self, team_name=vec.fanzone.TEAMS_LIST.aston_villa.title()):
        self.cms_config.update_fanzone(team_name)
        team_fanzone = self.cms_config.get_fanzone(team_name)
        if team_fanzone['fanzoneConfiguration']['showClubs'] is not True:
            raise CmsClientException('showClubs is not enabled')
        self.navigate_to_page(name='sport/football', fanzone=True)
        self.site.wait_content_state(state_name='Football')
        try:
            dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
            dialog_fb.imin_button.click()
        except:
            wait_for_haul(1)
            dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
            dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[team_name].click()
        wait_for_haul(5)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def get_surface_bet_from_fe(self, timeout=None):
        if timeout:
            wait_for_haul(timeout)
        surface_bets = wait_for_result(lambda: self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict)
        self._logger.info(list(surface_bets.keys()))
        self._logger.info(surface_bets.items())
        for name, sb_obj in surface_bets.items():
            sb_obj.scroll_to()
            if sb_obj.name.upper() == self.surface_bet_response['title'].upper():
                return sb_obj
        return None

    def get_status_of_surface_bet_module(self, time=1, expected_result=True):
        wait_for_haul(1)
        if time > 120:
            return not expected_result
        result = self.site.fanzone.tab_content.has_surface_bets()
        if (result is not None and expected_result == True) or (result is None and expected_result == False):
            return expected_result
        else:
            return self.get_status_of_surface_bet_module(time=time + 1, expected_result=expected_result)

    def wait_up_to_time_complete(self, end_time):
        now = get_date_time_as_string(date_time_obj=datetime.now(),
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'
        time_formate = '%Y-%m-%dT%H:%M:%S.%fZ'
        end_time = datetime.strptime(end_time, time_formate)
        now_time = datetime.strptime(now, time_formate)
        time_difference_in_sec = (end_time - now_time).total_seconds()
        wait_for_haul(time_difference_in_sec)

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Surface bet Creation in CMS:
        PRECONDITIONS: 1.Login to Environment specific CMS
        PRECONDITIONS: 2.Click Sports from side navigation and select 'Fanzone' option from sports category
        PRECONDITIONS: 3.Click 'Surface Bet Module' and click 'Create Surface bet'
        PRECONDITIONS: 4.Check the checkbox 'Enabled', 'Display on Highlights tab', 'Display on EDP' and 'Display in Desktop'
        PRECONDITIONS: 5.Enter All fields like
        PRECONDITIONS: Active Checkbox
        PRECONDITIONS: Title
        PRECONDITIONS: EventIds (Create with EventId)
        PRECONDITIONS: Show on Sports select 'All Sports'
        PRECONDITIONS: Show on EventHub
        PRECONDITIONS: Content Header
        PRECONDITIONS: Content
        PRECONDITIONS: Was Price
        PRECONDITIONS: Selection ID
        PRECONDITIONS: Display From
        PRECONDITIONS: Display To
        PRECONDITIONS: SVG Icon
        PRECONDITIONS: SVG Background
        PRECONDITIONS: 6.Check segment as 'Universal'
        PRECONDITIONS: 7.Click Save Changes
        PRECONDITIONS: Check the Sort Order of Surface bet Module
        PRECONDITIONS: Navigate to Sports-->All Sports-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id, end_date=self.end_date,all_available_events=True)
            event = next((event for event in events if (event['event'].get("typeId") == "442" and vec.fanzone.TEAMS_LIST.aston_villa.upper() in event['event'].get('name').upper())),None)
            if not event:
                # If no event is found after all iterations, raise an exception
                raise SiteServeException(
                    f'There are no events for {vec.fanzone.TEAMS_LIST.aston_villa} in the next {self.days} days')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selections = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_name = next((event_selection for event_selection in event_selections.keys() if event_selection.upper() == vec.fanzone.TEAMS_LIST.aston_villa.upper()), None)
            selection_id = event_selections.get(selection_name)
            if len(list(event_selections.values())):
                dummy = next((event_selection for event_selection in event_selections.keys() if event_selection.upper() != vec.fanzone.TEAMS_LIST.aston_villa.upper()), None)
                selection_id_for_dummy = event_selections.get(dummy)
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            selection_id_for_dummy = event.selection_ids[event.team2]

        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        surface_bet_module = self.cms_config.get_sport_module(sport_id=160, module_type='SURFACE_BET')[0]
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

        self.__class__.surface_bet_response = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                                      svg_icon=self.svg_icon,
                                                                                      svg_bg_id=None,
                                                                                      svg_bg_image=None, fanzone_teams=[vec.fanzone.TEAMS_LIST.aston_villa])

        self.cms_config.add_fanzone_surface_bet(selection_id=selection_id_for_dummy,
                                                svg_icon=self.svg_icon,
                                                svg_bg_id=None,
                                                svg_bg_image=None,
                                                contentHeader='Dummy Surface Bet', fanzone_teams=[vec.fanzone.TEAMS_LIST.aston_villa])

    def test_001_login_to_ladscoral_ampltenvironmentampgt_with_fanzone_subscribed_user(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt; with Fanzone subscribed user
        EXPECTED: User should be logged in
        """
        username = tests.settings.fanzone_aston_villa_users
        self.site.login(username=username)

    def test_002_validate_the_surface_bet_title(self, manually_subscribed=False):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        if self.device_type == 'mobile':
            all_sub_header_tabs = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            all_sub_header_tabs = self.site.header.sport_menu.items_as_ordered_dict
        fanzone_tab = next((tab for tab_name, tab in all_sub_header_tabs.items() if tab_name.upper() == 'FANZONE'),
                           None)
        if not fanzone_tab:
            if manually_subscribed:
                self.assertIsNotNone(fanzone_tab, f'fanzone tab is not available after enable')
            else:
                self.subscribe_FanZone_Team()
                self.test_002_validate_the_surface_bet_title(manually_subscribed=True)
        else:
            fanzone_tab.click()
            self.handle_fanzone_popups()

    def test_003_validate_the_surface_bet_is_displayed_on_fanzone_page(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on 'Fanzone' page
        EXPECTED: Surface bet created should reflect only on Fanzone page as per CMS config
        """
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self._logger.info(list(surface_bets.keys()))
        surface_bets_names = [name.upper() for name in list(surface_bets.keys())]
        self.assertIn(self.surface_bet_response['title'].upper(), surface_bets_names,
                      f'{self.surface_bet_response["title"]} is not in {surface_bets_names}')

    def test_004_validate_the_surface_bet_content_header_and_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header' and Validate the SVG icon and SVG background
        EXPECTED: Content Header' should be displayed as per CMS config
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """

        surface_bet = self.get_surface_bet_from_fe()

        surface_bet.scroll_to()

        self.assertEqual(surface_bet.content_header.upper(), self.surface_bet_response['contentHeader'].upper(),
                         f"actual content header : -{surface_bet.content_header.upper()}- is not same as "
                         f"expected content header : -{self.surface_bet_response['contentHeader'].upper()}-")

        self.assertEqual(surface_bet.header.icontext, f'#{self.svg_icon}',
                         f"actual svg icon : -{surface_bet.header.icontext}- is not same as"
                         f"expected svg icon : -#{self.svg_icon}-")

        self._logger.info(f'surface_bet.content.upper() : {surface_bet.content.upper()}')
        actual_content = surface_bet.content.upper()
        self.assertEqual(actual_content, self.surface_bet_response['content'].upper(),
                         f'actual content : \n'
                         f'-{actual_content}-\n'
                         f'is not as expected content:'
                         f'-{self.surface_bet_response["content"].upper()}-')

    def test_005_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        # covered in above step

    def test_006_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now,
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'  # formatting the now time as CMS time format
        display_from = self.surface_bet_response['displayFrom']
        display_to = self.surface_bet_response['displayTo']
        status = display_from < now < display_to
        self.assertTrue(status, f'Surface Bet is not displayed as per CMS configurations(in between start '
                                f'time and end time)')

    def test_007_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-22)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=-20)[:-3] + 'Z'
        # display from : past
        # display to : past
        self.cms_config.update_surface_bet(self.surface_bet_response['id'], displayFrom=start_time,
                                           displayTo=end_time)
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=False)

        self.assertFalse(alive,
                         f'{self.surface_bet_response["title"]} still in Front end surface bets {surface_bets_names}')

        # display to : future
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, days=3)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_response['id'],
                                           displayTo=end_time)
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=True)
        self.assertTrue(alive,
                        f'{self.surface_bet_response["title"]} not in Front end surface bets {surface_bets_names}')

        # display from : future
        start_time = get_date_time_as_string(date_time_obj=datetime.now(),
                                             time_format=self.time_format,
                                             url_encode=False, days=2)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_response['id'], displayFrom=start_time)
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=False)

        self.assertFalse(alive,
                         f'{self.surface_bet_response["title"]} still in Front end surface bets {surface_bets_names}')

    def test_008_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current
                     time.
        EXPECTED: Surface bet should disappear in FE
        """
        # display from : past
        # display to : 1 min from now
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-20)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, minutes=1.5)[:-3] + 'Z'

        if self.timezone.upper() == "UTC":
            end_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                       url_encode=False, minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            end_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                      url_encode=False, minutes=-59)[:-3] + 'Z'
        else:
            end_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                       url_encode=False, hours=-5.5, minutes=1)[:-3] + 'Z'

        self._logger.info(f'end_time_for_cms before update : {end_time_for_cms}')
        self.cms_config.update_surface_bet(self.surface_bet_response['id'], displayFrom=start_time,
                                           displayTo=end_time_for_cms)
        self._logger.info(
            f"after update : {self.cms_config.get_surface_bet(self.surface_bet_response['id'])['displayTo']}")
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=True)

        self.assertTrue(alive,
                        f'{self.surface_bet_response["title"]} not in Front end surface bets {surface_bets_names}')

        self.wait_up_to_time_complete(end_time)

        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=False)
        self.assertFalse(alive,
                         f'{self.surface_bet_response["title"]} is not disappeared in frontend , '
                         f'frontend surface bets : {surface_bets_names}')

    def test_009_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the
                     future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        # display from : 1 min from now
        # display to : future
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, minutes=1.5)[:-3] + 'Z'
        if self.timezone.upper() == "UTC":
            start_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                     url_encode=False, minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            start_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                    url_encode=False, minutes=-59)[:-3] + 'Z'
        else:
            start_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                     url_encode=False,hours=-5.5, minutes=1)[:-3] + 'Z'

        self._logger.info(f'start time : {start_time_cms}')
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=22)[:-3] + 'Z'

        self.cms_config.update_surface_bet(self.surface_bet_response['id'], displayFrom=start_time_cms,
                                           displayTo=end_time)

        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=False)
        self.assertFalse(alive,
                         f'{self.surface_bet_response["title"]} is not disappeared in frontend , '
                         f'frontend surface bets : {surface_bets_names}')

        self.wait_up_to_time_complete(start_time)

        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=True)
        self.assertTrue(alive,
                        f'{self.surface_bet_response["title"]} not in Front end surface bets {surface_bets_names}')

    def test_010_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted and place bet on the selection.
        """
        surface_bet = self.get_surface_bet_from_fe()
        surface_bet.scroll_to_we()
        bet_button = surface_bet.bet_button
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

    def test_011_click_on_reuse_selection_in_bet_recipte(self):
        """
        DESCRIPTION: click on reuse selection in bet recipte
        EXPECTED: Same selection which is in surface bet should be added to the bet slip and user should be
        able to place bet
        """
        # covered in above step

    def test_012_activatedeactivate_the_whole_surface_bet_module_on_homepage(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on homepage
        EXPECTED: Surface bet should display on Home page if it is activated
        EXPECTED: Surface bet should not display on Home page if it is deactivated
        """
        surface_bet_module = next(iter(self.cms_config.get_sport_module(sport_id=160, module_type='SURFACE_BET')))
        # deactivating whole surface bet module for fanzone
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=False)

        surface_bet_visible_status = self.get_status_of_surface_bet_module(expected_result=False)
        self.assertFalse(surface_bet_visible_status, f'surface bet module still visible even though surface bet '
                                                     f'module deactivated')

        surface_bet_module = next(iter(self.cms_config.get_sport_module(sport_id=160, module_type='SURFACE_BET')))
        # activating whole surface bet module for fanzone
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

        surface_bet_visible_status = self.get_status_of_surface_bet_module(expected_result=True)
        self.assertTrue(surface_bet_visible_status, f'surface bet module is not visible even though surface bet '
                                                    f'module activated')

    def test_013_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        self.svg_icon = 'footballnew'
        self.cms_config.update_surface_bet(self.surface_bet_response['id'], svgId=self.svg_icon)
        surface_bet = self.get_surface_bet_from_fe(timeout=2)
        for i in range(20):
            if surface_bet.header.icontext == f'#{self.svg_icon}':
                break
            surface_bet = self.get_surface_bet_from_fe(timeout=2)
            surface_bet.scroll_to_we()
        self.assertEqual(surface_bet.header.icontext, f'#{self.svg_icon}',
                         f"actual svg icon : -{surface_bet.header.icontext}- is not same as"
                         f"expected svg icon : -#{self.svg_icon}-")

    def test_014_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        self.cms_config.delete_surface_bet(self.surface_bet_response.get('id'))
        self.cms_config._created_surface_bets.remove(self.surface_bet_response.get('id'))

        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_response['title'].upper(),
                                                                   expected_result=False)
        self.assertFalse(alive,
                         f'{self.surface_bet_response["title"]} is not disappeared in frontend after deletion , '
                         f'frontend surface bets : {surface_bets_names}')