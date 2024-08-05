import { Component, Inject, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@core/services/cms/cms.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import environment from '@environment/oxygenEnvConfig';
import { BetShareImageCardService } from '@app/lazy-modules/bet-share-image-card/services/bet-share-image-card.service';
import { IBetShare } from '@app/betHistory/models/bet-share.model';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { bethistory } from '@app/lazy-modules/locale/translations/en-US/bethistory.lang';
import { BetShareGTAService } from '../services/bet-share-gta-tracking.service';

@Component({
  selector: 'share-to-social-media-dialog',
  templateUrl: './share-to-social-media-dialog.component.html',
  styleUrls: ['./share-to-social-media-dialog.component.scss']
})
export class ShareToSocialMediaDialogComponent extends AbstractDialogComponent {

  @ViewChild('shareToSocialMediaDialog', { static: true }) dialog;

  @Inject(MAT_DIALOG_DATA) public data: any;
  currencySymbol: string;
  isCoral: boolean;
  betStatusControlData: string;
  settledBetsCheck: boolean;
  flags: any ={};
  imageObj: HTMLImageElement;
  files: File[];
  brandLogo: HTMLImageElement;
  dataForming: string;
  cmsData: IBetShare;
  hrImageObj: HTMLImageElement;
  footballImageObj: HTMLImageElement;
  fiveASideImageObj: HTMLImageElement;
  openBetsImageObj: HTMLImageElement;
  settledBetsImageObj: HTMLImageElement;
  extensionUrlObj: HTMLImageElement;
  beGambleAwareLogoUrlObj: HTMLImageElement;
  popUpDesc: string;
  betDataToShare: any;
  shareData: any;
  bet: any;
  isShareAllowed: boolean = true;
  sportType = 'Sports';
  userPrefernceNames = [{ returns: 'Returns' },{ odds: 'Odds' },{ stake: 'Your Stake' },
  { selectionName: 'Selection Name' },{ eventName: 'Event Name' },{ date: 'Date' }];

  /**
   * to open dialog box of congrats message
   * @returns {void}
   */

  constructor(device: DeviceService,  windowRef: WindowRefService,
    private sessionStorageService: SessionStorageService,
    private cmsService: CmsService,
    protected betShareImageCardService:BetShareImageCardService,
    private nativeBridgeService: NativeBridgeService,
    private pubSubService: PubSubService, private betShareGTAService: BetShareGTAService
    ) {
    super(device, windowRef);
    this.isCoral = environment && environment.brand === 'bma';
    if(!this.cmsData){
      this.cmsService.fetchBetShareConfigDetails().subscribe((data) => {
        this.cmsData = data;
        this.createImageObjects();
      });
    }
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.pubSubService.subscribe('betSharing', this.pubSubService.API.BET_SHARING_COMPLETED, (data) => {
      this.prepareGTMObject(false, data.detail.appName);
    });
    this.isShareDisabled(this.flags);
    const canvas = <HTMLCanvasElement>document.getElementById('intialiseShareFonts');
    this.initializeFonts(canvas);   
  }

  initializeFonts(canvas){
    const context = canvas.getContext('2d');
    context.font = this.isCoral ? "40px PantonRustHeavyGr" : "40px Tungsten Bold";
    context.drawImage(this.hrImageObj, 0, 0, this.hrImageObj.width, this.hrImageObj.height);
    context.fillText( "Initialising header fonts" , 20, 20);
    context.font = this.isCoral ? "40px Rubik" : "40px Roboto Condensed";
    context.fillText( "Initialising description fonts" , 20, 20);
  }

  createImageObjects(){
    this.popUpDesc = this.cmsData.popUpDesc;
    this.hrImageObj= this.betShareImageCardService.prepImgObject( this.cmsData.horseRacingUrl );
    this.footballImageObj= this.betShareImageCardService.prepImgObject( this.cmsData.footBallUrl );
    this.fiveASideImageObj= this.betShareImageCardService.prepImgObject( this.cmsData.url5ASide );
    this.openBetsImageObj= this.betShareImageCardService.prepImgObject( this.cmsData.openBetsGenericUrl );
    this.settledBetsImageObj= this.betShareImageCardService.prepImgObject( this.cmsData.settledBetsGenericUrl );
    this.extensionUrlObj = this.betShareImageCardService.prepImgObject(this.cmsData.extensionUrl);
    this.beGambleAwareLogoUrlObj = this.betShareImageCardService.prepImgObject(`${this.cmsData.beGambleAwareLogoUrl}`);
    this.brandLogo = this.betShareImageCardService.prepImgObject(this.cmsData.brandLogoUrl);
  }

  public open(): void {
    if(this.params.data && this.params.data.sportType){
      this.bet = this.params.data.betData;
      this.dataForming = `${this.params.data.sportType}DataFormation`;
      this.shareData = this.betShareImageCardService[this.dataForming](this.params.data);
      this.betShareOverlayPopupData();
      super.open();
      this.windowRef.document.body.classList.add('bet-share-modal-open');
    }
  }

  betShareOverlayPopupData(){
    if (this.cmsData) {
      this.settledBetsCheck = (this.bet.eventSource ? this.bet.eventSource.settled : this.bet.settled ? this.bet.settled: this.bet.bet.settled) === 'Y';
        this.currencySymbol = this.params.data.currencySymbol;
      const status = this.bet.eventSource ? this.bet.eventSource.totalStatus : this.bet.status ? this.bet.status : this.bet.betData.bet.status;
      this.betStatusControlData = status === 'cashed out' ? 'cashedOutBetControl'
        : this.settledBetsCheck ? status === 'won' ? 'wonBetControl' : 'lostBetControl' : 'openBetControl';
      const dataType = this.cmsData[this.betStatusControlData];
      const userPreferncesList={};
        this.userPrefernceNames.forEach((userPrefData,index)=>{
          const key =Object.keys(userPrefData)[0];
          const flagIndex = dataType.findIndex((data)=>{ return data.name.split(' ').join('').toLowerCase().includes(key.toLowerCase())});
          this.flags[`${key}Flag`] = dataType[flagIndex].isSelected;
          if(dataType[flagIndex].isSelected){
            userPreferncesList[key] = userPrefData[key];
          }
        })
      const userPref = this.sessionStorageService.get('userPrefernceFlags');
      const keys = userPref && userPref[this.betStatusControlData] && Object.keys(userPref[this.betStatusControlData]);
      keys && keys.forEach((userPreferenceflag) => {
        this.flags[userPreferenceflag] = userPref[this.betStatusControlData][userPreferenceflag]
      })
      this.betDataToShare = {
        popUpTitle: this.popUpDesc,
        ...this.flags,
        description: userPreferncesList,
        shareData: this.shareData
      }
      this.isShareDisabled(this.flags);
    }
  }

  checked(isChecked: boolean, key: string): void {
    const data={};
    let sessionData = this.sessionStorageService.get('userPrefernceFlags');
    sessionData= sessionData? sessionData:{};
    if(sessionData && sessionData[this.betStatusControlData]){
      sessionData[this.betStatusControlData][key + 'Flag'] = isChecked;
    }else{
      data[key + 'Flag'] = isChecked;
      sessionData[this.betStatusControlData] = data;
    }
    this.flags[key + 'Flag'] = isChecked;
    this.isShareDisabled(this.flags);
    sessionData && this.sessionStorageService.set('userPrefernceFlags',sessionData);
  }

  close(closeClicked: boolean): void {
    this.windowRef.document.body.classList.remove('bet-share-modal-open');
    closeClicked && this.prepareGTMObject(false);
    super.closeDialog();
  }

  share(canvasOut?): void {
    this.close(false);
    this.shareData.flags = this.flags;
    const data = this.params.data.betData.eventSource || this.params.data.betData;
    const status = this.params.data.betData.eventSource ? this.params.data.betData.eventSource.totalStatus : this.params.data.betData.status;
    const settledStatus = this.params.data.betData.isSettled || this.params.data.betData.settled;
    const isOpen =  status === 'cashed out' ? false : ( settledStatus ? settledStatus === 'N': ( this.params.data.betData.eventSource ? this.params.data.betData.eventSource.settled === "N" : this.params.data.betData.bet.settled === "N" ) );
    this.shareData.imageObj = this.setSportBasedImageUrl(data,isOpen);
    this.shareData.betId = this.params.data.betData.eventSource ? this.params.data.betData.eventSource.betId : this.params.data.betData.id;
    this.shareData.isSettled = !isOpen;
    this.shareData.sortType = this.params.data.betData.eventSource && this.params.data.betData.eventSource.sortType;
    const BetType = this.shareData.betType !== 'lotto' ? (this.shareData.sortType ?  `${bethistory.betTypes[this.shareData.betType]} - ${this.shareData.sortType}` : bethistory.betTypes[this.shareData.betType]? bethistory.betTypes[this.shareData.betType] : this.shareData.betType) : this.shareData[0].marketName;
    const TPR = this.shareData.returns && ('£' + this.shareData.returns.toString().replace('£',''));
    const msg1 = status === 'cashed out' ? this.cmsData.cashedOutBetsShareCardMessage : isOpen ? this.cmsData.openBetShareCardMessage :
    status === "won" ? this.cmsData.wonBetShareCardMessage : this.cmsData.lostBetsShareCardMessage;
    this.shareData.cashedOutValue = ( status === 'cashed out' && this.shareData.isSettled ) ? ( data.gtmCashoutValue || data.potentialPayout ) : '';
    const data1 = this.replacePlaceholder(msg1, BetType, TPR);
    this.shareData.msg1 = data1;
    if(isOpen) {
      const msg2 = this.cmsData.openBetShareCardSecondMessage;
      const data2 = this.replacePlaceholder(msg2, BetType, TPR);
      this.shareData.msg2 = data2;
    }
    this.prepareGTMObject(true);

    const betShareImgData = this.betShareImageCardService.shareImageDataMapper(this.flags,this.shareData,this.params.data.sportType,this.currencySymbol);
    this.prepareImg(betShareImgData, canvasOut);
  }

  replacePlaceholder(literal, betType, tpr) {
    let message: string = '';
    message = literal.replace('${BetType}', betType);
    message = message.replace('${TPR}', tpr);
    return message;
  }

  setSportBasedImageUrl(data,isOpenBet: boolean): any {
    const eventCategoryId = [], categoryName = [];
    let isUniqueSport;
    if(data.leg){
      data.leg.forEach((legItem)=>{
        eventCategoryId.push(legItem.eventEntity ? legItem.eventEntity.categoryId : ( legItem.part && ( Array.isArray(legItem.part[0].outcome) ? legItem.part[0].outcome[0].eventCategory.id :
                                legItem.part[0].outcome.eventCategory.id ) ) );                         
        categoryName.push(legItem.eventEntity ? legItem.eventEntity.categoryName : ( legItem.part && ( Array.isArray(legItem.part[0].outcome) ? legItem.part[0].outcome[0].eventCategory.name :
                            legItem.part[0].outcome.eventCategory.name ) ) );
        if(new Set(eventCategoryId).size !== 1 || new Set(categoryName).size !== 1) {
          isUniqueSport = false;
          return isUniqueSport;
        }
        else{
          isUniqueSport = true;
        }
      });

    }
    if (!isUniqueSport) {
      return isOpenBet ? this.openBetsImageObj : this.settledBetsImageObj;
    }
    else if(this.params.data.sportType !== 'lotto' && ( eventCategoryId[0] === environment.CATEGORIES_DATA.racing.horseracing.id) && this.cmsData.horseRacingUrl)
    {
      return this.hrImageObj;
    }
    else if(data.bybType === '5-A-Side' && categoryName[0] === "Football"  && this.cmsData.url5ASide){
      return this.fiveASideImageObj;
    }
    else if(categoryName[0] === "Football"  && this.cmsData.footBallUrl){
      return this.footballImageObj;
    }
    else {
      return isOpenBet ? this.openBetsImageObj : this.settledBetsImageObj;
    }
  }

  prepareImg(data, canvasOut?): void {
    try {
      const canvas = canvasOut? canvasOut : <HTMLCanvasElement>document.getElementById(data.betId);
      const context = canvas.getContext('2d');
      let yAxis = 100;
      const urlImg = data.imageObj;
      if (urlImg) {
        let count = data.length;
        canvas.width = urlImg.width;
        let linesCount = 0;
        if (data.betType === 'Totepool') {
          count = 1;
          linesCount += data.length - 1;
          for(let i = 0; i < data.length; i++) {
            linesCount += this.returnLength(data, i);
          }
        } else {
          linesCount += this.returnLength(data, 0)
        }

        let selLength = 0;
        if (data[0].selectionName && ['Bet Builder', 'Build Your Bet', '5-A-Side'].includes(data.betType)) {
          selLength = data[0].selectionName.length;
        }

        let bbLength = 0;
        if (['Bet Builder', 'Build Your Bet'].includes(data.betType)) {
          data[0].selectionName && data[0].selectionName.forEach( name => {
            if (name.includes(',')) {
              bbLength++;
            }
          });
        }

        let lottoResultsLen = 0;
        if (data.betType === 'lotto') {
          lottoResultsLen = data[0].lotteryDrawResults.length;
        }

        const calculatedHeight = 320 + (count * linesCount * (linesCount === 3 ? 30 : linesCount === 2 ? 35 : 25)) + (selLength * 50) + (bbLength * 15) + (lottoResultsLen * 40);
        canvas.height =  (calculatedHeight <= urlImg.height) ? urlImg.height : calculatedHeight;

        if (!urlImg.height) {
          urlImg.height = canvas.height;
        }

        const extensionLoops = Math.floor(canvas.height / urlImg.height);

        // Sports image
        context.drawImage(urlImg, 0, 0, urlImg.width, urlImg.height);

        // Extension image
        for(let i = 1; i <= extensionLoops; i++) {
          context.drawImage(this.extensionUrlObj, 0, urlImg.height*i, urlImg.width, this.extensionUrlObj.height);
        }
        // Bet Gamble Aware logo
        context.drawImage(this.beGambleAwareLogoUrlObj, 20, canvas.height - 35, 160, 20);
        if (data.betFullDate) {
          context.font = this.isCoral ? "15px Rubik" : "15px Roboto Condensed";
          context.fillStyle = "#fff";
          context.fillText(`${data.betFullDate.toUpperCase()}`, 20, 40, 300);
        }
        // Brand logo
        context.drawImage(this.brandLogo, 412, 20, 110, 20);
        context.font = this.isCoral ? "40px PantonRustHeavyGr" : "40px Tungsten Bold";
        context.fillStyle = "#fff";
        if(data.msg1){
          const msg1LenBefore = context.measureText(data.msg1.toUpperCase()).width;
          if (msg1LenBefore > (canvas.width - 40)) {
            context.font = this.isCoral ? "30px PantonRustHeavyGr" : "30px Tungsten Bold";
          }
          context.fillText(`${data.msg1.toUpperCase()}`, 20, yAxis += 20, canvas.width - 40);
        }
        context.font = this.isCoral ? "30px PantonRustHeavyGr" : "30px Tungsten Bold";
        data.msg2 && context.fillText(`${data.msg2.toUpperCase()}`, 20, yAxis += 35, canvas.width - 40);
        if(data[0].selectionHeaderName && data.betType.toLowerCase().includes('pool')){
          context.font = this.isCoral ? "bold 20px Rubik" : "bold 20px Roboto Condensed";
          context.fillText(this.fittingString(context, data[0].selectionHeaderName, 329), 20, yAxis += 20);
        }

        if(data[0].selectionOutcomes && data[0].selectionOutcomes.length > 0 && (data[0].marketName.includes('Build Your Bet') || ['Bet Builder','5-A-Side'].includes(data.betType)) ){
          yAxis += 20;
          data[0].selectionOutcomes.forEach((linedata) => {
            yAxis += 20;
            linedata.split(',').forEach((line)=>{
              context.font = this.isCoral ? "bold 20px Rubik" : "bold 20px Roboto Condensed";
              context.fillText(this.fittingString(context, line, 329), 20, yAxis += 20);
            });
          });
        }
        data.forEach((linedata) => {
          const line1 = linedata.line1;
          const line2 = linedata.line2;
          const line3 = linedata.line3;
          yAxis += 30;

          if (line1 && typeof line1 === 'string') {
              context.font = this.isCoral ? "bold 20px Rubik" : "bold 20px Roboto Condensed";
              context.fillText(this.fittingString(context, line1, 329), 20, yAxis += 20);
          }
          else if(line1 && Array.isArray(line1)) {
            line1.forEach((line)=>{
              context.font = this.isCoral ? "bold 20px Rubik" : "bold 20px Roboto Condensed";
              context.fillText(this.fittingString(context, line, 329), 20, yAxis += 20);
            });
          }

          if (line2 && typeof line2 === 'string') {
            context.font = this.isCoral ? "15px Rubik" : "15px Roboto Condensed";
            context.fillText(this.fittingString(context, line2, 329), 20, yAxis += 20);
          }
          else if(line2 && Array.isArray(line2)) {
            line2.forEach((line)=>{
              context.font = this.isCoral ? "15px Rubik" : "15px Roboto Condensed";
              context.fillText(this.fittingString(context, line, 329), 20, yAxis += 20);
            });
          }

          if (line3 && typeof line3 === 'string') {
            context.font = this.isCoral ? "bold 17px Rubik" : "bold 17px Roboto Condensed";
            context.fillText(this.fittingString(context, line3, 329), 20, yAxis += 20);
          }
          else if(line3 && Array.isArray(line3)) {
            line3.forEach((line) => {
              context.font = this.isCoral ? "bold 17px Rubik" : "bold 17px Roboto Condensed";
              context.fillText(this.fittingString(context, line, 329), 20, yAxis += 20);
            });
          }
        });

        if(data[0].lotteryDrawResults && data.betType === 'lotto')
        {
          data[0].lotteryDrawResults.forEach((lineData)=>{
            yAxis += 20;
            context.font = this.isCoral ? "bold 20px Rubik" : "bold 20px Roboto Condensed";
            context.fillText(this.fittingString(context, lineData.drawLineName, 329), 20, yAxis += 20);
          })
        }

        context.font = "bold 20px Calibri";
        context.fillText(this.fittingString(context, "__________________________________", 329, true), 20, yAxis += 10);

        context.font = this.isCoral ? "bold 20px Rubik" : "bold 20px Roboto Condensed";
        context.beginPath();
        context.moveTo(20, yAxis);
        context.lineTo(346, yAxis);
        context.closePath();

        if (data.stake) {
          context.fillText("TOTAL STAKE:", 20, yAxis += 30);
        }
        const retunrsLabel = data.isSettled ? "RETURNS:" : "POT. RETURNS:";
        if (data.stake && data.returns) {
          context.fillText(retunrsLabel, 170, yAxis);
        } else if (data.returns) {
          context.fillText(retunrsLabel, 20, yAxis += 30);
        }

        context.font = this.isCoral ? "bold 30px Rubik" : "bold 30px Roboto Condensed";
        context.fillStyle = "#FAC031";
        data.stake && context.fillText(data.stake, 20, yAxis += 30);
        if (data.stake && data.returns) {
          context.fillText(data.returns, 170, yAxis)
        } else if (data.returns) {
          context.fillText(data.returns, 20, yAxis += 30)
        }
        context.font = this.isCoral ? "10px Rubik" : "10px Roboto Condensed";
        context.fillStyle = "#fff";
        context.fillText(`ODDS CORRECT AT ${data.betFullDateTime}`, 20, yAxis += 30);
        this.sendEditedImage(data, null, canvasOut);
      }
    }
    catch(e) {
      console.log("Error while preparing canvas image", e);
    }
  }

  sendEditedImage(data, fileReader?, canvasOut?): void {
    try {
      this.files = [];
      const canvas = canvasOut ? canvasOut : <HTMLCanvasElement>document.getElementById(data.betId);
      canvas.toBlob((blob) => {
        this.callBlob(blob);
      });
    }
    catch(e) {
      console.log("Error while calling the blob", e);
    }
  }

  callBlob (blob, fileReader?) {
    const filesArray = [
      new File(
        [blob],
        'betshare.jpg',
        {
          type: "image/jpeg",
          lastModified: new Date().getTime()
        }
      )
    ];

    const sportsUrl = this.cmsData.genericSharingLink;

    if (this.device.isAndroid && this.device.isWrapper) {
      try {
        const reader = fileReader? fileReader : new window.FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => {
        // send base64data string to android as a method param
          this.nativeBridgeService.shareContentOnSocialMediaGroups({base64data: reader.result.toString(), sportsUrl});
        }
      } catch (e) {
        console.error("Error while sending base64 data", e);
      }
    } else {
      this.files.push(filesArray[0]);

      const shareData = {
        files: filesArray
      };

      if (this.device.isAndroid) {
        shareData['url'] = sportsUrl;
      }

      if (this.windowRef.nativeWindow.navigator.canShare && this.windowRef.nativeWindow.navigator.canShare(shareData)) {
        this.windowRef.nativeWindow.navigator.share(shareData)
          .then(() => console.log('Share was successful.'))
          .catch((error) => console.log('Sharing failed', error));
      }
    }
  }

  statusText(status: string): string {
    return (status === 'won' || status === 'cashed out') ? `You ${status}: `:'Potential returns: ';
  }

  tranformWithCurrency(data: string): string{
    if(data){
      return (data.toString().indexOf(this.currencySymbol)  >= 0)? data : this.betShareImageCardService.transfromToCurrency(data, this.currencySymbol);
    }
  }

  private fittingString(ctx, str: string, maxWidth:number, isLine = false): string {
    let width = ctx.measureText(str).width;
    const ellipsis = isLine ? '_' : '…';
    const ellipsisWidth = ctx.measureText(ellipsis).width;
    if (width<=maxWidth) {
      return str;
    } else {
      let len = str.length;
      while (width >= maxWidth-ellipsisWidth && len-- > 0) {
        str = str.substring(0, len);
        width = ctx.measureText(str).width;
      }
      return str+ellipsis;
    }
  }

  private isShareDisabled(flags: any): void {
    this.isShareAllowed = false;
    for (const [key, value] of Object.entries(flags)) {
      if(value) {
        const flagKey = key.split('Flag')[0];
        const keyValue = this.betDataToShare.shareData[flagKey] ? this.betDataToShare.shareData[flagKey] : (this.betDataToShare.shareData[0] && this.betDataToShare.shareData[0][flagKey]);
        this.userPrefernceNames.forEach((up) => {
          if (up.hasOwnProperty(`${flagKey}`) && keyValue) {
            this.isShareAllowed = true;
          }
        })
      }
      if (this.isShareAllowed) {
        break;
      }
    }
  }

  private prepareGTMObject(shareClicked: boolean, appName?: string): void {
    const positionEvent = ( this.params.data.betData.location === "cashOutSection" ) ? 'cash out' : ( this.settledBetsCheck ? 'settled bets': 'open bets' );
    const gtaSportType = this.params.data.sportType === 'regularBets'? 'sports' : (this.params.data.sportType === 'totePotPoolBet'? 'pools': this.params.data.sportType);
    let eventDetails = '';
    if (shareClicked) {
      for (const [key, value] of Object.entries(this.flags)) {
        if(value) {
          const flagKey = key.split('Flag')[0];
          const keyValue = this.betDataToShare.shareData[flagKey] ? this.betDataToShare.shareData[flagKey] :this.betDataToShare.shareData[0][flagKey];
          this.userPrefernceNames.forEach((up) => {
            if (up.hasOwnProperty(`${flagKey}`) && keyValue) {
              eventDetails = eventDetails + up[`${flagKey}`].toLowerCase() + ':';
            }
          })
        }
      }
    } else {
      eventDetails = appName ? `${appName}:` : 'cancelled:';
    }
    this.betShareGTAService.setGtmData(positionEvent, gtaSportType, eventDetails.substring(0, eventDetails.length - 1));
  }

  private returnLength(data: any, index: number): number {
    let lines = 0;
    if (data[index].line1) {
      if (typeof data[index].line1 === 'string') {
        ++lines;
      } else if (Array.isArray(data[index].line1)) {
        lines += data[index].line1.length;
      }
    }
    if (data[index].line2) {
      if (typeof data[index].line2 === 'string') {
        ++lines;
      } else if (Array.isArray(data[index].line2)) {
        lines += data[index].line2.length;
      }
    }
    if (data[index].line3) {
      if (typeof data[index].line3 === 'string') {
        ++lines;
      } else if (Array.isArray(data[index].line3)) {
        lines += data[index].line3.length;
      }
    }
    return lines;
  }
}
