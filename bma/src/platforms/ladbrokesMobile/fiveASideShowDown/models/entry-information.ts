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
    _id: string;
    playerId?: string;
    contestantId?: string;
    marketId?: string;
}

export interface IEntrySummaryInfo {
    rank?: number;
    contestId?: string;
    userId: string; // name
    priceNum: number | string;
    voided: boolean;
    betId?: string;
    priceDen: number | string;
    overallProgressPct: number;
    gifts?: any;
    winningamount?: number;
    entryId: string; // to get the leg details
    outcomes?: Array<IOutCome>;
    odds?:string;
    isOpened?: boolean;
    stake?: string;
    outcomeIds?: Array<string>;
    legs?: Array<IOutCome>;
    oddsDecimal?: number | string;
    id: string;
    index?: number;
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
