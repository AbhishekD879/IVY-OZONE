import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # event creation
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.mobile_only  # applicable for tablet as well
@pytest.mark.low
@pytest.mark.safari
@vtest
class Test_C2593956_Verify_navigation_through_ITV_RacesExtra_Place_Races_carousels(BaseRacing):
    """
    TR_ID: C2593956
    VOL_ID: C11508491
    NAME: Verify navigation through ITV Races/Extra Place Races carousels
    DESCRIPTION: This test case verifies navigation through ITV Races/Extra Place Races carousels
    PRECONDITIONS: 1. ITV/Extra Place Races feature toggle should be set to "ON"
    PRECONDITIONS: 2. There should be enough Horse Racing events with 'Featured race'(ITV races) flag and with 'Extra place' flags configured in TI so they can't fit the width of the screen.
    PRECONDITIONS: 3. Go to oxygen application and navigate to Featured tab on Horse Racing page.
    PRECONDITIONS: Design for both Brands can be found here: https://jira.egalacoral.com/browse/BMA-35023
    PRECONDITIONS: <Module name> - "Offers and Extra place" (Ladbrokes), "Enhanced Races" (Coral)
    PRECONDITIONS: 'Featured race'(ITV races) - is checked on event level
    PRECONDITIONS: 'Extra place' flag - is checked on market level
    """
    keep_browser_open = True
    quantity_of_events = 9 if tests.settings.brand == 'ladbrokes' else 3

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with enabled 'Featured Racing Types' check box on event level (drilldownTagNames="EVFLAG_FRT") and races should be from different types
        DESCRIPTION: Create event with enabled 'Extra Place Race' check box on market level (drilldownTagNames="MKTFLAG_EPR") and races should be from different types
        DESCRIPTION: Open Horse Racing landing page
        """
        self.__class__.created_events = []

        for i in range(1, self.quantity_of_events + 1):
            event = self.ob_config.add_UK_racing_event(time_to_start=5 * i, featured_racing_types=True,
                                                       market_extra_place_race=True, number_of_runners=1)
            event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            self.created_events.append(event_name[:10] if self.brand == 'ladbrokes' else event_name)

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_001_verify_module_displaying(self):
        """
        DESCRIPTION: Verify <Module name> Module  displaying
        EXPECTED: * <Module name> Module is displayed on Featured tab
        EXPECTED: * ITV and Extra Place Races carousels are displayed with related events inside
        EXPECTED: * ITV and Extra Place Races are displayed as separate carousels
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')
        self.__class__.itv_module_events = sections[self.enhanced_races_name].itv_module.items_as_ordered_dict
        self.assertTrue(self.itv_module_events,
                        msg=f'There are no events in "{self.itv_module_events}" module section')
        for event_name in self.created_events:
            self.assertIn(event_name, self.itv_module_events,
                          msg=f'"{event_name}" cannot be found in "{list(self.itv_module_events.keys())}" '
                              f'events list of "{vec.racing.ITV}" module')

        self.__class__.extra_place_module_events = \
            sections[self.enhanced_races_name].extra_place_offer_module.items_as_ordered_dict
        self.assertTrue(self.extra_place_module_events,
                        msg=f'There are no events in "{self.extra_place_module_events}" module section')
        for event_name in self.created_events:
            self.assertIn(event_name, self.extra_place_module_events,
                          msg=f'"{event_name}" cannot be found in "{list(self.extra_place_module_events.keys())}" '
                              f'events list of "{vec.racing.EXTRA_PLACE_TITLE}" module')

    def test_002_verify_navigation_through_itv_carousel(self):
        """
        DESCRIPTION: Verify navigation through ITV carousel
        EXPECTED: * User is able to navigate through carousels by swiping through
        EXPECTED: * Extra Place Races carousel remains untouched while navigation through ITV carousel
        """
        # Not handling swipe atm TODO: VOL-1099
        last_itv_event_name = self.created_events[-1]
        last_itv_event = self.itv_module_events.get(last_itv_event_name)
        self.assertTrue(last_itv_event, msg=f'"{last_itv_event_name}" not found in ITV section')
        self.assertTrue(last_itv_event.is_displayed(), msg=f'"{last_itv_event_name}" is not displayed')

    def test_003_verify_navigation_through_extra_place_races_carousel(self):
        """
        DESCRIPTION: Verify navigation through Extra Place Races carousel
        EXPECTED: * User is able to navigate through carousels using by swiping through
        EXPECTED: * ITV Races carousel remains untouched while navigation through Extra Place Races carousel
        """
        # Not handling swipe atm TODO: VOL-1099
        last_extra_place_event_name = self.created_events[-1]
        last_extra_place_event = self.extra_place_module_events.get(last_extra_place_event_name)
        self.assertTrue(last_extra_place_event, msg=f'"{last_extra_place_event_name}" not found in Extra Place section')
        self.assertTrue(last_extra_place_event.is_displayed(), msg=f'"{last_extra_place_event_name}" is not displayed')
