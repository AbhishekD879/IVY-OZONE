export const SIGNPOSTING_MESSAGES = {
    LIMITED_AVAILABILITY: 'LIMITED AVAILABILITY',
    SOLD_OUT: 'SOLD OUT',
    ENDING_SOON: 'ENDING SOON',
    ENDED: 'ENDED',
    ENDING_IN: 'EXPIRES IN',
    MAX_PURCHASED: 'MAX PURCHASED'
};

export const BETPACK_PLACEHOLDER = {
    LIMIT: '<userLimit>',
    MAX_CLAIMS: '<max-claims>',
    TOKEN_COUNT:'**count**'
};
export const PX='px';

export const BetPack='Bet Pack'

export const BETPACK_STATICTEXT = {
    INBETTOKENS: 'IN BET TOKENS',
    UNLIMITED: 'unlimited',
    LIMITPARAMS_ACTIVELIMITS: 'activeLimits',
    COLORWHITE: '#FFFFFF'
};

export const BETPACK_STORAGE_KEY: string = 'betpackData';

export const BETPACKOFFER = [{
    "freebetOfferId": "37505",
    "freebetOfferName": "Samurais Test Demo offer",
    "freebetOfferLimits": {
        "limitEntry": {
            "limitId": 379475,
            "limitSort": "OFFER_MAX_CLAIMS_LIMIT",
            "limitRemaining": 0,
            "limitDefinition": {
                "limitComponent": {
                    "limitParam": [
                        {
                            "name": "current",
                            "value": 5
                        },
                        {
                            "name": "threshold",
                            "value": 5
                        }
                    ]
                }
            }
        }
    }
},{
    "freebetOfferId": "37506",
    "freebetOfferName": "Samurais Test Demo offer"
},{
    "freebetOfferId": "37507",
    "freebetOfferName": "Samurais Test Demo offer",
    "freebetOfferLimits": {
    }
},
{
    "freebetOfferId": "37508",
    "freebetOfferName": "Samurais Test Demo offer",
    "freebetOfferLimits": {
        "limitEntry": {
            "limitId": 379475,
            "limitSort": "OFFER_MAX_CLAIMS_LIMIT"
        }
    }
}
];

export const ACCOUNT_LIMIT = {
    "response": {
        "model": {
            "activeLimits": {
                "limitEntry": {
                    "limitSort": "BETPACK_DAILY_CUST_LIMIT",
                    "limitRemaining": 1,
                    "limitResetTime": "2022-09-20 23:59:59",
                    "limitDefinition": {
                        "limitComponent": {
                            "limitParam": [
                                {
                                    "name": "current",
                                    "value": 0
                                },
                                {
                                    "name": "threshold",
                                    "value": 1
                                }
                            ]
                        }
                    }
                }
            },

        },
    }
}
