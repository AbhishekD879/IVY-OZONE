import { IBase } from "@app/core/services/cms/models/base.model";

export interface IFanzoneSyc extends IBase {
    changeTeamTimePeriodMsg?: string;
    customTeamNameText?: string;
    daysToChangeTeam?: number;
    dontShowAgain?: string;
    okCTA?: string;
    remindLaterHideDays?: string;
    sycChangeCTA?: string;
    sycConfirmCTA?: string;
    sycConfirmMsgDesktop?: string;
    sycConfirmMsgMobile?: string;
    sycConfirmTitle?: string;
    sycDescription?: string;
    sycExitCTA?: string;
    sycLoginCTA?: string;
    sycNoTeamSelectionTitle?: string;
    sycPopUpDescription?: string;
    sycPopUpTitle?: string;
    sycPreLoginNoTeamSelectionMsg?: string;
    sycPreLoginTeamSelectionMsg?: string;
    sycThankYouTitle?: string;
    sycTitle?: string;
    thankYouMsg?: string;
}

export interface fanzoneUserData {
    DontShowMeAgain?: boolean;
    remindMeLater?: boolean;
    iMIn?: boolean;
    [key: string]: any;
    teamId?: string;
    teamName?: string; 
    subscriptionDate?: string;
    showSYCPopupOn?: string;
}

export interface IThankYouPopup {
    sycPopUpDescription: string,
    sycTitle: string,
    ctaSecondaryBtn: string,
    teamId: string,
    daysToChangeTeam?: number
}

export interface IDaysNotCompletedPopup {
    sycPopUpDescription: string,
    sycTitle: string,
    ctaSecondaryBtn: string
}