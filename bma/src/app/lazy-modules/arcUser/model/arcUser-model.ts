export interface IArcUserData {
    id: string;
    createdBy: string;
    createdByUserName: string;
    updatedBy: string;
    updatedByUserName: string;
    createdAt: string;
    updatedAt: string;
    sortOrder: string;
    profile: string;
    modelRiskLevel: string;
    reasonCode: string;
    sportsActions: IsportsActions[];
    frequency: string;
    enabled: boolean;
    brand: string;
}
export interface IsportsActions {
    action: string;
    messagingContent ?: string;
    enabled ?: boolean;
}
