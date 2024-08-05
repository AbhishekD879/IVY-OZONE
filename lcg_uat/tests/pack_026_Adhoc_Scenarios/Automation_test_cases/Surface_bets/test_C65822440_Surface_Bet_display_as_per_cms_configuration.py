import pytest
import voltron.environments.constants as vec
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
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.homepage_featured
@vtest
class Test_C65822440_Surface_Bet_display_as_per_cms_configuration(Common):
    """
    TR_ID: C65822440
    NAME: Surface Bet display as per cms configuration
    DESCRIPTION: We are creating the Surface bet in CMS and validating the same in Sportsbook UI.
    PRECONDITIONS: User should have the selection ID for which he is going to create Surface Bet.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Sports pages > Sports category
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            svg_bg_id = None
            if self.brand != 'bma':
                self.__class__.svgBg = None
                sb_bg_img_path = None
            else:
                self.__class__.svgBg = None
                sb_bg_img_path = None
        else:
            event = self.ob_config.add_football_event_to_england_premier_league()
            selection_id = event.selection_ids[event.team1]
            self.__class__.eventID = event.event_id
            svg_bg_id = 'surface-bet-bg-bigc'
            if self.brand != 'bma':
                self.__class__.svgBg = 'background-image: url("https://cms-stg.ladbrokes.com/cms/images/uploads/svg/857e5e8b-9f31-4396-ae7d-5d4dce231b9e.svg");'
                sb_bg_img_path = '/images/uploads/svg/857e5e8b-9f31-4396-ae7d-5d4dce231b9e.svg'
            else:
                self.__class__.svgBg = 'background-image: url("https://cms-stg.coral.co.uk/cms/images/uploads/svg/19db124f-c9a5-46c3-8f38-682a20e5f05b.svg");'
                sb_bg_img_path = '/images/uploads/svg/19db124f-c9a5-46c3-8f38-682a20e5f05b.svg'
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)

        self.cms_config.create_event_hub(index_number=index_number)

        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
        sb_module_cms = None
        for module in sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                sb_module_cms = module
                break
        if sb_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET', page_id=index_number)
        else:
            surface_bet_module_status = next((module['disabled'] for module in sports_module_event_hub
                                             if module['moduleType'] == 'SURFACE_BET'), None)
            if surface_bet_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=sb_module_cms, active=True)

        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0, 16],
                                                      eventIDs=[self.eventID],
                                                      event_hub_id=index_number,
                                                      edp_on=True,
                                                      highlightsTabOn=True,
                                                      svg_icon='football',
                                                      svg_bg_id=svg_bg_id,
                                                      svg_bg_image=sb_bg_img_path,
                                                      displayOnDesktop=True
                                                      )
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.__class__.sb_cms_configurations = surface_bet
        wait_for_haul(20)

    def test_001_launc_the_cms_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launc the CMS and login with valid credentials.
        EXPECTED: CMS should be logged in.
        """
        # covered in preconditions

    def test_002_go_to_main_navigation_ampgt_sports_pages_ampgt_homepage(self):
        """
        DESCRIPTION: Go to Main Navigation &amp;gt; Sports pages &amp;gt; Homepage
        EXPECTED: Surface Bet Module' should present.
        """
        # covered in preconditions

    def test_003_go_to_surface_bet_module(self):
        """
        DESCRIPTION: Go to surface Bet module
        EXPECTED: User should able to see Create Surface Bet, Active and Expired Surface bets.
        """
        # covered in preconditions

    def test_004_to_create_new_surface_bet_click_on_create_surface_bet(self):
        """
        DESCRIPTION: To Create New Surface Bet, Click on 'Create Surface Bet'.
        EXPECTED: User should naviagte New Surface Bet page where user needs to provide the required information to create Surface Bet.
        """
        # covered in preconditions

    def test_005_provide_the_valid_title_name_eg_test(self):
        """
        DESCRIPTION: Provide the valid Title name eg: "Test".
        EXPECTED: The title field should be accesible and "Test" should be updated
        """
        # covered in preconditions

    def test_006_provide_the_event_id_for_which_user_wants_to_create_surface_bet_which_is_taken_from_the_spots_book__eg13218777(
            self):
        """
        DESCRIPTION: Provide the Event id (for which user wants to create surface bet) which is taken from the spots book . Eg:13218777
        EXPECTED: The Event ID field should be accesible and "13218777" should be updated
        """
        # covered in preconditions

    def test_007_select_the_valid_sport_form_the_show_on_sports_dropdown_eg_football(self):
        """
        DESCRIPTION: Select the valid sport form the Show on Sports dropdown. Eg: Football
        EXPECTED: Football should be selected
        """
        # covered in preconditions

    def test_008_select_the_eventhub_from_the_show_on_eventhub_dropdown_eg_us_sports(self):
        """
        DESCRIPTION: Select the EventHub from the Show on EventHub dropdown. Eg: US Sports
        EXPECTED: US sports should be selected
        """
        # covered in preconditions

    def test_009_provide_the_valid_content_header_eg_football_surface_bet(self):
        """
        DESCRIPTION: Provide the valid Content header eg: "Football surface bet"
        EXPECTED: The Content header field should be accesible and "Football surface bet" should be updated
        """
        # covered in preconditions

    def test_010_provide_the_valid_content_eg_this_is_the_a_football_surafce_bet(self):
        """
        DESCRIPTION: Provide the valid Content eg: "This is the a football surafce bet"
        EXPECTED: The Content field should be accesible and "This is the a football surafce bet" should be updated
        """
        # covered in preconditions

    def test_011_provide_the_was_price_say_23(self):
        """
        DESCRIPTION: Provide the Was price say 2/3
        EXPECTED: Was price should be accesible and updated.
        """
        # covered in preconditions

    def test_012_verify_the_display_from_and_display_to_fields(self):
        """
        DESCRIPTION: Verify the Display from and Display To fields.
        EXPECTED: The two dates should be auto populated and set to 24 hrs duartion by default and these should be accessible to user.
        """
        # covered in preconditions

    def test_013_click_on_the_surface_bet_module_and_modify_the_display_to_date_to_some_past_date(self):
        """
        DESCRIPTION: Click on the surface bet module and Modify the 'Display To' date to some past date.
        EXPECTED: As 'Display to' date always future date, User should be blocked with error message upon saving changes .
        """
        # covered in preconditions

    def test_014_go_to_svg_icon_and_start_typing_sport_name(self):
        """
        DESCRIPTION: Go to SVG Icon and start typing sport name
        EXPECTED: Once we type in the sport, overlay shoul display the related SVG icons
        """
        # covered in preconditions

    def test_015_select_the_football_svg_icon_(self):
        """
        DESCRIPTION: Select the football SVG Icon .
        EXPECTED: SVG icon should be selected.
        """
        # covered in preconditions

    def test_016_go_to_svg_background_and_start_typing_sport_name(self):
        """
        DESCRIPTION: Go to SVG Background and start typing sport name
        EXPECTED: Once we type in the sport, overlay shoul display the related SVG backgrounds
        """
        # covered in preconditions

    def test_017_select_the_football_svg_background(self):
        """
        DESCRIPTION: Select the football SVG Background.
        EXPECTED: SVG background should be selected.
        """
        # covered in preconditions

    def test_018_select_the_universal_without_exlusion_of_segments(self):
        """
        DESCRIPTION: Select the Universal without exlusion of segments
        EXPECTED: As user selected universal, the surface should be visible all users.
        """
        # covered in preconditions

    def test_019_select_the_universal_by_providing_the_segment_which_needs_to_be_excluded_for_this_surface_bet_for_example_abcd(
            self):
        """
        DESCRIPTION: Select the universal By providing the segment which needs to be excluded for this surface bet for example 'ABCD'.
        EXPECTED: The surface bet should visible in homepage for all users except 'ABCD' segmented user.
        """
        # covered in preconditions

    def test_020_select_the_segment_inclusion_by_providing_the_segment_for_example_efgh(self):
        """
        DESCRIPTION: Select the Segment inclusion by providing the segment for example 'EFGH'
        EXPECTED: The surface bet should visible in homepage only for 'EFGH' Segmented user.
        """
        # covered in preconditions

    def test_021_verify_the_create_button_without_providing_selection_id(self):
        """
        DESCRIPTION: Verify the create button without providing Selection Id.
        EXPECTED: Create button should be disable.
        """
        # covered in preconditions

    def test_022_go_to_selection_id_field_and_provide_the_valid_selection_id_eg689507038(self):
        """
        DESCRIPTION: Go to Selection Id field and provide the valid Selection Id eg:689507038
        EXPECTED: Id should be added.
        """
        # covered in preconditions

    def test_023_verify_the_the_create_button(self):
        """
        DESCRIPTION: Verify the the create button.
        EXPECTED: Create button should be Enable and accesible.
        """
        # covered in preconditions

    def test_024_before_creating_check_the_enabled_check_box(self):
        """
        DESCRIPTION: Before creating Check the Enabled check box
        EXPECTED: Through this option user should enable the Surface bet.
        """
        # covered in preconditions

    def test_025_check_the_display_on_highlights_tab(self):
        """
        DESCRIPTION: Check the Display on Highlights tab.
        EXPECTED: The surface bet should be visible in Highlights tab.(This is Automatically select by checking on 'Display in desktop').
        """
        # covered in preconditions

    def test_026_check_the_display_on_edp(self):
        """
        DESCRIPTION: Check the Display on EDP.
        EXPECTED: The surface bet should be visible in Events display pages also.
        """
        # covered in preconditions

    def test_027_check_the_display_in_desktop(self):
        """
        DESCRIPTION: Check the Display in Desktop.
        EXPECTED: The surface bet should be visible in desktop mode.
        """
        # covered in preconditions

    def test_028_once_we_provide_all_information_for_surface_bet_creation_and_click_on_create(self):
        """
        DESCRIPTION: Once we provide all information for Surface bet creation and click on create.
        EXPECTED: "Surface Bet  is created" message should display with OK CTA
        """
        # Covered in Preconditions

    def test_029_go_back_to_surface_bet_module_list_and_verify_the_active_surface_bets(self):
        """
        DESCRIPTION: Go Back to Surface Bet Module List and verify the Active Surface bets.
        EXPECTED: Recently created surface Bet should be present in Active Surface bets.
        """
        # covered in preconditions

    def test_030_login_to_sportsbook_application_and_validate_the_surface_bet(self):
        """
        DESCRIPTION: Login to sportsbook application and validate the surface bet.
        EXPECTED: Surface Bet should display as per CMS configuration
        """
        if self.device_type == 'mobile':
            # checking whether there are surface bets in home page
            surface_bet_content = self.site.home.tab_content.has_surface_bets(expected_result=True)
            self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on home page")
            # reading the surface bets in home page
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        else:
            # getting the featured tab home page
            home_featured_tab = self.site.home.get_module_content(vec.SB.HOME_FEATURED_NAME)
            self.assertTrue(home_featured_tab, msg='No module found on Home Page')
            # checking whether there are surface bets in home page
            surface_bet_content = home_featured_tab.has_surface_bets(expected_result=True)
            self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on home page")
            surface_bets = home_featured_tab.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, list(surface_bets.keys()),
                      f'surface bet : "{self.surface_bet_title}" is not found in {list(surface_bets.keys())}')
        # getting the surface bet which is created among the surface bets in home page
        surface_bet_content = surface_bets.get(self.surface_bet_title)
        surface_bet_content.scroll_to()
        self.assertEqual(surface_bet_content.header.icontext,
                         '#football', f'Svg Icon is not same as configured in cms')
        if tests.settings.backend_env != 'prod':
            self.assertEqual(surface_bet_content.get_attribute('style'), self.svgBg,
                             f'svg Background is not same as cms config')
        self.assertEqual(surface_bet_content.header.title.upper(), self.sb_cms_configurations['title'].upper(),
                         f'Actual title : "{surface_bet_content.header.title.upper()}" is not same as '
                         f'Expected title : "{self.sb_cms_configurations["title"].upper()}"')
        self.assertEqual(surface_bet_content.content_header.upper(),
                         self.sb_cms_configurations['contentHeader'].upper(),
                         f'Actual Content Header :"{surface_bet_content.content_header.upper()}" is not same as'
                         f'Expected Content Header : "{self.sb_cms_configurations["contentHeader"].upper()}"')
        self.assertEqual(surface_bet_content.content.strip().upper(),
                         self.sb_cms_configurations['content'].strip().upper(),
                         f'Actual Content : "{surface_bet_content.content.strip().upper()}" is not same as '
                         f'Expected Content : "{self.sb_cms_configurations["content"].strip().upper()}"')

    def test_031_verify_the_sports_page_it_shown_in_sportsbook_ui(self):
        """
        DESCRIPTION: Verify the sports page it shown in sportsbook UI.
        EXPECTED: This should be same as CMS configuration as per test above data it should be in Football.
        """
        # navigiating to the slp page and then checking that surface_bet_content is displayed
        self.navigate_to_page('sport/football')
        # checking whether there are surface bets in slp
        surface_bet_content = self.site.sports_page.tab_content.has_surface_bets(expected_result=True)
        self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on foot ball")
        # reading the surface bets in slp
        surface_bets = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, list(surface_bets.keys()),
                      f'surface bet : "{self.surface_bet_title}" is not found in {list(surface_bets.keys())}')
        # getting the surface bet which is created among the surface bets in slp
        surface_bet_content = surface_bets.get(self.surface_bet_title)
        surface_bet_content.scroll_to()
        self.assertEqual(surface_bet_content.header.icontext,
                         '#football', f'Svg Icon is not same as configured in cms')
        if tests.settings.backend_env != 'prod':
            self.assertEqual(surface_bet_content.get_attribute('style'), self.svgBg,
                             f'svg Background is not same as cms config')
        self.assertEqual(surface_bet_content.header.title.upper(), self.sb_cms_configurations['title'].upper(),
                         f'Actual title : "{surface_bet_content.header.title.upper()}" is not same as '
                         f'Expected title : "{self.sb_cms_configurations["title"].upper()}"')
        self.assertEqual(surface_bet_content.content_header.upper(),
                         self.sb_cms_configurations['contentHeader'].upper(),
                         f'Actual Content Header :"{surface_bet_content.content_header.upper()}" is not same as'
                         f'Expected Content Header : "{self.sb_cms_configurations["contentHeader"].upper()}"')
        self.assertEqual(surface_bet_content.content.strip().upper(),
                         self.sb_cms_configurations['content'].strip().upper(),
                         f'Actual Content : "{surface_bet_content.content.strip().upper()}" is not same as '
                         f'Expected Content : "{self.sb_cms_configurations["content"].strip().upper()}"')

        self.navigate_to_edp(event_id=self.eventID)
        surface_bet_content = self.site.sports_page.tab_content.has_surface_bets(expected_result=True)
        self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on foot ball")
        # reading the surface bets in edp
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, list(surface_bets.keys()),
                      f'surface bet : "{self.surface_bet_title}" is not found in {list(surface_bets.keys())}')
        # getting the surface bet which is created among the surface bets in edp
        surface_bet_content = surface_bets.get(self.surface_bet_title)
        surface_bet_content.scroll_to()
        self.assertEqual(surface_bet_content.header.icontext,
                         '#football', f'Svg Icon is not same as configured in cms')
        if tests.settings.backend_env != 'prod':
            self.assertEqual(surface_bet_content.get_attribute('style'), self.svgBg,
                             f'svg Background is not same as cms config')
        self.assertEqual(surface_bet_content.header.title.upper(), self.sb_cms_configurations['title'].upper(),
                         f'Actual title : "{surface_bet_content.header.title.upper()}" is not same as '
                         f'Expected title : "{self.sb_cms_configurations["title"].upper()}"')
        self.assertEqual(surface_bet_content.content_header.upper(),
                         self.sb_cms_configurations['contentHeader'].upper(),
                         f'Actual Content Header :"{surface_bet_content.content_header.upper()}" is not same as'
                         f'Expected Content Header : "{self.sb_cms_configurations["contentHeader"].upper()}"')
        self.assertEqual(surface_bet_content.content.strip().upper(),
                         self.sb_cms_configurations['content'].strip().upper(),
                         f'Actual Content : "{surface_bet_content.content.strip().upper()}" is not same as '
                         f'Expected Content : "{self.sb_cms_configurations["content"].strip().upper()}"')

    def test_032_verify_the_eventhub_it_shown_in_sportsbook_ui(self):
        """
        DESCRIPTION: Verify the Eventhub it shown in sportsbook UI.
        EXPECTED: This should be same as CMS configuration as per test above data it should be in 'US Sports'
        """
        self.site.back_button.click()
        # evnet hub is only for mobile devices validation of the surface bet content
        if self.device_type == 'mobile':
            self.device.refresh_page()
            # getting tabs in home page for mobile
            home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
            home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
            if self.event_hub_tab_name not in home_page_tab_names:
                wait_for_haul(20)
                self.device.refresh_page()
                home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
                home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
            self.assertIn(self.event_hub_tab_name,
                          home_page_tab_names,
                          f'Surface Bet Event Hub tab:{self.event_hub_tab_name} is not found in '
                          f'Current Home Page tabs : {home_page_tab_names}')
            self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name),None)
            # navigating to the event hub tab which is created
            home_page_tabs.get(self.event_hub_tab_name).click()
            self.assertEqual(self.site.home.tabs_menu.current,
                             self.event_hub_tab_name,
                             f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')
            # checking whether there are surface bets in event hub tab
            has_surface_bet_content = self.site.home.tab_content.has_surface_bets(expected_result=True)
            self.assertTrue(has_surface_bet_content, "Surface Bets Content is not Shown on home page")
            # reading the surface bets in event hub tab
            self.__class__.surface_bets = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict
            self.assertTrue(self.surface_bets, msg='No Surface Bets found')
            self.assertIn(self.surface_bet_title, list(self.surface_bets.keys()),
                          f'surface bet : "{self.surface_bet_title}" is not found in {list(self.surface_bets.keys())}')
            # getting the surface bet which is created among the surface bets in event hub tab
            surface_bet_content = self.surface_bets.get(self.surface_bet_title)
            surface_bet_content.scroll_to()
            self.assertEqual(surface_bet_content.header.icontext,
                             '#football', f'Svg Icon is not same as configured in cms')
            if tests.settings.backend_env != 'prod':
                self.assertEqual(surface_bet_content.get_attribute('style'), self.svgBg,
                                 f'svg Background is not same as cms config')
            self.assertEqual(surface_bet_content.header.title.upper(), self.sb_cms_configurations['title'].upper(),
                             f'Actual title : "{surface_bet_content.header.title.upper()}" is not same as '
                             f'Expected title : "{self.sb_cms_configurations["title"].upper()}"')
            self.assertEqual(surface_bet_content.content_header.upper(),
                             self.sb_cms_configurations['contentHeader'].upper(),
                             f'Actual Content Header :"{surface_bet_content.content_header.upper()}" is not same as'
                             f'Expected Content Header : "{self.sb_cms_configurations["contentHeader"].upper()}"')
            self.assertEqual(surface_bet_content.content.strip().upper(),
                             self.sb_cms_configurations['content'].strip().upper(),
                             f'Actual Content : "{surface_bet_content.content.strip().upper()}" is not same as '
                             f'Expected Content : "{self.sb_cms_configurations["content"].strip().upper()}"')

    def test_033_validate_the_title_content_header__content_was_price_svg_iconsvg_background_(self):
        """
        DESCRIPTION: Validate the Title, Content Header,  Content, Was price, SVG Icon,SVG background .
        EXPECTED: Sportsbook UI data and CMS data should match.
        """
        # Covered in above steps
