import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.greyhounds
@pytest.mark.reg157_fix
@pytest.mark.mobile_only
@vtest
class Test_C9769894_Verify_More_link_functionality_for_Next_Races_module_on_Greyhounds(BaseRacing):
    """
    TR_ID: C9769894
    VOL_ID: C23201020
    NAME: Verify 'More' link functionality for 'Next Races' module on Greyhounds
    DESCRIPTION: This test case verifies 'More' link functionality for 'Next Races' module on Greyhounds
    PRECONDITIONS: 1. "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app.
    PRECONDITIONS: 3. Tap on 'Next Races' tab on the Greyhounds.
    PRECONDITIONS: 4. Race events are available for the current day.
    PRECONDITIONS: 5. List of Event Cards is displayed at the page.
    PRECONDITIONS: Note:
    PRECONDITIONS: 1. The number of events is not CMS configurable. There should be always 20 events displayed.
    PRECONDITIONS: 2. To get info about class use link:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        if cls.virtual_races_enabled == 'Yes':
            cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                             field_name='isVirtualRacesEnabled',
                                                             field_value='Yes')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
        PRECONDITIONS: Load Oxygen app.
        PRECONDITIONS: Tap on 'Next Races' tab on the Greyhounds.
        """
        self.__class__.virtual_races_enabled = "No"
        self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id)

        greyhound_next_races_toggle = self.get_initial_data_system_configuration().get('GreyhoundNextRacesToggle', {})
        if not greyhound_next_races_toggle:
            greyhound_next_races_toggle = self.cms_config.get_system_configuration_item('GreyhoundNextRacesToggle')
        if not greyhound_next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for greyhounds in CMS')
        self.site.open_sport(name=vec.sb.GREYHOUND.upper())
        self.__class__.next_races_tab = self.site.greyhound.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
        self.assertTrue(self.next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
        greyhound_next_races_filter = self.cms_config.get_system_configuration_item("NextRacesFiltersGreyHounds")
        if greyhound_next_races_filter.get('EnableFilters'):
            filters = self.site.greyhound.tab_content.filters_list.items_as_ordered_dict
            filter_name = next((filter_name for filter_name in filters.keys() if (filter_name.upper() != "VIRTUALS" and filter_name.upper() != "ALL")), None)
            if filter_name:
                filters.get(filter_name).click()
            else:
                self.__class__.virtual_races_enabled = \
                    self.cms_config.get_system_configuration_structure()['GreyhoundNextRaces']['isVirtualRacesEnabled']
                if self.virtual_races_enabled == 'Yes':
                    self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                                          field_name='isVirtualRacesEnabled',
                                                                          field_value='No')
                    wait_for_haul(60)
                    self.device.refresh_page()
        self.__class__.sections = self.get_sections('greyhound-racing')
        self.assertTrue(self.sections, msg='No race sections are found in next races')

    def test_001_verify_more_link_displaying(self):
        """
        DESCRIPTION: Verify 'More' link displaying.
        EXPECTED: * Link is displayed at the 'Event Card' header.
        EXPECTED: * Link is displayed for each event in the 'Next Races' module.
        EXPECTED: * Link is aligned to the right.
        """
        for race_name, race in self.sections.items():
            self.assertTrue(race.header.has_view_full_race_card(),
                            msg=f'"More" link is not found for race: "{race_name}"')

    def test_002_tap_on_more_link(self):
        """
        DESCRIPTION: Tap on 'More' link.
        EXPECTED: The user is taken to the particular event details page.
        """
        race_name, race = list(self.sections.items())[0]
        race.header.click()
        event_title = self.site.greyhound_event_details.event_name.strip()
        self.assertEqual(event_title, race_name.title(), msg=f'Actual race title "{event_title}" does not match with expected race title "{race_name.title()}"')

    def test_003_tap_on_the_back_button(self):
        """
        DESCRIPTION: Tap on the 'Back' button.
        EXPECTED: The previously visited page is opened.
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Greyhounds')
        self.assertTrue(self.next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected when user revisits the page')
