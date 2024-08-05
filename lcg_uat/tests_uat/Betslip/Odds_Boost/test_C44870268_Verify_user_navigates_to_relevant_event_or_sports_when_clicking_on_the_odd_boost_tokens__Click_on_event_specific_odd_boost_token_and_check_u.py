import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from datetime import datetime, timedelta
from time import sleep


# @pytest.mark.prod - This test case is limited to QA2 only because can't create odds boost tokens on prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.odds_boost
@vtest
class Test_C44870268_Verify_user_navigates_to_relevant_event_or_sports_when_clicking_on_the_odd_boost_tokens__Click_on_event_specific_odd_boost_token_and_check_user_navigates_to_particular_event__Click_on_odd_boost_token_which_can_use_for_any_sports_check_user_naviga(Common):
    """
    TR_ID: C44870268
    NAME: "Verify user navigates to relevant event or sports when clicking on the odd boost tokens - Click on event specific odd boost token and check user navigates to particular event. - Click on odd boost token which can use for any sports check user naviga
    """
    keep_browser_open = True

    def validation_of_odds_boost_page(self):
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(odds_boost_sections, msg='"Odds boost sections" are not displayed')
        tokens = odds_boost_sections[1].items_as_ordered_dict.items()
        self.assertTrue(tokens, msg='"Boost token" is not displayed')
        if self.brand == 'bma':
            for token_name, token in tokens:
                if token_name == 'for_at_testing':
                    token.click()
                    sleep(2)
                    break
        else:
            for token_name, token in tokens:
                if token_name == 'automation_offer':
                    token.click()
                    sleep(2)
                    break

    def test_001_verify_user_navigates_to_relevant_event_or_sports_when_clicking_on_the_odd_boost_tokens(self):
        """
        DESCRIPTION: Verify user navigates to relevant event or sports when clicking on the odd boost tokens
        EXPECTED: when clicking on the odd boost tokens user is navigated to relevant event or sports successfully
        """
        # covered in steps 2 and 4

    def test_002_click_on_event_specific_odd_boost_token_and_check_user_navigates_to_particular_event(self):
        """
        DESCRIPTION: Click on event specific odd boost token and check user navigates to particular event.
        EXPECTED: when clicking on the odd boost tokens user is navigated to event specific page (edp)successfully
        """
        self.__class__.username_one = tests.settings.odds_boost_user
        self.site.login(username=self.username_one)
        self.site.close_all_dialogs()
        event = self.ob_config.add_badminton_event_to_autotest_league()
        event_id = event.event_id
        exp_date = datetime.now() + timedelta(hours=4)
        self.ob_config.grant_odds_boost_token(username=self.username_one, level='event',
                                              id=event_id, expiration_date=exp_date)
        self.navigate_to_page('/oddsboost')
        self.validation_of_odds_boost_page()
        event_data = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.assertTrue(event_data, msg=f'Can not get event info with id {event_id} from SiteServe')

    def test_003_click_on_odd_boost_token_which_can_use_for_any_sports_check_user_navigates_to_homepage(self):
        """
        DESCRIPTION: Click on odd boost token which can use for any sports check user navigates to homepage.
        EXPECTED: User is navigated to the homepage
        """
        self.ob_config.grant_odds_boost_token(username=self.username_one)
        self.navigate_to_page('/oddsboost')
        self.site.wait_content_state(vec.odds_boost.PAGE.title.upper())
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())[1]
        token = list(odds_boost_sections.items_as_ordered_dict.values())[0]
        token.click()

    def test_004_click_on_sports_specific_token_and_check_user_navigates_to_particular_sports_landing_page(self):
        """
        DESCRIPTION: Click on sports specific token and check user navigates to particular sports landing page"
        EXPECTED: User is navigated to particular sports landing page
        """
        sport_category_id = self.ob_config.backend.ti.greyhound_racing.category_id
        exp_date = datetime.now() + timedelta(hours=2)
        self.ob_config.grant_odds_boost_token(username=self.username_one, level='category',
                                              id=sport_category_id, expiration_date=exp_date)
        self.navigate_to_page('/oddsboost')
        self.validation_of_odds_boost_page()
        actual_title = self.site.greyhound.header_line.page_title.title
        if self.brand == 'bma':
            self.assertEqual(actual_title, vec.sb.GREYHOUND.upper(),
                             msg=f'Actual title: "{actual_title}" is not equal with the'
                                 f'Expected title: "{vec.sb.GREYHOUND.upper()}"')
        else:
            self.assertEqual(actual_title, vec.sb.GREYHOUND,
                             msg=f'Actual title: "{actual_title}" is not equal with the'
                                 f'Expected title: "{vec.sb.GREYHOUND}"')
