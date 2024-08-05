export interface ITeamImage {
    originalname?: string;
    filename?: string;
    svg?: string;
    path?: string;
    filetype?: string;
}

export interface ITeamAsset {
    primaryColour: string;
    secondaryColour: string;
    teamName?: string;
    teamsImage?: ITeamImage;
    fiveASideToggle?: boolean;
    secondaryNames?: Array<string>;
}