import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.helpers import normalize_name


# @pytest.mark.crl_tst2  # should be adapted for ladbrokes. testcase is currently outdated
# @pytest.mark.crl_stg2 # todo: VOL-5608 Update C717578 "Displaying of yourcall icons on Football Coupons" due to new design
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
# we can not run such test simultaneously with other coupons
@pytest.mark.consequent
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-49502')
@vtest
class Test_C717578_Displaying_of_yourcall_icons_on_Football_Coupons(BaseCouponsTest, BaseBanachTest):
    """
    TR_ID: C717578
    NAME: Displaying of yourcall icons on Football Coupons
    PRECONDITIONS: * Coupon with and without YourCall and/or Banach leagues is created https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
    PRECONDITIONS: * YourCall and/or Banach leagues leagues (competitions) are added and turned on in YourCall page in CMS
    PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * Coral app is loaded and Coupons tab on Football page is opened
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    """
    keep_browser_open = True
    coupon_name = 'Football Auto Test Coupon'
    yc_section_name = 'PREMIER LEAGUE'
    sections = None
    euro_elite_coupon_name = 'Euro Elite Coupon'

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case verifies logic of displaying of +B icons (BuildYourBet) on Competition accordions on Coupon Details page
        PRECONDITIONS: * Coupon with and without YourCall and/or Banach leagues is created https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
        PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
        PRECONDITIONS: * YourCall and/or Banach leagues leagues (competitions) are added and turned on in YourCall page in CMS
        PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS and/or
        PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
        PRECONDITIONS: * Coral app is loaded and Coupons tab on Football page is opened
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
        """
        self.__class__.not_yc_section_name = tests.settings.football_autotest_competition_league_2
        self.cms_config.your_call_league_switcher()
        self.cms_config.update_yourcall_icons_tabs()

        # Add event with YourCall icon
        event_params = self.ob_config.add_football_event_to_england_premier_league()
        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.yc_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.yc_event_name}"')

        self.__class__.yc_league_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        self.ob_config.add_event_to_coupon(market_id=market_id, coupon_name=self.coupon_name)

        # Add event without YourCall icon
        event_params = self.ob_config.add_football_event_to_autotest_league2()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_league2.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.eventID_not_yc = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_not_yc,
                                                               query_builder=self.ss_query_builder)
        self.__class__.not_yc_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.not_yc_event_name}"')

        self.ob_config.add_event_to_coupon(market_id=market_id, coupon_name=self.coupon_name)

        # Add event with Banach league
        event_params = self.ob_config.add_football_event_to_england_premier_league()
        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.eventID_banach = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_banach,
                                                               query_builder=self.ss_query_builder)
        self.__class__.banach_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.banach_event_name}"')

        self.__class__.yc_league_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        market_id = self.ob_config.market_ids[self.eventID_banach][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=market_id, coupon_name=self.euro_elite_coupon_name)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_navigate_to_coupon_details_page_of_coupon_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Coupon Details page of coupon from preconditions
        """
        self.navigate_to_page(name='sport/football')
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=self.coupon_name)

    def test_002_observe_accordionheader_of_competition_league_that_is_added_and_enabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition (league), that is added and enabled in CMS and is returned from DS
        EXPECTED: For mobile/tablet view:
        EXPECTED: '#Yourcall' icon is displayed on the right of module accordion/header
        EXPECTED: in case cash out icon is displayed, yourcall icon is displayed before it
        EXPECTED: For desktop view:
        EXPECTED: #Yourcall icon is displayed on the left side, before accordion title
        EXPECTED: cash out icon is displayed on the right side, before expand/collapse accordion arrow
        EXPECTED: BYB icon is not displayed on type (league) level
        """
        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.yc_section_name, self.sections.keys(),
                      msg=f'Event section: "{self.yc_section_name}" not found in sections list: "{self.sections.keys()}"')
        self.assertIn(self.not_yc_section_name, self.sections.keys(),
                      msg=f'Event section: "{self.not_yc_section_name}" '
                      f'not found in sections list: "{self.sections.keys()}"')

        # B+ Your call is displaying
        yc_event_negative = self.get_event_from_league(event_id=self.eventID, section_name=self.yc_section_name)
        self.assertTrue(yc_event_negative.has_byb_icon(),
                        msg=f'\'B+\' (yourcall icon) icon is not shown in: "{self.yc_section_name}"')

    def test_003_observe_accordionheader_of_competitionleague_that_is_added_and_enabled_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition(league), that is added and enabled in CMS and is NOT returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        not_yc_event_section = self.sections[self.not_yc_section_name]
        not_yc_event = self.get_event_from_league(event_id=self.eventID_not_yc, section_name=self.not_yc_section_name)

        if self.yc_event_section.group_header.icons_count > 1:
            self.assertFalse(self.yc_event_section.group_header.has_cash_out_mark,
                             msg=f'Event section: "{self.yc_section_name}" has cash out icon')

        self.assertFalse(not_yc_event.has_byb_icon(expected_result=False),
                         msg=f'\'B+\' (yourcall icon) icon displayed for: "{self.not_yc_section_name}"')
        if not_yc_event_section.group_header.icons_count > 0:
            self.assertFalse(not_yc_event_section.group_header.has_cash_out_mark,
                             msg=f'Event section: "{self.not_yc_section_name}" has cash out icon')

    def test_004_observe_accordionheader_of_competitionleague_that_is_not_added_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition(league), that is NOT added in CMS and is returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        # We can not disable leagues with Yourcall
        pass

    def test_005_observe_accordionheader_of_competitionleague_that_is_not_added_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition(league), that is NOT added in CMS and is NOT returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        # We can not disable leagues with Yourcall
        pass

    def test_006_navigate_to_cms_and_disable_any_competitionleague_that_is_returned_from_ds(self):
        """
        DESCRIPTION: Navigate to CMS and disable any competition(league), that is returned from DS
        """
        # We can not disable leagues with Yourcall
        pass

    def test_007_navigate_back_to_coupon_details_page_of_coupon_from_preconditions_refresh_page_observe(self):
        """
        DESCRIPTION: * Navigate back to Coupon Details page of coupon from preconditions
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Observe accordion/header of competition(league), that is added and disabled in CMS and is returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        # We can not disable leagues with Yourcall

    def test_008_navigate_to_cms_and_uncheck_enableicon_checkbox_in_system_configuration_yourcalliconsandtabs(self):
        """
        DESCRIPTION: Navigate to CMS and uncheck 'enableIcon' checkbox in System-configuration -> YOURCALLICONSANDTABS
        """
        # We can not change anything on system-configuration
        pass

    def test_009__navigate_back_to_coupon_details_page_of_coupon_from_preconditions(self):
        """
        DESCRIPTION: * Navigate back to Coupon Details page of coupon from preconditions
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Observe accordion/header of competition(league), that is added and enabled in CMS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        # We can not change anything on system-configuration
        pass

    def test_010_repeat_steps_2_for_league_competition_that_is_added_and_enabled_in_cms(self):
        """
        DESCRIPTION: Repeat Step 2 for league (competition), that is added and enabled in CMS and is returned from Banach
        """
        self.device.go_back()
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=self.euro_elite_coupon_name)

    def test_011_navigate_to_coupon_details_page_of_coupon_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Coupon Details page of coupon from preconditions and observe accordion/header of competition (league), that is added and enabled in CMS and is returned from both DS and Banach (Example: Premier League etc)
        EXPECTED: '+B' icon (BYB) is displayed for appropriate competition on event card only ONCE.
        """
        yc_event_negative = self.get_event_from_league(event_id=self.eventID_banach, section_name=self.yc_section_name)
        self.assertTrue(yc_event_negative.has_byb_icon(),
                        msg=f'\'B+\' (yourcall icon) icon is not shown in: "{self.yc_section_name}"')
