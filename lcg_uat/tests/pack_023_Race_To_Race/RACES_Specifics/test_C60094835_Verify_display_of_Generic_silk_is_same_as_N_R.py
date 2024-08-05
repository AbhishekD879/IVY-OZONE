import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.reg165_fix
@vtest
class Test_C60094835_Verify_display_of_Generic_silk_is_same_as_N_R(BaseRacing):
    """
    TR_ID: C60094835
    NAME: Verify display of Generic silk is same as N/R
    DESCRIPTION: This test case verifies  Generic silk should be same as non-runner silk and should match with mock screens mentioned in Zeplin
    PRECONDITIONS: 1.Generic silk should display for all the horses by default
    PRECONDITIONS: If bespoke silk present it should display otherwise generic silk should present
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_001_login_to_the_application_and_navigate_to_horse_racing_from_header_sub_menuin_mobile_from_sports_ribbonor_in_play___horse_racing(self):
        """
        DESCRIPTION: Login to the application and navigate to horse racing from header sub menu(In mobile from sports ribbon)
        DESCRIPTION: or In play - Horse racing
        EXPECTED: Horse racing landing page - meetings tab should display
        EXPECTED: if user is navigate from in play tab in play horse racing events should display
        """
        self.site.login()
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

    def test_002_click_on_any_event_from_uk_and_ire_for_which_bespoke_silk_is_not_provided_at_least_for_one_horse(self):
        """
        DESCRIPTION: Click on any event from UK and IRE for which bespoke silk is not provided at least for one horse
        EXPECTED: All the horse in EDP should have bespoke silk
        EXPECTED: for the horse which don't have bespoke silk should display generic silk
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_UK_racing_event(number_of_runners=1)
        is_silk_generic = None
        self.site.wait_splash_to_hide(10)
        # Getting a specific Meeting
        uk_irish_races = list(self.site.horse_racing.tab_content.accordions_list.get_items(
            name=self.uk_and_ire_type_name).values())[0]
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

        meetings = wait_for_result(lambda: uk_irish_races.items_as_ordered_dict, timeout=5)
        self.assertTrue(meetings,
                        msg=f'Failed to display meetings for section: "{vec.racing.UK_AND_IRE_TYPE_NAME}"')
        for mtng in range(len(meetings.items())):
            meeting_name, meeting = list(meetings.items())[mtng]
            events = meeting.items_as_ordered_dict
            self.assertTrue(events,
                            msg=f'Failed to display events for meeting: "{meeting_name}"')
            flag = True
            for evnt in range(len(events)):
                event = list(events.values())[evnt]
                if not event.is_resulted:
                    event.click()
                    if flag:
                        if self.site.wait_for_stream_and_bet_overlay():
                            self.site.stream_and_bet_overlay.close_button.click()
                        if self.site.wait_for_my_stable_onboarding_overlay():
                            self.site.my_stable_onboarding_overlay.close_button.click()
                        flag = False
                    section_nw = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict['WIN OR E/W']
                    self.assertTrue(section_nw, msg='No one section was found')
                    section_nw.click()
                    selected_market_name, selected_market = list(self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.items())[0]
                    self.assertTrue(selected_market, msg='No expected market tabs found on EDP')
                    outcomes = selected_market.items_as_ordered_dict
                    self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % selected_market_name)
                    for outcm in range(len(outcomes)):
                        outcome_name, outcome = list(outcomes.items())[outcm]
                        outcome.scroll_to()
                        if not outcome.is_non_runner and not event.has_race_off():
                            is_silk_generic = wait_for_result(lambda: outcome.is_silk_generic, timeout=5)
                            if outcome.silk:
                                self.assertTrue(outcome.has_bespoke_silks, msg=f'Bespoke silk is not displayed for the horse: "{outcome_name}"')
                            if is_silk_generic is True:
                                self.assertTrue(outcome.has_silks, msg=f'Silk is not appeared for generic outcome: "{outcome_name}"')
                                font_size = outcome.css_property_value('font-size')
                                self.assertTrue(font_size, msg='font size is not verified')
                                font_family = outcome.css_property_value('font-family')
                                self.assertTrue(font_family, msg='font family is not verified')
                                font_weight = outcome.css_property_value('font-weight')
                                self.assertTrue(font_weight, msg='font weight is not verified')
                                font_color = outcome.css_property_value('color')
                                self.assertTrue(font_color, msg='font color is not verified')
                                break
                            elif outcm == len(outcomes) - 1:
                                self.device.go_back()
                                self.site.wait_splash_to_hide(5)
                                sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(self.uk_and_ire_type_name)
                                sections.scroll_to()
                                meetings = sections.items_as_ordered_dict
                                meeting = list(meetings.values())[mtng]
                                events = meeting.items_as_ordered_dict
                                break
                if is_silk_generic is True:
                    break
            if is_silk_generic is True:
                break
        if is_silk_generic is None:
            self._logger("'No events found with expected outcome in 'UK AND IRISH RACES' ")
            exit()

    def test_003_verify_css_of_generic_silk(self):
        """
        DESCRIPTION: Verify CSS of generic silk
        EXPECTED: TBD
        """
        # Covered in step2
