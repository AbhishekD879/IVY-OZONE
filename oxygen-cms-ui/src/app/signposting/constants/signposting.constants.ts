export const SignpostingConstants = {
    FREEBET_SIGNPOSTING: 'Freebet Signposting',
    FREEBET_SIGNPOSTS: 'Freebet Signposts',
    CREATE_NEW_SIGNPOSTING: 'Create Signposting',
    EDIT_SIGNPOSTING: 'Edit Signposting:',
    SAVE_CHANGES: 'Save Changes',
    CREATE_SIGNPOSTING: 'Create signposting',
    THRESHOLD_VALUE: 'Threshold value',
    MESSAGE_DISPLAY: 'Message display',
    REVERT_CHANGES: 'Revert Changes',
    ERROR_MESSAGE: '*This property should not exceed 100 characters',
    REMOVE: 'Remove',
    TITLE: 'Title',
    THRESHOLD_TYPE: 'Threshold type',
    DECIMAL: 'Decimal',
    FRACTION: 'Fraction'
}

export const defaultSignpostingData = {
    id: '',
    createdBy: '',
    createdByUserName: '',
    updatedBy: '',
    updatedByUserName: '',
    createdAt: '',
    updatedAt: '',
    sortOrder: 0,
    brand: 'bma',
    freeBetType: '',
    fromOffer: '',
    betConditions: '',
    sport: '',
    event: '',
    market: '',
    price: {
        priceType: 'decimal',
        priceNum: null,
        priceDen: null,
        priceDec: null
    },
    signPost: '',
    disabled: true,
    isActive: true,
    title: ''
}

export enum selectThresholdTypes {
    Decimal = 'decimal',
    Fractional = 'fractional'
}