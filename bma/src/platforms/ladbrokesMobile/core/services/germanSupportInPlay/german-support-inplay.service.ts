import { Injectable } from '@angular/core';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IInplayAllSports } from '@app/inPlay/models/inplay-all-sports.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { IStructureCacheData } from '@app/inPlay/models/structure.model';

@Injectable()
export class GermanSupportInPlayService {

  private restrictedSportsCategoriesIds: string[];
  private isGermanUser: Function;
  private userWasGerman: boolean = false;
  private readonly structureTypeArray: string[] = ['livenow', 'upcoming', 'liveStream', 'upcomingLiveStream'];

  constructor(
    private germanSupportService: GermanSupportService) {
    // shortcuts
    this.restrictedSportsCategoriesIds = this.germanSupportService.restrictedSportsCategoriesIds;
    this.isGermanUser = this.germanSupportService.isGermanUser.bind(this.germanSupportService);
  }

  isNewUserFromOtherCountry(): boolean {
    if (this.userWasGerman && !this.isGermanUser()) {
      this.userWasGerman = false;
      return true;
    }

    if (!this.userWasGerman && this.isGermanUser()) {
      this.userWasGerman = true;
      return true;
    }

    return false;
  }

  getGeFilteredRibbonItemsForInPlay(ribbonDataItems: IRibbonItem[]): IRibbonItem[] {
    if (!ribbonDataItems.length) {
      return ribbonDataItems;
    }
    const allSportTabData = ribbonDataItems[0].categoryId === 0 ? ribbonDataItems[0] : null,
      filtered = this.getGeFilteredRibbonItems(ribbonDataItems);

    return allSportTabData ? Object.assign(filtered[0], this.getRibbonAllSportCounter(filtered)) && filtered : filtered;
  }

  getGeFilteredRibbonItems(ribbonDataItems: IRibbonItem[]): IRibbonItem[] {
    if (!this.isGermanUser()) {
      return ribbonDataItems;
    }

    this.userWasGerman = true;

    if (!this.isAnyRestrictedItem(ribbonDataItems)) {
      return ribbonDataItems;
    }

    return this.filterRestrictedInRibbon(ribbonDataItems);
  }

  applyFiltersToStructureData(structureData: IInplayAllSports | IStructureCacheData): void {
    if (!this.isGermanUser()) {
      return;
    }

    this.userWasGerman = true;

    const structureTypeArray = this.collectStructureTypes(structureData);

    if (!this.isAnyRestrictedSportsInStructure(structureData, structureTypeArray)) {
      return;
    }

    this.filterRestrictedInStructure(structureData, structureTypeArray);

    structureTypeArray.forEach(structureType => {
      Object.assign(structureData[structureType], this.getEventIdsAndCountFromStructure(structureData, structureType));
    });
  }

  private collectStructureTypes(structureData: IInplayAllSports | IStructureCacheData): string[] { // ['livenow', 'upcoming', ...]
    return this.structureTypeArray.reduce((arr, curr) => structureData[curr] ? arr.concat(curr) : arr, []);
  }

  private filterRestrictedInRibbon(data: IRibbonItem[]): IRibbonItem[] {
    return data.filter(entity => !this.restrictedSportsCategoriesIds.includes(entity.categoryId.toString()));
  }

  private filterRestrictedInStructure(structureData: IInplayAllSports | IStructureCacheData, structureTypeArray: string[]): void {
    structureTypeArray.forEach(structureType => {
      for (let i = structureData[structureType].eventsBySports.length - 1; i >= 0; i--) {
        if (this.restrictedSportsCategoriesIds.includes(structureData[structureType].eventsBySports[i].categoryId.toString())) {
          structureData[structureType].eventsBySports.splice(i, 1);
        }
      }
    });
  }

  private getEventIdsAndCountFromStructure(structureData: IInplayAllSports | IStructureCacheData, structureType)
    : Partial<IInplayAllSports | IStructureCacheData> {
    return structureData[structureType].eventsBySports.reduce((acc, curr) => {
      acc.eventCount += curr.eventCount;
      acc.eventsIds = acc.eventsIds.concat(curr.eventsIds);
      return acc;
    }, { eventCount: 0, eventsIds: [] });
  }

  private getRibbonAllSportCounter(ribbonData: IRibbonItem[]): Partial<IRibbonItem> {
    return ribbonData.reduce((acc, curr, currIndex) => {
      if (currIndex) {
        acc.liveEventCount += curr.liveEventCount;
        acc.upcomingEventCount += curr.upcomingEventCount;
        acc.liveStreamEventCount += curr.liveStreamEventCount;
        acc.upcommingLiveStreamEventCount += curr.upcommingLiveStreamEventCount;
      }

      return acc;

    }, { liveEventCount: 0, upcomingEventCount: 0, liveStreamEventCount: 0, upcommingLiveStreamEventCount: 0 });
  }

  private isAnyRestrictedItem(data: (IRibbonItem | ISportSegment)[]): boolean {
    return data.some(entity => this.restrictedSportsCategoriesIds.includes(entity.categoryId.toString()));
  }

  private isAnyRestrictedSportsInStructure(structureData: IInplayAllSports | IStructureCacheData, structureTypeArray: string[]): boolean {
    return structureTypeArray.some(structureType => this.isAnyRestrictedItem(structureData[structureType].eventsBySports));
  }
}
