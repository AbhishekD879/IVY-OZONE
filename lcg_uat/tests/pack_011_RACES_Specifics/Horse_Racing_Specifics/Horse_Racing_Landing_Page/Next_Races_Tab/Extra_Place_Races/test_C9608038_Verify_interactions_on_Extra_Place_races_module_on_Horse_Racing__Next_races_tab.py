import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # Cannot create Extra place races on prod/hl
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.mobile_only
@vtest
class Test_C9608038_Verify_interactions_on_Extra_Place_races_module_on_Horse_Racing__Next_races_tab(BaseRacing):
    """
    TR_ID: C9608038
    VOL_ID: C17518536
    NAME: Verify interactions on 'Extra Place' races module on Horse Racing > 'Next races' tab
    DESCRIPTION: This test case verifies clicks on 'View' link, 'Extra Place' main content area and 'Extra Place' signposting icon
    """
    keep_browser_open = True
    event_level_flag, market_level_flag = 'EVFLAG_EPR', 'MKTFLAG_EPR'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. "Next Races" tab for Horse Racing EDP should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
        PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
        PRECONDITIONS: 3. User is viewing 'Next Races' tab on Horse Racing EDP
        PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
        PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
        PRECONDITIONS: - HR event should have a primary market 'Win or Each Way'
        PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
        PRECONDITIONS: **To check info regarding event use the following link:**
        PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
        PRECONDITIONS: where,
        PRECONDITIONS: X.XX - current supported version of OpenBet release
        PRECONDITIONS: ZZZZ - an event id
        PRECONDITIONS: **To configure 'Extra Place' signposting icon:**
        PRECONDITIONS: 1) Open CMS -> Promotions ->  EXTRA PLACE RACE (if promotion is configured in another case use the instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Promotions+CMS+configuration).
        PRECONDITIONS: 2) Required fields for CMS configuration of created EXTRA PLACE RACE promotion:
        PRECONDITIONS: * 'Is Signposting Promotion' checkbox (should be checked for activation Promo SIgnposting for different promotions)
        PRECONDITIONS: * 'Event-level flag' field
        PRECONDITIONS: * 'Market-level flag' field
        PRECONDITIONS: * 'Overlay BET NOW button url' field (not required but without current URL 'BET NOW' button will be unclickable)
        PRECONDITIONS: * 'Promotion Text' field (for editing promo footer text / not required)
        """
        extra_place_race_event = self.ob_config.add_UK_racing_event(time_to_start=5,
                                                                    market_extra_place_race=True,
                                                                    number_of_runners=1,
                                                                    lp_prices=['1/2'])
        self.__class__.extra_place_race_event_name = f'{extra_place_race_event.event_off_time} ' \
            f'{self.horseracing_autotest_uk_name_pattern}'

        self.navigate_to_page(name='horse-racing')

        tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
        self.assertTrue(tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')

    def test_001_tap_on_extra_place_event_content_area(self):
        """
        DESCRIPTION: Tap on 'Extra Place' event content area
        EXPECTED: Event content area is clickable and leads to Race Card of a corresponding event
        """
        extra_place = self.site.horse_racing.next_races.extra_place_module
        event_name_text = extra_place.name
        extra_place.click()
        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, event_name_text,
                         msg=f'Current event name: "{event_title}" '
                         f'does not match with expected: "{event_name_text}"')

    def test_002_navigate_back_to_horse_racing_page_and_tap_on__sign(self):
        """
        DESCRIPTION: Navigate back to Horse Racing page and tap on '>' sign
        EXPECTED: Navigation to Race Card of a corresponding event takes place
        """
        self.site.back_button.click()
        extra_place = self.site.horse_racing.next_races.extra_place_module
        event_name_text = extra_place.name
        extra_place.arrow_icon.click()
        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, event_name_text,
                         msg=f'Current event name: "{event_title}" '
                         f'does not match with expected: "{event_name_text}"')

    def test_003_navigate_back_to_horse_racing_page_and_tap_on_extra_place_signposting_icon(self):
        """
        DESCRIPTION: Navigate back to Horse Racing page and tap on 'Extra Place' signposting icon
        EXPECTED: Respective promo pop-up appears
        """
        self.site.back_button.click()
        self.site.horse_racing.next_races.extra_place_module.extra_place_race.click()

        self.__class__.promo_key = self.cms_config.constants.PROMO_KEY_EPR
        dialog_name = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                          market_level_flag=self.market_level_flag)['popupTitle']
        vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE = vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE.format(dialog_name)

        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE, timeout=2)
        self.assertTrue(self.dialog.name, msg='Extra Place dialog is not shown')
