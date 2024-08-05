
import { IMatchDayRewardsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';

export const MATCHDAY_REWARDS_MOCK: IMatchDayRewardsResponse = {
    currentBadgeLocation: 22,
    placedBetToday: false,
    tokenAmount: '5',
    freeBetPositionSequence: [3,6,9,30],
    termsAndConditions: 'terms and conditions string ',
    fullTermsURI: 'sports.coral.co.uk',
    proxyError: {
        code: 0,
        status: 'status',
        error: 'no error',
        message: 'message',
        url: 'error url'
    }
};
