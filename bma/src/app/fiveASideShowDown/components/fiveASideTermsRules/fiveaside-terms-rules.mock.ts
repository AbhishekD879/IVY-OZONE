import { IFAQ } from '@core/services/cms/models/frequently-asked-question';
import { ITermsAndConditions } from '@core/services/cms/models/terms-and-conditions';

export const FAQS_MOCK: IFAQ[] = [
    {
        'id': '5e6f2f85c9e77c000118b4cc',
        'createdBy': '54905d04a49acf605d645271',
        'createdByUserName': null,
        'updatedBy': '54905d04a49acf605d645271',
        'updatedByUserName': null,
        'createdAt': '2020-03-16T07:49:25.414Z',
        'updatedAt': '2020-03-16T07:49:54.220Z',
        'isExpanded': false,
        'question': 'How Do Showdowns Work?',
        'answer': `Lorem ipsum dolor sit amet, consectetur adipiscing elit,
         sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
          Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
           nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
             Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
              deserunt mollit anim id est laborum`,
        'brand': 'ladbrokes'
    },
    {
        'id': '5e6f2f85c9e77c000118b4cd',
        'createdBy': '54905d04a49acf605d645271',
        'createdByUserName': null,
        'updatedBy': '54905d04a49acf605d645271',
        'updatedByUserName': null,
        'isExpanded': false,
        'createdAt': '2020-03-16T07:49:25.414Z',
        'updatedAt': '2020-03-16T07:49:54.220Z',
        'question': 'What is five a side showdown?',
        'answer': 'Platform to compete with all the users.',
        'brand': 'ladbrokes'
    }
];

export const T_AND_C: ITermsAndConditions = {
    'id': '5e6f2f85c9e77c000118b4cc',
    'createdBy': '54905d04a49acf605d645271',
    'createdByUserName': null,
    'updatedBy': '54905d04a49acf605d645271',
    'updatedByUserName': null,
    'title': 'title',
    'url':'url',
    'createdAt': '2020-03-16T07:49:25.414Z',
    'updatedAt': '2020-03-16T07:49:54.220Z',
    'text': `<p style="width: 100%; margin-top: 12px; margin-bottom: 12px; font-family: Helvetica; font-size: 15px;
     font-weight: bold; color: #e3e3e3;">How Do Showdowns Work?</p>
    <p style="width: 100%; margin-top: 12px; margin-bottom: 36px; font-family: Helvetica; font-size: 13px; color: #e3e3e3;">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
     dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
     sunt in culpa qui officia deserunt mollit anim id est laborum</p>
     <p style="width: 100%; margin-top: 12px; margin-bottom: 12px; font-family: Helvetica; font-size: 15px;
     font-weight: bold; color: #e3e3e3;">How Do Showdowns Work?</p>
    <p style="width: 100%; margin-top: 12px; margin-bottom: 36px; font-family: Helvetica; font-size: 13px; color: #e3e3e3;">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
     dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
     sunt in culpa qui officia deserunt mollit anim id est laborum</p>
     <p style="width: 100%; margin-top: 12px; margin-bottom: 12px; font-family: Helvetica; font-size: 15px;
     font-weight: bold; color: #e3e3e3;">How Do Showdowns Work?</p>
    <p style="width: 100%; margin-top: 12px; margin-bottom: 36px; font-family: Helvetica; font-size: 13px; color: #e3e3e3;">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
     dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
     sunt in culpa qui officia deserunt mollit anim id est laborum</p>
     <p style="width: 100%; margin-top: 12px; margin-bottom: 12px; font-family: Helvetica; font-size: 15px;
     font-weight: bold; color: #e3e3e3;">How Do Showdowns Work?</p>
    <p style="width: 100%; margin-top: 12px; margin-bottom: 36px; font-family: Helvetica; font-size: 13px; color: #e3e3e3;">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
     dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
     sunt in culpa qui officia deserunt mollit anim id est laborum</p>`,
    'brand': 'ladbrokes'
};
