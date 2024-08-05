export interface IMGArenaScoreboard {
    operator: string;
    sport: string;
    targetModule: string;
    eventId: string;
    version: string;
    language: string;
    targetElementSelector: string;
    initialContext?: IInitialContextForGolf;
    options: IOptionsForGolf;
}

export interface IOptionsForGolf {
    videoPlaybackEnabled: boolean;
}

export interface IInitialContextForGolf {
    view: string;
    roundNo: string;
    groupNo: string;
    holeNo: string;
}