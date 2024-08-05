export interface IShowdownLobbyContest {
    category?: string;
    categoryName?: string;
    date?: string;
    displayCount?: number;
    contests? : any;
}

export interface IShowdownLobbyResponse {
   showdownCards: IShowdownLobbyContest[];
}

export interface ITransition {
    disabled: boolean;
    element: HTMLElement;
    fromState: string | boolean;
    phaseName: string;
    toState: boolean | string;
    totalTime: number;
    triggerName: string;
}

export interface LobbyData {
    brand: string;
    userId: string;
    offSet: number;
    token: string;
}
