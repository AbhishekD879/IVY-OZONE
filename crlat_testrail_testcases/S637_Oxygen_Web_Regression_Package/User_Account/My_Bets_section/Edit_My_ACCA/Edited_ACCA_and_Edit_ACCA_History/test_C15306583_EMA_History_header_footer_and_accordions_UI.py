import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C15306583_EMA_History_header_footer_and_accordions_UI(Common):
    """
    TR_ID: C15306583
    NAME: EMA History: header, footer and accordions UI
    DESCRIPTION: This test case verifies UI of the header, footer and accordions within EMA history overlay
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Coral TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Ladbrokes TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+OpenBet+System
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have 2 edited bets: 1) Bet edited only once; 2) Bet edited twice or more; 3) Edited Bet where are selections are from resulted events.
    """
    keep_browser_open = True

    def test_001___load_the_application_and_tap_my_bets__open_bets__tap_edit_acca_history_button_under_the_edited_bet__verify_accordions_state_and_ui_elements_of_the_header_footer_and_accordion(self):
        """
        DESCRIPTION: - Load the application and tap 'My Bets' > 'Open Bets'
        DESCRIPTION: - Tap 'Edit Acca History button' under the edited bet
        DESCRIPTION: - Verify accordions state and UI elements of the header, footer and accordion
        EXPECTED: Edit Acca history overplay is opened
        EXPECTED: **Header UI:**
        EXPECTED: - 'Edit Acca History' title in bold
        EXPECTED: - 'X' button on the right side of the header
        EXPECTED: **Coral**
        EXPECTED: - Blue background
        EXPECTED: **Ladbrokes**
        EXPECTED: - White background
        EXPECTED: **Accordions state and UI:**
        EXPECTED: - If bet was edited only once - accordion is expanded by default
        EXPECTED: - If bet was edited more then once - accordions are collapsed by default
        EXPECTED: - Accordions are ordered by acca edit date (latest at the bottom)
        EXPECTED: - Accordions have down arrow on the right side while they are collapsed
        EXPECTED: - No arrow on the right side of the accordion while it is expanded
        EXPECTED: - Grey background
        EXPECTED: - Acca name in upper case written with black color text
        EXPECTED: - Description 'Original Bet' with date and time in format 'hh:mm - dd mmm' (e.g. 19:42 - 08 Feb)
        EXPECTED: - All other edited acca accordions have description 'Edited Bet' with date and time in format 'hh:mm - dd mmm' (e.g. 19:42 - 08 Feb)
        EXPECTED: **Footer UI:**
        EXPECTED: - Stake and Returns titles with their values (e.g. Stake: £1.00 | Returns: £1.00)
        EXPECTED: - For Coral: Only Returns value is displayed in bold; For Ladbrokes Stake and Returns values are displayed in bold
        EXPECTED: - 'Bet Receipt:' <Bet_Receipt_Id>
        EXPECTED: - Date and time in format 'hh:mm - dd mmm' (e.g. 19:45 - Nov) on the right side
        EXPECTED: - 'CASH OUT HISTORY' title (For Ladbrokes it's displayed in bold)
        EXPECTED: - 'Stake used:' in bold and stake value on the right side (e.g. £1.00)
        EXPECTED: - 'Cashed out:' in bold and stake cash out value on the the right side (e.g. £1.00)
        EXPECTED: - '*£<Cashout_value> cash out used to edit your bet'
        """
        pass

    def test_002___close_the_ema_history_overlay_and_go_to_my_bets__settled_bets__tap_edit_acca_history_button_under_the_bet_with_selections_from_resulted_events__verify_accordions_state_and_ui_elements_of_the_header_footer_and_accordion(self):
        """
        DESCRIPTION: - Close the EMA history overlay and go to 'My Bets' > 'Settled Bets'
        DESCRIPTION: - Tap 'Edit Acca History button' under the bet with selections from resulted events
        DESCRIPTION: - Verify accordions state and UI elements of the header, footer and accordion
        EXPECTED: Edit Acca history overplay is opened
        EXPECTED: **Header UI:**
        EXPECTED: - 'Edit Acca History' title in bold
        EXPECTED: - 'X' button on the right side of the header
        EXPECTED: **Coral**
        EXPECTED: - Blue background
        EXPECTED: **Ladbrokes**
        EXPECTED: - White background
        EXPECTED: **Accordions state and UI:**
        EXPECTED: - If bet was edited only once - accordion is expanded by default
        EXPECTED: - If bet was edited more then once - accordions are collapsed by default
        EXPECTED: - Accordions are ordered by acca edit date (latest at the bottom)
        EXPECTED: - Accordions have down arrow on the right side while they are collapsed
        EXPECTED: - No arrow on the right side of the accordion while it is expanded
        EXPECTED: - Grey background
        EXPECTED: - Acca name in upper case written with black color text
        EXPECTED: - Description 'Original Bet' with date and time in format 'hh:mm - dd mmm' (e.g. 19:42 - 08 Feb)
        EXPECTED: - All other edited acca accordions have description 'Edited Bet' with date and time in format 'hh:mm - dd mmm' (e.g. 19:42 - 08 Feb)
        EXPECTED: **Footer UI:**
        EXPECTED: - Stake and Returns titles with their values (e.g. Stake: £1.00 | Returns: £1.00)
        EXPECTED: - For Coral: Only Returns value is displayed in bold; For Ladbrokes Stake and Returns values are displayed in bold
        EXPECTED: - 'Bet Receipt:' <Bet_Receipt_Id>
        EXPECTED: - Date and time in format 'hh:mm - dd mmm' (e.g. 19:45 - Nov) on the right side
        EXPECTED: - 'CASH OUT HISTORY' title (For Ladbrokes it's displayed in bold)
        EXPECTED: - 'Stake used:' in bold and stake value on the right side (e.g. £1.00)
        EXPECTED: - 'Cashed out:' in bold and stake cash out value on the the right side (e.g. £1.00)
        EXPECTED: - '*£<Cashout_value> cash out used to edit your bet'
        """
        pass
