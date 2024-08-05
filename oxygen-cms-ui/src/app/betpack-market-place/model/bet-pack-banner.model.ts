import { Filename } from '@app/client/private/models';
import { Base } from 'app/client/private/models/base.model';
export interface BannerModel {
    welcomeMsg: string;
    termsAndCondition: string;
    termsAndConditionLink: string;
    bannerImage?: Filename;
    bannerImageFileName?: string;
    enabled: string;
    id?: string;
    createdBy?: string;
    createdByUserName?: string;
    updatedBy?: string;
    updatedByUserName?: string;
    createdAt?: string;
    updatedAt?: string;
    brand?: string;
    disabled?: boolean;
}
export interface bannerImages{
    bannerImage:string,
    bannerImgInMarketPlacePage:string,
    bannerImgInReviewPage:string
}
export interface FilterModel extends Base {
    filterName: string;
    filterActive: boolean;
    isLinkedFilter?:boolean;
    linkedFilterWarningText?:string;
}

export interface StaticFieldModel extends Base {
    buyButtonLabel: string;
    buyBetPackLabel: string;
    gotoMyBetPacksLabel: string;
    depositMessage: string;
    kycArcGenericMessage: string;
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
    betPackReview: string;
    maxPurchasedLabel: string;
    maxPurchasedTooltip: string;
    limitedLabel: string;
    limitedTooltip: string;
    soldOutLabel: string;
    soldOutTooltip: string;
    endingSoonLabel: string;
    endingSoonTooltip: string;
    expiresInLabel: string;
    expiresInTooltip: string;
    endedLabel: string;
    endedTooltip: string;
    maxOnePurchasedLabel: string;
    maxOnePurchasedTooltip: string;
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
    featuredBetPackBackgroundLabel: string;
    serviceError: string;
    goToReviewText: string;
    goToBetbundleText: string;
    allFilterPillMessage?:string
    isDailyLimitBannerEnabled:boolean;
    allFilterPillMessageActive:boolean;
    comingSoon: string;
    comingSoonSvg:string;
}
export interface BetPackModel extends Base {
    betPackId: string;
    betPackTitle: string;
    betPackPurchaseAmount: number;
    betPackFreeBetsAmount: number;
    betPackFrontDisplayDescription: string;
    sportsTag: string[];
    betPackStartDate: string;
    betPackEndDate: string;
    maxTokenExpirationDate: string;
    futureBetPack: boolean;
    filterBetPack: boolean;
/// new
    isLinkedBetPack?: boolean;
    linkedBetPackWarningText?: string;
    betPackSpecialCheckbox: boolean;
    betPackMoreInfoText: string;
    filterList: string[];
    betPackActive: boolean;
    triggerID: string;
    betPackTokenList: IToken[];
    sortOrder: number;
    maxClaims: number;
}

export interface IToken {
    tokenId: number;
    tokenTitle: string;
    deepLinkUrl: string;
    tokenValue: string;
    id: string;
}

export const BannerTestData: BannerModel = {
    'id': '611b88622418810936bdefc8',
    'createdBy': '6077c980f33e2e2e095ba4cb',
    'createdByUserName': null,
    'updatedBy': '6077c980f33e2e2e095ba4cb',
    'updatedByUserName': null,
    'createdAt': '2021-08-17T09:58:58.796Z',
    'updatedAt': '2021-08-17T09:59:26.695Z',
    'brand': 'bma',
    'welcomeMsg': 'test on tst0 env',
    'termsAndCondition': 'data',
    'bannerImage': {
        'filename': '9dc6fb37-9169-4d67-8620-51c24337bf1e.png',
        'originalname': 'test-image3.png',
        'path': '/images/uploads/freeRideSplashPage',
        'size': 3001,
        'filetype': 'image/png'
    },
    'termsAndConditionLink': '/',
    'enabled': 'false',
    'bannerImageFileName': '9dc6fb37-9169-4d67-8620-51c24337bf1e.png'
};
export const  bannerFormGroup={
    bannerImage: null,
  bannerImageFileName: '',
  welcomeMsg:  '',
  termsAndCondition:  '',
  termsAndConditionLink:  '',
  enabled: [false],
  bannerTextDescInMarketPlacePage: '',
  bannerTextDescInReviewPage:  '',
  bannerActiveInMarketPlace: false,
  bannerActiveInReviewPage: false,
  expiresInActive: false,
  expiresInText:  '',
  id: '',
  createdBy: '',
  updatedBy:  '',
  updatedAt: [''],
  brand: 'bma',
  createdAt: '',
  updatedByUserName:  '',
  createdByUserName:  '',
   }

