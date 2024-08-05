import { IFAQ } from '@app/five-a-side-showdown/models/frequently-asked-questions';

export const FAQ_TABLE_COLUMNS = [
    {
        name: 'Question',
        property: 'question',
        link: {
            hrefProperty: 'id',
            path: 'add-edit'
        },
        type: 'link',
        width: 10
    }
];

export const FAQ_ROUTES = {
  base: '/five-a-side-showdown/faq',
};

export const FILTER_PROPERTIES = ['question'];

export const FAQ_DEFAULT_VALUS: IFAQ = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: null,
    question: null,
    answer: null
};

export const FAQ_SNACKBAR = {
    message: 'New FAQ Order Saved!!',
    action: 'OK!'
};

export const FAQ_ERROR_LABELS = {
    getFAQs: 'Error in fetching the list of FAQs',
    getFAQ: 'Error in fetching the FAQ',
    createFAQ:  'Error while creating the FAQ',
    editFAQ: 'Error in editing FAQ',
    removeFAQ: 'Error in removing FAQ',
    reorderFAQs: 'Error in reordering the FAQs'
};

export const REMOVE_CONFIRMATION_DIALOG = {
    title: 'Remove FAQ',
    message: 'Are You Sure You Want to Remove FAQ'
};

export const REMOVE_NOTIFICATION_DIALOG = {
    title: 'Remove Completed',
    message: 'FAQ is Removed.'
};

export const BREADCRUMBS_LABEL = 'FAQ';

export const ACTION_TYPE = {
    remove: 'remove',
    save: 'save',
    revert: 'revert'
};

export const SAVE_NOTIFICATION_DIALOG = {
    title: 'FAQ Saving',
    message: 'FAQ is Saved.'
};

export const FAQFORM = {
    faqLabel: 'FAQ',
    questionLabel: 'Question',
    answerLabel: 'Answer'
};

export const FAQ_LIST_FORM = {
    headerLabel: 'FAQs',
    subHedaerLabl: 'FAQs for Choosen Brand',
    createFAQLabel: 'Create FAQ'
};
