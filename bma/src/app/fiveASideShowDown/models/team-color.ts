export interface ITeamImage extends File {
    originalname?: string;
    filename?: string;
    svg?: string;
}
export interface ITeamColor {
    primaryColour: string;
    secondaryColour: string;
    teamName?: string;
    teamsImage?: ITeamImage;
    fiveASideToggle?: boolean;
    secondaryNames?: Array<string>;
}
export interface ITeamImageCrest {
    imageWidth?: number;
    crestWidth?: number;
    imageHeight?: number;
    crestHeight?: number;
}
