import { Base } from './base.model';
import { Filename } from '@app/client/public/models/filename.model';

export interface SplashPage extends Base {
  title: string;
  brand: string;
  strapLine: string;
  paragraphText1: string;
  paragraphText2: string;
  paragraphText3: string;
  playForFreeCTAText: string;
  seeYourSelectionsCTAText: string;
  seePreviousSelectionsCTAText: string;
  loginToViewCTAText: string;
  showPreviousGamesButton: boolean;
  backgroundSvgFile: Filename;
  backgroundSvgFilename: string;
  logoSvgFile: Filename;
  logoSvgFilename: string;
  footerSvgFile: Filename;
  footerSvgFilename: string;
  footerText: string;
  isChanged: boolean;

}

export const EMPTY_SP = {
  id: '-1',
  title: '',
  strapLine: '',
  paragraphText1: '',
  paragraphText2: '',
  paragraphText3: '',
  playForFreeCTAText: '',
  seeYourSelectionsCTAText: '',
  seePreviousSelectionsCTAText: '',
  loginToViewCTAText: '',
  backgroundSvgFile: {} as Filename,
  backgroundSvgFilename: '',
  logoSvgFile: {} as Filename,
  logoSvgFilename: '',
  footerSvgFile: {} as Filename,
  footerSvgFilename: '',
  footerText: '',
  updatedBy: '',
  updatedAt: '',
  createdBy: '',
  createdAt: '',
  brand: '',
  updatedByUserName: '',
  createdByUserName: '',
  showPreviousGamesButton: false,
  isChanged: false
};
