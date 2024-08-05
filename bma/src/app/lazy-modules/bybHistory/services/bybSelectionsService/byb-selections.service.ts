import { Injectable } from '@angular/core';
import { IBetHistoryLeg, IBetHistoryPart } from '@app/betHistory/models/bet-history.model';
import { IBybSelection, IBybDefaultSelectionStatus } from '@lazy-modules/bybHistory/models/byb-selection.model';
import { BET_STATUSES, STATUSES } from '@bybHistoryModule/constants/byb-5aside-markets-config.constant';
import { Subject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class BybSelectionsService {

  public hideTooltipTriggerSub: Subject<IBybSelection> = new Subject<IBybSelection>();
  private storedSelection:IBybSelection;

  /**
   * Stores the latest clicked info icon's selection and triggers next for the existing selection's tooltip to close.
   *
   * @param {IBybSelection} selection
   * @memberof BybSelectionsService
   */
  replaceStoredSelection(selection: IBybSelection): void {
    if(this.storedSelection !== selection) {
      this.hideTooltipTriggerSub.next(this.storedSelection);
      this.storedSelection = selection;
    }
  }

  getSortedSelections(leg: IBetHistoryLeg): IBybSelection[] {
    return leg.part.map((part: IBetHistoryPart) => {
      return this.createSelection(part, leg);
    }).sort((a, b) => {
      if (a.title < b.title) { return -1; }
      if (a.title > b.title) { return 1; }
      return 0;
    });
  }

  private createSelection(part: IBetHistoryPart, leg: IBetHistoryLeg): IBybSelection {
    const description = this.capitalize(part.description);
    const eventMarketDesc = this.capitalize(part.eventMarketDesc);
    const betCompletion: boolean = part.outcome[0].result.confirmed === BET_STATUSES.SETTLED;
    const { status, partSettled, showBetStatusIndicator } = this.getDefaultSelectionStatus(part);
    const sel: IBybSelection = { part, title: '', status, partSettled, showBetStatusIndicator, betCompletion };

    // Anytime Goalscorer
    if (/Anytime Goalscorer$/i.test(eventMarketDesc)) {
      sel.title = `${description} Anytime Goalscorer`;
      return sel;
    }

    // To Keep A Clean Sheet (remove yes/no)
    if (/To Keep A Clean Sheet$/i.test(eventMarketDesc)) {
      sel.title = description.replace(/ - (Yes|No)/i, '');
      sel.isCleanSheetMarket = true;
      return sel;
    }

    // To Be Shown A Card
    if (eventMarketDesc.includes('To Be Shown A Card')) {
      sel.title = this.formCardedTitle(description);
      return sel;
    }

    // To Score 2 Or More Goals
    if (eventMarketDesc.match(/Build Your Bet TO SCORE \d Or More Goals/i)) {
      sel.title = this.formGoalsTitle(description, eventMarketDesc);
      return sel;
    }

    // Replace to have -> to make for passes, assists, tackles
    if (/(Passes|Assists|Tackles)/i.test(eventMarketDesc)) {
      sel.title = this.formPlayerMakeTitle(description);
      return sel;
    }

    // Other player bets
    if (this.checkForCommonPlayerBetTitle(eventMarketDesc)) {
      sel.title = this.formCommonPlayerBetTitle(description);
      return sel;
    }

    // Default title and description
    sel.title = description;
    sel.desc = this.formBYBTitle(leg, eventMarketDesc);
    return sel;
  }
  /**
   * @param  {string} text
   * @returns string
   * example: i/p:RáDéBó AáBó o/p :Rádébó Aábó
   */
  private capitalize(text: string): string {
    // Kept this commented below code for reference
    // Regex Changed as per the requirement
    // return text.toLowerCase()
    //   .replace(/\b(\w)/g, letter => letter.toUpperCase());
    return text.toLowerCase().replace(/(^.|\s\S)/g, (e) => {
      return e.toUpperCase();
    });
  }

  private formCardedTitle(description: string): string {
    return `${description} To Be Carded`;
  }

  private formGoalsTitle(description: string, eventMarketDesc: string): string {
    const title = eventMarketDesc.replace(/Build Your Bet /ig, '');
    return `${description} ${title}`
      .replace(/ or more/gi, '+');
  }

  private formPlayerMakeTitle(description: string): string {
    return description
      .replace(/ or more/gi, '+')
      .replace(/to have/gi, 'To Make');
  }

  private formCommonPlayerBetTitle(description: string): string {
    return description
      .replace(/ or more/gi, '+')
      .replace(/to be/gi, 'To Have')
      .replace(/SHOTS WOODWORK/gi, 'Shots Hit The Woodwork')
      .replace(/Offside /gi, 'Offsides ');
  }

  private formBYBTitle(leg: IBetHistoryLeg, eventMarketDesc: string): string {
    const name = (leg.eventEntity && leg.eventEntity.name) || (leg.backupEventEntity && leg.backupEventEntity.name) ||
      (leg.part[0].eventDesc);
    const [home, away] = name.split(' v ');

    return eventMarketDesc.replace(/Build Your Bet /ig, '')
      .replace(/participant_1/gi, home)
      .replace(/participant_2/gi, away);
  }

  private checkForCommonPlayerBetTitle(eventMarketDesc: string) {
    return eventMarketDesc.includes('Build Your Bet Player') &&
      !eventMarketDesc.includes('To Get First Booking') &&
      !eventMarketDesc.includes('To Outscore The Opposition');
  }

  /**
   * mark selections to use updates from OPTA or not
   * @param selections
   * @private
   */
  private getDefaultSelectionStatus(part: IBetHistoryPart): IBybDefaultSelectionStatus {
    let status;
    let partSettled = false;
    let showBetStatusIndicator;

    if (part.outcome[0].result.confirmed === 'Y') {
      status = part.outcome[0].result.value === 'W' ? STATUSES.WON : STATUSES.LOSE;
      partSettled = true;
      showBetStatusIndicator = true;
    }

    return { status, partSettled, showBetStatusIndicator };
  }
}
