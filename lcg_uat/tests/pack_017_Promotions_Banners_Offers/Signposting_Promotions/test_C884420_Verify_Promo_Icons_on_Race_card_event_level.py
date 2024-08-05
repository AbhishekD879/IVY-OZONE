import pytest

import voltron.environments.constants as vec
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_hl
# @pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.promotions
@pytest.mark.racing
@pytest.mark.module_ribbon
@pytest.mark.greyhounds
@pytest.mark.next_races
@pytest.mark.horseracing
@pytest.mark.cms
@pytest.mark.promotions_banners_offers
@pytest.mark.desktop
@vtest
class Test_C884420_Verify_Promo_Icons_on_Race_card_event_level(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C884420
    VOL_ID: C9697671
    NAME: Verify Promo Icons on <Race> card event level
    """
    keep_browser_open = True
    event_level_flag, market_level_flag = 'EVFLAG_EPR', 'MKTFLAG_EPR'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Add Featured module
        """
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        dialog_name = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                          market_level_flag=self.market_level_flag)['popupTitle']
        dialog_name = dialog_name.upper() if self.brand != 'ladbrokes' else dialog_name
        vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE = vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE.format(dialog_name)

        self.__class__.horse_racing_name_pattern = \
            self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
        event = self.ob_config.add_UK_racing_event(extra_place_race=True, number_of_runners=1)
        racing_event_off_time = event.event_off_time
        self.__class__.racing_created_event_name = f'{racing_event_off_time} {self.horse_racing_name_pattern}'

        next_event = self.ob_config.add_UK_racing_event(extra_place_race=True,
                                                        number_of_runners=1,
                                                        ew_terms=self.ew_terms,
                                                        lp_prices={0: '2/3'},
                                                        time_to_start=1)
        self.__class__.next4_event_off_time = next_event.event_off_time
        self.__class__.next4_event_name = f'{self.next4_event_off_time} {self.horse_racing_name_pattern}'.upper()

        racing_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.module_race_type = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=racing_type_id)['title'].upper()

        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_race_type)

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: Horse Racing landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_002_verify_signposting_promotion_on_the_next_races_and_tap_the_icon(self):
        """
        DESCRIPTION: Verify the event with **Extra Place Race** promotion on the "Next Races" module
        EXPECTED: Promo icon is shown on the race card header at the right side
        EXPECTED: In case if both cashout and a promotion are available for the event, both icons are shown
        """
        self.__class__.next_event = self.get_event_from_next_races_module(event_name=self.next4_event_name)
        self.assertTrue(self.next_event.promotion_icons.has_extra_place_race(),
                        msg=f'There\'s no Extra Place Race promotion shown for "{self.next4_event_name}')

    def test_003_tap_on_the_extra_place_race_promo_icon(self):
        """
        DESCRIPTION: Tap on the Extra Place Race promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        self.next_event.promotion_icons.extra_place_race.click()
        self.check_promotion_dialog_appearance_and_close_it(expected_title=vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE)

    def test_004_check_icon_presence_on_featured_tab_race_type_section(self):
        """
        DESCRIPTION: Verify the event with **Extra Place Race** promotion on "Featured" tab of the Homepage:
        DESCRIPTION: * for module by Race Type ID
        DESCRIPTION: Tap the icon
        EXPECTED: Promo icon is shown on the race card at the left side
        EXPECTED: In case if both cashout and a promotion are available for the event, both icons are properly shown
        EXPECTED: Promo footer is shown after tapping the icon
        """
        self.site.go_to_home_page()
        module_content = self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        module_content.scroll_to()
        section = module_content.accordions_list.items_as_ordered_dict.get(self.module_race_type)
        try:
            events = section.items_as_ordered_dict
        except StaleElementReferenceException:
            section = self.get_section(self.module_race_type)
            events = section.items_as_ordered_dict
        self.assertTrue(events, msg='*** No events present on page')
        self.assertIn(self.racing_created_event_name, events.keys(),
                      msg=f'Added event "{self.racing_created_event_name}" was not found among events "{events.keys()}"')
        event = events[self.racing_created_event_name]
        self.assertTrue(event.promotion_icons.has_extra_place_race(),
                        msg=f'There\'s no Extra place race promotion shown for "{self.racing_created_event_name}"')
        event.scroll_to()
        event.promotion_icons.extra_place_race.click()
        self.check_promotion_dialog_appearance_and_close_it(
            expected_title=vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE)
