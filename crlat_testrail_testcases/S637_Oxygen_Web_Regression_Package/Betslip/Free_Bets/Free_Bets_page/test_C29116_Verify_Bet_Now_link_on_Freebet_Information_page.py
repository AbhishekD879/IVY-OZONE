import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29116_Verify_Bet_Now_link_on_Freebet_Information_page(Common):
    """
    TR_ID: C29116
    NAME: Verify 'Bet Now' link on 'Freebet Information' page
    DESCRIPTION: This Test Case verified 'Bet Now' link on 'Freebet Information' page.
    PRECONDITIONS: 1. User is logged in ( freebets list is received in **user** request only after login)
    PRECONDITIONS: 2. **accountFreebets?freebetTokenType=SPORT** request is used to get a list of all free bets and called on 'My Balance &
    PRECONDITIONS: Freebets' page ONLY (open dev tools -> Network ->XHR tab)
    PRECONDITIONS: 3. User have Free Bets available on their account:
    PRECONDITIONS: *Selection lvl
    PRECONDITIONS: *Market lvl
    PRECONDITIONS: *Event lvl
    PRECONDITIONS: *Type lvl
    PRECONDITIONS: *Class lvl
    PRECONDITIONS: *Any
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_my_freebetsbonuses_page(self):
        """
        DESCRIPTION: Navigate to the 'My Freebets/Bonuses' page
        EXPECTED: * My Freebets/Bonuses' page is opened
        EXPECTED: * List of available Freebets is shown
        """
        pass

    def test_003_navigate_to_the_freebet_details_page_for_freebet_what_is_applied_on_the_selection_level(self):
        """
        DESCRIPTION: Navigate to the Freebet Details page for Freebet what is applied on the Selection level
        EXPECTED: * 'Freebet Information' page is opened
        EXPECTED: * Freebet description is present
        EXPECTED: * 'Bet Now' link is present
        """
        pass

    def test_004_clicktap_on_bet_now_link(self):
        """
        DESCRIPTION: Click/Tap on 'Bet Now' Link
        EXPECTED: User is redirected to the relevant <Sport> Event Details page
        """
        pass

    def test_005_repeat_steps_2_4_for_freebet_what_is_applied_on_the_market_level(self):
        """
        DESCRIPTION: Repeat Steps 2-4 for Freebet what is applied on the Market level
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_2_4_for_freebet_what_is_applied_on_the_event_level(self):
        """
        DESCRIPTION: Repeat Steps 2-4 for Freebet what is applied on the Event level
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_the_my_freebetsbonuses_page(self):
        """
        DESCRIPTION: Navigate to the 'My Freebets/Bonuses' page
        EXPECTED: * My Freebets/Bonuses' page is opened
        EXPECTED: * List of available Freebets is shown
        """
        pass

    def test_008_navigate_to_the_freebet_details_page_for_freebet_what_is_applied_on_the_type_level(self):
        """
        DESCRIPTION: Navigate to the Freebet Details page for Freebet what is applied on the Type level
        EXPECTED: * 'Freebet Information' page is opened
        EXPECTED: * Freebet description is present
        EXPECTED: * 'Bet Now' link is present
        """
        pass

    def test_009_clicktap_on_bet_now_link(self):
        """
        DESCRIPTION: Click/Tap on 'Bet Now' Link
        EXPECTED: User is redirected to the relevant <Sport> Landing page
        """
        pass

    def test_010_repeat_steps_7_9_for_freebet_what_is_applied_on_the_class_level(self):
        """
        DESCRIPTION: Repeat steps 7-9 for Freebet what is applied on the Class level
        EXPECTED: 
        """
        pass

    def test_011_navigate_to_the_my_freebetsbonuses_page(self):
        """
        DESCRIPTION: Navigate to the 'My Freebets/Bonuses' page
        EXPECTED: * My Freebets/Bonuses' page is opened
        EXPECTED: * List of available Freebets is shown
        """
        pass

    def test_012_navigate_to_the_freebet_details_page_for_freebet_what_is_applied_on_the_any_level(self):
        """
        DESCRIPTION: Navigate to the Freebet Details page for Freebet what is applied on the 'Any' level
        EXPECTED: * 'Freebet Information' page is opened
        EXPECTED: * Freebet description is present
        EXPECTED: * 'Bet Now' link is present
        """
        pass

    def test_013_clicktap_on_bet_now_link(self):
        """
        DESCRIPTION: Click/Tap on 'Bet Now' Link
        EXPECTED: User is redirected to the Home page
        """
        pass

    def test_014_repeat_steps_12_14_when_the_information_requested_to_ss_is_unavailable_for_any_of_the_freebets_above_old_event_undisplayed_type_etc(self):
        """
        DESCRIPTION: Repeat steps 12-14 when the information requested to SS is unavailable for any of the Freebets above (old Event, undisplayed Type, etc.)
        EXPECTED: User is redirected to the Home page
        """
        pass
