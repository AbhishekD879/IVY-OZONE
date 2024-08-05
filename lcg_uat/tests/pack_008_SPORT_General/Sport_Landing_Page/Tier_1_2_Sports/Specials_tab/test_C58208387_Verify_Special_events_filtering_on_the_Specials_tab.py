import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot change Special market status
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.specials
@pytest.mark.desktop
@vtest
class Test_C58208387_Verify_Special_events_filtering_on_the_Specials_tab(BaseSportTest):
    """
    TR_ID: C58208387
    NAME: Verify Special events filtering on the  'Specials' tab
    DESCRIPTION: This test case verifies special events filtering on the 'Specials' tab
    DESCRIPTION: **Will be available from 102.0 Coral and 102.0 Ladbrokes**
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: **Special** events should contain the following settings:
    PRECONDITIONS: Set the **drilldownTagNames = MKTFLAG_SP** on market level
    PRECONDITIONS: ('Specials' flag to be ticked on market level in TI)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available on SS
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def get_special_event(self, event_name):
        """
        Get Special event from Specials sections
        :param event_name event name
        :return: Special event
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Specials sections found')
        section = sections.get(self.league_name)
        self.assertTrue(section, msg=f'Specials section "{self.league_name}" not found')
        section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for section "{self.league_name}')
        return events.get(event_name)

    def get_event_status(self, event_name):
        """
        Get Special event status
        :param event_name event name
        :return: Special event status
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        return self.get_special_event(event_name)

    def wait_event_undisplayed(self, event_name):
        """
        Wait Special event undisplayed
        :param event_name event name
        :return: True or False
        """
        return wait_for_result(
            lambda: self.get_event_status(event_name) is None,
            name='Special event to be undisplayed',
            expected_result=True,
            timeout=5)

    def test_000_preconditions(self):
        """
        DESCRIPTION: 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available on SS
        DESCRIPTION: Create event
        DESCRIPTION: Navigate to the Sports Landing Page
        DESCRIPTION: Choose the 'Specials' tab
        """
        specials_tab_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials

        specials_tab_name = self.get_sport_tab_name(name=specials_tab_cms_name,
                                                    category_id=self.ob_config.football_config.category_id)

        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        event_params = self.ob_config.add_autotest_premier_league_football_event(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=market_name)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.event_id = event_params.event_id
        self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=event_params.ss_response)
        self.__class__.market_name, self.__class__.market_id = \
            next(iter(self.ob_config.market_ids.get(self.event_id).items()))
        self._logger.info(f'*** Created 1st Football event "{self.event_name}" with ID "{self.event_id}"')

        event_params_2 = self.ob_config.add_autotest_premier_league_football_event(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=market_name)
        self.__class__.event_name_2 = event_params_2.ss_response['event']['name']
        self._logger.info(f'*** Created 2nd Football event "{self.event_name_2}" with ID "{event_params_2.event_id}"')

        result = wait_for_result(
            lambda: self.is_tab_present(tab_name=specials_tab_cms_name,
                                        category_id=self.ob_config.football_config.category_id),
            name='Specials tab to be displayed',
            poll_interval=4,
            timeout=40)
        self.assertTrue(result, msg='Specials tab is not displayed')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=vec.football.FOOTBALL_TITLE)
        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(specials_tab_name)
        self.assertEqual(tabs_menu.current, specials_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current} is not as expected "{specials_tab_name}"')

    def test_001_verify_events_filtering_on_the_page(self):
        """
        DESCRIPTION: Verify events filtering on the page
        EXPECTED: All Special events available for particular Sports are present
        """
        # verified in step 2

    def test_002_verify_filtering_for_special_events(self):
        """
        DESCRIPTION: Verify filtering for special events
        EXPECTED: Events with next attributes are shown:
        EXPECTED: - eventSortCode="MTCH"/"TNMT"
        EXPECTED: - drilldownTagNames: "MKTFLAG_SP" - **on market level**
        """
        sport_event = self.get_special_event(self.event_name)
        self.assertTrue(sport_event, msg=f'Event: "{self.event_name}" not found')
        sport_event_2 = self.get_special_event(self.event_name_2)
        self.assertTrue(sport_event_2, msg=f'Event: "{self.event_name_2}" not found')

    def test_003_open_the_ob_system_set_specials_false_for_the_market_save_the_changes(self):
        """
        DESCRIPTION: * Open the OB system.
        DESCRIPTION: * Set 'Specials': False for the market.
        DESCRIPTION: * Save the changes.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: Events with next attributes are NOT shown:
        EXPECTED: - eventSortCode="MTCH"/"TNMT"
        EXPECTED: - **NO** drilldownTagNames:"MKTFLAG_SP" - **on market level**
        """
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get(self.market_name).values()))
        self.ob_config.make_market_special(
            market_id=self.market_id,
            market_template_id=market_template_id,
            event_id=self.event_id,
            status='N',
            flags='')

        sp_event_status = self.wait_event_undisplayed(self.event_name)
        self.assertTrue(sp_event_status, msg=f'Event: "{self.event_name}" is shown"')
        sport_event_2 = self.get_special_event(self.event_name_2)
        self.assertTrue(sport_event_2, msg=f'Event: "{self.event_name_2}" not found"')
