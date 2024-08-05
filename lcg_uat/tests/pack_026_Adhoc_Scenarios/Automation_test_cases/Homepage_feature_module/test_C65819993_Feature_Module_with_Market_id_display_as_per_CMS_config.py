import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.adhoc_suite
@pytest.mark.reg165_fix
@pytest.mark.homepage_featured
@vtest
class Test_C65819993_Feature_Module_with_Market_id_display_as_per_CMS_config(Common):
    """
    TR_ID: C65819993
    NAME: Feature Module with Market id  display as per CMS config
    DESCRIPTION: Feature Module with Market id display as per CMS config
    PRECONDITIONS: OB : Create events under any sport
    PRECONDITIONS: Front end : User should be created and events created in OB should be loaded
    PRECONDITIONS: User should have admin access to CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: Feature module tab should be created
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            markets = event['event']['children']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            markets = event.ss_response['event']['children']
        Featured_module = False
        for number in range(len(markets)):
            if markets[number]['market']['name'].title() == 'Match Betting' or markets[number]['market']['name'].title() == "Match Result":
                market_id = markets[number]['market']['id']
                Featured_module = self.cms_config.add_featured_tab_module(select_event_by='Market',
                                                                          id=market_id, title="C65819993",
                                                                          show_all_events=True,
                                                                          events_time_from_hours_delta=-4.5,
                                                                          module_time_from_hours_delta=-10)
                if Featured_module:
                    break
        self.assertTrue(Featured_module, msg=f'Featured module is not created')
        self.__class__.featured_module_events = []
        for i in (range(len(Featured_module['data']))):
            self.featured_module_events.append(Featured_module['data'][i]['name'].upper())
        self.__class__.featured_tab_module_name = Featured_module['title'].upper()

    def test_001_launch_cms_application(self):
        """
        DESCRIPTION: Launch CMS application
        EXPECTED: CMS application should be launched sucessfully
        """
        # Covered in above pre-condition step

    def test_002_login_to_cms_application(self):
        """
        DESCRIPTION: Login to CMS application
        EXPECTED: User should be logged in sucessfully
        """
        # Covered in above pre-condition step

    def test_003_click_on_feature_tab_modules_on_the_left_side_menu(self):
        """
        DESCRIPTION: Click on feature tab modules on the left side menu
        EXPECTED: Feature tab module page should be loaded
        """
        # Covered in above pre-condition step

    def test_004_click_on_create_feature_tab_module(self):
        """
        DESCRIPTION: Click on create feature tab module
        EXPECTED: CMS page with below details should be loaded , with active check box selected by default
        EXPECTED: Fields :
        EXPECTED: Title
        EXPECTED: Max Events to Display
        EXPECTED: Max Selections to Display
        EXPECTED: Expanded by default Etc....
        """
        # Covered in above pre-condition step

    def test_005_choose_title__max_events_to_display_amp__max_selections_to_display(self):
        """
        DESCRIPTION: Choose title , max events to display &amp;  max selections to display
        EXPECTED: User to enter below
        EXPECTED: Title -Type any valid name as title ( Ex : Football FM , Tennis FM )
        EXPECTED: Max events to display - Click on the empty field against it and choose any valid number
        EXPECTED: Max selections to display - Click on the empty field against it and choose any valid number from 1 to 3
        """
        # Covered in above pre-condition step

    def test_006_choose_expanded_by_default_check_box(self):
        """
        DESCRIPTION: Choose "Expanded by default" check box
        EXPECTED: "Expanded by default" should be checked in
        """
        # Covered in above pre-condition step

    def test_007_choose_visible_from_date_as_today(self):
        """
        DESCRIPTION: Choose visible from date as today
        EXPECTED: Choose today date from the calendar and choose timing
        """
        # Covered in above pre-condition step

    def test_008_choose_visible_to_date_as_any_future_date(self):
        """
        DESCRIPTION: Choose visible to date as any future date
        EXPECTED: Choose any future date from the calendar till the module needs to be displayed in front end
        """
        # Covered in above pre-condition step

    def test_009_enable_desktoptablet_and_mobile_under_publish_to_channels(self):
        """
        DESCRIPTION: Enable desktop,tablet and mobile under publish to channels
        EXPECTED: All the checkboxes under Desktop, mobile and tablet needs to be selected
        """
        # Covered in above pre-condition step

    def test_010_under_events_loading_module__choose_select_events_by_as_market_id_from_the_drop_down(self):
        """
        DESCRIPTION: Under events loading module , choose select events by as "Market id from the drop down"
        EXPECTED: Enter market id of the sport
        EXPECTED: Ex : Football event market id -
        EXPECTED: Tennis event market id -
        """
        # Covered in above pre-condition step

    def test_011_click_on_the_calender_icon_against_events_from_option(self):
        """
        DESCRIPTION: Click on the calendar icon against "events from" option
        EXPECTED: Choose the date from which feature module should be displayed from front end, also select the timing against the date ( Events in OB should be present with in this date and time range)
        """
        # Covered in above pre-condition step

    def test_012_click_on_the_calender_icon_against_events_to_(self):
        """
        DESCRIPTION: Click on the calendar icon against "events to "
        EXPECTED: Choose the date till when the feature module should be displayed, also select the timing against the date
        """
        # Covered in above pre-condition step

    def test_013_click_on_reload_option_under_loaded_from_open_bet(self):
        """
        DESCRIPTION: Click on "Reload" option under Loaded from open bet
        EXPECTED: Events under the configured event id should be displayed
        """
        # Covered in above pre-condition step

    def test_014_click_on_apply_under_loaded_from_openbet(self):
        """
        DESCRIPTION: Click on apply under "Loaded from OpenBet"
        EXPECTED: Events should be displayed under "Events in Module"
        EXPECTED: Note : Number of events to be displayed here should be same as the number configured against "Max Events to Display".
        EXPECTED: Also ensure events are there in OB under the said event id and time range
        """
        # Covered in above pre-condition step

    def test_015_validate_universal_should_be_auto_selected(self):
        """
        DESCRIPTION: Validate universal should be auto selected
        EXPECTED: universal should be auto selected
        """
        # Covered in above pre-condition step

    def test_016_click_on_create_module(self):
        """
        DESCRIPTION: Click on create module
        EXPECTED: Feature module with title mentioned should be created
        EXPECTED: Note :  ![](index.php?/attachments/get/2f4315d2-bdb5-4fae-8043-7670f65f429a)
        """
        # Covered in above pre-condition step

    def test_017_launch_front_end_application___lads_or_coral(self):
        """
        DESCRIPTION: Launch Front end application - Lads or coral
        EXPECTED: Feature module should be displayed in front end
        EXPECTED: Example :
        EXPECTED: ![](index.php?/attachments/get/0bc12ca9-fdb1-4652-95a3-53a8b94ed00b)
        """
        self.site.wait_content_state("homepage")
        self.__class__.sections = None
        featured_module = None
        for i in range(5):
            featured_module = self.site.home.get_module_content(
                self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            featured_module.scroll_to()
            self.sections = featured_module.accordions_list.items_as_ordered_dict
            self.sections = [section.upper() for section in self.sections]
            if self.featured_tab_module_name not in self.sections:
                wait_for_haul(5)
                self.device.refresh_page()
                wait_for_haul(5)
            else:
                break
        self.featured_tab_module_name = next(
            (section for section in self.sections if section.upper() == self.featured_tab_module_name), None)
        section = featured_module.accordions_list.items_as_ordered_dict.get(self.featured_tab_module_name)
        self.assertTrue(section, msg=f'Section "{self.featured_tab_module_name}" is not found on FEATURED tab')
        self.assertTrue(section.is_expanded(),
                        msg=f'Section "{self.featured_tab_module_name}" feature module is not expanded')
        actual_featured_module_events = [item_name.upper() for item_name in section.items_names]
        self.assertListEqual(self.featured_module_events, actual_featured_module_events,
                             msg=f'actual featured module events {actual_featured_module_events} '
                                 f'not equals to expected featured module events {self.featured_module_events}')
