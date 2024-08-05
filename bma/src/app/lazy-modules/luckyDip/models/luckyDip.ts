import { IOutcome, IOutcomeDetails } from "@core/models/outcome.model";
import { IPrice } from "@core/models/price.model";
import { ISiteCoreTeaserFromServer } from "@app/core/models/aem-banners-section.model";

export interface ILuckyDip {
    id?: string;
    luckyDipBannerConfig?: ILuckyDipBanner;
    playerPageBoxImgPath?: string;
    luckyDipFieldsConfig?: ILuckyDipFieldsConfig;

}
export interface ILuckyDipBanner {
    animationImgPath?: string;
    bannerImgPath?: string;
    overlayBannerImgPath?: string;
}

export interface ILuckyDipFieldsConfig {
    title?: string;
    desc?: string;
    welcomeMessage?: string;
    betPlacementTitle?: string;
    betPlacementStep1?: string;
    betPlacementStep2?: string;
    betPlacementStep3?: string;
    termsAndConditionsURL?: string;
    playerCardDesc?: string;
    potentialReturnsDesc?: string;
    backCTAButton?: string;
    depositButton?: string;
    gotItCTAButton?: string;
    placebetCTAButton?: string;
}

export interface ILuckyDipRemoteBetSlipSelection {
    eventIsLive: boolean;
    outcomes: IOutcome[];
    typeName: string;
    price: string;
    handicap?: {type:string,raw:string};
    goToBetslip: boolean;
    modifiedPrice: IPrice;
    eventId: number;
    isOutright: boolean;
    isSpecial: boolean;
    GTMObject:{ categoryID: string; typeID: string; eventID: string; selectionID: string; };
    details :Partial<IOutcomeDetails>;
    templateMarketName:string;
    selectionInfo?: ISelectionInfo
}

export interface ISelectionInfo {
    eventName: string;
    marketName: string;
    outcomeName: string;
    newOdds: string;
    potentialOdds: string;
}

export interface AnimationDataConfig {
    cmsConfig: ILuckyDipAnimationCmsConfig;
    playerData:ILuckyDipAnimationPlayer;
    svg: any;
}

export interface ILuckyDipAnimationCmsConfig {
    gotItCTAButton: string;
        playerPageBoxImgPath: string
        playerCardDesc: string
        potentialReturnsDesc: string
}

export interface ILuckyDipAnimationPlayer {
    playerName: string;
    amount: string
    odds: string
       
}

export interface ILdSiteCoreBanner {
    type?: string;
    teasers?: ISiteCoreTeaserFromServer[];
  }