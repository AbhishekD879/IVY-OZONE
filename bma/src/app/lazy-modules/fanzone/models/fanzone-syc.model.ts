import { IBase } from "@core/services/cms/models/base.model";

export interface IFanzoneSyc extends IBase {
    pageName: string,
    sycTitle: string,
    sycPopUpTitle: string,
    sycDescription: string,
    sycPopUpDescription: string,
    sycImage: string,
    okCTA: string,
    remindLater: string,
    remindLaterHideDays: string,
    dontShowAgain: string,
    seasonStartDate: string,
    seasonEndDate: string,
    customTeamNameText: string,
    sycCTA?: string,
    sycChangeCTA: string,
    sycExitCTA: string,
    thankYouMsg: string,
    changeTeamTimePeriodMsg: string,
    daysToChangeTeam: number
}

export interface fanzoneUserData {
    DontShowMeAgain?: boolean;
    remindMeLater?: boolean;
    iMIn?: boolean;
    [key: string]: any;
    teamId?: string;
    teamName?: string;
    daysToChangeTeam?: number;
    subscriptionDate?: string;
    showSYCPopupOn?: string;
    isResignedUser?: boolean;
}