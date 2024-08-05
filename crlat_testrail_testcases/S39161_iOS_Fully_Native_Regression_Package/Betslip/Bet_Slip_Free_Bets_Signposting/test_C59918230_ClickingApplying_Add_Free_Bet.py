import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C59918230_ClickingApplying_Add_Free_Bet(Common):
    """
    TR_ID: C59918230
    NAME: Clicking&Applying Add Free Bet
    DESCRIPTION: This test case describes Clicking&Applying Add Free Bet behavior
    DESCRIPTION: Designs:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?q=free&sid=5eada1f2d9cc2c193e409814
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea99a214c42b7267ad5f237
    PRECONDITIONS: - user has a free bet available
    PRECONDITIONS: - qualifying selection is added to bet slip
    PRECONDITIONS: - betslip is expanded
    PRECONDITIONS: - free bet is selected
    """
    keep_browser_open = True

    def test_001_click_on_add_free_bet_button(self):
        """
        DESCRIPTION: Click on Add Free Bet Button
        EXPECTED: - Free Bet Overlay closes
        EXPECTED: - Free bet value is added to Total Stake field with Free Bet design
        EXPECTED: -  Signposting is updated to 'Remove Free Bet' button
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/119425551)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/119778923)
        """
        pass

    def test_002_input_additional_value_to_the_bet(self):
        """
        DESCRIPTION: Input additional value to the bet
        EXPECTED: total stake is updated to reflect this using the Free Bet value + Users Stake
        EXPECTED: Ladbrokes:
        EXPECTED: Light mode:
        EXPECTED: ![](index.php?/attachments/get/119778925)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/119778927)
        EXPECTED: Coral:
        EXPECTED: Light mode:
        EXPECTED: ![](index.php?/attachments/get/119778926)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/119778928)
        """
        pass

    def test_003_tap_on_remove_free_bet_button(self):
        """
        DESCRIPTION: Tap on 'remove free bet' button
        EXPECTED: - Free Bet icon on Total stake is removed
        EXPECTED: - Remove Free Bet button is updated to 'Use Free Bet' button where the Free Bet journey restarts
        EXPECTED: ![](index.php?/attachments/get/119425550)
        """
        pass
