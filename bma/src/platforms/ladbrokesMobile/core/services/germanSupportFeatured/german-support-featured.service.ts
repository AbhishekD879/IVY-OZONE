import { Injectable } from '@angular/core';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { IFeaturedModel } from '@featured/models/featured.model';
import { IOutputModule } from '@featured/models/output-module.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';

@Injectable()
export class GermanSupportFeaturedService {
  isGermanUser: Function;

  private restrictedSportsCategoriesIds: string[];
  private userWasGerman: boolean = false;
  private latestFeaturedData: IFeaturedModel = null;
  private modulesFilters = {
    EventsModule: this.nonDataModuleFilter,
    SurfaceBetModule: this.dataModuleFilter,
    QuickLinkModule: this.nonDataModuleFilter,
    HighlightCarouselModule: this.dataModuleFilter,
    InplayModule: this.dataModuleFilter,
    RecentlyPlayedGameModule: this.nonDataModuleFilter,
  };

  constructor(
    private germanSupportService: GermanSupportService,
    private coreTools: CoreToolsService) {
    // shortcuts
    this.restrictedSportsCategoriesIds = this.germanSupportService.restrictedSportsCategoriesIds;
    this.isGermanUser = this.germanSupportService.isGermanUser.bind(this.germanSupportService);
    this.moduleFilterHandler = this.moduleFilterHandler.bind(this);
  }

  /**
   * Return and cache featured data on FEATURED_STRUCTURE_CHANGED event
   * @param data
   */
  getInitialData(data: IFeaturedModel): IFeaturedModel {
    this.latestFeaturedData = this.coreTools.deepClone(data);

    if (this.isGermanUser()) {
      this.userWasGerman = true;
      return this.filterData(data);
    }
    return data;
  }

  /*
  Return data from cache when user is different each time
   */
  getActualData(): IFeaturedModel | null {
    if (this.latestFeaturedData) {
      const featured = this.coreTools.deepClone(this.latestFeaturedData);

      if (this.userWasGerman && !this.isGermanUser()) {
        this.userWasGerman = false;
        return featured;
      }

      if (!this.userWasGerman && this.isGermanUser()) {
        this.userWasGerman = true;
        return this.filterData(featured);
      }
    }

    return null;
  }

  moduleFilterHandler(module: IOutputModule): IOutputModule | null {
    /*
    Catch module handlers that are not supported.
    New modules that will be created in future will not handle filtering
    and potential bugs will go silently!
     */
    if ({}.hasOwnProperty.call(this.modulesFilters, module['@type'])) {
      return this.modulesFilters[module['@type']].call(this, module);
    }

    console.warn(`GermanSupportFeaturedService - module: ${module['@type']} is not covered by filter on featured tab!`);

    return module;
  }

  private filterData(data: IFeaturedModel): IFeaturedModel | null {
    if (!data) {
      return null;
    }

    data.modules = data.modules.filter(m => this.eventsModuleFilter(m))
      .map(this.moduleFilterHandler)
      .filter(m => m); // filter null modules

    return data;
  }

  private eventsModuleFilter(module: IOutputModule): boolean {
    return module['@type'] === 'EventsModule' ? this.isEntityAllowed(module) : true;
  }

  private isEntityAllowed(entity: IOutputModule | ISportEvent): boolean {
    return entity.categoryId ? !this.restrictedSportsCategoriesIds.includes(entity.categoryId.toString()) : true;
  }

  private dataModuleFilter(module: IOutputModule): IOutputModule | null {
    const data: ISportEvent[] = module.data.filter(event => this.isEntityAllowed(event));

    if (data.length) {
      module.data = data;
      return module;
    }

    return null;
  }

  private nonDataModuleFilter(module: IOutputModule): IOutputModule {
    return module;
  }
}
