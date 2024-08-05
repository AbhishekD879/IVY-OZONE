import { Base } from '@app/client/private/models/base.model';

export interface LuckyDip extends Base {
    luckyDipBannerConfig: LuckyDipBannerConfig;
    luckyDipFieldsConfig: LuckyDipFieldsConfig;
    playerPageBoxImgPath: string;
}

export interface LuckyDipBannerConfig {
    animationImgPath: string;
    bannerImgPath: string;
    overlayBannerImgPath: string;
}

export interface LuckyDipFieldsConfig {
    title: string;
    desc: string;
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
