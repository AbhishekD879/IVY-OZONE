import { IEuroLoyalty } from '@app/client/private/models/euroLoyalty.model';

export const EuroLoyaltyConstants = {
    labels: {
        HowItWorksText: 'how-it-works-text',
        HowItWorks: 'How it works*',
        EuroHowItWorks: 'euro-loyalty.how-it-works-text',
        MatchDayRewards: 'Match Day Rewards',
        SpecialPagesURL: 'special-pages/EuroLoyal',
        EuroLoyaltyConfig: 'Euro Loyalty Config',
        RewardsConfig: 'RewardsConfiguration',
        ModeEdit: 'mode_edit',
        EditTable: 'Edit table',
        EndEditTable: 'End Edit table',
        AddCircle: 'add_circle',
        AddProperty: 'Add Property',
        TierNo: 'Tier No.',
        TierName: 'tierName',
        FreebetLocation: 'Freebet Locations',
        OfferIDSequence: 'Offer Ids/Sequence',
        Action: 'Action',
        RemoveCircle: 'remove_circle',
        CheckCircle: 'check_circle',
        SaveChanges: 'Save changes',
        TermsAndConditionsText: 'terms-and-conditions-text',
        TermsAndConditions: 'Terms and Conditions*',
        EuroTermsAndCondtions: 'euro-loyalty.terms-and-conditions-text',
        FullTCUrl: 'Full terms and conditions URL',
        CharLimitForTermsAndConditions: 100
    },
    messages: {
        removePropertyPromptMsg: 'Are You Sure You Want to Remove This Property?',
        removePropertyTitle: 'Remove Property from Group',
        configTitle: 'Euro loyalty Configuration',
        configUpdateMsg: 'Euro loyalty Configuration is updated.',
        configSaveMsg: 'Euro loyalty Configuration is Saved.',
        configRemoveMsg: 'Euro config is removed.',
        removeConfigTitle: 'Remove Completed'
    },
    placeholders: {
        TierNo: 'Tier number',
        Locations: 'Locations',
        OfferIds: 'Offer Ids',
        FullTermsAndConditionsUrl: 'Full terms and conditions Url'
    },
    actions: {
        Save: 'save',
        Revert: 'revert',
        Remove: 'remove',
    },
    errors: {
        UnhandledAction: 'Unhandled Action',
        IntegerErrorMessage: 'Enter only integers',
        PositiveIntegerMessage: 'Enter positive integer',
        OfferIdError: 'Offer ids should be one more than no. of freebet locations',
        CharLimitError: 'Max 100 characters allowed',
        DuplicateMsg: 'Duplicate value'
    }
};

export const EuroLoyaltyValues: IEuroLoyalty = {
    pageName: `EuroLoyal`,
    tierInfo: [{
      tierName: '',
      offerIdSeq: '',
      freeBetPositionSequence: ''
    }],
    howItWorks: '',
    fullTermsURI: '',
    brand: '',
    termsAndConditions: ''
};
