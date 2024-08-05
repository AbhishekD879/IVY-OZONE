import { Base } from 'app/client/private/models/base.model';
export interface MystableModel extends Base{
  horsesRunningToday: boolean,
  entryPointIcon: string,
  entryPointLabel: string,
  editLabel: string,
  saveLabel: string,
  editIcon: string,
  signpostingIcon: string,
  notesSignPostingIcon: string,
  bookmarkIcon:string,
  unbookmarkIcon:string,
  active: boolean,
  emptyStableLabel1:string;
  emptyStableLabel2:string;
  noHorsesCtaButton:string;
  saveIcon:string;
  editNoteIcon:string;
  noHorsesIcon:string;
  antePost:boolean;
  mybets:boolean;
  settledBets:boolean;
  stableTooltipText:string;
  todayRunningHorsesText:string;
  horseCountExceededMsg:string;
  todayRunningHorsesSvg:string;
  inProgressIcon:string;
  crcActive: boolean;
  crcLogo?: string;
  crcLabel?: string;
  crcSignPostingIcon?:string;
  crcSaveAllText?:string;
  crcWhiteBookmarkIcon?:string;
  crcBlackBookmarkIcon?:string;
  crcGotoRacingClubText?:string;
  crcGotoRacingClubUrl?:string; 
}