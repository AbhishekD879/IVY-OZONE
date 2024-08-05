import { IBase } from "@app/core/services/cms/models/base.model";

export interface IReviewPage {
    betPackId: string;
    betPackTitle: string;
    betPackPurchaseAmount: string;
    betPackFreeBetsAmount: string;
    betPackFrontDisplayDescription: string;
    betPackMoreInfoText: string;
    sportsTag: string[];
    betPackStartDate: string;
    betPackEndDate: string;
    betPackPurchaseDate?: string;
    betPackPurchaseLongDate?: string;
    betPackTokenList: ITokenData[];
}

export interface ITokenData extends IToken {
    expiresIntimer?: number;
    isExpiresIn?: boolean;
    formatDate?: string;
    freebetTokenExpiryDate: string;
    freebetTokenAwardedDate: string;
    freebetTokenAwardedLongDate?: Date;
}

export interface IToken {
    tokenId: number | string;
    tokenTitle: string;
    deepLinkUrl: string;
    tokenValue: string | number;
    active: boolean;
}
export interface BetPackModel extends IBase {
    betPackId: string;
    betPackTitle: string;
    betPackPurchaseAmount: number | string;
    betPackFreeBetsAmount: number | string;
    betPackFrontDisplayDescription: string;
    sportsTag: string[];
    betPackStartDate: string;
    betPackEndDate: string;
    maxTokenExpirationDate: string;
    futureBetPack: boolean;
    filterBetPack: boolean;
    betPackSpecialCheckbox: boolean;
    betPackMoreInfoText: string;
    linkedBetPackWarningText: string;
    isLinkedBetPack: boolean;
    filterList: string[];
    betPackActive: boolean;
    triggerID: number | string;
    betPackTokenList: IToken[];
    sortOrder: number;
    purchased?: boolean;
    active?: boolean;
    signPostingMsg?: string;
    signPostingToolTip?: string;
    expiresIntimer?: number;
    disableBuyBtn?: boolean;
    expireIn?: string;
    maxClaims?: number;
    offerGroupId?: string;
    showSignPost?:boolean;
}

export interface BetPackLabels extends IBase {
    buyButtonLabel: string;
    buyBetPackLabel: string;
    gotoMyBetPacksLabel: string;
    betNowLabel: string;
    makeADepositLabel: string;
    depositMessage: string;
    kycArcGenericMessage: string;
    myBetpackTitle: string;
    useByLabel: string;
    maxBetPackPerDayBannerLabel: string;
    betPackAlreadyPurchasedPerDayBannerLabel: string;
    betPackMarketplacePageTitle: string;
    errorTitle: string;
    errorMessage: string;
    goToBettingLabel: string;
    goBettingURL: string;
    moreInfoLabel: string;
    buyNowLabel: string;
    notLoggedIn: string;
    betPackReview: string;
    maxPurchasedLabel: string;
    limitedLabel: string;
    soldOutLabel: string;
    endingSoonLabel: string;
    expiresInLabel: string;
    endedLabel: string;
    maxOnePurchasedLabel: string;
    reviewErrorMessage: string;
    reviewErrorTitle: string;
    reviewGoBettingURL: string;
    reviewGoToBettingLabel: string;
    betPackInfoLabel: string;
    lessInfoLabel: string;
    betPackSuccessMessage: string;
    backgroundImage?: Filename;
    backgroundImageFileName?: string;
    backgroundImg?: string;
    maxOnePurchasedTooltip: string;
    limitedTooltip: string;
    expiresInTooltip: string;
    endingSoonTooltip: string;
    endedTooltip: string;
    soldOutTooltip: string;
    maxPurchasedTooltip: string;
    featuredBetPackBackgroundLabel: string;
    serviceError: string;
    goToReviewText: string,
    goToBetbundleText: string,
    isDailyLimitBannerEnabled:boolean,
    allFilterPillMessageActive:boolean,
    comingSoon: string,
    comingSoonSvg: string,
}

export interface Filter {
    filterName: string;
    filterActive: boolean;
    filterNameFrCurr?: string;
    isVisible?: boolean;
    sortOrder?: number;
    isLinkedFilter:boolean;
    linkedFilterWarningText:string;
}
export interface FilterModel extends IBase {
    filterName: string;
    filterActive: boolean;
    sortOrder: number;
    isLinkedFilter:boolean;
    linkedFilterWarningText:string;

}
export interface Filename {
    filename: string;
    originalname?: string;
    path: string;
    size: number;
    filetype: string;
}
export interface BannerModel extends IBase {
    welcomeMsg: string;
    termsAndCondition: string;
    termsAndConditionLink: string;
    buttonText: string;
    bannerImage?: Filename;
    bannerImageFileName?: string;
    enabled: boolean;
    bannerActiveInMarketPlace?: boolean;
    bannerActiveInReviewPage?: boolean;
    bannerTextDescInMarketPlacePage?: string;
    bannerTextDescInReviewPage?: string;
    expiresInActive?: boolean;
    expiresInIconImage?: string;
    expiresInText?: string;
    marketPlaceBgImageFileName?: string;
    marketPlaceImageFileName?: string;
    reviewPageBgImageFileName?: string;
    reviewPageImageFileName?: string
}

export interface BetpackSocketStorageModel {
    id: string;
    betpackEndDate: string;
    current: number | string;
    threshold: number | string;
    expiryData?: string;
    maxClaimLimitRemaining: string | number;
    betpackStartDate: string;
}

export interface signObject {
    betpackId: string;
    signPost: string;
    signPostTooltip: string;
}

export interface API_GETLIMITS {
    id: string;
    betpackEndDate: string;
    current: string | number;
    threshold: string | number;
    expiry: string;
    maxClaimLimitRemaining: string | number;
    betpackStartDate: string
}

export interface IGetFreeBetOffersList {
    offerId?: number | string;
    group?: Array<IGetGroupedToken>;
}

export interface IGetGroupedToken {
    groupNumber?: number | string;
    tokensAssociatedToGroup?: Array<IGetTokens>;
}

export interface IGetTokens {
    tokenId?: string | number;
    formatDate?: string
    freebetTokenExpiryDate?: string;
    freebetTokenAwardedDate?: string;
    freebetTokenAwardedLongDate?: Date;
    freebetTokenValue?: string;
}

export interface BetPackDialogModel extends IBase {
    bp: BetPackModel,
    betpackLabels: BetPackLabels,
    isBuyInfoClicked: boolean,
    clicked: boolean,
    reviewPage: boolean,
    signPostingMsg: string,
    signPostingToolTip: string,
    expiresIntimer: number
}
