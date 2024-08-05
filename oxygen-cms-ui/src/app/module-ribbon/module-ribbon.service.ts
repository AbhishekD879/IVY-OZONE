import { Injectable } from '@angular/core';
import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import { ApiClientService } from '@app/client/private/services/http';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { Observable } from 'rxjs/Observable';
import * as _ from 'lodash';

@Injectable()
export class ModuleRibbonService {

  constructor(
    private apiClientService: ApiClientService
  ) {
  }

  getEventHubs(): Observable<IEventHub[]> {
    return this.apiClientService.eventHub().getAllEventHubs();
  }

  getPossibleEventHubsToMap(tabs: ModuleRibbonTab[]): Observable<IEventHub[]> {
    return this.getEventHubs()
      .map((eventHubs: IEventHub[]) => {
        _.each(tabs, (tab) => {
          if (tab.internalId.indexOf('tab-eventhub') >= 0) {
            const hubIndexMatch = tab.url.match(/\d+$/);
            const hubIndexInTab = hubIndexMatch && parseInt(hubIndexMatch[0], 10);
            _.remove(eventHubs, {
              indexNumber: hubIndexInTab
            });
          }
         });

        return eventHubs;
      });
  }
}
