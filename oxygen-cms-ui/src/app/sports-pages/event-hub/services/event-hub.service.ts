import { Injectable } from '@angular/core';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { ApiClientService } from '@app/client/private/services/http';
import { Observable } from 'rxjs/Observable';
import { HttpResponse } from '@angular/common/http';
import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import * as _ from 'lodash';
import { concatMap } from 'rxjs/operators';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { forkJoin } from 'rxjs/observable/forkJoin';

@Injectable()
export class EventHubService {

  constructor(
    private apiClientService: ApiClientService
  ) { }

  getHubList(): Observable<IEventHub[]> {
    return this.apiClientService.eventHub().getAllEventHubs();
  }

  getHubData(hubId: string): Observable<IEventHub> {
    return this.apiClientService.eventHub().getEventHubById(hubId);
  }

  createHub(hubData: IEventHub): Observable<IEventHub> {
    return this.apiClientService.eventHub().postNewEventHub(hubData);
  }

  updateHubData(hubData: IEventHub): Observable<IEventHub> {
    return this.apiClientService.eventHub().updateEventHub(hubData);
  }

  /**
   * Remove sport-modules, mapped to EventHub, during eventhub Deleting
   */
  removeHubModules(hubIndex: number): Observable<any> {
    return this.apiClientService.homepages().getAllModulesBySport('eventhub', hubIndex)
      .map((res) => res.body)
      .pipe(concatMap((sportsModules: SportsModule[]) => {
        const requestQueue = [];

        if (!sportsModules || sportsModules.length === 0) {
          return Observable.of(null);
        }

        sportsModules.forEach((module: SportsModule) => {
          requestQueue.push((() => {
            return this.apiClientService.homepages().removeModule(module.id);
          })());
        });

        return forkJoin(requestQueue);
      }));
  }

  /**
   * Remove EventHub and Ribbon tab if it is mapped to some.
   * @param hub
   */
  removeHub(hub: IEventHub): Observable<IEventHub> {
    // load tabs to check mapped eventhubs
    return this.apiClientService.moduleRibbonTab()
      .getByBrand()
      .map((moduleRibbonResponse: HttpResponse<ModuleRibbonTab[]>) => {
        return moduleRibbonResponse.body;
      })
      .pipe(concatMap((moduleRibbonList: ModuleRibbonTab[]) => {
        // `any` not ModuleRibbonTab due to some lodash issue (https://github.com/DefinitelyTyped/DefinitelyTyped/issues/25758)
         const mappedTab: ModuleRibbonTab = _.find(moduleRibbonList, (tab: any) => {
          if (tab.directiveName.toLowerCase() === 'eventhub' && (hub.indexNumber === tab.hubIndex)) {
            return tab;
          }
        });

        if (mappedTab) {
          // remove tab, where EventHub is mapped.
          return this.apiClientService.moduleRibbonTab().remove(mappedTab.id)
            .pipe(concatMap(
              () => this.apiClientService.eventHub().removeEventHub(hub.id)
            ));
        }

        return this.apiClientService.eventHub().removeEventHub(hub.id);
      }))
      .pipe(concatMap(
        () => {
          return this.removeHubModules(hub.indexNumber);
        }
      ));
  }
}
