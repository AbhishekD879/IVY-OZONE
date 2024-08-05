import { IBase } from '@app/core/services/cms/models/base.model';

export interface IPrizePool {
    cash: number;
    firstPlace: number;
    tickets: number;
    freeBets: number;
    vouchers: number;
    totalPrizes: number;
    summary: string;
}
export interface IContest extends IBase {
    generatedId: string;
    name: string;
    icon: string;
    startDate: string;
    event: string;
    entryStake: string;
    isFreeBetsAllowed: string;
    prizePool: IPrizePool;
    contestPrizes: string;
    sponsorText: string;
    sponsorLogo: string;
    size: number;
    teams: number;
    description: string;
    blurb: string;
    entryConfirmationText: string;
    nextContestId: string;
    display: boolean;
    testAccount?: boolean;
    realAccount?: boolean;
}
