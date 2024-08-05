import { DataTableColumn } from '@app/client/private/models';
import { ContestForm } from '@app/five-a-side-showdown/models/contest-manager';

export const ACTION_TYPE = {
  remove: 'remove',
  save: 'save',
  revert: 'revert'
};

export const REORDER_MSG = {
    message: 'Contests Order Saved!',
    action: 'Ok!'
};

export const SAVE_NOTIFICATION_DIALOG = {
  title: 'Contest Update Completed',
  message: 'Contest is Saved.',
};

export const ICON_SVG_FORM_NAME = 'contestIcon';

export const SPONSOR_SVG_FORM_NAME = 'contestLogo';

export const SAVE_SVG_IMAGES_FAILURE_MSG = {
  msg: `Contest details Updated, but svg Images are not uploaded`,
};

export const CREATE_CONTEST_DIALOG = {
  title: 'Create Contest:',
  message: 'Do You Want to Create Contest ?.',
};


export const IMAGE_FORMAT_DIALOG = {
  title: 'Error. Unsupported file type.',
  message: "Supported 'svg'.",
};

export const UPLOAD_BTNS = {
  uploadFileLabel: 'Upload File',
  changeFileLabel: 'Change File',
};

export const REMOVE_CONFIRMATION_DIALOG = {
  title: 'Remove Contest',
  message: 'Are You Sure You Want to remove contest',
};

export const REMOVE_CONFIRMATION_SUCCESS_DIALOG = {
  title: 'Remove Completed',
  message: 'Contest is removed.',
};

export const REMOVE_CONFIRMATION_MULTI_DIALOG = {
  title: 'Remove Contests',
  message: 'Are You Sure You Want to Remove selected contests ?',
};

export const REMOVE_CONFIRMATION_MULTI_SUCCESS_DIALOG = {
  title: 'Remove Completed',
  message: 'Selected contests Removed.',
};

export const SUPPORTED_IMAGE_FILE_EXTENSIONS = ['image/svg', 'image/svg+xml'];

export const BREADCRUMB_DATA = {
  contestLabel: 'Contest',
  contests_url: '/five-a-side-showdown',
  edit_url: '/five-a-side-showdown/edit',
};

export const CONTEST_ERROR_LABELS = {
  loadingContestLabel: 'Error in loading the contests',
  createContestLabel:  'Error while creating the contest',
  editingContests: 'Error in editing contests with ',
  savingContest: 'Error in saving contest ',
  removingContest: 'Error in removing contest ',
  enableAccountSelection: 'To proceed further, please enable one of these fields test or real Accounts'
}

export const BONUS_SUPPRESSION_ERROR_LABELS = {
  loadingBonusSupModules: 'Error in loading the Modules',
  createBonusSupModule:  'Error while creating the Module',
  editingBonusSupModule: 'Error in editing Module with ',
  savingBonusSupModule: 'Error in saving Module ',
  removingBonusSupModule: 'Error in removing Module ',
}

export const CONTESTFORM: ContestForm = {
  contestId: 'ContestId',
  contestTitle: 'Contest: ',
  nameLabel: 'Name',
  nameMsg: 'Name should be entered',
  iconLabel: 'Icon',
  removeFileLabel: 'Remove File',
  startDateLabel: 'Start Date',
  startDateMsg: 'Start Date needs to be entered',
  eventLabel: 'Event',
  entryStakeLabel: 'Entry Stake',
  entryStakeMsg: 'Entry Stake should be entered',
  freeBetsLabel: 'Free Bets Allowed',
  sponsorLogoLabel: 'Sponsor Logo',
  sponsorTextLabel: 'Sponsor Text',
  removeLabel: 'Remove ',
  maxEntries: 'Max Entries',
  maxEntriesPerUser: 'Max Entries Per User',
  blurbLabel: 'Game Blurb',
  entryLabel: 'Entry Confirmation',
  nextContestIdLabel: 'Next Contest Id',
  displayLabel: 'Display',
  currentEntriesLabel: 'Current Entries',
  realAccountLabel: 'Real Account',
  testAccountLabel: 'Test Account',
  descriptionLabel: 'Description',
  createContestLabel: 'Create Contest',
  contestHeadingLabel: 'Contest Page',
  contestTableHeaderLabel: 'Active Contests',
  contestTableNoDataLabel : 'No Data Found for Contests',
  saveLabel: 'Save',
  saveAnotherLabel: 'Save & Add Another',
  cancelLabel: 'Cancel',
  userAccountsLabel: `User's Allowed :`,
  enableServiceLabel: 'Enable Service Message',
  serviceMsgLabel: 'Enter Service Message',
  invitationalContest: 'Invitational Contest',
  contestType: 'Invitational Contest Display',
  generatedMagicLink: 'Magic Link',
  contestURL: 'Contest URL',
  copyContestURL: 'Copy Contest URL',
  crmPrizeIndicator: 'Automatic Prize Payout'
};

export const CONTEST_TABLE_COLUMNS: Array<DataTableColumn> = [
  {
    name: 'Contest Name',
    property: 'name',
    link: {
      hrefProperty: 'id',
      path: 'edit',
    },
    type: 'link',
    width: 2,
  },
  {
    name: 'Date - Event start date',
    property: 'startDate',
    type: 'date',
    width: 2,
  },
  {
    name: 'Active',
    property: 'display',
    type: 'boolean',
    width: 1,
  },
];

export const FILTER_PROPERTIES = ['name'];

export const CONTEST_DEFAULT_VALUS = {
  id: '',
  updatedBy: '',
  updatedAt: '',
  createdBy: '',
  createdAt: '',
  updatedByUserName: '',
  createdByUserName: '',
  name: '',
  lang: '',
  brand: null,
  entryStake: ''
};

export const SAVE_CONFIRMATION_DIALOG = {
  title: 'Add Contest',
  yesOption: 'Save',
  noOption: 'Cancel',
};

export const DOWNLOAD_CSV_BUTTON = {
  contestInformation: 'Download Contest Information CSV',
  prizeReport: 'Download Prize Report CSV',
  contestURL: 'CONTEST_INFORMATION',
  prizeReportURL: 'PRIZE_REPORT'
};
