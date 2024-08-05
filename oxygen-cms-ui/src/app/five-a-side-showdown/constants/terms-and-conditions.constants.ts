import { ITermsAndConditions } from '@app/five-a-side-showdown/models/terms-and-conditions';

export const TANDC_DEFAULT_VALUS: ITermsAndConditions = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: null,
    text: null,
    title: null,
    url: null
};

export const T_AND_C_FORM = {
    headerLabel: 'Terms and Conditions',
    textLabel: 'Text',
    titleLabel: 'Title',
    urlLabel: 'URL'
};
