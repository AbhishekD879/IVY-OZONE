import { IPrizePool } from '@app/five-a-side-showdown/models/prize-pool';

export interface ContestForm {
    contestId: string;
    contestTitle: string;
    nameLabel: string;
    nameMsg: string;
    iconLabel: string;
    removeFileLabel: string;
    startDateLabel: string;
    startDateMsg: string;
    eventLabel: string;
    entryStakeLabel: string;
    entryStakeMsg: string;
    freeBetsLabel: string;
    sponsorLogoLabel: string;
    sponsorTextLabel: string;
    removeLabel: string;
    maxEntries: string;
    maxEntriesPerUser: string;
    blurbLabel: string;
    entryLabel: string;
    nextContestIdLabel: string;
    displayLabel: string;
    realAccountLabel: string;
    testAccountLabel: string;
    descriptionLabel: string;
    createContestLabel: string;
    contestHeadingLabel: string;
    contestTableHeaderLabel: string;
    contestTableNoDataLabel: string;
    saveLabel: string;
    saveAnotherLabel: string;
    cancelLabel: string;
    userAccountsLabel: string;
    currentEntriesLabel?: string;
    enableServiceLabel: string;
    serviceMsgLabel: string;
    invitationalContest:string;
    contestType:string;
    generatedMagicLink:string;
    contestURL: string;
    copyContestURL: string;
    crmPrizeIndicator: string;
}

export interface HTMLInputEvent extends Event {
   target: HTMLInputElement & EventTarget;
}
export interface IAddContest  {
    brand: string;
    createdAt: string;
    createdBy: string;
    createdByUserName: string;
    id: string;
    lang: string;
    name: string;
    entryStake: string;
    startDate: string;
    updatedAt: string;
    updatedBy: string;
    updatedByUserName: string;
    event?: string;
    utcStartDate?: string;
    display?: boolean;
    intialContestId?: string;
}

export interface IContest {
    id: string;
    createdBy?: string;
    createdByUserName?: string;
    updatedBy?: string;
    updatedByUserName?: string;
    createdAt?: string;
    updatedAt?: string;
    sortOrder?: number;
    generatedId?: string;
    name: string;
    icon?: IContestFile;
    startDate: string;
    contestId?: string;
    entryStake: string;
    isFreeBetsAllowed?: boolean;
    originalname?: string;
    prizePool?: IPrizePool;
    payTable?: any[];
    sponsorText?: string;
    sponsorLogo?: IContestFile ;
    maxEntries?: string;
    maxEntriesPerUser?: string;
    description?: string;
    blurb?: string;
    entryConfirmationText?: string;
    nextContestId?: string;
    display?: boolean;
    brand?: string;
    isActive?: boolean;
    isiconSvgChanged?: boolean;
    isSponsorSvgChanged?: boolean;
    testAccount?: boolean;
    realAccount?: boolean;
    completed?: boolean;
    reportGenerated?: boolean;
    entriesSize?: number;
    utcStartDate?: string;
    serviceMsg?: string;
    enableServiceMsg?: boolean;
    isInvitationalContest? : boolean;
    isPrivateContest?: boolean;
    contestURL: string;
    crmPrizeIndicator: boolean;
    intialContestId?: string;
    event?: string;
 }

 export interface IContestFile extends File {
    originalname?: string;
 }

 export interface DialogData {
    data: {
        dialogType: string;
        dialogData: IContest;
    }
 }
