export interface IARC {
    items: IArcConfig[];
}
export interface IArcConfig {
    profile: string;
    modelRiskLevel: string | number;
    reasonCode: string | number;
    sportsActions: ISportAction[];
    frequency: string;
    enabled: boolean;
    brand: string;
}

export interface ISportAction {
    action: string;
    messagingContent: string;
    gcLink: string;
    enabled: boolean
}
export interface IMasterGroup {
    id: string,
    masterLineName: string,
    values: IValues[]
}
export interface IValues {
    id: string,
    name: string
}

export interface ILink {
    label: string;
    path: string;
}