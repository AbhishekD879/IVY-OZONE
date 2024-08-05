import { DataTableColumn, Filename } from '@app/client/private/models';

export const PAY_TABLE_COLUMNS: Array<DataTableColumn> = [
    {
        name: 'Prize Type',
        property: 'type'
    },
    {
        name: 'Prize Value',
        property: 'value'
    },
    {
        name: '% of Field',
        property: 'percentageOfField'
    },
    {
        name: '# of Entries',
        property: 'numberOfEntries'
    },
    {
        name:'Trigger ID',
        property:'freebetOfferId'
    }
];

export const FILTER_PROPERTIES = ['type'];

export const PRIZE_MANAGER_FORM_ERRORS = {
    required: 'This field is required'
};

export const PRIZE_TYPES = [ 'Cash', 'Ticket', 'Voucher', 'FreeBet'];

export const PRIZE_TYPES_MAPPER = {
    CASH: 'Cash',
    TICKET: 'Ticket',
    VOUCHER: 'Voucher',
    FREEBET: 'FreeBet'
}

export const DEFAULT_FILENAME = {
    originalname: ''
} as Filename;

export const SUPPORTED_FILE_TYPES = ['image/svg', 'image/svg+xml'];

export const SVG_ERROR_NOTIFICATION = {
    title: `Error. Unsupported file type.`,
    message: `Supported 'svg' files only.`
};

export const ADD_PRIZE_DIALOG = {
    title: 'Add New Prize',
    yesOption: 'Save',
    noOption: 'Cancel'
};

export const EDIT_PRIZE_DIALOG = {
    title: 'Edit Prize',
    yesOption: 'Save',
    noOption: 'Cancel'
};

export const REMOVE_PRIZE_DIALOG = {
    title: 'Remove Prize',
    message: `Are You sure You want to remove whole prize Entry`,
};

export const PRIZE_ERROR_LABELS = {
    getPrizeList: 'Error in fetching the list of prizes for contest',
    createPrize:  'Error while creating the prize for contest',
    editingPrize: 'Error in editing prize for contest',
    removingPrize: 'Error in removing prize for contest'
};

export const ICON_FILE = 'iconFile';

export const SIGNPOSTING_FILE = 'signPostingFile';

export const ICON_PROPERTIES = {
  OUTPUT: 'prizeIcon',
  INPUT: 'icon'
};

export const SIGNPOSTING_PROPERTIES = {
   OUTPUT: 'prizeSignposting',
   INPUT: 'signPosting'
};

export const PRIZE_DEFAULT_VALUES = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    prizeIcon: null,
    prizeSignposting: null,
    brand: null,
    freebetOfferId: null
};

export const PRIZE_FORM = {
    typeLabel: 'Prize Type',
    valueLabel: 'Prize Value',
    textLabel: 'Prize Text',
    iconLabel: 'Prize Icon',
    signpostingLabel: 'Prize Signposting',
    percentageLabel: '% of Field',
    numberOfEntries: '# of Entries',
    freebetOfferId: 'Trigger ID'
};
