import { Injectable } from "@angular/core";
import { CurrencyPipe } from "@angular/common";
import { BehaviorSubject } from "rxjs";

import { TimeService } from "@app/core/services/time/time.service";
import TotePoolBet from "@app/betHistory/betModels/totePoolBet/tote-pool-bet.class";
import { IOutcome } from "@app/core/models/outcome.model";
import { LocaleService } from "@app/core/services/locale/locale.service";
import { FiltersService } from "@app/core/services/filters/filters.service";
import { ILeg } from "@app/betslip/services/models/bet.model";
import { SessionStorageService } from "@app/core/services/storage/session-storage.service";
import { IBetHistoryLeg } from "@app/betHistory/models/bet-history.model";
import { BybSelectionsService } from "../../bybHistory/services/bybSelectionsService/byb-selections.service";

@Injectable()
export class BetShareImageCardService {
  otherDay: Date | string;
  startTime: Date;
  todayText: string;
  loading: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  shareData: any;
  flags: any;
  imagesLoaded = false;
  timer: any;

  constructor(private timeService: TimeService,
      private localeService: LocaleService,
      private filtersService: FiltersService,
      private currencyPipe: CurrencyPipe,
      private sessionStorageService: SessionStorageService,
      private bybSelectionsService: BybSelectionsService) {
      this.todayText = this.localeService.getString('bethistory.today');
  }

