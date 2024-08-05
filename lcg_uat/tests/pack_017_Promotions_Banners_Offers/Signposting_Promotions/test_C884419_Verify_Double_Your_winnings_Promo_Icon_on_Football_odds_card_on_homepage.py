import pytest
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod  # Coral only
# @pytest.mark.crl_hl
@pytest.mark.promotions
@pytest.mark.module_ribbon
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@pytest.mark.desktop
@vtest
class Test_C884419_Verify_Double_Your_winnings_Promo_Icon_on_Football_odds_card_on_Homepage(BaseFeaturedTest):
    """
    TR_ID: C884419
    NAME: Verify Double Your winnings Promo Icon on Football odds card on HomePage
    """
    keep_browser_open = True
    today_event_name, live_event_name = None, None
    event = None
    section_name = tests.settings.football_autotest_league
    coupon_name = vec.siteserve.EXPECTED_COUPON_NAME
    event_level_flag, market_level_flag = 'EVFLAG_DYW', 'MKTFLAG_DYW'

    def check_dyw_promotion_for_event(self, event):
        self.assertTrue(event.promotion_icons.has_double_your_winnings(),
                        msg=f'Event {event.event_name} does not have "Double Your Winnings" promotion')
        event.promotion_icons.double_your_winnings.click()
        self.check_promotion_dialog_appearance_and_close_it(
            expected_title=vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS)

    def verify_event_is_present_on_featured_tab(self, module_name):
        self.wait_for_featured_module(name=module_name)
        try:
            featured_modules = self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)) \
                .accordions_list.items_as_ordered_dict
        except StaleElementReferenceException:
            featured_modules = self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)) \
                .accordions_list.items_as_ordered_dict
        self.assertTrue(featured_modules, msg='*** No modules present on page')
        module_events = featured_modules[module_name].items_as_ordered_dict
        self.assertTrue(module_events, msg='*** No events present on page')
        self.assertIn(self.today_event_name, module_events.keys(),
                      msg=f'Added event "{self.today_event_name}" was not found on page "{module_events.keys()}"')
        self.check_dyw_promotion_for_event(event=module_events[self.today_event_name])

    def test_001_create_test_events(self):
        """
        DESCRIPTION: Create test events with "Double Your winnings" promotion available
        DESCRIPTION: Add Featured Tab Module with event with "Double Your winnings" promotion available
        """
        live_start_time = self.get_date_time_formatted_string(seconds=10)

        event = self.ob_config.add_football_event_to_featured_autotest_league(
            is_live=True, start_time=live_start_time, double_your_winnings=True, img_stream=True)
        self.__class__.live_event_name = event.team1 + ' v ' + event.team2

        event = self.ob_config.add_football_event_to_featured_autotest_league(double_your_winnings=True)
        self.__class__.today_event_name = event.team1 + ' v ' + event.team2

        type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, id=type_id,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title']

        dialog_name = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                          market_level_flag=self.market_level_flag)['popupTitle'].upper()
        vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS = vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS.format(dialog_name)

    def test_002_check_the_event_with_double_your_winnings_promotion_on_the_homepage_and_tap_the_icon_in_all_listed_locations(self):
        """
        DESCRIPTION: Check the event with **Double Your Winnings** promotion on the Homepage:
        DESCRIPTION: * Homepage -> In Play tab
        DESCRIPTION: * Homepage -> Live Stream tab
        DESCRIPTION: * Homepage -> Featured tab
        DESCRIPTION: and tap the icon in all listed locations
        EXPECTED: Corresponding promo icon is shown on the event odds card
        EXPECTED: Promo footer is displayed after tapping the icon
        """
        if self.device_type == 'mobile':
            live_stream = self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream))
            self.site.wait_splash_to_hide(timeout=15)
            sections = live_stream.live_now.items_as_ordered_dict
        else:
            name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream)
            cms_right_menu_items = self.cms_config.get_left_menu_items()
            if name in cms_right_menu_items:
                self.site.open_sport(name=name)
            else:
                self.navigate_to_page(name='live-stream')
            self.site.wait_content_state('LiveStream')
            sections = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(sections, msg='*** No event sections are present on page')
        self.assertIn(vec.inplay.IN_PLAY_FOOTBALL, sections.keys(), msg=f'"{vec.sb.FOOTBALL}" not found in "{sections.keys()}"')
        section = sections.get(vec.inplay.IN_PLAY_FOOTBALL)
        section.expand()
        is_section_expanded = section.is_expanded()
        self.assertTrue(is_section_expanded, msg=f'"{vec.sb.FOOTBALL}" section is not expanded')
        league = list(section.items_as_ordered_dict.values())[0]
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg='*** No events present on page')
        self.softAssert(self.assertIn, self.live_event_name, events.keys(),
                        msg=f'Added event "{self.live_event_name}" was not found on page')
        self.check_dyw_promotion_for_event(event=events[self.live_event_name])

        if self.device_type == 'mobile':
            event = self.get_event_for_homepage_inplay_tab(sport_name=vec.inplay.IN_PLAY_FOOTBALL,
                                                           league_name=tests.settings.featured_autotest_league.title(),
                                                           event_name=self.live_event_name)

            self.check_dyw_promotion_for_event(event=event)
        if self.device_type == 'mobile':
            self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            section_list = self.site.home.tab_content.in_play_module.items_as_ordered_dict
            self.assertTrue(section_list, msg='*** No sections present on page')
            if vec.inplay.IN_PLAY_FOOTBALL not in section_list.keys():
                self.verify_event_is_present_on_featured_tab(module_name=self.module_name.upper())
            else:
                section = section_list.get(vec.inplay.IN_PLAY_FOOTBALL)
                self.assertTrue(section, msg=f'"{vec.sb.FOOTBALL}" section is not found in "{section_list.keys()}"')
                section_events = section.items_as_ordered_dict
                self.assertTrue(section_events, msg='*** No events present on page')
                if self.today_event_name not in section_events.keys():
                    self.verify_event_is_present_on_featured_tab(module_name=self.module_name.upper())
                else:
                    self.assertIn(self.today_event_name, section_events.keys(),
                                  msg=f'Added event "{self.today_event_name}" was not found on page "{section_events.keys()}"')
                    self.check_dyw_promotion_for_event(event=section_events[self.today_event_name])
        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')
            home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            home_page_modules = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(home_page_modules, msg='No one module found on Home Page')
            featured_section = home_page_modules.get(home_featured_tab_name)
            featured_modules = featured_section.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(featured_modules, msg='No one FEATURED module found')
            module = featured_modules.get(self.module_name.upper())
            section_events = module.items_as_ordered_dict
            self.assertTrue(section_events, msg='*** No events present on page')
            self.assertIn(self.today_event_name, section_events.keys(),
                          msg=f'Added event "{self.today_event_name}" was not found on page "{section_events.keys()}"')
            self.check_dyw_promotion_for_event(event=section_events[self.today_event_name])
