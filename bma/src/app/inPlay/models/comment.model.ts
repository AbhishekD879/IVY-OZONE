export interface IComment {
    teams: { [index: string]: any };
    facts: any[];
    latestPeriod: { [index: string]: any };
    setsScores: { [index: string]: any };
    runningSetIndex: number;
    runningGameScores: { [index: string]: any };
}
