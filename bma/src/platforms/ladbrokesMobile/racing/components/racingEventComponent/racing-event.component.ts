import { Component, OnInit } from '@angular/core';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';

/**
 * @class Racing event controller'responseCreationTime'
 */
@Component({
  templateUrl: 'racing-event.component.html',
  selector: 'racing-event'
})
export class LadbrokesRacingEventComponent extends RacingEventComponent implements OnInit {
  showVerdict: boolean = false;
  racingPostVerdictData: IRacingPostVerdict;
  isMobile: boolean = this.deviceService.isMobile;
  isTablet: boolean = this.deviceService.isTablet;
  isRacingPostVerdictAvailable: boolean;
  isSpOnly: boolean;
  isInfoHidden: {'info':boolean};
  readonly MARKETS_CONTAINER: string = '.markets-container div div.scroll-container';

  ngOnInit(): void {
    super.ngOnInit();
    if (this.eventEntity) {
      this.racingPostVerdictData = this.eventEntity.racingPostVerdict;
      this.syncToApplySorting();
      this.isSpOnly = this.spOnly;
    }
    this.isRacingPostVerdictAvailable = (this.sportName !== 'greyhound' &&
      this.racingPostVerdictData && this.racingPostVerdictData.isFilled);
  }

  /**
   * Click on Horse Block.
   *
   * Toggle Horse Information Area.
   *
   * param {array} summary of expanded and collapsed areas.
   * param {number} market index.
   * param {number} outcome index.
   *
   */
  onExpandSection(expandedSummary: Array<Array<boolean>>, mIndex: number, oIndex: number): void {
    expandedSummary[mIndex][oIndex] = !expandedSummary[mIndex][oIndex];
    const hideInfoChecker: boolean = expandedSummary[mIndex].every((v: boolean) => v === false);
    this.isInfoHidden = { 'info': !hideInfoChecker };
    const gtmData = {
      event: "trackEvent",
      eventAction: "race card",
      eventCategory: this.isGreyhoundEdp ? 'greyhounds' : 'horse racing',
      eventLabel: expandedSummary[mIndex][oIndex] ? 'show more' : 'show less',
      categoryID: this.eventEntity.categoryId,
      typeID: this.eventEntity.typeId,
      eventID: this.eventEntity.id
    }
    this.gtmService.push(gtmData.event, gtmData);
  }

  toggleShowOptions(expandedSummary: Array<Array<boolean>>, mIndex: number, showOption: boolean): void {
    for (let i = 0; i < expandedSummary[mIndex].length; i++) {
      expandedSummary[mIndex || 0][i] = showOption;
    }
  }

  formatAntepostTerms(str: string): string {
    const newStr = str
      .replace(/(odds)/ig, 'Odds')
      .replace(/(places)/ig, 'Places')
      .replace(/\d+\/\d+( odds)/ig, match => {
        return `${match}`;
      });
    return newStr.replace(/[0-9]+(?!.*[0-9])/, match => `${match}`);
  }

  toggleRacingPostVerdict(): void {
    this.showVerdict = !this.showVerdict;

    this.gtmService.push('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'race card',
      eventLabel: 'racing post verdict'
    });
  }


  get spOnly(): boolean {
    return  this.eventEntity.markets.map(
      (market) => market.priceTypeCodes).every(
        (el) => el.includes('SP') && !el.includes('LP'));
  }
  set spOnly(value:boolean){}
}
