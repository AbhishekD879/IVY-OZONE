import { IBase } from '@app/core/services/cms/models/base.model';
import { ISportEvent } from '@app/core/models/sport-event.model';

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
    icon: IIcon;
    startDate: string;
    event: string;
    entryStake: string;
    isFreeBetsAllowed: string;
    prizePool: IPrizePool;
    contestPrizes: string;
    sponsorText: string;
    sponsorLogo: any;
    realAccount?: boolean;
    testAccount?: boolean;
    maxEntries: number;
    maxEntriesPerUser: number;
    description: string;
    blurb: string;
    entryConfirmationText: string;
    nextContestId: string;
    display: boolean;
    events?: ISportEvent[];
    isInvitationalContest?: boolean;
    isPrivateContest ?: boolean;
    contestSize?: number;
    serviceMsg?: string;
    enableServiceMsg?: boolean;
}

export interface IIcon {
    filename: string;
    originalname: string;
    path: string;
    size: string;
    filetype: string;
    fullPath: string;
    svgId: string;
}
