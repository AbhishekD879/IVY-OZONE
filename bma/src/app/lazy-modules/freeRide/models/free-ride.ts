import { IBetError } from '@bpp/services/bppProviders/bpp-providers.model';

export interface IFreeRideCampaign {
    id?: string;
    name?: string;
    brand?: string;
    displayFrom: string;
    displayTo: string;
    isPotsCreated?: boolean;
    questionnarie?: IQuestionnarie;
}

export interface IQuestionnarie {
    questions: IQuestions[];
    summaryMsg: string;
    welcomeMessage: string;
    horseSelectionMsg: string;
}

export interface IQuestions {
    questionId?: number;
    quesDescription?: string;
    options?: IOptions[];
    chatBoxResp?: string;
}

export interface IOptions {
    optionId: number;
    optionText: string;
}

export interface ISplashPage {
    bannerImageUrl?: string;
    buttonText?: string;
    brand?: string;
    isBetReceipt: boolean;
    isHomePage: boolean;
    freeRideLogoUrl: string;
    id?: string;
    splashImageUrl?: string;
    termsAndCondition?: string;
    termsAndConditionLink?:string;
    termsAndConditionHyperLinkText?:string;
    welcomeMsg?: string;
}

export interface IRaceEvent {
    horseName: string;
    jockeyName: string;
    raceName: string;
    raceTime: string;
    silkUrl: string;
    categoryName: string;
    typeName: string;
    name: string;
    className: string;
    eventId: string | number;
    betError?: IBetError[];
}

export interface IBpError {
    path: string;
    errMsg: string;
}

export interface IUserSelectionDetail {
    freebettoken: string;
    clientUserAgent: string;
    isAccountBet: string;
    userDto: IUserName;
    currencyRef: string;
    ipAddress: string;
    channelRef: string;
    campaignId: string;
    brand: string;
    userAnswers: IUserAnswer[];
}

export interface IOverlayData {
    isSoundChecked: boolean;
    splashInfo: ISplashPage;
    campaignInfo: IFreeRideCampaign;
    freeBetToken: string;
}

export interface IUserName {
    userName: string;
}

export interface IUserAnswer {
    questionId?: number;
    optionId: number;
}

export interface IDOMData {
    parentElem: HTMLElement | string;
    childElem: HTMLElement | string;
}
