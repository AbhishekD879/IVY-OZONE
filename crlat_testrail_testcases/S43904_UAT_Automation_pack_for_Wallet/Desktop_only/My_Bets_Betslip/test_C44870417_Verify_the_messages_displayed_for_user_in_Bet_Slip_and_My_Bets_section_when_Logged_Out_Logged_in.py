import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870417_Verify_the_messages_displayed_for_user_in_Bet_Slip_and_My_Bets_section_when_Logged_Out_Logged_in(Common):
    """
    TR_ID: C44870417
    NAME: Verify the messages displayed for user in Bet Slip and My Bets section when Logged Out/Logged in.
    DESCRIPTION: This TC is verify different messages shown in Bet Slip and My Bets section for logged in/out users.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_logged_out_user____verify_user_sees_a_message_prompting_them_to_log_in_when_selected_any_of_the_tabs_within_my_bets_as_below__open_bets_tab_please_log_in_to_see_your_open_bets__cash_out_please_log_in_to_see_your_cash_out_bets__settled_bets_please_log_in_to_see_your_settled_bets(self):
        """
        DESCRIPTION: "LOGGED OUT USER  - Verify user sees a message prompting them to log in when selected any of the tabs within My Bets as below
        DESCRIPTION: - Open Bets tab: 'Please log in to see your Open bets'
        DESCRIPTION: - Cash Out: 'Please log in to see your Cash out bets'
        DESCRIPTION: - Settled Bets: 'Please log in to see your Settled bets'
        EXPECTED: User sees following messages:
        EXPECTED: - Open Bets tab: 'Please log in to see your Open bets'
        EXPECTED: - Cash Out: 'Please log in to see your Cash out bets'
        EXPECTED: - Settled Bets: 'Please log in to see your Settled bets'
        """
        pass

    def test_002_logged_in____verify_user_sees_their_bets_on_the_relevant_tabs_when_they__select_any_of_the_tabs_within_my_bets__cash_out_or_open_bets_tab_as_below_the_header_eg_double__clickable_text__eg_edit_my_acca_if_available_for_the_bet__bet_details__eg_liverpool_96_match_result_liverpool_v_crystal_palace_time__date__clickable_area_chevron_to_navigate_to_the_event_details__footer_with_the_stake_and_potential_returns__cash_out_button_cash_out_tab_only(self):
        """
        DESCRIPTION: LOGGED IN  - Verify user sees their bets on the relevant tabs when they  select any of the tabs within My Bets ( cash out or open bets tab) as below
        DESCRIPTION: -The Header: e.g. Double
        DESCRIPTION: - Clickable text : e.g Edit my ACCA (if available for the bet)
        DESCRIPTION: - Bet details : e.g Liverpool @9/6, Match result, Liverpool v Crystal palace, time & Date
        DESCRIPTION: - Clickable area (chevron) to navigate to the event details
        DESCRIPTION: - Footer with the stake and potential returns
        DESCRIPTION: - Cash out button (Cash Out tab only)
        EXPECTED: Logged In user sees following messages.
        EXPECTED: -The Header: e.g. Double
        EXPECTED: - Clickable text : e.g Edit my ACCA (if available for the bet)
        EXPECTED: - Bet details : e.g Liverpool @9/6, Match result, Liverpool v Crystal palace, time & Date
        EXPECTED: - Clickable area (chevron) to navigate to the event details
        EXPECTED: - Footer with the stake and potential returns
        EXPECTED: - Cash out button (Cash Out tab only)
        """
        pass

    def test_003_no_bets_messages____verify_user_sees__open_bets_tab_you_currently_have_no_open_bets__cash_out_you_currently_have_no_cash_out_bets__settled_bets_you_have_no_settled_bets(self):
        """
        DESCRIPTION: NO BETS MESSAGES  - Verify user sees
        DESCRIPTION: - Open Bets tab: 'You currently have no Open bets'
        DESCRIPTION: - Cash Out: 'You currently have no Cash out bets'
        DESCRIPTION: - Settled Bets: 'You have no Settled bets'
        EXPECTED: Logged in user sees
        EXPECTED: - Open Bets tab: 'You currently have no Open bets'
        EXPECTED: - Cash Out: 'You currently have no Cash out bets'
        EXPECTED: - Settled Bets: 'You have no Settled bets'
        """
        pass

    def test_004_signposting_for_promotions___verify_user_has_bets_available_on_the_cash_out_open_bets_or_settled_bets_tab_and__promotions_are_available_for_any_of_the_bets_on_the_tab_ie_promo_flag_is_ticked_in_obthen_they_should_see_signposting_for_the_available_promotions_up_to_a_maximum_of_two_promos_(self):
        """
        DESCRIPTION: SIGNPOSTING FOR PROMOTIONS - Verify user has bets available on the cash-out, open bets, or settled bets tab and  promotions are available for any of the bets on the tab (i.e promo flag is ticked in OB)
        DESCRIPTION: THEN they should see signposting for the available promotions (up to a maximum of two promos )
        EXPECTED: User is able to see applicable promotion sign postings up to a maximum of two promos.
        """
        pass

    def test_005_server_unavailable_message___verify_user_sees_server_unavailable_message_when_service_for_the_site_is_interrupted_and_they_can_view_and_select_the_existing_reload_cta_button_to_refresh_the_page_as_normal(self):
        """
        DESCRIPTION: SERVER UNAVAILABLE MESSAGE - Verify user sees 'server unavailable' message when service for the site is interrupted and they can view and select the existing 'Reload' cta button to refresh the page as normal."
        EXPECTED: User sees 'server unavailable' message when service for the site is interrupted and they can view and select the existing 'Reload' cta button to refresh the page as normal."
        """
        pass
