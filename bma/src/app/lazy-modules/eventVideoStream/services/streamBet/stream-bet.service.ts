import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { Subject } from 'rxjs';

export class StreamBetService {
  lastTemplateLoadedSubj: Subject<void> = new Subject<void>();
  multiOddMarketCounter = 0;
  totalMultiOddMarketElemsCount = 0;
  constructor(
  ) {}

  getMarketTemplate(currentMarket: IMarket, eventEntity: ISportEvent): string {
    if(currentMarket){
    if (eventEntity?.categoryId?.toString() === '21') {
      return 'horse-racing-template';
    }else if(currentMarket.templateType === 'single-counter-double-odd' || currentMarket.templateType === 'single-drop-double-odd') {
      return currentMarket.templateType === 'single-counter-double-odd' ? 'single-counter-double-odd' : 'single-drop-double-odd';
    } 
    else if (this.isSingleDropSingleOdd(currentMarket)) {
      return 'single-drop-single-odd';
    }
    else if (this.isDoubleDropSingleOdd(currentMarket)) {
      return 'double-drop-single-odd';
    }
    else if (this.isSingleDropDoubleOdd(currentMarket)) {
      return 'single-drop-double-odd';
    }
    else if(this.isSingleCounterDoubleOdd(currentMarket)){
      return 'single-counter-double-odd';
    }
    else if (this.isMultipleOdds(currentMarket) || this.isDoubleOdds(currentMarket)) {
      return 'price-odd-button';
    }
    else if (this.isCorrectScoreMarket(currentMarket)) {
      return 'correct-score-market';
    } else {
      return 'special-market';
    }
  }
  }
  
  isCorrectScoreMarket(currentMarket: IMarket): boolean {
    return currentMarket.dispSortName === "CS";
  }

   isSingleDropSingleOdd(currentMarket: IMarket): boolean {
      const marketName: string = currentMarket.name?.toLowerCase().replace(/([^a-zA-Z0-9])+/g, "");
      const templateName: string = currentMarket.templateMarketName; // need to check
      const sortName: string = currentMarket.dispSortName;
      const minorCode = currentMarket.marketMeaningMinorCode;
    const singleDropSingleOddMinorCodeConfig = ["FS", "LS", "AG", "MG", "HS"];
    const isMarketNameExcludedFromSingleDropSingleOdd = ["matchwinningmargin", "highestscoringquarterteamtowin", "extratimetotalgoals",
      "totalbookings", "doublechance", "timeoffirsthalfgoal", "totalbookingpoints", "bookingpoints2ways", "inplayspecial", "1sthalfwinningmargin", "yourcallspecials", "matchspecial"];

    const isMarketNameSingleDropSingleOdd = ["fifamanofthematch", "firstteamhomegoalscorer",
      "firstteamawaygoalscorer", "nextplayertoscore", "scoreandteamtolose", "toscoreexactly1", "toscoreexactly2",
      "toscoreexactly3", "scorefirstandteamdraw", "scorefirstandteamlose", "playertooutscoretheopposition", "playertoscoreinbothhalves",
      "playertoscoreinfirst10minutes", "firstpointscorer", "eachwaygoalscorer", "halftimefulltime", "extratimehalftimefulltime"];

    if (singleDropSingleOddMinorCodeConfig.includes(minorCode)) {
      return true;
    }

    if (sortName === "L1" && marketName.match(/scoreafter\d+frames/)) {
      return true;
    }

    if (templateName.match(/Player ([AB]) Most Consecutive Frames Won/)) {
      return true;
    }

    if (marketName === "serieswinner") {
      return true;
    }

    if (isMarketNameExcludedFromSingleDropSingleOdd.includes(marketName)) {
      return false;
    }

    if (currentMarket.outcomes?.length >= 3 && currentMarket.outcomes.length <= 33 && isMarketNameSingleDropSingleOdd.includes(marketName)) {
      return true;
    }

    return sortName === "--"
      && minorCode === "--"
      && marketName === "lastgoalscorer";
}

   isSingleDropDoubleOdd(currentMarket: IMarket): boolean{
    const outcomeLength: number = currentMarket.outcomes.length;
    const marketName: string = currentMarket.name;
    if(outcomeLength % 2 === 0
            && (marketName.match(new RegExp("Match Result (and|&) Over/Under.* Goals"))
            || marketName.match(new RegExp("Both Teams to Score (and|&) Over/Under .* Goals"))
            || marketName.match(new RegExp("(1st|First) Half (and|&) Over/Under .* Goals"))
            || marketName.match(new RegExp("(2nd|Second) Half (and|&) Over/Under .* Goals")))){
           return true;
            }
    return false;      
  }
  
   isDoubleDropSingleOdd(currentMarket: IMarket):boolean{
    const marketName: string = currentMarket.name?.toLowerCase().replace(/([^a-zA-Z0-9])+/g, "");
    return marketName && (marketName === "highestscoringquarterteamtowin" || marketName.includes("doubleresult"));
  }

   isMultipleOdds(currentMarket: IMarket): boolean {
    const isMultipleSortCodeConfig = ["MR", "3W", "L3", "H1", "H2", "HT", "MH", "SC", "LC"];
    if (isMultipleSortCodeConfig.includes(currentMarket.dispSortName)) {
      return true;
    }
    return false;
  }

   isSingleCounterDoubleOdd(currentMarket: IMarket):boolean {
    return currentMarket.dispSortName === "HL";
  }

   isDoubleOdds(currentMarket: IMarket): boolean {
    const isDoubleOddsConfig = ["BO", "2W", "L2", "HH", "AH", "WH", "GB", "TN", "NN", "2WFBR"];
    const outcomeLength: number = currentMarket.outcomes?.length;
    const marketName: string = currentMarket.name;
    if(outcomeLength && marketName){
      if (isDoubleOddsConfig.includes(currentMarket.dispSortName)) {
        return true;
      }
      if (outcomeLength === 2 && (marketName.match(new RegExp("Home Team Total Points Odd/Even")) || marketName.match(new RegExp("Away Team Total Points Odd/Even"))
        || marketName.match(new RegExp(".* Set Extra Points Required\\?")))) {
        return true;
      }
    }
    return false;
  }

}