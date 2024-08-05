import { IConfigGroup, IEuroLoyalty, ITierInfo } from '@app/client/private/models/euroLoyalty.model';

export const EUROLOYAL_MOCK: IEuroLoyalty = {
    pageName: `EuroLoyal`,
    tierInfo: [{
        tierName: '3',
        offerIdSeq: '["35904", "35906", "35908", "35909", "35917", "35918", "35919", "35920", "35921", "35922", "35923"]',
        freeBetPositionSequence: '[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]'
    }],
    howItWorks: '<p>Place qualifying bet to get badge for the day</p>',
    fullTermsURI: 'https://hospitality.euro2020.co.uk/match-schedule/',
    brand: 'bma',
    termsAndConditions: '<p>Place qualifying bet to get badge for the day.</p>\n<p>Make sure to come back next day and place bet</p>'
};

export const CONFIGGROUP_MOCK: IConfigGroup = {
    items : [
        {
            tierName: '1',
            offerIdSeq: [11],
            freeBetPositionSequence: [12345, 23456]
        },
        {
            tierName: '2',
            offerIdSeq: [12],
            freeBetPositionSequence: [12245, 23256]
        }
    ]
};

export const NEWCONFIGGROUPSET_MOCK: IConfigGroup = {
    items : [
    {
        tierName: '1',
        offerIdSeq: [11],
        freeBetPositionSequence: [12345, 23456]
    },
    {
        tierName: '3',
        offerIdSeq: [13],
        freeBetPositionSequence: [12345, 23356]
    }
    ]
};

export const NEWCONFIGGROUPSET2_MOCK: IConfigGroup = {
    items : [
        {
            tierName: '1',
            offerIdSeq: [11],
            freeBetPositionSequence: [12345, 23456]
        },
        {
            tierName: '2',
            offerIdSeq: [12],
            freeBetPositionSequence: [12245, 23256]
        }
    ]
};

export const WRONGCONFIG_MOCK: IConfigGroup = {
    items : [
        {
            tierName: '1',
            offerIdSeq: '11',
            freeBetPositionSequence: '12345'
        },
        {
            tierName: '1',
            offerIdSeq: '12',
            freeBetPositionSequence: '12245, 23256, 34567'
        }
    ]
};

export const NEWITEM_MOCK: ITierInfo = {
    tierName: '3',
    offerIdSeq: [13],
    freeBetPositionSequence: [12345, 23356]
};

export const NEWCONFIG_MOCK: IConfigGroup = {
    items: [
        {
            tierName: '1',
            offerIdSeq: [11],
            freeBetPositionSequence: [12345, 23456]
        },
        {
            tierName: '2',
            offerIdSeq: [12],
            freeBetPositionSequence: [12245, 23256]
        },
        {
            tierName: '3',
            offerIdSeq: [13],
            freeBetPositionSequence: [12345, 23356]
        }]
};

export const MESSAGES_MOCK = {
    configTitle: 'Euro loyalty Configuration',
    configUpdateMsg: 'Euro loyalty Configuration is updated.',
    configSaveMsg: 'Euro loyalty Configuration is Saved.',
    configRemoveMsg: 'Euro config is removed.',
    removeConfigTitle: 'Remove Completed'
};

export const OBJECTITEMS_MOCK: ITierInfo[] = [
    {
        tierName: '1',
        offerIdSeq: [324, 532],
        freeBetPositionSequence: [234]
    },
    {
        tierName: '3',
        freeBetPositionSequence: [3, 6, 9],
        offerIdSeq: [35904, 35906, 35908, 35909]
    }
];

export const PROP_MOCK: ITierInfo = {
    tierName: '4',
    offerIdSeq: [3, 5],
    freeBetPositionSequence: [12134, 23455, 23565]
};