  prepImgObject(cmsData?: string): HTMLImageElement {
    const imageObj: HTMLImageElement = new Image();
    imageObj.crossOrigin = "Anonymous";
    imageObj.onload = () => {
      clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        this.imagesLoaded = true;
      }, 0)
    };
    if (cmsData) {
        imageObj.src = cmsData;
    }
    return imageObj;
  }

  shareImageDataMapper(flags: any, shareData: any, sportType: string, currencySymbol: string): any {
    const betData = Object.assign([], shareData);
    betData.forEach((data) => {
      if (sportType === "regularBets") {
        if (shareData.betType !== 'Bet Builder' && !data.marketName.includes('Build Your Bet') && !(shareData.sortType && shareData.sortType.toLowerCase().includes('cast')) && shareData.betType !== '5-A-Side' ) {
          data.line1 = flags.selectionNameFlag ? (flags.oddsFlag ? `${data.selectionName} @ ${data.odds}` : data.selectionName) : (flags.oddsFlag ? `@ ${data.odds}` : '');
          data.line2 = data.marketName;
          data.line3 = flags.eventNameFlag ? (!data.eventStartTime ? data.eventName : `${data.eventName}, ${data.eventStartTime}`) : '';
        } else {
          if (data.marketName.includes('Build Your Bet') || ['Bet Builder','5-A-Side'].includes(shareData.betType)){
            data.selectionOutcomes = flags.selectionNameFlag ? (data.marketName.includes('Build Your Bet') && data.marketName.split('-')[1]) ? [`${data.selectionName}`, `- ${data.marketName.split('-')[1]}`]: data.selectionName : '';
          }
          else if(shareData.sortType.toLowerCase().includes('cast')){
            data.line1 = flags.selectionNameFlag ? data.selectionName : '';  
          }
          data.line2 = flags.oddsFlag ? `${data.marketName}  @ ${data.odds}` : data.marketName;
          data.line3 = flags.eventNameFlag ? (!data.eventStartTime ? data.eventName : `${data.eventName}, ${data.eventStartTime}`) : '';
        }
      } else {
        data.selectionHeaderName = sportType.toLowerCase().includes('pool') ? data.marketName: '';
        data.line1 = flags.eventNameFlag ? ( ['totePotPoolBet','lotto'].includes(sportType) ? data.eventName : data.marketName ) : '';
        data.line2 = flags.selectionNameFlag ? (sportType === 'lotto' ? data.selectionName.join(' ') :  data.selectionName) : '';
        data.line3 = (sportType === 'totePoolBet' ? (flags.eventNameFlag ? data.eventName : ''): '');
      }
    })
    betData.stake = flags.stakeFlag ? shareData.stake ? (shareData.stake.toString().indexOf(currencySymbol)  >= 0) ? shareData.stake : this.transfromToCurrency(shareData.stake, currencySymbol) : '' : '';
    const returnsValue = ( shareData[0].status === 'cashed out' && shareData.isSettled ) ? shareData.cashedOutValue : shareData.returns;
    betData.returns = flags.returnsFlag ? (returnsValue) ? (returnsValue.toString().indexOf(currencySymbol)  >= 0) ? returnsValue : this.transfromToCurrency(returnsValue, currencySymbol) : '' : '';
    betData.betFullDate = flags.dateFlag ? shareData.betFullDate : '';
    return betData;
  }

  getOutcomeTitle(pool: TotePoolBet, outcome: IOutcome, index: number): string {
    if (!pool) {
        return '';
    }
    let outcomeTitle: string,
        showRunnerNumber: boolean;

    /**
     * If order of bet selection is matter than display place of runner,
     * in other case runner number should be displayed
     */
    if (pool.isOrderedBet) {
        outcomeTitle = `${index + 1}. ${outcome.name}`;
    } else {
      /**
       * Display runner number only for bets with more than 1 selections
       * @type {boolean}
       */
      showRunnerNumber = pool.poolOutcomes.length > 1 && !outcome.isFavourite;
      outcomeTitle = showRunnerNumber ? `${outcome.runnerNumber}. ${outcome.name}` : outcome.name;
    }
    return outcomeTitle;
  }

  /**
   * Get start time for current leg
   * @param leg {object} jackpot leg
   */
  getEventStartTime(leg: ILeg): string {
    this.setStartTime(leg);
    return this.otherDay
        ? this.filtersService.date(this.otherDay, 'dd MMM, h:mm a')
        : `${this.todayText}, ${this.filtersService.date(this.startTime, 'h:mm a')}`;
  }

  transfromToCurrency(shareData, currencySymbol) {
    return this.currencyPipe.transform(shareData, currencySymbol, 'code');
  }

  getTotePtPoolOutcomeTitle(outcome): string {
    return outcome.isFavourite ? outcome.name : `${outcome.runnerNumber}. ${outcome.name}`;
  }

  totePotPoolBetDataFormation(data) {
    const poolEntity = data.betData;
    const legList = [];
    let betLeg = {};
    let eventNamesData: any, selectionNamesData = [];
    poolEntity.leg.forEach((leg, index) => {
      eventNamesData = `Leg ${index + 1} ${poolEntity.getRaceTitle(leg)}`;
      leg.orderedOutcomes.forEach((outcome) => {
        selectionNamesData.push(this.getTotePtPoolOutcomeTitle(outcome));
      })
      betLeg = {
        eventName: eventNamesData,
        marketName: poolEntity.toteMarketTitle ==='Placepot7' ? 'ITV7 Placepot': poolEntity.toteMarketTitle,
        selectionName: selectionNamesData,
        odds: "",
        status: poolEntity.status
      }
      legList.push(betLeg);
      selectionNamesData = [];
    })
    this.shareData = legList;
    this.setStakesandReturns(poolEntity);
    return this.shareData;
  }
  
  setStakesandReturns(poolEntity){
    this.shareData.stake = poolEntity.totalStake;
    this.shareData.returns = poolEntity.totalReturns;
    this.shareData.date = this.betPlacedDate(poolEntity.date);
    this.shareData.betFullDate = this.betPlacedDate(poolEntity.date,true);
    this.shareData.betFullDateTime = this.betPlacedDate(poolEntity.date,true,true);
    this.shareData.betType = poolEntity.betTitle;
  }

  totePoolBetDataFormation(data) {
    const poolEntity = data.betData;
    const legList = [];
    let leg = {};
    leg = {
      eventName: `${poolEntity.raceNumberTitle} ${  poolEntity.getRaceTitle(poolEntity.leg[0])}`,
      selectionName: poolEntity.toteMarketTitle,
      marketName: data.marketName,
      odds: "",
      status: poolEntity.status
    }
    legList.push(leg);
    this.shareData = legList;
    this.setStakesandReturns(poolEntity);
    return this.shareData;
  }
  
  jackPotPoolDataFormation(data) {
    const poolEntity = data.betData.bet;
    let leg = {};
    const eventNamesData = [], result = [];
    poolEntity.legs.forEach((peleg) => {
      eventNamesData.push(peleg.adjustedResult);
      result.push(peleg.adjustedResult);
    })
    leg = {
      eventName: eventNamesData,
      selectionName: poolEntity.name,
      marketName: "",
      odds: "",
      eventStartTime: data.eventTime,
      status: poolEntity.status
    }
    this.shareData = leg;
    this.shareData.stake = result;
    this.shareData.returns = poolEntity.totalReturns;
    this.shareData.date = this.betPlacedDate(poolEntity.date);
    this.shareData.betFullDate = this.betPlacedDate(poolEntity.date,true);
    this.shareData.betType = poolEntity.betTitle;
    this.shareData.betFullDateTime = this.betPlacedDate(poolEntity.date,true,true);
    return this.shareData;
  }

  regularBetsDataFormation(data) {
    const event = data.betData.eventSource;
    const dataSession = this.sessionStorageService.get('betDetailsToShare');
    const betDataToShare = data.bets.find((bet) => {
      return event.id === bet.eventSource.id;
    });
    const legList = [];
    let leg = {};
    let outcomeNames=[];
    let marketName,name;
    betDataToShare.eventSource.leg.forEach((o1: IBetHistoryLeg) => {
      if (o1.removedLeg || o1.status === 'void') {
        return;
      }
      const eventId = o1.backupEventEntity ? o1.backupEventEntity.id : o1.eventEntity.id;
      const outComeId = (Array.isArray(o1.part[0].outcome)? o1.part[0].outcome[0].id : o1.part[0].outcome);
      const dataSessionId = `${eventId}-${o1.cashoutId}-${outComeId}`;
      const odds = dataSession[dataSessionId].odds;
      const eventName = dataSession[dataSessionId].eventName;
      const time = dataSession[dataSessionId].time;
      const eventMarketDesc = dataSession[dataSessionId].eventMarketDescription;
      if(!['Bet Builder','Build Your Bet','5-A-Side'].includes(betDataToShare.eventSource.bybType) ) {
        outcomeNames = dataSession[dataSessionId].outcomeNames;
        name =  !dataSession[dataSessionId].isMultiples ?  this.filtersService.filterPlayerName(outcomeNames[0]):outcomeNames;
        marketName = this.filtersService.filterAddScore(eventMarketDesc, outcomeNames[0]);    
      } else{        
        const selections = this.bybSelectionsService.getSortedSelections(o1);
          selections.forEach((sel)=>{
          let selec = '';
          selec = sel.title ? (sel.desc ? sel.title+','+sel.desc : sel.title) :'';
          outcomeNames.push(selec);
        });
        name = outcomeNames;
        marketName = this.filtersService.filterAddScore(dataSession[dataSessionId].eventMarketDescription, dataSession[dataSessionId].outcomeNames[0]);
      }
      leg = {
        eventName: eventName,
        selectionName: name,
        odds: odds,
        status: betDataToShare.eventSource.totalStatus,
        marketName: marketName,
        eventStartTime: time
      }
      legList.push(leg);         
    })
    this.shareData = legList;
    this.shareData.stake =  betDataToShare.eventSource.stake;
    this.shareData.returns = betDataToShare.eventSource.potentialPayout !== 'N/A' ? betDataToShare.eventSource.potentialPayout : '';    
    this.shareData.date = this.betPlacedDate(betDataToShare.eventSource.date);
    this.shareData.betFullDate = this.betPlacedDate(betDataToShare.eventSource.date,true);
    this.shareData.betFullDateTime = this.betPlacedDate(betDataToShare.eventSource.date,true,true);
    this.shareData.betType = betDataToShare.eventSource.bybType || betDataToShare.eventSource.betType;
    return this.shareData;
  }
  
  betPlacedDate(betPlacedDate: string, showYear?: boolean, showTime?: boolean): string {
    const betPlacedDateTime = new Date(this.timeService.convertDateStr(betPlacedDate));
    const datePattern = "HH:mm, dd/MM/yyyy";
    if (showTime && showYear) {
      return this.timeService.formatByPattern(this.timeService.getLocalDateFromString(betPlacedDate), datePattern);
    }
    else if (showYear) {
      return `${betPlacedDateTime.getDate()} ${betPlacedDateTime.toLocaleString('default', { month: 'short' })} ${betPlacedDateTime.getFullYear()}`;
    }
    return `${betPlacedDateTime.getDate()} ${betPlacedDateTime.toLocaleString('default', { month: 'short' })}`;
  }
  
  lottoDataFormation(betInfo: any) {
    let leg = {};
    const legList = []
    const selectionName =[];
    const bet=betInfo.betData;
    bet.balls.forEach((data)=> selectionName.push(data.ballNo));
    const lotteryDrawResults = [];

    bet.lotteryResults && bet.lotteryResults.forEach((lotteryDraw,index)=>{
      const lotteryLineDraw = {};
      lotteryLineDraw['drawLineName'] = `Line- ${index+1} - ${this.dateAndTimeFmt(lotteryDraw.drawAt)}`;
      lotteryDrawResults.push(lotteryLineDraw);
    })
    leg = {
      eventName: bet.drawName,
      selectionName: selectionName,
      marketName: bet.name,
      odds: "",//no odds in lotto bets
      status: bet.status,
      lotteryDrawResults: lotteryDrawResults
    }
    legList.push(leg);
    this.shareData = legList;
    this.shareData.stake = bet.stake;
    this.shareData.returns = bet.totalReturns;
    this.shareData.date = this.betPlacedDate(bet.betDate);
    this.shareData.betFullDate = this.betPlacedDate(bet.betDate,true);
    this.shareData.betFullDateTime = this.betPlacedDate(bet.betDate,true,true);
    this.shareData.betType= betInfo.sportType;
    return this.shareData;
  }

  dateAndTimeFmt(dateTimeFmt) {
    const parsedDateString = this.timeService.convertDateStr(dateTimeFmt);
    const formatedDate = new Date(this.timeService.formatByPattern(parsedDateString, 'yyyy/MM/dd HH:mm:ss', '', false));
    return this.timeService.getDatetimeWithFormatSuffix(formatedDate, false, true);
  }

  /**
   * Set start time for current leg and handle date time if it's today event
   * @param leg {object} jackpot leg
   */
  private setStartTime(leg: ILeg): void {
    this.otherDay = '';
    this.startTime = this.timeService.getLocalDateFromString(leg.startTime.replace(/T/gi, ' '));
    const currentDate: Date = new Date(),
        isSameDate: boolean = this.startTime.getDate() === currentDate.getDate(),
        isSameMonth: boolean = this.startTime.getMonth() === currentDate.getMonth(),
        isSameYear: boolean = this.startTime.getFullYear() === currentDate.getFullYear();

    if (!(isSameMonth && isSameDate && isSameYear)) {
        this.otherDay = this.startTime;
    }
  }
}
