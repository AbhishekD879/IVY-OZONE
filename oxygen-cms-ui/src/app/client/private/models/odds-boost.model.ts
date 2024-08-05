import { Base } from './base.model';
import {SvgFilename} from './svgfilename.model';

export interface OddsBoost extends Base {
  enabled: boolean;
  loggedOutHeaderText: string;
  loggedInHeaderText: string;
  termsAndConditionsText: string;
  moreLink: string;
  allowUserToToggleVisibility: boolean;
  daysToKeepPopupHidden: number;

  svgFilename: SvgFilename;
  lang: string;
  svg: string;
  svgId: string;
  noTokensText:string;
  countDownTimer:string;
}
