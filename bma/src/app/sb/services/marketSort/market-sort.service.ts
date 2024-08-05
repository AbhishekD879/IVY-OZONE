import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { ITypeSegment, IGroupedByDateItem } from '@app/inPlay/models/type-segment.model';

@Injectable()
export class MarketSortService {
  /**
   * Aplly filter value to one event
   * @param {ITypeSegment} eventsSectionData
   * @param {string} marketFilter
   */
  setMarketFilterForOneSection(eventsSectionData: ITypeSegment, marketFilter: string): void {
    const groupedEvents = eventsSectionData && eventsSectionData.groupedByDate;
    eventsSectionData && (eventsSectionData.defaultValue = marketFilter);

    if (groupedEvents) {
      _.forEach(groupedEvents, (eventsGroup: IGroupedByDateItem) => {
        this.hideSectionIfNoVisibleEvents(eventsGroup, marketFilter);
      });
    }
  }


  /**
   * Aplly filter value to multiple events
   * Hide events section and Group of events if they are grouped
   * @param {ITypeSegment[]} sectionsArray
   * @param {string} marketFilter
   */
  setMarketFilterForMultipleSections(sectionsArray: ITypeSegment[], marketFilter: string): void {
    _.each(sectionsArray, (section: ITypeSegment) => {
      section.defaultValue = marketFilter;
      this.hideSectionIfNoVisibleEvents(section, marketFilter);

      // if events have group, additionally check and hide group of events.
      if (section.groupedByDate) {
        _.forEach(section.groupedByDate, (eventsGroup: IGroupedByDateItem) => {
          this.hideSectionIfNoVisibleEvents(eventsGroup, marketFilter);
        });
      }
    });
  }


  /**
   * Deactivate section if there are no events after filtering
   * @param {ITypeSegment} section
   * @param {string} marketFilter
   */
  private hideSectionIfNoVisibleEvents(section: IGroupedByDateItem | ITypeSegment, marketFilter: string): void {
    if(marketFilter){
      let anyEventOfType: boolean = false;
      const marketFilterList = marketFilter.toLowerCase().split(',');
      _.each(section.events, event => {
        const frameMrkts = [];
        event.markets.sort((secMrktElm, fstMrktElm) => {
          return (secMrktElm.displayOrder < fstMrktElm.displayOrder) ? -1 : 1;
        });
        _.each(event.markets, market => {
          if (marketFilterList.indexOf(market.templateMarketName.toLowerCase()) !== -1) {
            anyEventOfType = true;
            market.hidden = frameMrkts.indexOf(market.templateMarketName) !== -1 ? true : false;
            frameMrkts.push(market.templateMarketName);
          }
        });
      });
      section.deactivated = !anyEventOfType;
    }
  }
}
