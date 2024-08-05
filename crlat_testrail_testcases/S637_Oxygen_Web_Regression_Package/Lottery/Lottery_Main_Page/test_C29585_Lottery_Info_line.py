import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.lotto
@vtest
class Test_C29585_Lottery_Info_line(Common):
    """
    TR_ID: C29585
    NAME: Lottery Info line
    DESCRIPTION: This Test Case verifies Lottery Info line data.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: BMA-2308 'Lottery - Select a lottery'
    DESCRIPTION: BMA-7413 'Lotto - info line'
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   'bet until' date and time = 'shutAtTime' for the next from current date and time 'draw_id' for selected lottery
    """
    keep_browser_open = True

    def test_001_tap_on_lotto_icon_from_sportsmenu_ribbonor_a_z_page(self):
        """
        DESCRIPTION: Tap on 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: 'Lotto' page is opened
        """
        pass

    def test_002_tap_on_any_lotto_icon_within_lottery_selector_carousel(self):
        """
        DESCRIPTION: Tap on any 'Lotto' icon within Lottery Selector Carousel
        EXPECTED: *   Each Lottery has Info line in between the lottery selector and Numbers Selector Module
        EXPECTED: *   Info line shows the name of the Lottery and time left for the next draw
        EXPECTED: *   Lottery info line should be in the following format:
        EXPECTED: **'Description' + "- **bet until**" + **"shutAtTime"
        EXPECTED: e.g. **Spanish Lottery** - bet until: 2/12/2015 19:45
        EXPECTED: The date, time and format is displayed in GMT/UK:
        EXPECTED: *   Date format: DD/MM/YYYY
        EXPECTED: *   Time format: HH:MM 24 hour clock (00:00 - 23:59)
        EXPECTED: *   Count down is in a next line (omit days if there is 0 day, omit hours if there is 0 hour left)
        EXPECTED: *   Omit '0', if left time is one-digit figure
        EXPECTED: *   'Information' icon is displayed in the right side of info line
        """
        pass

    def test_003_tap_on_information_icon(self):
        """
        DESCRIPTION: Tap on 'Information' icon
        EXPECTED: User is redirected to the following URL:
        EXPECTED: https://coral-eng.custhelp.com/app/answers/detail/a_id/1823/kw/lottery
        """
        pass

    def test_004_tap_on_different_lotteries_and_repeat_step_2_3(self):
        """
        DESCRIPTION: Tap on different Lotteries and repeat step №2-3
        EXPECTED: 
        """
        pass
