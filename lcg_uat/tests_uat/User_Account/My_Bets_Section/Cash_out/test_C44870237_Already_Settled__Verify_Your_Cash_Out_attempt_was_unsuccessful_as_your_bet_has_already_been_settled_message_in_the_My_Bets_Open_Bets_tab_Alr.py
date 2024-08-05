import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870237_Already_Settled__Verify_Your_Cash_Out_attempt_was_unsuccessful_as_your_bet_has_already_been_settled_message_in_the_My_Bets_Open_Bets_tab_Already_Cashedout__Verify_Your_Cash_Out_attempt_was_unsuccessful_as_your_bet_has_already_been_Cashe(Common):
    """
    TR_ID: C44870237
    NAME: "Already Settled - Verify  ""Your Cash Out attempt was unsuccessful as your bet has already been settled."" message in the My Bets > Open Bets tab. Already Cashedout - Verify ""Your Cash Out attempt was unsuccessful as your bet has already been Cashe
    DESCRIPTION: "Already Settled - Verify  ""Your Cash Out attempt was unsuccessful as your bet has already been settled."" message in the My Bets > Open Bets tab.
    DESCRIPTION: Already Cashedout - Verify ""Your Cash Out attempt was unsuccessful as your bet has already been Cashed Out."" message in the My Bets > Open Bets tab .
    DESCRIPTION: Freebet cash-out not allowed  - Verify ""'Bets placed with a free bet or bets triggering a free bet offer cannot be cashed out."" message in the My Bets > Open Bets tab.
    DESCRIPTION: Cash-out not available for certain bet types - Verify 'Cash out is unavailable on this bet.'  message in the My Bets > Open Bets tab.
    DESCRIPTION: SP Selection - Verify 'Bets placed at starting price (SP) cannot be cashed out.'  message in the My Bets > Open Bets tab.
    DESCRIPTION: Cash out from location not allowed  - Verify  'Sorry, we cannot authorise cash out from your location. Please contact us.' message in My Bets > Open Bets tab .
    DESCRIPTION: Account is blocked from cash-out - Verify ''Sorry, we cannot authorise Cash Out from your account. Please contact us if you feel this may be in error' message in My Bets > Open Bets tab .
    DESCRIPTION: Cash-out value is £0.00 - Verify 'Cash Out is unavailable because the offer is less than 0.00' message in My Bets > Open Bets tab
    DESCRIPTION: Cash out no odds available - Verify 'One or more events in your bet are not available for in-play Cash Out.' message in My Bets > Open Bets tab
    DESCRIPTION: In play cash-out not available for some of your selections - Verify 'One or more events in your bet are not available for cash out' message in
    DESCRIPTION: Example: Football and Badminton double, of which only football is available for cash-out
    DESCRIPTION: Load error - Verify 'Cash Out unsuccessful, please try again.' message When user select the cash out button and  an error occurs when loading
    PRECONDITIONS: 
    """
    keep_browser_open = True
