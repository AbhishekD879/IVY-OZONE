import pytest
import voltron.environments.constants as vec

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.promotions_banners_offers
@pytest.mark.cms
@vtest
class Test_C884422_Verify_Promo_Icons_on_Race_market_level(BaseRacing):
    """
    TR_ID: C884422
    NAME: Verify Promo Icons on <Race> market level
    DESCRIPTION: This test case verifies promo icons on <Race> event detail pages for the following promotions:
    DESCRIPTION: * Faller’s Insurance (available only for Horse Racing)
    DESCRIPTION: * Beaten by a Length (available for Horse Racing and Greyhounds)
    DESCRIPTION: * Extra Place Race (available only for Horse Racing)
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-34455 Promo/Signposting: Pop-up: Customer no longer sees pop-ups appear as a Footer Banner] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-34455
    PRECONDITIONS: * There have to be <Race> events with each promotion from the list:
    PRECONDITIONS: * Faller’s Insurance (available **ONLY** for Horse Racing)
    PRECONDITIONS: * Beaten by a Length (available for Horse Racing **AND** Greyhounds)
    PRECONDITIONS: * Extra Place Race (available **ONLY** for Horse Racing)
    PRECONDITIONS: * Make sure that there are promotion created in CMS and linked to active signposting promotions (by Market Flags)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * Information about promotions, available for the event, is received in <drilldownTagNames> attribute in SiteServer response for the event
    PRECONDITIONS: **Parameters:**
    PRECONDITIONS: * **MKTFLAG_FI** - Faller's Insurance
    PRECONDITIONS: * **MKTFLAG_BBAL** - Beaten by a Length
    PRECONDITIONS: * **MKTFLAG_EPR**  - Extra Place Race
    PRECONDITIONS: Link to response on TST2 endpoints:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    PRECONDITIONS: For **Ladbrokes**: "Faller’s Insurance" and "Beaten by a Length" promotions should be turned off in CMS (Promotions)
    """
    keep_browser_open = True
    event_level_flags = ['EVFLAG_BBL', 'EVFLAG_EPR']
    market_level_flags = ['MKTFLAG_BBAL', 'MKTFLAG_EPR']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        extra_place_race_dialog_name = self.get_promotion_details_from_cms(
            event_level_flag=self.event_level_flags[1],
            market_level_flag=self.market_level_flags[1])['popupTitle']
        dialog_name = extra_place_race_dialog_name.upper() if self.brand != 'ladbrokes' else \
            extra_place_race_dialog_name
        vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE = vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE.format(dialog_name)

        if self.brand != 'ladbrokes':
            beaten_by_length_dialog_name = self.get_promotion_details_from_cms(
                event_level_flag=self.event_level_flags[0],
                market_level_flag=self.market_level_flags[0])['popupTitle'].upper()
            vec.dialogs.DIALOG_MANAGER_BEATEN_BY_A_LENGTH = vec.dialogs.DIALOG_MANAGER_BEATEN_BY_A_LENGTH.format(beaten_by_length_dialog_name)

        event = self.ob_config.add_UK_racing_event(market_extra_place_race=True, number_of_runners=1,
                                                   ew_terms=self.ew_terms)
        self.__class__.eventID = event.event_id

        if self.brand != 'ladbrokes':
            event_1 = self.ob_config.add_UK_racing_event(market_extra_place_race=True, market_beaten_by_a_length=True,
                                                         number_of_runners=1, ew_terms=self.ew_terms)
            self.__class__.eventID_1 = event_1.event_id

    def test_001_navigate_to_the_race_edp_page_with_extra_place_race_promotion_available(self):
        """
        DESCRIPTION: Navigate to the <Race> EDP Page with **Extra Place Race** promotion available
        EXPECTED: * Promo icon is shown on the same level as 'Each Way: 1/4 Odds - Places 1-2-3-4' (for ex.) placed on the right
        EXPECTED: * Promo icon is shown after CashOut icon (if available)
        EXPECTED: * Promo icon is shown before BPG icon (if BPG is available for current event)
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]

        self.__class__.section_header = market.section_header
        self.assertTrue(self.section_header.promotion_icons.has_extra_place_race(),
                        msg='Extra Place Race promo icon is not shown')
        self.assertTrue(self.section_header.cash_out_label.is_displayed(),
                        msg='Cash Out label not displayed on card header')

        market_width = self.section_header.size["width"]
        extra_place_race_location = self.section_header.promotion_icons.extra_place_race.location.get('x')
        self.assertTrue(market_width / 2 < extra_place_race_location,
                        msg='Extra Place Race icon is not displayed on the right side of market header')

        extra_place_race_coordinates = self.section_header.promotion_icons.extra_place_race.location.get('x')
        cash_out_coordinates = self.section_header.cash_out_label.location.get('x')

        self.assertTrue(extra_place_race_coordinates > cash_out_coordinates,
                        msg=f'Extra Place Race icon is not displayed after Cashout. Extra Place Race coordinates: '
                            f'"{extra_place_race_coordinates}", Cashout coordinates: "{cash_out_coordinates}"')

    def test_002_tap_on_the_extra_place_race_promo_icon(self):
        """
        DESCRIPTION: Tap on the Extra Place Race promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        self.section_header.promotion_icons.extra_place_race.click()
        self.check_promotion_dialog_appearance_and_close_it(expected_title=vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE)

    def test_003_repeat_this_test_case_for_a_race_event_for_which_2_promo_icons_are_available_at_the_same_time(self):
        """
        DESCRIPTION: Repeat this test case for a <Race> event, for which 2 promo icons are available at the same time
        EXPECTED: * Two icons are shown next to each other
        EXPECTED: * Corresponding promo pop up is shown after tapping on each icon
        """
        if self.brand != 'ladbrokes':
            self.navigate_to_edp(event_id=self.eventID_1, sport_name='horse-racing')
            markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(markets, msg='No markets found')
            market = list(markets.values())[0]

            self.__class__.section_header = market.section_header
            self.assertTrue(self.section_header.promotion_icons.has_extra_place_race(),
                            msg='Extra Place Race promo icon is not shown')
            self.assertTrue(self.section_header.promotion_icons.has_beaten_by_a_length(),
                            msg='Beaten by a Length promo icon is not shown')

            market_width = self.section_header.size["width"]
            extra_place_race_location = self.section_header.promotion_icons.extra_place_race.location.get('x')
            self.assertTrue(market_width / 2 < extra_place_race_location,
                            msg='Extra Place Race icon is not displayed on the right side of market header')

            beaten_by_a_length_location = self.section_header.promotion_icons.beaten_by_a_length.location.get('x')
            self.assertTrue(market_width / 2 < beaten_by_a_length_location,
                            msg='Beaten by a Length icon is not displayed on the right side of market header')

            self.section_header.promotion_icons.extra_place_race.click()
            self.check_promotion_dialog_appearance_and_close_it(expected_title=vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE)

            self.section_header.promotion_icons.beaten_by_a_length.click()
            self.check_promotion_dialog_appearance_and_close_it(expected_title=vec.dialogs.DIALOG_MANAGER_BEATEN_BY_A_LENGTH)
