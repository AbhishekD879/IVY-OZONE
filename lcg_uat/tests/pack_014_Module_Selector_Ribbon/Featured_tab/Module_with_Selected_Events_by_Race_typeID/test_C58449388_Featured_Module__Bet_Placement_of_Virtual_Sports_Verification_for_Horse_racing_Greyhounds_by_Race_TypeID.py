import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58449388_Featured_Module__Bet_Placement_of_Virtual_Sports_Verification_for_Horse_racing_Greyhounds_by_Race_TypeID(BaseBetSlipTest, BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C58449388
    NAME: Featured Module - Bet Placement of Virtual Sports Verification for Horse racing/Greyhounds by <Race> TypeID
    DESCRIPTION: This test case verifies bet placement on Virtual Horses/Greyhounds from Featured module.
    PRECONDITIONS: Login with user account that has positive balance.
    """
    keep_browser_open = True

    def test_001_load_application_and_reach_featured_module_on_the_home_page(self):
        """
        DESCRIPTION: Load application and reach "Featured module" on the Home Page.
        EXPECTED:
        """
        params = self.ob_config.add_virtual_racing_event(number_of_runners=3)
        self.eventID = params.event_id
        self.__class__.selection_name, self.__class__.selection_id = list(params.selection_ids.items())[0]
        self.__class__.selection_name1, self.__class__.selection_id1 = list(params.selection_ids.items())[1]
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection',
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
            show_expanded=False,
            id=self.selection_id)['title'].upper()
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection',
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
            show_expanded=False,
            id=self.selection_id1)['title'].upper()
        self.site.wait_content_state('Homepage')
        self.site.login()

    def test_002_find_virtual_horsesgreyhounds_event_and_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Find Virtual Horses/Greyhounds event and add selection to the Betslip.
        EXPECTED: Selected 'Price/Odds' buttons are highlighted in green
        EXPECTED: Betslip counter is increased.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.assertEqual(self.get_betslip_content().selections_count, '1',
                         msg=f'Selections count "{self.get_betslip_content().selections_count}" '
                         f'is not the same as expected "6"')

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selections with bet details are displayed in the Betlsip
        EXPECTED: Selections are present in Section 'Singles (2)'
        EXPECTED: 'Multiples(1)' section contains multiples calculated based on added selections
        """
        self.place_single_bet()

    def test_004_set_stake_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Set "Stake" and tap 'Place Bet' button
        EXPECTED: Bet is placed
        EXPECTED: Bet receipt appears in Betslip
        EXPECTED: 'Reuse selections' and 'Go Betting' buttons are present in footer.
        """
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')
        self.assertTrue(self.site.bet_receipt.footer.reuse_selection_button.is_displayed(),
                        msg='"Reuse Selection" button isn\'t present')
