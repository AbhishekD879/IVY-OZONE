import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.rugby_union_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65969023_Verify_Rugby_Union_sport_landing_page_display_as_per_CMS_configuration(Common):
    """
    TR_ID: C65969023
    NAME: Verify Rugby Union  sport landing page display as per CMS configuration
    DESCRIPTION: The test case verifies the sports landing page of Rugby Union as per the CMS configuration
    PRECONDITIONS: In CMS--&gt; Sport Pages--&gt;Sport Category--&gt; General Sport Configuration--&gt; Enter the mandatory details and save.
    PRECONDITIONS: Primary and Top markets and Save Changes with required fields
    PRECONDITIONS: In CMS -&gt; System Config -&gt; Structure -&gt; Enable the Market Switcher for the Rugby Union sport.
    """
    keep_browser_open = True

    mandatory_fields = {
        'disabled': False,
        'inApp': True,
        'showInPlay': True,
        'showInHome': True,  # show in sport ribbon
        'showInAZ': True,
        'outrightSport': False,
        'showScoreboard': True,
        'multiTemplateSport': True
    }

    markets = {
        "primaryMarkets": "|Match Result|,|Match Betting|,|Handicap Match Result|,|Total Match Points|,|No Draw Handicap 1|,|No Draw Handicap 2|,|No Draw Handicap 3|,|Handicap Betting|",
        "topMarkets": "|Game Lines 3 way:Match Result,Handicap Betting,Total Match Points|",
        "aggrigatedMarkets": [
            {
                "marketName": "Game Lines 3 way",
                "titleName": "Match Result,Handicap Betting,Total Match Points"
            }
        ]
    }

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS--&gt; Sport Pages--&gt;Sport Category--&gt; General Sport Configuration--&gt; Enter the mandatory details and save.
        PRECONDITIONS: Primary and Top markets and Save Changes with required fields
        PRECONDITIONS: In CMS -&gt; System Config -&gt; Structure -&gt; Enable the Market Switcher for the Rugby Union sport.
        """
        # verifying rugby union sport and it's configurations {mandatory_fields and markets}
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == vec.olympics.RUGBYUNION:
                self.__class__.sport_id = sport['id']
                self.mandatory_fields = {field: self.mandatory_fields[field] for field in self.mandatory_fields if self.mandatory_fields[field] != sport.get(field)}

                is_primary_markets_available = sport.get('primaryMarkets') != ""
                if not is_primary_markets_available:
                    self.mandatory_fields['primaryMarkets'] = self.markets['primaryMarkets']

                is_top_markets_available = sport.get("topMarkets") != ""
                if not is_top_markets_available:
                    self.mandatory_fields['topMarkets'] = self.markets['topMarkets']
                    self.mandatory_fields['aggrigatedMarkets'] = self.markets['aggrigatedMarkets']

                if self.mandatory_fields:
                    self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                          **self.mandatory_fields)
                break
        else:
            raise VoltronException(f'{vec.olympics.RUGBYUNION} sport not found in sports categories')

        # checking the market switcher status and enabling for rugby union
        market_switcher_config = self.get_initial_data_system_configuration().get('MarketSwitcher', {})
        if not market_switcher_config:
            market_switcher_config = self.cms_config.get_system_configuration_item('MarketSwitcher')

        if not market_switcher_config['rugbyunion']:
            self.cms_config.update_system_configuration_structure(config_item='MarketSwitcher',
                                                                  field_name='rugbyunion',
                                                                  field_value=True)

        # getting active tabs from CMS
        list_of_tabs_response = self.cms_config.get_sport_tabs(self.ob_config.rugby_union_config.category_id)
        self.__class__.events_status = {tab['displayName'].upper(): tab['hasEvents'] for tab in list_of_tabs_response if tab['enabled']}
        try:
            in_play = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.rugby_union_config.category_id)
        except:
            in_play = "IN-PLAY"

        if in_play not in self.events_status:
            in_play_events = self.get_active_events_for_category(category_id=self.ob_config.rugby_union_config.category_id,
                                                            in_play_event=True, raise_exceptions=False)
            self.__class__.events_status[in_play.upper()] = bool(in_play_events)

        if self.device_type == 'desktop':
            self.__class__.sport_tabs_from_cms = [tab['displayName'].upper() for tab in list_of_tabs_response if tab['enabled']]
        else:
            self.__class__.sport_tabs_from_cms = [tab['displayName'].upper() for tab in list_of_tabs_response if
                                                  not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application is Launched successfully
        """
        self.site.go_to_home_page()
        self.site.wait_content_state("Home")

    def test_002_navigate_to_rugbyunion___ampgt_select_rugby_union_from_the_sports_ribbon_or_the_a_z_menu(self):
        """
        DESCRIPTION: Navigate to RugbyUnion --&amp;gt; Select Rugby union from the sports ribbon or the A-Z menu.
        EXPECTED: User should be redirected to the Rugby Union sport landing page.
        """
        try:
            self.site.open_sport(vec.olympics.RUGBYUNION)
        except:
            self.navigate_to_page('sport/rugby-union', test_automation=False)

    def test_003_verify_all_tabs_of_rugby_union_in_sport_landing_page_with_today_tomorrow_and_feature_data_details(self):
        """
        DESCRIPTION: Verify all tabs of Rugby union in Sport landing page with Today, Tomorrow and Feature Data details.
        EXPECTED: All tabs should display as per General sport configuration in CMS.
        EXPECTED: Matches, Competitions, In play Etc.
        """
        self.__class__.tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        if self.device_type != "mobile":
            try:
                in_play = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.ob_config.rugby_union_config.category_id)
            except:
                in_play = "IN-PLAY"
            if in_play not in self.sport_tabs_from_cms:
                self.__class__.sport_tabs_from_cms.append(in_play)
            for tab_name in self.tabs:
                self.assertIn(tab_name, self.sport_tabs_from_cms, f"Tab : {tab_name} is not in CMS tabs : {self.sport_tabs_from_cms}")
        else:
            self.assertListEqual(list(self.tabs.keys()), self.sport_tabs_from_cms, f'Actual Sport Tabs on FE :"{list(self.tabs.keys())}" are not same as'
                                                                                   f'Expected Sport Tabs configured in CMS : "{self.sport_tabs_from_cms}"')

    def test_004_verify_that_message_is_displayed_if_no_events_are_available_in_respective_tabs(self):
        """
        DESCRIPTION: Verify that message is displayed if no events are available in respective tabs.
        EXPECTED: Message should show up stating 'No events found' when there are no events in any specific tab.
        """
        for tab_name, tab in self.tabs.items():
            tab.click()
            self.assertEqual(self.site.sports_page.tabs_menu.current, tab_name, f'Unable to switch on {tab_name}')
            self.site.wait_content_state_changed()
            current_tab_events_status_fe = not self.site.sports_page.tab_content.has_no_events_label()
            tab_events_status_from_cms = self.events_status.get(tab_name.upper())
            self.assertEqual(current_tab_events_status_fe, tab_events_status_from_cms, f'Events Available Status from CMS: {tab_events_status_from_cms}\n'
                                                                                       f'Events Available Status in FE : {current_tab_events_status_fe}')
