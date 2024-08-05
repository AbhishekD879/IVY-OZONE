import { Base } from '@app/client/private/models/base.model';

export interface Fanzone extends Base {
    name: string;
    active?: boolean;
    launchBannerUrl?: string;
    teamId?: string;
    openBetID?: string;
    fanzoneBanner?: string;
    assetManagementLink?: string;
    primaryCompetitionId?: string;
    secondaryCompetitionId?: string;
    clubIds?: string;
    hexColorCode?: string;
    location?: string;
    fanzoneConfiguration?: FanzoneConfig;
    nextGamesLbl?: string;
    outRightsLbl?: string;
    premierLeagueLbl?: string;
    clubInfo?: ClubPromo[];
    is21stOrUnlistedFanzoneTeam?:boolean;
}

export interface FanzoneConfig {
    showNowNext?: boolean;
    showCompetitionTable?: boolean;
    showStats?: boolean;
    showClubs?: boolean;
    showGames?: boolean;
    showSlotRivals?: boolean;
    showScratchCards?: boolean;
    sportsRibbon?: boolean;
    atozMenu?: boolean;
    homePage?: boolean;
    footballHome?: boolean;
    launchBannerUrlDesktop?: string;
    fanzoneBannerDesktop?: string;
    showBetsBasedOnOtherFans?:boolean;
    showBetsBasedOnYourTeam?:boolean;
}

export interface ClubPromo extends Base {
    active?: boolean;
    title?: string;
    bannerLink?: string;
    description?: string;
    validityPeriodStart?: string;
    validityPeriodEnd?: string;
    pageName?: string;
}

export interface Syc extends Base {
    pageName?: string;
    sycPopUpTitle?: string;
    sycPopUpDescription?: string;
    sycImage?: string;
    okCTA?: string;
    remindLater?: string;
    remindLaterHideDays?: string;
    dontShowAgain?: string;
    seasonStartDate?: string;
    seasonEndDate?: string;
    sycTitle?: string;
    sycThankYouTitle?: string;
    sycDescription?: string;
    customTeamNameText?: string;
    customTeamNameDescription?: string;
    sycLoginCTA?: string;
    sycConfirmCTA?: string;
    sycChangeCTA?: string;
    sycExitCTA?: string;
    sycCancelCTA?: string;
    sycConfirmTitle?: string;
    sycNoTeamSelectionTitle?: string;
    thankYouMsg?: string;
    sycPreLoginTeamSelectionMsg?: string;
    sycPreLoginNoTeamSelectionMsg?: string;
    sycConfirmMsgMobile?: string;
    sycConfirmMsgDesktop?: string;
    changeTeamTimePeriodMsg?: string;
    daysToChangeTeam?: number;
}

export interface IFanzoneComingBack extends Base {
    fzComingBackPopupDisplay?: boolean;
    active?: string;
    pageName?: string;
    fzComingBackTitle?: string; 
    fzComingBackDescription?: string;
    fzComingBackOKCTA?: string;
    fzComingBackDisplayFromDays?: string;
    fzComingBackHeading?: string;
    fzComingBackBadgeUrlMobile?: string;
    fzComingBackBadgeUrlDesktop?: string;
    fzComingBackBgImageDesktop?: string;
    fzComingBackBgImageMobile?: string;
}
export interface IFanzoneNewSeason extends Base {
    pageName?: string;
    fzNewSeasonTitle?: string; 
    fzNewSeasonDescription?: string;
    fzNewSeasonBannerUrl?: string;
    fzNewSeasonHeading?: string;
    fzNewSeasonBgImageMobile?: string;
    fzNewSeasonBgImageDesktop?: string;
    fzNewSeasonBadgeDesktop?: string;
    fzNewSeasonBadgeMobile?: string;
    fzNewSeasonLightningDesktop?: string;
    fzNewSeasonLightningMobile?: string;
}
export interface Preferences {
    name: string;
    key: string;
}

export interface INewSignPosting extends Base{
    pageName?: string;
    active: boolean;
    newSignPostingIcon: string;
    startDate: string;
    endDate: string;
}

export interface IPopUp extends Base{
    pageName?: string;
    title: string;
    description: string;
    closeCTA: string;
    playCTA: string;
}


export interface FzPreferences extends Base {
    active: boolean;
    pcDescription: string;
    pcKeys: Preferences[];
    ctaText: string;
    subscribeText: string;
    confirmText: string;
    confirmCTA: string;
    exitCTA: string;
    notificationPopupTitle?: string;
    unsubscribeTitle?: string;
    notificationDescriptionDesktop?: string;
    unsubscribeDescription?: string;
    noThanksCTA?: string;
    optInCTA?: string;
    pushPreferenceCentreTitle?: string;
    genericTeamNotificationTitle?: string;
    genericTeamNotificationDescription?:string;
}

export interface IFzOptinEmail extends Base {
    pageName?: string;
    fanzoneEmailPopupTitle?: string;
    fanzoneEmailPopupDescription?: string;
    fanzoneEmailPopupOptIn?: string;
    fanzoneEmailPopupRemindMeLater?: string;
    fanzoneEmailPopupDontShowThisAgain?: string;
}