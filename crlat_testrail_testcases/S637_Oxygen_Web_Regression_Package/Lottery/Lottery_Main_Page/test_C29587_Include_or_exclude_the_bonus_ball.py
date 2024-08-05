import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.lotto
@vtest
class Test_C29587_Include_or_exclude_the_bonus_ball(Common):
    """
    TR_ID: C29587
    NAME: Include or exclude the bonus ball
    DESCRIPTION: This Test Case verifies including or excluding of the bonus ball for Lotteries.
    DESCRIPTION: **Jira Ticket:**
    DESCRIPTION: BMA-2319 'Lottery - Include or exclude the bonus ball'
    DESCRIPTION: BMA-7415 'Lotto - bonus ball bug'
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    """
    keep_browser_open = True

    def test_001_tap_on_lotto_icon_from_sports_menu_ribbon_or_a_z_page(self):
        """
        DESCRIPTION: Tap on 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: 'Lotto' page is opened
        """
        pass

    def test_002_tap_on_each_of_the_following_lotteries___ny_lotto___spanish_lotto___irish_lotto___49s_lotto___hong_kong_lotto___singapore_lotto___daily_million___canadian_lotto(self):
        """
        DESCRIPTION: Tap on each of the following Lotteries:
        DESCRIPTION: *   NY Lotto
        DESCRIPTION: *   Spanish Lotto
        DESCRIPTION: *   Irish Lotto
        DESCRIPTION: *   49's Lotto
        DESCRIPTION: *   Hong Kong Lotto
        DESCRIPTION: *   Singapore Lotto
        DESCRIPTION: *   Daily Million
        DESCRIPTION: *   Canadian Lotto
        EXPECTED: *   The Bonus Ball checkbox is displayed for all listed Lotteries under Numbers Selector ribbon.
        EXPECTED: *   'Include Bonus Ball?' label is placed next to checkbox.
        EXPECTED: *   'Include Bonus Ball?' checkbox is NOT ticked by default.
        """
        pass

    def test_003_select_numbers_for_selected_lottery_wheels(self):
        """
        DESCRIPTION: Select numbers for selected Lottery wheels
        EXPECTED: *   Selected numbers are displayed appropriately on wheels
        EXPECTED: *   Odds is displayed according to '**priceNum**' & '**priceDen**' attributes by '**numberCorrect**' that correspond to quantity of numbers selected
        """
        pass

    def test_004_tap_on_the_toggle(self):
        """
        DESCRIPTION: Tap on the toggle
        EXPECTED: *   Selected numbers remain
        EXPECTED: *   The relevant odds for the selected Lottery shoud be displayed according to SS 'name' attribute
        EXPECTED: e.g. New York Lotto:
        EXPECTED: **Toggle OFF: **
        EXPECTED: <lottery id="6" sort="NYL" name="|N.Y. Lotto 6 ball|" description="|N.Y. Lotto|" />
        EXPECTED: <lotteryPrice id="18" lotteryId="6" numberCorrect="3" numberPicks="3" priceNum="1250" priceDen="1" />
        EXPECTED: **Toggle ON:**
        EXPECTED: <lottery id="8" sort="NYL7" name="|N.Y. Lotto 7 ball|" description="|N.Y. Lotto|" />
        EXPECTED: <lotteryPrice id="33" lotteryId="8" numberCorrect="3" numberPicks="3" priceNum="600" priceDen="1" />
        """
        pass

    def test_005_tap_off_the_toggle(self):
        """
        DESCRIPTION: Tap off the toggle
        EXPECTED: *   **"-" **is displayed in each of the Wheels by default
        EXPECTED: *   Toggle default state is displayed (see step 2)
        """
        pass

    def test_006_tap_on_each_of_the_following_lotteries___australian_tattslotto___australian_ozlotto___french_lotto___german_lotto(self):
        """
        DESCRIPTION: Tap on each of the following Lotteries:
        DESCRIPTION: *   Australian Tattslotto
        DESCRIPTION: *   Australian Ozlotto
        DESCRIPTION: *   French Lotto
        DESCRIPTION: *   German Lotto
        EXPECTED: The Bonus Ball checkbox is hidden for the listed Lotteries.
        """
        pass