export const LabelsTestData: StaticFieldModel = {
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    buyButtonLabel: '',
    buyBetPackLabel: '',
    gotoMyBetPacksLabel: '',
    depositMessage: '',
    kycArcGenericMessage: '',
    useByLabel: '',
    maxBetPackPerDayBannerLabel: '',
    betPackAlreadyPurchasedPerDayBannerLabel: '',
    betPackMarketplacePageTitle: '',
    errorTitle: '',
    errorMessage: '',
    goToBettingLabel: '',
    goBettingURL: '',
    moreInfoLabel: '',
    buyNowLabel: '',
    betPackReview: '',
    maxPurchasedLabel: '',
    limitedLabel: '',
    soldOutLabel: '',
    endingSoonLabel: '',
    expiresInLabel: '',
    endedLabel: '',
    maxOnePurchasedLabel: '',
    reviewErrorMessage: '',
    reviewErrorTitle: '',
    reviewGoBettingURL: '',
    reviewGoToBettingLabel: '',
    betPackInfoLabel: '',
    lessInfoLabel: '',
    betPackSuccessMessage: '',
    maxPurchasedTooltip: '',
    limitedTooltip: '',
    soldOutTooltip: '',
    endingSoonTooltip: '',
    expiresInTooltip: '',
    endedTooltip: '',
    maxOnePurchasedTooltip: '',
    featuredBetPackBackgroundLabel: '',
    serviceError:'',
    goToReviewText: '',
    goToBetbundleText: '',
    allFilterPillMessage:'',
    isDailyLimitBannerEnabled:false,
    allFilterPillMessageActive:false,
    comingSoon: '',
    comingSoonSvg:''
};

export const LabelsTestData1: StaticFieldModel = {
    id: 'Labels',
    brand: 'Labels',
    createdBy: 'Labels',
    createdAt: 'Labels',
    updatedBy: 'Labels',
    updatedAt: 'Labels',
    updatedByUserName: 'Labels',
    createdByUserName: 'Labels',
    buyButtonLabel: 'Labels',
    buyBetPackLabel: 'Labels',
    gotoMyBetPacksLabel: 'Labels',
    depositMessage: 'Labels',
    kycArcGenericMessage: 'Labels',
    useByLabel: 'Labels',
    maxBetPackPerDayBannerLabel: 'Labels',
    betPackAlreadyPurchasedPerDayBannerLabel: 'Labels',
    betPackMarketplacePageTitle: 'Labels',
    errorTitle: 'Labels',
    errorMessage: 'Labels',
    goToBettingLabel: 'Labels',
    goBettingURL: 'Labels',
    moreInfoLabel: 'Labels',
    buyNowLabel: 'Labels',
    betPackReview: 'Labels',
    maxPurchasedLabel: 'Labels',
    limitedLabel: 'Labels',
    soldOutLabel: 'Labels',
    endingSoonLabel: 'Labels',
    expiresInLabel: 'Labels',
    endedLabel: 'Labels',
    maxOnePurchasedLabel: 'Labels',
    reviewErrorMessage: 'Labels',
    reviewErrorTitle: 'Labels',
    reviewGoBettingURL: 'Labels',
    reviewGoToBettingLabel: 'Labels',
    betPackInfoLabel: 'Labels',
    lessInfoLabel: 'Labels',
    betPackSuccessMessage: 'Labels',
    maxPurchasedTooltip: '',
    limitedTooltip: '',
    soldOutTooltip: '',
    endingSoonTooltip: '',
    expiresInTooltip: '',
    endedTooltip: '',
    maxOnePurchasedTooltip: '',
    featuredBetPackBackgroundLabel: '',
    serviceError:'',
    goToReviewText: '',
    goToBetbundleText: '',
    allFilterPillMessage:'',
    isDailyLimitBannerEnabled:false,
    allFilterPillMessageActive:false,
    comingSoon: '',
    comingSoonSvg:''
};
export const LabelsTestData2: StaticFieldModel = {
    id: '5ce4bc44c9e77c0001cfd014',
    brand: 'bma',
    createdBy: null,
    createdAt: '2019-05-22T03:04:36.169Z',
    updatedBy: '5645b8a220bd9e0800afdc57',
    updatedAt: '2022-10-25T09:23:22.771Z',
    updatedByUserName: null,
    createdByUserName: null,
    buyButtonLabel: 'Labels',
    buyBetPackLabel: 'Labels',
    gotoMyBetPacksLabel: 'Labels',
    depositMessage: 'Labels',
    kycArcGenericMessage: 'Labels',
    useByLabel: 'Labels',
    maxBetPackPerDayBannerLabel: 'Labels',
    betPackAlreadyPurchasedPerDayBannerLabel: 'Labels',
    betPackMarketplacePageTitle: 'Labels',
    errorTitle: 'Labels',
    errorMessage: 'Labels',
    goToBettingLabel: 'Labels',
    goBettingURL: 'Labels',
    moreInfoLabel: 'Labels',
    buyNowLabel: 'Labels',
    betPackReview: 'Labels',
    maxPurchasedLabel: 'Labels',
    limitedLabel: 'Labels',
    soldOutLabel: 'Labels',
    endingSoonLabel: 'Labels',
    expiresInLabel: 'Labels',
    endedLabel: 'Labels',
    maxOnePurchasedLabel: 'Labels',
    reviewErrorMessage: 'Labels',
    reviewErrorTitle: 'Labels',
    reviewGoBettingURL: 'Labels',
    reviewGoToBettingLabel: 'Labels',
    betPackInfoLabel: 'Labels',
    lessInfoLabel: 'Labels',
    betPackSuccessMessage: 'Labels',
    maxPurchasedTooltip: 'toolTip',
    limitedTooltip: 'toolTip',
    soldOutTooltip: 'toolTip',
    endingSoonTooltip: 'toolTip',
    expiresInTooltip: 'toolTip',
    endedTooltip: 'toolTip',
    maxOnePurchasedTooltip: 'toolTip',
    featuredBetPackBackgroundLabel: 'toolTip',
    serviceError: 'toolTip',
    goToReviewText: 'test',
    goToBetbundleText: 'test',
    allFilterPillMessage:'',
    isDailyLimitBannerEnabled:false,
    allFilterPillMessageActive:false,
    comingSoon: '',
    comingSoonSvg:''
}
export const FILTER1 : FilterModel = {
    filterName: undefined,
    filterActive: false,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: ''
};
export const FILTER2 : FilterModel = {
    filterName: 'Today',
    filterActive: false,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: ''
};
export const FILTER3 : FilterModel = {
    filterName: 'All',
    filterActive: false,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: ''
};
export const FILTER4 : FilterModel = {
    filterName: 'All@',
    filterActive: false,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: ''
};

