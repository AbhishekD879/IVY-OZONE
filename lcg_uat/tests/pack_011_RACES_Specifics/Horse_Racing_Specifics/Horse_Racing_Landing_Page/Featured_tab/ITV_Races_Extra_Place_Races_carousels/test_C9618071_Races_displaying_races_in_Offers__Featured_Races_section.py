from string import capwords

import pytest

from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # Cannot create ITV race and Extra place races on prod/hl.
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.mobile_only
@vtest
class Test_C9618071_Races_displaying_races_in_Offers__Featured_Races_section(BaseRacing):
    """
    TR_ID: C9618071
    VOL_ID: C11508489
    NAME: <Races>: displaying races in 'Offers & Featured Races' section
    DESCRIPTION: This test case verifies displaying of <Races> in 'Offers & Featured Races' section
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
        PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
        PRECONDITIONS: - You should have next Horse Race events:
        PRECONDITIONS: 1) With enabled 'Featured Racing Types' check box on event level (drilldownTagNames="EVFLAG_FRT") and races should be from different types
        PRECONDITIONS: 2) With enabled 'Extra Place Race' check box on market level (drilldownTagNames="MKTFLAG_EPR") and races should be from different types
        PRECONDITIONS: - You should be on Horse Racing landing page
        """
        event = self.ob_config.add_UK_racing_event(featured_racing_types=True, market_extra_place_race=True,
                                                   number_of_runners=1)
        self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'[:10]
        self.navigate_to_page(name='horse-racing')

    def test_001_verify_displaying_of_offers_and_featured_races_section(self):
        """
        DESCRIPTION: Verify displaying of 'Offers & Featured Races' section
        EXPECTED: 'Offers & Featured Races' section is shown
        """
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(vec.racing.OFFERS_AND_FEATURED_RACES, self.sections.keys(),
                      msg='"Enhanced Races" section is not displayed')

    def test_002_verify_displaying_of_the_events_with_enabled_featured_racing_types_check_box(self):
        """
        DESCRIPTION: Verify displaying of the events with enabled 'Featured Racing Types' check box
        EXPECTED: - Events are displayed in "ITV Races" sub category within 'Offers & Featured Races' section
        EXPECTED: - 'ITV' icon is shown at the top right corner of the sub category
        EXPECTED: - First 4-5 letters of race type are displayed under race time
        """
        self.__class__.offer_and_featured_races = self.sections.get(vec.racing.OFFERS_AND_FEATURED_RACES, None)
        self.assertTrue(self.offer_and_featured_races.has_itv_module(), msg='ITV module is not present')

        actual_itv_header = self.offer_and_featured_races.itv_module.header_name.text
        self.assertEquals(actual_itv_header, vec.racing.ITV,
                          msg=f'"ITV Races" is not displayed, Actual: "{actual_itv_header}", '
                              f'Expected: "{vec.racing.ITV}"')
        self.assertTrue(self.offer_and_featured_races.itv_module.has_itv_icon(),
                        msg=f'Icon for "{vec.racing.ITV}" is not present')

        itv_grid_list = self.offer_and_featured_races.itv_module.items_as_ordered_dict
        self.assertTrue(itv_grid_list, msg='Cannot find events in "ITV Races" module')
        itv_event = itv_grid_list.get(self.event_name)
        self.assertTrue(itv_event, msg=f'"{self.event_name}" not found in ITV module')

        for event_name, event in itv_grid_list.items():
            self.assertTrue(len(event.race_name) <= 4, msg=f'More than 4 letters of race type are displayed in '
                                                           f'"ITV Races" module for "{event_name}"')

    def test_003_verify_displaying_of_the_events_with_enabled_extra_place_race_check_box(self):
        """
        DESCRIPTION: Verify displaying of the events with enabled 'Extra Place Race' check box
        EXPECTED: - The event is displayed in "Extra Place Offer" sub category within 'Offers & Featured Races' section
        EXPECTED: - 'Extra Place' icon is shown at the top right corner of the sub category
        EXPECTED: - First 4-5 letters of race type are displayed under race time
        """
        self.assertTrue(self.offer_and_featured_races.has_extra_place_module(), msg='Extra Place module is not present')

        actual_extra_place_header = self.offer_and_featured_races.extra_place_offer_module.header_name.text
        expected_header_title = capwords(vec.racing.EXTRA_PLACE_TITLE)
        self.assertEquals(actual_extra_place_header, expected_header_title,
                          msg=f'"Extra Place Offer" is not displayed, Actual: "{actual_extra_place_header}", '
                              f'Expected: "{expected_header_title}"')

        self.assertTrue(self.offer_and_featured_races.extra_place_offer_module.has_extra_place_races_icon(),
                        msg=f'Icon for "{expected_header_title}" is not present')

        extra_place_grid_list = self.offer_and_featured_races.extra_place_offer_module.items_as_ordered_dict
        self.assertTrue(extra_place_grid_list, msg='Cannot find events in "Extra Place Race" module')
        extra_place_event = extra_place_grid_list.get(self.event_name)
        self.assertTrue(extra_place_event, msg=f'"{self.event_name}" not found in ITV module')

        for event_name, event in extra_place_grid_list.items():
            self.assertTrue(len(event.race_name) <= 4, msg=f'More than 4 letters of race type are displayed in '
                                                           f'"Extra Place Race" module for "{event_name}"')
