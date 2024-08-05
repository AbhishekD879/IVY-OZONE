import { SafeHtml } from '@angular/platform-browser';

export class QuestionEngineSplashPageModel {
  backgroundSvgFilePath: string;
  ctaButtonText: string;
  footerSvgFilePath: string;
  footerSvgUrl: string;
  footerText: string;
  loginToViewCTAText: string;
  logoSvgFilePath: string;
  logoSvgUrl: string;
  paragraphText1: string;
  paragraphText2: string;
  paragraphText3: string;
  playForFreeCTAText: string;
  seePreviousSelectionsCTAText: string;
  seeYourSelectionsCTAText: string;
  strapLine: SafeHtml;
  showPreviousGamesButton: boolean;

  constructor(
    strapLine: SafeHtml,
    paragraphText1: string,
    paragraphText2: string,
    paragraphText3: string,
    footerText: string,
    footerSvgUrl: string,
    footerSvgFilePath: string,
    logoSvgUrl: string,
    logoSvgFilePath: string,
    ctaButtonText: string,
    loginToViewCTAText: string,
    playForFreeCTAText: string,
    seePreviousSelectionsCTAText: string,
    seeYourSelectionsCTAText: string,
    backgroundSvgFilePath: string,
    showPreviousGamesButton: boolean
  ) {
    this.strapLine = strapLine;
    this.paragraphText1 = paragraphText1;
    this.paragraphText2 = paragraphText2;
    this.paragraphText3 = paragraphText3;
    this.footerText = footerText;
    this.footerSvgUrl = footerSvgUrl;
    this.footerSvgFilePath = footerSvgFilePath;
    this.logoSvgUrl = logoSvgUrl;
    this.logoSvgFilePath = logoSvgFilePath;
    this.ctaButtonText = ctaButtonText;
    this.loginToViewCTAText = loginToViewCTAText;
    this.playForFreeCTAText = playForFreeCTAText;
    this.seePreviousSelectionsCTAText = seePreviousSelectionsCTAText;
    this.seeYourSelectionsCTAText = seeYourSelectionsCTAText;
    this.backgroundSvgFilePath = backgroundSvgFilePath;
    this.showPreviousGamesButton = showPreviousGamesButton;
  }
}