export const FiltersTestData: FilterModel[] = [{
    filterName: '',
    filterActive: false,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    isLinkedFilter:false,
    linkedFilterWarningText:''
}];

export const FiltersTestData1: FilterModel[] = [{
    filterName: 'test',
    filterActive: true,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    isLinkedFilter:true,
    linkedFilterWarningText:'test'
}];
export const FiltersTestData2: FilterModel[] = [{
    filterName: 'test',
    filterActive: true,
    id: '',
    brand: '',
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    isLinkedFilter:true,
    linkedFilterWarningText:''
}];

export interface onboardImageDataModel extends Base{
    isActive: boolean;
    images: Array<OnboardModel>;
}
export interface OnboardModel {
    id?: string;
    isAdd?: boolean;
    onboardImageDetails?: onboardImageDetailsModel;
    onboardImg?: onboardImageFile;
    imageType: string;
    imageLabel: string;
    nextCTAButtonLabel?: string;
}
export interface onboardImageDetailsModel {
    filename: string,
    originalname: string,
    path: string,
    filetype: string
    size?: number,
}
export interface onboardImageFile {
    name: string,
    type: string,
    webkitRelativePath?: string,
    lastModified: number,
    size?: number
}

export const onboardData = {
    "id": "62f621c5a22245379b28a20b",
    "createdBy": "5645b8a220bd9e0800afdc57",
    "createdByUserName": "ozoneqa@ivycomptech.com",
    "updatedBy": "5645b8a220bd9e0800afdc57",
    "updatedByUserName": "ozoneqa@ivycomptech.com",
    "createdAt": "2022-08-29T06:01:38.404Z",
    "updatedAt": "2022-08-29T06:01:38.542Z",
    "sortOrder": -103,
    "brand": "bma",
    "isActive": true,
    "images": [
        {
            "imageLabel": "Welcome",
            "nextCTAButtonLabel": "Next",
            "onboardImageDetails": {
                "filename": "c53a4125-bf67-42b0-93cd-9fd74a9e10e2.jpg",
                "originalname": "1.jpg",
                "path": "/images/uploads/onboarding/betPackOnboarding",
                "size": 137853,
                "filetype": "image/jpeg"
            },
            "imageType": "onboarding",
            "id": "630c56426ecdeb62bb69f30c"
        }
    ]
}

export const newOnboardDara = [{
    'id': '630c56426ecdeb62bb69f30c',
    'isAdd': true,
    "onboardImageDetails": {
        "filename": "c53a4125-bf67-42b0-93cd-9fd74a9e10e2.jpg",
        "originalname": "1.jpg",
        "path": "/images/uploads/onboarding/betPackOnboarding",
        "size": 137853,
        "filetype": "image/jpeg"
    },
    'onboardImg': {
        'name': '1.png',
        'size': 38656,
        'type': 'image/png',
        'webkitRelativePath': 'abc',
        'lastModified': 123,
    },
    'imageType': 'onboard',
    'imageLabel': 'welcome',
    'nextCTAButtonLabel': 'next'
}]
