import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Involves creation of horse event not valid for prod
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.medium
@pytest.mark.races_negative_p3  # Marker for testcases having long/short/extralong market description
@vtest
class Test_C60094949_Verify_the_display_of_short_long_extra_long_description(BaseRacing):
    """
    TR_ID: C60094949
    NAME: Verify the display of short/long/extra long description
    DESCRIPTION: Verify the description text displayed under the Market header when the description texts are short,long and Extra long
    PRECONDITIONS: 1.  Horse racing & Grey Hound racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Horse racing/ Greyhounds market description table should be enabled in CMS
    """
    keep_browser_open = True
    markets = [('antepost',),
               ('betting_without',),
               ('win_only',)]
    short_desc = 'Antepost'
    long_desc = 'Created long description for betting_without market for automation testing purpose'
    extra_long_desc = 'Created extra long description for win_only market for automation testing purpose' \
                      'Created extra long description for win_only market for automation testing purpose'

    @classmethod
    def custom_tearDown(cls):

        if tests.settings.cms_env != 'prd0':
            cls.get_cms_config().create_and_update_markets_with_description(name='Antepost',
                                                                            description=cls.desc1)
            cls.get_cms_config().create_and_update_markets_with_description(name='Win Only', description=cls.desc2)
            cls.get_cms_config().create_and_update_markets_with_description(name='Betting Without',
                                                                            description=cls.desc3)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events
        EXPECTED: Racing events is created
        """
        event_params = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=1)
        self.__class__.event_id = event_params.event_id
        greyhound_event_params = self.ob_config.add_UK_greyhound_racing_event(markets=self.markets, number_of_runners=1)
        self.__class__.greyhound_event_id = greyhound_event_params.event_id

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        if self.get_initial_data_system_configuration().get('RacingEDPMarketsDescription', {}).get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)

    def test_002_navigate_to_racing_edp_template_and_edit_the_market_description_table1_add_short_description_to_one_of_the_market_template2_add_long_description_to_another_market_template3_add_extra_long_description_to_another_market_template(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and edit the Market description table
        DESCRIPTION: 1: Add Short Description to one of the market template
        DESCRIPTION: 2: Add Long Description to another market template
        DESCRIPTION: 3: Add Extra Long description to another market template
        EXPECTED: User should be able to Edit and save the changes successfully
        """
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        for item in racing_edp_market_list:
            if item.get('name') == 'Antepost':
                self.__class__.desc1 = item.get('description')
            elif item.get('name') == 'Win Only':
                self.__class__.desc2 = item.get('description')
            elif item.get('name') == 'Betting Without':
                self.__class__.desc3 = item.get('description')
        self.cms_config.create_and_update_markets_with_description(name='Antepost', description=self.short_desc,
                                                                   HR=True, GH=True)
        self.cms_config.create_and_update_markets_with_description(name='Win Only', description=self.extra_long_desc,
                                                                   HR=True, GH=True)
        if self.brand == 'bma':
            self.cms_config.create_and_update_markets_with_description(name='Betting W/O', description=self.long_desc,
                                                                       HR=True, GH=True)
        else:
            self.cms_config.create_and_update_markets_with_description(name='Betting Without', description=self.long_desc,
                                                                       HR=True, GH=True)

    def test_003_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(vec.sb.HORSERACING.upper(), sports.keys(),
                          msg=f'"{vec.sb.HORSERACING.upper()}" is not found in the header sport menu')
            sports.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_005_click_on_any_race_which_has_the_market_templates_available_for_which_description_are_added_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description are added in CMS
        EXPECTED: User should be navigated to EDP page
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_006_validate_the_description_below_the_market_tab_for_short_long_and_extra_long_textsindexphpattachmentsget120830388indexphpattachmentsget120830389indexphpattachmentsget120830390indexphpattachmentsget120830391indexphpattachmentsget120830392(self):
        """
        DESCRIPTION: Validate the description below the Market tab for Short, Long and Extra Long texts
        DESCRIPTION: ![](index.php?/attachments/get/120830388)
        DESCRIPTION: ![](index.php?/attachments/get/120830389)
        DESCRIPTION: ![](index.php?/attachments/get/120830390)
        DESCRIPTION: ![](index.php?/attachments/get/120830391)
        DESCRIPTION: ![](index.php?/attachments/get/120830392)
        EXPECTED: User should be displayed description as per the Zeplin styles
        """
        if self.brand == 'ladbrokes':
            tab_names = [vec.racing.RACING_EDP_MARKET_TABS.antepost, vec.racing.RACING_EDP_BETTING_WITHOUT,
                         vec.racing.RACING_EDP_MARKET_TABS.win_only]
        else:
            tab_names = [vec.racing.RACING_EDP_MARKET_TABS.antepost, vec.racing.RACING_EDP_MARKET_TABS.betting_wo,
                         vec.racing.RACING_EDP_MARKET_TABS.win_only]
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='Market tabs not found')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(tab_names[0])
        market_description = self.site.racing_event_details.market_description
        self.assertEqual(self.short_desc, market_description, msg=f'Actual description: "{self.short_desc}" is not same as'
                                                                  f' Expected description: "{market_description}"')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(tab_names[1])
        market_description = self.site.racing_event_details.market_description
        self.assertEqual(self.long_desc, market_description,
                         msg=f'Actual description: "{self.long_desc}" is not same as'
                             f' Expected description: "{market_description}"')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(tab_names[2])
        market_description = self.site.racing_event_details.market_description
        self.assertEqual(self.extra_long_desc, market_description,
                         msg=f'Actual description: "{self.extra_long_desc}" is not same as'
                             f' Expected description: "{market_description}"')

    def test_007_repeat_the_same_for_grey_hound_racing(self):
        """
        DESCRIPTION: Repeat the same for Grey Hound racing
        """
        self.navigate_to_edp(event_id=self.greyhound_event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        if self.brand == 'ladbrokes':
            tab_names = [vec.racing.RACING_EDP_MARKET_TABS.antepost, vec.racing.RACING_EDP_BETTING_WITHOUT,
                         vec.racing.RACING_EDP_MARKET_TABS.win_only]
        else:
            tab_names = [vec.racing.RACING_EDP_MARKET_TABS.antepost, vec.racing.RACING_EDP_MARKET_TABS.betting_wo,
                         vec.racing.RACING_EDP_MARKET_TABS.win_only]
        market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='Market tabs not found')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(tab_names[0])
        market_description = self.site.greyhound_event_details.market_description
        self.assertEqual(self.short_desc, market_description,
                         msg=f'Actual description: "{self.short_desc}" is not same as'
                             f' Expected description: "{market_description}"')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(tab_names[1])
        market_description = self.site.greyhound_event_details.market_description
        self.assertEqual(self.long_desc, market_description,
                         msg=f'Actual description: "{self.long_desc}" is not same as'
                             f' Expected description: "{market_description}"')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(tab_names[2])
        market_description = self.site.greyhound_event_details.market_description
        self.assertEqual(self.extra_long_desc, market_description,
                         msg=f'Actual description: "{self.extra_long_desc}" is not same as'
                             f' Expected description: "{market_description}"')
