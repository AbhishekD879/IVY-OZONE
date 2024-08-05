import { IARC } from "@app/client/private/models/arcConfig.model";

export const ArcConfigurationValues: IARC = {
    items: [{
        profile: '',
        modelRiskLevel: '',
        reasonCode: '',
        sportsActions: [],
        frequency: '0',
        enabled: false,
        brand: ''
    }],
};

export const ArcConfigurationConstants = {
    labels: {
        arcconfguration: 'ARC Configurations',
        modelandrisk: 'Model and RiskLevel',
        ModeEdit: 'mode_edit',
        profile: 'Profile',
        arcConfig: 'ARC Config',
        EditTable: 'Edit Profile',
        EndEditTable: 'End Edit Profile',
        AddCircle: 'add_circle',
        AddProperty: 'Add Profile',
        MOH: 'Reason Code',
        sportsActions: 'Sport Actions',
        Frequency: 'Frequency',
        Message: 'Message',
        Action: 'Action',
        SRNo: 'SR No',
        RemoveCircle: 'remove_circle',
        CheckCircle: 'check_circle',
        SaveChanges: 'Save changes',
        Toggle: 'Enabled',
        SpecialPagesURL: 'special-pages/arc-configurations'
    },
    messages: {
        removePropertyPromptMsg: 'Are You Sure You Want to Remove This Profile?',
        removePropertyTitle: 'Remove Profile from Group',
        configTitle: 'ARC Configuration',
        configUpdateMsg: 'ARC Configuration is updated.',
        configSaveMsg: 'ARC Configuration is Saved.'
    },
    placeholders: {
        SRNo: 'SR NO',
        modelRiskLevel: 'Model and RiskLevel',
        reasonCode: 'ReasonCode',
        profile: 'Profile',
        sportsActions: 'Sport Actions',
        frequency: 'Frequency',
        enabled: 'Enable',
        message: 'Message Content'
    },
    actions: {
        Save: 'save',
        Revert: 'revert',
        Remove: 'remove',
    },
    errors: {
        UnhandledAction: 'Unhandled Action',
        CheckAction: 'Select any value',
        SportsMessage: 'Select atleast one sports action',
        ProfileError: 'Enter unique profile'
    },
    data: {
        MR: ['2 - Problem Gambler Low', '3 - Problem Gambler  Medium', '4 - Problem Gambler High', '5 - Problem Gambler V High', '6 - At Risk Low', '7 - At Risk Medium', '8 - At Risk High'],
        MOH: ['1 - Difference in spend from norm', '2 - Frequency of play', '3 - Frequency of play increase', '4 - Deposit frequency', '5 - Declined deposits', '6 - Multiple payment methods', '7 - Credit Cards', '8 - Cancelled withdrawals', '9 - Late night play', '10 - Speed of Play', '11 - Chaotic Play', '12 - Deposit Amount', '13 - Tenure*', '14 - In Session TopUp*', '15 - Variety of Games*', '16 - Frequency of Play TOSL7D', '17 - Player days'],
        Sports: [
            { action: 'Homepage & landing pages', messagingContent: '', gcLink: '', enabled: false },
            { action: 'Betslip', messagingContent: '', gcLink: '', enabled: false },
            { action: 'Betreceipt', messagingContent: '', gcLink: '', enabled: false },
            { action: 'My Bets', messagingContent: '', gcLink: '', enabled: false },
            { action: 'Quick bet removal', messagingContent: '', gcLink: '', enabled: false },
            { action: 'Gaming cross sell removal', messagingContent: '', gcLink: '', enabled: false }
        ]
    }
};