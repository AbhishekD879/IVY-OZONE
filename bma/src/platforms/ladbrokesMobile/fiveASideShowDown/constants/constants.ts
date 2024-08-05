import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';

export const RULES_TABS: ITab[] = [{
      id: 'pay-table',
      label: 'Pay Table',
      title: 'Pay Table',
      isFiveASideNewIconAvailable: false,
      url: ''
    }, {
      id: 'faqs',
      label: 'FAQs',
      title: 'FAQs',
      isFiveASideNewIconAvailable: false,
      url: ''
    }, {
      id: 'terms-and-conditions',
      label: 'T&C’s',
      title: 'T&C’s',
      isFiveASideNewIconAvailable: false,
      url: ''
    }
  ];

  export const REMOVE_ELEMENTS = ['.back-btn', '.build-btn', '.rules-btn'];
