export interface lbConfigCols {
    originalName: string,
    displayName: string,
    subtitle: string,
    style: string,
    applyMasking: boolean
}

export interface leaderboardConfig {
    id: string,
    brand: string,
    name: string,
    topX: number,
    individualRank: number,
    filePath: string,
    genericTxt: string,
    status: boolean,
    columns: Array<lbConfigCols>;

}

export interface userRankRequest {
    promotionId: string,
    customerId: string,
    customerRanking: boolean,
    noOfPosition: number

}

export interface lbData {
    customerId: string,
    displayName: string,
    displayRank: string,
    correctAnswers: string,
    orderRank: string,
    lastUpdated: string,
    Score: string,
    winresult: string

}

export interface leaderBoardUserRankData {
    lastFileModified: string,
    userRank: lbData,
    topXRank: Array<lbData>
}