import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { BET_TYPES } from '@betslip/constants/bet-slip.constant';

import { LocaleService } from '@core/services/locale/locale.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { LUCKY_TYPES } from '@betslip/constants/bet-slip.constant';
@Injectable({ providedIn: BetslipApiModule })
export class BetInfoDialogService {
  private racingCategories: { [sport: string]: { id: string } };
  isLadbrokes = environment.brand === 'ladbrokes';
  constructor(
    private localeService: LocaleService,
    private infoDialogService: InfoDialogService,
    protected cmsService: CmsService,
  ) {
    this.racingCategories = environment.CATEGORIES_DATA.racing;
  }

  /**
   * Indicates whether it is a racing
   * @param {string} sportId
   * @return {boolean}
   */
  isRacing(sportId: string): boolean {
    return _.some(this.racingCategories, sport => sport.id === sportId);
}
  getLuckyPopupText(lucky, betsdata,getmultiples,luckytext): any {
    let formattedText ; 
    const format:any[]=[];
    betsdata.forEach((value)=>{
      if(Number(value.multiplier) > 1){
        const percentage = Number((value.multiplier*100-100).toFixed(0));
        if(lucky == LUCKY_TYPES.L15.TYPE && value.num_win == LUCKY_TYPES.L15.ALL_WIN ){
          format.push(`All winners - ${percentage}%{BR}`);
        }else if (lucky == LUCKY_TYPES.L31.TYPE && value.num_win == LUCKY_TYPES.L31.ALL_WIN){
          format.push(`All winners - ${percentage}%{BR}`);
        }else if(lucky == LUCKY_TYPES.L63.TYPE && value.num_win == LUCKY_TYPES.L63.ALL_WIN){
          format.push(`All winners - ${percentage}%{BR}`);
        }else{
          format.push(`${Number(value.num_win) == 1 ? value.num_win + ' winner' : value.num_win +' winners'} - ${percentage}%{BR}`);
        }
      }
    })
    if(getmultiples==="betslip"){
      formattedText=luckytext.BetSlipPopUpMessage.replace("{BONUS}", `${format.join('')}`);
    }
    if(getmultiples==="bet receipt"){
      formattedText =  luckytext.BetReceiptPopUpMessage.replace("{BONUS}", `${format.join('')}`);
    }
    if(getmultiples==="settled bets"){
      formattedText =  luckytext.SettledBetPopUpMessage.replace("{BONUS}", `${format.join('')}`);
    }
    return formattedText.replaceAll("{BR}", "<br/>");
  }
  /**
   * Open dialog with multiples info
   * @param {string} betType
   * @param {number} stakeMultiplier
   */
  multiple(betType: string, stakeMultiplier: number, betsdata?:any, isLuckySignPost?: boolean, getmultiples?:string, label?: string): void {
    const isAllBonusAvailable = !(betsdata && betsdata.every(item => Number(item.multiplier) == 1));
    const luckytext = this.cmsService.systemConfiguration['LuckyBonus'];
    const isCmsParams = this.checkProps(luckytext, getmultiples); 
    if(isLuckySignPost == undefined && ['L15', 'L31', 'L63'].includes(betType) && betsdata && luckytext && isCmsParams && isAllBonusAvailable){
      return;
    }
    this.infoDialogService.openInfoDialog(
      this.getDialogTitle(betType, luckytext, getmultiples, betsdata, isCmsParams, isAllBonusAvailable),
      isLuckySignPost? this.getLuckyPopupText(betType, betsdata,getmultiples,luckytext) :this.getMultiplesInfo(betType, stakeMultiplier), //todo: luckybonus : fetch text from API for lucky
      'bs-selection-info-dialog',
      undefined,
      undefined,
      this.getButtons(),
      this.getLinks(isLuckySignPost, (luckytext && luckytext["MoreInfoURL"])),
      isLuckySignPost,
      getmultiples,
      label
    );
  }

  getLinks(isLuckySignPost, Url?): any {
    if(isLuckySignPost) {
       return [
        {
          caption: this.localeService.getString('bs.more'),
          cssClass: 'link-more', //todo: luckybonus : change the class and apply style accordingly
          hyperlink: Url
        }
      ]
    } 
    return [];
  }

  getButtons() : any {
    const buttons = [
      {
        caption: this.localeService.getString('bs.ok'),
        cssClass: 'btn-style2',
        handler: () => {
          this.infoDialogService.closePopUp();
        }
      }
    ]
    return buttons;
  }

  /**
   * returns multiple info
   * @param {string} betTypeName
   * @param {number} stakeMultiplier
   * @return {string}
   */
  private getMultiplesInfo(betTypeName: string, stakeMultiplier: number): string {
    const generalBetType = this.getGeneralBetType(betTypeName);
    const text = this.localeService.getString(`bs.${generalBetType}_dialog_info`);
    return text === 'KEY_NOT_FOUND' ? this.localeService.getString('bs.betsNumber', [stakeMultiplier]) :
      this.localeService.getString(`bs.${generalBetType}_dialog_info`);
  }

  private getGeneralBetType(betType: string): string {
    if (betType.indexOf(BET_TYPES.accumulatorBet) !== -1) {
      return `${BET_TYPES.accumulatorBet}_common`;
    } else if (betType.indexOf(BET_TYPES.singleAboutBet) !== -1) {
      return `${BET_TYPES.singleAboutBet}_common`;
    } else if (betType.indexOf(BET_TYPES.doubleAboutBet) !== -1) {
      return `${BET_TYPES.doubleAboutBet}_common`;
    } else {
      return betType;
    }
  }

  private getDialogTitle(betType: string, luckytext, getmultiples, betsdata, isCmsParams, isAllBonusAvailable): string {
    if(luckytext && (['L15', 'L31', 'L63'].includes(betType)) && betsdata && isCmsParams && isAllBonusAvailable){
      let headerMessage; 
      const headerValue = betType.replace('L', 'Lucky ');
      if(getmultiples==="betslip"){
        headerMessage=luckytext.BetSlipPopUpHeader.replace("{BET_TYPE}", headerValue);
      }
      if(getmultiples==="bet receipt"){
        headerMessage =  luckytext.BetReceiptPopUpHeader.replace("{BET_TYPE}", headerValue);
      }
      if(getmultiples==="settled bets"){  
        headerMessage =  luckytext.SettledBetPopUpHeader.replace("{BET_TYPE}", headerValue);
      }
      return headerMessage;
    }else{
      return this.localeService.getString(`bs.${this.getGeneralBetType(betType)}`);
    }
  }
  
  private checkProps(cmsData, section): boolean{
    if (cmsData) {
      let headerKey, messageKey;
      switch (section) {
        case 'betslip':
          headerKey = 'BetSlipPopUpHeader';
          messageKey = 'BetSlipPopUpMessage';
          break;
        case 'bet receipt':
          headerKey = 'BetReceiptPopUpHeader';
          messageKey = 'BetReceiptPopUpMessage';
          break;
        case 'settled bets':
          headerKey = 'SettledBetPopUpHeader';
          messageKey = 'SettledBetPopUpMessage';
          break;
        default:
          return false;
      }
      return !!(cmsData[headerKey] && cmsData[headerKey].trim().length > 0 && cmsData[messageKey] && cmsData[messageKey].trim().length > 0);
    }
    return false;
  }
}