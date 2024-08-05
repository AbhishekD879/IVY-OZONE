import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.cms
@pytest.mark.horseracing
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.desktop
@pytest.mark.low
@vtest
class Test_C1108081_Verify_Next_Races_Header_And_Race_Time(BaseRacing):
    """
    TR_ID: C1108081
    NAME: Verify 'Next Races' Header & Race Time
    DESCRIPTION: This test case if for checking the correctness of 'Next Races' module header and race time.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: AUTOTEST [C10791965]
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To control Events displaying in the Next Races Widget on the Horse Racing page, go to **CMS**  -> Tap '**System-configuration**' -> **NEXTRACES**
    PRECONDITIONS: To load CMS use the next link: CMS_ENDPOINT/keystone/structure where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 2) To retrieve all events by class id included in the module use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:YY&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY is a comma separated list of Class id's(e.g. 97 or 97, 98);
    PRECONDITIONS: YY - sport category id (Horse Racing category id = 21)
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) Parameter typeName defines 'Race Meetings' name
    PRECONDITIONS: Parameter 'startTime' defines event start time (note, this is not a race local time)
    """
    keep_browser_open = True
    ew_terms = None
    expected_ew_terms = {"ew_places": 2, "ew_fac_num": 1, "ew_fac_den": 8}
    lp = {0: '1/4', 1: '3/8'}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create racing event with Each Way terms
        PRECONDITIONS: Load Oxygen app
        """
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, ew_terms=self.expected_ew_terms,
                                                          lp_prices=self.lp, cashout=True, time_to_start=1)
        self.__class__.event_off_time = event_params.event_off_time
        self.__class__.event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern}'.upper()

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * <Horse Racing> landing page is opened
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' module is displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as '
                         f'expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

        self.__class__.next_races = self.get_next_races_section()

    def test_002_verify_next_races_accordion_header(self):
        """
        DESCRIPTION: Verify 'Next Races' accordion header
        EXPECTED: * The title of the Header is 'Next Races' (***Header is CMS controlled & internationalised***)*
        EXPECTED: * The title is displayed on the left side of the accordion
        """
        header_name = self.next_races.name
        self.assertEqual(header_name, self.next_races_title,
                         msg=f'Module title "{header_name}" is not the same as expected "{self.next_races_title}"')

    def test_003_verify_the_next_races_accordion_collapse_expand_state(self):
        """
        DESCRIPTION: Verify the 'Next Races' accordion collapse/expand state
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 1. From default state 'expanded', Next 4 Races’ module should collapse when tapping ( - ) or any other area of the accordion header
        EXPECTED: 2. Next 4 Races’ module should expand back when tapping ( + ) or any other area of the accordion header
        EXPECTED: **For Desktop:**
        EXPECTED: * From default state 'expanded', Next 4 Races’ module collapses when tapping the arrow-down symbol or any other area of the accordion header
        EXPECTED: * Next 4 Races’ module expands back when tapping the arrow-up symbol or any other area of the accordion header
        EXPECTED: Note: The '^' arrow symbol is displayed on the right side of the accordion
        """
        group_header = self.next_races.group_header
        group_header.click()
        self.assertFalse(self.next_races.is_expanded(expected_result=False, timeout=3),
                         msg='Next Races module do not collapse after tapping on accordion header')
        group_header.click()
        self.assertTrue(self.next_races.is_expanded(),
                        msg='Next Races module do not expand after tapping on accordion header')
        if self.brand != 'ladbrokes':
            self.assertTrue(group_header.has_chevron_arrow(), msg='No arrow symbol on the accordion header')

            self.assertTrue(group_header.chevron_arrow.location.get('y') > group_header.location.get('y'),
                            msg='The "^" arrow symbol is displayed on the right side of the accordion')

    def test_004_verify_sub_header(self):
        """
        DESCRIPTION: Verify sub-header
        EXPECTED: * Race sub-header is shown in next format** 'HH:MM EventName' [Example: "1:40 FAKENHAM"]
        EXPECTED: * Cash Out icon is shown on the right if the event has cashoutAvail="Y in SS response
        EXPECTED: * Text IS NOT clickable
        """
        if self.brand != 'ladbrokes':
            self.__class__.event = self.get_event_from_next_races_module(event_name=self.event_name)
            self.assertTrue(self.event.has_cashout_label(), msg='Cashout label are not shown on Next Races carousel event')

    def test_005_verify_each_way_terms_in_sub_header(self):
        """
        DESCRIPTION: Verify each way terms in sub header
        EXPECTED: Each way terms are NOT shown even if  **isEachWayAvailable='true'**
        """
        if self.device_type == 'mobile':
            self.__class__.event = self.get_event_from_next_races_module(event_name=self.event_name)
            self.assertFalse(self.event.has_each_way_terms(expected_result=False),
                             msg='Each Way terms are shown on Next Races carousel event')

    def test_006_verify_event_time_and_name_correctness(self):
        """
        DESCRIPTION: Verify event time and name correctness
        EXPECTED: Event time and name correspond to the **'name'** attribute from the Site Server response
        """
        # checked in previous steps

    def test_007_for_desktop_go_to_the_desktop_homepage___check_next_races_carousel_under_the_in_play_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' carousel under the In-Play widget
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' carousel is shown
        """
        if self.device_type == 'desktop':
            self.site.go_to_home_page()
            self.__class__.next_races = self.site.home.get_module_content(module_name=self.next_races_title)
            self.assertTrue(self.next_races.is_displayed(), msg='"Next Races" carousel is not displayed')

    def test_008_for_desktop_repeat_steps_3__6(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 3 - 6
        """
        # todo: fix in https://jira.egalacoral.com/browse/VOL-3415
        # if self.device_type == 'desktop':
        #     self.test_003_verify_the_next_races_accordion_collapse_expand_state()
        #     self.__class__.next_races = self.site.home.get_module_content(module_name=self.next_races_title)
        #     self.assertTrue(self.next_races, msg=f'There is no "{self.next_races_title}" section')
        #     self.test_004_verify_sub_header()
        #     self.test_005_verify_each_way_terms_in_sub_header()
        #     self.test_006_verify_event_time_and_name_correctness()
