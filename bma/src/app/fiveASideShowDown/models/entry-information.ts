import { IPriceRecord } from '@app/fiveASideShowDown/models/IPrize';

export interface IOutCome {
    legprogressdetails?: string;
    isSetteled?: boolean;
    outcomeId: string;
    legSequence?: number;
    statCategory?: string;
    statInfo?: string;
    statValue?: string;
    optaStatValue?: number;
    marketName: string;
    progressPercentage?: number;
    country?: string;
    outcomeName: string;
    title?: string;
    id: string;
    playerId?: string;
    contestantId?: string;
    marketId?: string;
    progressPct?: number;
    statTarget?: string;
    teamName?: string;
    homeAway?: string;
    status?: string;
}

export interface IEntrySummaryInfo {
    rank?: number | string;
    contestId?: string;
    userId: string; // name
    priceNum: number | string;
    voided?: boolean;
    betId?: string;
    priceDen: number | string;
    overallProgressPct: number;
    gifts?: any;
    winningamount?: number;
    entryId?: string;
    stake?: string;
    outcomeIds?: Array<string>;
    legs?: Array<IOutCome>;
    odds?: string;
    prizes?: IPriceRecord[];
    oddsDecimal?: number | string;
    isOpened?: boolean;
    isOverlayOpend?: boolean;
    id: string;
    index?: number;
    rankEqual?: string;
    rankProgress?: number;
    previousIndex?: number;
    currentIndex?: number;
    rankedIndex?: number;
    userEntry?: boolean;
    hidden?: boolean;
}
export interface IctaGtmTrack {
    eventCategory: string;
    eventAction: string;
    eventLabel: string;
}

export interface ILeaderboardInfo {
    contestId?: string;
    leaderboardEntries?: Array<IEntrySummaryInfo>;
    userEntries?: Array<IEntrySummaryInfo>;
}

export interface IHeaderArea {
    homeName: string;
    awayName: string;
    homeScore: string;
    awayScore: string;
    flagHomeIcon: string;
    flagAwayIcon: string;
    isScoresAvailable: boolean;
}
