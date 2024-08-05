export interface IFanzoneGamesSignPostingData {
    active: boolean;
    startDate: string;
    endDate: string;
}

export interface IFanzoneGamesPopupData {
    title: string;
    description: string;
    closeCTA: string;
    playCTA: string;
}

export interface IFanzoneGame {
    gameName: string;
    gameDisplayName: string;
    gameVariantName: string;
    gameThumbnailUrl: string;
    gameLaunchUrl: string;
    showGame: boolean;
}
