import { IBadgePath, IEuroMessages, IEuroDisplayMessages } from '@app/euro/models/euro.model';

export const HOW_IT_WORKS: string = 'euro-dialog';
export const EURO_DISPLAY_MESSAGES: IEuroDisplayMessages  = {
    CONGRATULATIONS_MSG: {
        CONGRATS: 'CONGRATULATIONS',
        EARNED: 'You\'ve earned ',
        STAMP: 'You\'ve collected today\'s stamp',
        FREEBET:'$freeBet Free Bet',
        NEXT_DAY: 'Get a reward every 3 days of the tournament you bet',
        MORE_STAMPS: 'Collect 3 more stamps to unlock your next reward'
    },
     FREEBET: {
        REWARD: 'COLLECT A STAMP TODAY',
        QUALIFYING_SINGLE_BET: 'Simply place a ',
        QUALIFYING_MULTIPLE_BET: '$freeBet qualifying bet'
    }
};

export const EURO_MESSAGES: IEuroMessages = {
    TITLE: 'EURO 2020',
    HOW_IT_WORKS: 'How it works',
    FULL_TERMS_AND_COND: 'Full Terms and Conditions',
    TERMS_AND_COND: 'Terms and Conditions',
    ERROR_MESSAGE: 'Something went wrong, please try after sometime',
    ERROR_USER_MESSAGE: 'We\'re sorry, please come back later.',
    HOW_IT_WORKS_DIALOG: 'euro-dialog',
    EURO_BADGE: 'euroBadge',
    FREE_BET: 'FREE BET',
    MOBILE_BADGES_EACH_ROW: 3,
    DESKTOP_BADGES_EACH_ROW: 6,
    ERROR_HOWITWORKS: '<p>Oops! We are having trouble loading this page</p>',
    PROMOTIONS: '/promotions',
    DEFAULT_TOKEN: '5',
    TOTAL_BADGES: 30
};
export const BADGE_COLOR: IBadgePath = {
    BALL_0: '#Ball-0',
    BALL_1: '#Ball-1',
    BALL_2: '#Ball-2',
    BALL_EMPTY: '#Ball-empty'
};


