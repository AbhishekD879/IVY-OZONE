import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from time import sleep


# @pytest.mark.tst2 # QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.question_engine
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C58668197_Verify_the_GA_tracking_of_the_CTA_Upsell_button(BaseDataLayerTest):
    """
    TR_ID: C58668197
    NAME: Verify the GA tracking of the CTA Upsell button
    DESCRIPTION: This test case verifies the Google Analytics tracking of the CTA Upsell button.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. The Upsell is configured.
    PRECONDITIONS: 3. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 4. The User is logged in.
    PRECONDITIONS: 5. The User has already played a Quiz.
    PRECONDITIONS: 6. Open DevTools in browser.
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cls.quiz['upsell']['options']['11;21'] = " "
        cms_config.update_question_engine_quiz(quiz_id=cls.quiz['id'], title=cls.quiz['title'],
                                               payload=cls.quiz)

    def get_selectionid(self):
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('No outcomes available')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        selection_Name, selection_ID = list(selection_ids.items())[0]
        return selection_ID

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The User is logged into CMS.
        PRECONDITIONS: 2. The User opens previously created Quiz.
        PRECONDITIONS: 3. Content for Splash page configured before.
        PRECONDITIONS: 4. The User has already played the current game (but the results aren't available yet).
        """
        self.__class__.quiz = self.create_question_engine_quiz()
        self.__class__.selection_ID = self.get_selectionid()
        self.quiz['upsell']['options']['11;21'] = self.selection_ID
        self.cms_config.update_question_engine_quiz(quiz_id=self.quiz['id'], title=self.quiz['title'],
                                                    payload=self.quiz)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, async_close_dialogs=False)
        self.navigate_to_page('footballsuperseries')
        self.site.question_engine.cta_button.click()
        questions = self.site.quiz_home_page.question_container.items_as_ordered_dict.values()
        for question in questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[0].click()
            sleep(4)
        self.site.quiz_page_popup.submit_button.click()

    def test_001_proceed_to_the_results_page(self):
        """
        DESCRIPTION: Proceed to the Results page.
        EXPECTED: The Results page is opened.
        """
        result = self.site.quiz_results_page.latest_tab
        self.assertTrue(result, msg='The Results page is opened')

    def test_002_click_on_the_cta_upsell_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the CTA Upsell button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Betslip',
        EXPECTED: 'eventAction' : 'Add to betslip',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<EVENT NAME>>',
        EXPECTED: 'category': ‘16',
        EXPECTED: 'variant': ‘434',
        EXPECTED: 'brand': 'Match Result',
        EXPECTED: 'dimension60': '11527917',
        EXPECTED: 'dimension61': '<<SELECTION ID>>',
        EXPECTED: 'dimension62': 0,
        EXPECTED: 'dimension63’: 0,
        EXPECTED: 'dimension64': ‘/correct4/after/latest-quiz’,
        EXPECTED: 'dimension65': ‘/correct4',
        EXPECTED: }]
        EXPECTED: }
        EXPECTED: }
        EXPECTED: })
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Betslip',
        EXPECTED: 'eventAction' : 'Add to betslip',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<EVENT NAME>>',
        EXPECTED: 'category': ‘16',
        EXPECTED: 'variant': ‘434',
        EXPECTED: 'brand': 'Match Result',
        EXPECTED: 'dimension60': '11527917',
        EXPECTED: 'dimension61': '<<SELECTION ID>>',
        EXPECTED: 'dimension62': 0,
        EXPECTED: 'dimension63’: 0,
        EXPECTED: 'dimension64': ‘/{sourceId}/after/latest-quiz’,
        EXPECTED: 'dimension65': ‘/{sourceId}',
        EXPECTED: }]
        EXPECTED: }
        EXPECTED: }
        EXPECTED: })
        """
        title = self.site.quiz_results_page.tab_content.upsell.upsell_title
        self.site.quiz_results_page.tab_content.upsell.bet_button.click()
        sleep(3)
        expected_response = {'event': 'trackEvent', 'eventCategory': 'Betslip', 'eventAction': 'Add to betslip',
                             'eventLabel': 'success', 'ecommerce':
                                 {'add': {'products': [
                                     {'name': {title}, 'category': '16', 'variant': '434', 'brand': 'Match Result',
                                      'dimension60': '11527917', 'dimension61': {self.selection_ID}, 'dimension62': 0,
                                      'dimension63': 0,
                                      'dimension64': '/footballsuperseries/after/latest-quiz',
                                      'dimension65': 'banner'}]}}}
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='add to betslip')
        self.assertEqual(expected_response.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{expected_response.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(expected_response.get("eventCategory").upper(), actual_response.get("eventCategory").upper(),
                         msg=f'Expected eventCategory value "{expected_response.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(expected_response.get("eventAction").upper(), actual_response.get("eventAction").upper(),
                         msg=f'Expected eventAction value "{expected_response.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(self.selection_ID, actual_response.get("ecommerce")["add"]["products"][0]["dimension61"],
                         msg=f'Expected dimension61 value "{self.selection_ID}" is not '
                             f'same as actual dimension61 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension61"]}"')
        self.assertEqual(expected_response.get("ecommerce")["add"]["products"][0]["dimension64"].title(), actual_response.get("ecommerce")["add"]["products"][0]["dimension64"].title(),
                         msg=f'Expected dimension64 value "{expected_response.get("ecommerce")["add"]["products"][0]["dimension64"]}" is not '
                             f'same as actual dimension64 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension64"]}"')
        self.assertEqual(expected_response.get("ecommerce")["add"]["products"][0]["dimension65"].title(), actual_response.get("ecommerce")["add"]["products"][0]["dimension65"].title(),
                         msg=f'Expected dimension65 value "{expected_response.get("ecommerce")["add"]["products"][0]["dimension65"]}" is not '
                             f'same as actual dimension65 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension65"]}"')
