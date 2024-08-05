import { Base } from '@app/client/private/models/base.model';

export interface IAddLuckyDip {
    createdAt: string;
    createdBy: string;
    createdByUserName: string;
    id: string;
    updatedAt: string;
    updatedBy: string;
    updatedByUserName: string;
    description?: string;
    luckyDipConfigLevel?: string;
    luckyDipConfigLevelId?: string;
    intialLuckyDipId?: string;
}
export interface DialogData {
    data: {
        dialogType: string;
        dialogData: IAddLuckyDip;
    }
}
export interface LuckyDipV2 extends Base {
    status: boolean;
    description: string;
    luckyDipConfigLevel: string;
    luckyDipConfigLevelId: string;
    luckyDipBannerConfig: LuckyDipBannerConfig;
    luckyDipFieldsConfig: LuckyDipFieldsConfig;
    playerPageBoxImgPath: string;
    displayOnCompetitions: boolean;
}

export interface LuckyDipBannerConfig {
    animationImgPath: string;
    bannerImgPath: string;
    overlayBannerImgPath: string;
}

export interface LuckyDipFieldsConfig {
    title: string;
    welcomeMessage: string;
    betPlacementTitle: string;
    betPlacementStep1: string;
    betPlacementStep2: string;
    betPlacementStep3: string;
    termsAndConditionsURL: string;
    playerCardDesc: string;
    potentialReturnsDesc: string;
    placebetCTAButton: string;
    backCTAButton: string;
    gotItCTAButton: string;
    depositButton: string;
}
export interface ILuckyDipMapping extends Base {
    active?: boolean;
    categoryId?: string;
    typeIds?: string;
}
