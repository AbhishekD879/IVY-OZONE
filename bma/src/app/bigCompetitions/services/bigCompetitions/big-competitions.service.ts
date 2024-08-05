import { of as observableOf, Observable, Observer, Subject } from 'rxjs';

import { map, catchError, concatMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as _ from 'underscore';

import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { BigCompetitionsProvider } from '@app/bigCompetitions/services/bigCompetitionsProvider/big-competitions-provider.service';
import {
  BigCompetitionsLiveUpdatesService
} from '@app/bigCompetitions/services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { IBCModule, IBCData, ICompetitionTab, ICompetitionSubTab, ICompetitionModules } from './big-competitions.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { OutcomeTemplateHelperService } from '@app/sb/services/outcomeTemplateHelper/outcome-template-helper.service';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { CmsToolsService } from '@core/services/cms/cms.tools';

@Injectable()
export class BigCompetitionsService {
  competitionObservable: Observable<IBCData>;
  activeCategoryId: string;
  storedModules: ICompetitionModules[];
  brand = {brand:'Coral', device: 'Mobile'};
  structure: IBCData | {};
  public aemBanner = new Subject<ICompetitionModules[]>();
  private basePath: string;
  gModules = ['AEM', 'SURFACEBET', 'HIGHLIGHT_CAROUSEL'];
  constructor(
    private cacheEventsService: CacheEventsService,
    private bigCompetitionsProvider: BigCompetitionsProvider,
    private bigCompetitionsLiveUpdatesService: BigCompetitionsLiveUpdatesService,
    private routingState: RoutingState,
    private route: ActivatedRoute,
    private router: Router,
    private outcomeTemplateHelperService: OutcomeTemplateHelperService,
    private cmsToolsService: CmsToolsService,
  ) {
    this.activeCategoryId = undefined;
    this.basePath = '/big-competition';
    this.storedModules = [];
    this.structure = {};
  }

  /**
   * Stores competition to isolated cache.
   * @param {Object} competition
   */
  storeCategoryId(id: string): void {
    this.activeCategoryId = id;
  }
  setAEMBanner(value) {
    this.aemBanner.next(value);
  }
  /**
   * Get big competition data structure(tabs,subtabs).
   * @return {Observable}.
   */
  getTabs(competitionName: string): Observable<IBCData> {
    this.competitionObservable = Observable.create((observer: Observer<IBCData | {}>) => {
      this.bigCompetitionsProvider.tabs(competitionName)
        .subscribe((data: IBCData) => {
          if (!data.competitionTabs || !data.competitionTabs.length) {
            this.router.navigate(['/']);
            observer.next({});
            observer.complete();
          } else {
            this.structure[competitionName] = this.parseTabs(data);
            observer.next(data);
            observer.complete();
          }
        }, error => {
          console.warn(error);
          this.router.navigate(['/']);
          observer.error(error);
          observer.complete();
        });
    });
    return this.competitionObservable;
  }

  /**
   * Get modules list using route segment params.
   * @return {Observable} which will return modules {Array}.
   */
  getModules(subTabName?: string): Observable<IBCModule[]> {
    const subTab = this.routingState.getRouteParam('subTab', this.route.snapshot) || subTabName;
    const service: string = subTab ? 'subtab' : 'tab';
    const id: string = subTab ? this.findSubTab().id : this.findTab().id;
    // unsubscribe from live updates
    if (this.storedModules.length) {
      this.bigCompetitionsLiveUpdatesService.unsubscribe(this.getEvents(this.storedModules));
    }
    return this.bigCompetitionsProvider[service](id)
      .pipe(map((data: IBCData) => {
        const events: ISportEvent[] = this.getEvents(data.competitionModules);
        this.storedModules = [];

        // subscribe to live updates
        if (events.length) {
          this.storedModules = data.competitionModules;

          this.cacheEventsService.store('bigCompetitions', this.groupEvents(events));
          // Subscribe for live updates(LS MS)
          this.bigCompetitionsLiveUpdatesService.subscribe(events);
        }
        const aemBann = data.competitionModules.filter((module: ICompetitionModules) => this.gModules.includes(module.type));
        this.setAEMBanner(aemBann);
        data.competitionModules = data.competitionModules.map((module: ICompetitionModules) => {
          if (module.promotionsData && module.promotionsData.promotions) {
            module.promotionsData.promotions = this.cmsToolsService.processResult(module.promotionsData.promotions);
          }
          module.brand = this.brand;
          return module;
        });
        return data.competitionModules;
      }), catchError(error => {
        this.storedModules = [];
        console.warn(`module id: ${id} data wasn't loaded.`, error);
        return observableOf([]);
      }));
  }

  /**
   * Get events from each module
   * @param modules
   * @returns {Array}
   */
  // ICompetitionModules[]
  getEvents(modules: any): ISportEvent[] {
    let events = [];

    _.each(modules, (module: IBCModule) => {
      if (module.groupModuleData && module.groupModuleData.data) {
        events = events.concat(module.groupModuleData.data[0].ssEvents);
      } else if (module.markets && module.markets.length) {
        const eventsEntities = _.pluck(module.markets, 'data');
        events = events.concat(eventsEntities);
      } else if (module.events && module.events.length) {
        events = events.concat(module.events);
      } else if (module.knockoutEvents && module.knockoutEvents.length) {
        events = events.concat(module.knockoutEvents.reduce((arr, curr) => curr.obEvent ? arr.concat(curr.obEvent) : arr, []));
      }
    });

    return _.compact(events);
  }

  getParticipants(competition: string) {
    return this.bigCompetitionsProvider.participants(competition);
  }
  /**
   * Get module data by id.
   * @param {string} id
   * @return {Observable} which will return module data.
   */
  getModule(id: string): Observable<ICompetitionModules> {
    return this.bigCompetitionsProvider.module(id);
  }

  /**
   * Wait for structure loading then get subTabs list.
   * @return {Observable} which will resolve {Array}.
   */
  getSubTabs(): Observable<ICompetitionSubTab[]> {
    if (_.isEmpty(this.structure)) {
      return this.competitionObservable.pipe(concatMap(() => {
        const tab: ICompetitionTab = this.findTab();
        return observableOf((tab && tab.competitionSubTabs) || []);
      }));
    } else {
      const tab: ICompetitionTab = this.findTab();
      return observableOf((tab && tab.competitionSubTabs) || []);
    }
  }

  /**
   * Sets correctedOutcomeMeaningMinorCode for outcomes.
   * @param {Array} events
   */
  addOutcomeMeaningMinorCode(events: IBigCompetitionSportEvent[]): void {
    _.each(events, (event: IBigCompetitionSportEvent) => {
      event.isBCH = true;
      this.outcomeTemplateHelperService.setOutcomeMeaningMinorCode(event.markets, event);
    });
  }

  /**
   * Find tab data using route params.
   * @return {Object} tab.
   */
  findTab(): ICompetitionTab {
    const competitionName: string = this.routingState.getRouteParam('name', this.route.snapshot);
    const tabName: string = this.routingState.getRouteParam('tab', this.route.snapshot);
    const struct: IBCData = this.structure[competitionName];
    const tabs: ICompetitionTab[] = struct && struct.competitionTabs;
    if(tabs.length && !!tabName && !tabs.find(x=>x.name.toLocaleLowerCase() === tabName.toLocaleLowerCase())) {
      this.router.navigate([tabs[0].path]);
    }

    if (!tabs || !tabs.length) {
      console.warn('No tabs created for this competition.');
      this.router.navigate(['/']);
      return null;
    }
    return _.findWhere(tabs, { path: `${struct.path}/${tabName}` }) || tabs[0];
  }

  /**
   * Parse data and add base path prefix for routing.
   * @param {Object} data.
   * @return {Object} data.
   */
  private parseTabs(data: IBCData): IBCData {
    data.path = `${this.basePath}${data.path}`;
    _.each(data.competitionTabs, (tab: ICompetitionTab) => {
      tab.url = `${this.basePath}${tab.path}`;
      tab.path = `${this.basePath}${tab.path}`;
      if (tab.competitionSubTabs) {
        _.each(tab.competitionSubTabs, (subtab: ICompetitionSubTab) => {
          subtab.path = `${this.basePath}${subtab.path}`;
        });
      }
    });
    return data;
  }

  /**
   * Find subtab data using route params.
   * @return {Object} subtab object.
   */
  private findSubTab(): ICompetitionSubTab {
    const tab: ICompetitionTab = this.findTab();
    const subtab: string = this.routingState.getRouteParam('subTab', this.route.snapshot);

    return _.findWhere(tab.competitionSubTabs, { path: `${tab.path}/${subtab}` }) || tab.competitionSubTabs[0];
  }

  /**
   * Group events with same id's but different markets
   * @param {Array} events
   * @return {Array} events
   */
  private groupEvents(events: ISportEvent[]): ISportEvent[] {
    const groupedEvents = _.groupBy(events, 'id');

    return _.map(groupedEvents, arr => {
      if (arr.length > 1) {
        return Object.assign({}, arr[0], {
          markets: _.uniq(_.flatten(_.pluck(arr, 'markets')), 'id')
        });
      }

      return arr[0];
    });
  }
}

