import { DataTableColumn } from '@app/client/private/models';
import { RacingEdpMarket } from '@app/client/private/models/racing.edpmarket.model';

export const ACTION_TYPE = {
    remove: 'remove',
    save: 'save',
    revert: 'revert'
};

export const SAVE_CONFIRMATION_DIALOG = {
    title: 'Add New EDP Market Block',
    yesOption: 'Save',
    noOption: 'Cancel'
};

export const SAVE_NOTIFICATION_DIALOG = {
    title: 'Racing EDP Market Saving',
    message: 'Racing EDP Market is Saved.'
};

export const REMOVE_CONFIRMATION_DIALOG = {
    title: 'Remove racing EDP Market',
    message: 'Are You Sure You Want to Remove Racing Edp Market:'
};

export const SNACKBAR = {
    message: 'New Racing Edp Markets Order Saved!!',
    action: 'OK!'
};

export const REMOVE_NOTIFICATION_DIALOG = {
    title: 'Remove Completed',
    message: 'EDP Market is Removed.'
};

export const RACING_EDP_ROUTES = {
    base: '/racing-edp-markets',
};

export const BREADCRUMBS_LABEL = 'RACING EDP MARKETS';

export const RACING_EDP_ERRORS = {
    unhandledAction: 'Unhandled Action',
    createError: 'Can not create Racing EDP market'
};

export const RACING_EDP_TABLE_COLUMNS: Array<DataTableColumn> = [
    {
        name: 'Market Name',
        property: 'name',
        link: {
            hrefProperty: 'id'
        },
        type: 'link'
    },
    {
        name: 'Enabled For Racings',
        property: 'racing'
    }
];

export const FILTER_PROPERTIES = ['name'];

export const RACING_TYPE = {
    horseRacing: 'HR',
    greyHound: 'GH'
};

export const RACING_DEFAULT_VALUS: RacingEdpMarket = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    name: '',
    lang: '',
    description: '',
    brand: null,
    isHR: false,
    isGH: false,
    isNew: false
};
