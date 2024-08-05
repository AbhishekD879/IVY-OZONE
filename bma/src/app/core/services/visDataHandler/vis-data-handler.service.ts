import { concatMap, map } from 'rxjs/operators';
import { Observable, throwError, from as fromPromise } from 'rxjs';
import { Injectable } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as _ from 'underscore';
import { CmsService } from '@coreModule/services/cms/cms.service';

import environment from '@environment/oxygenEnvConfig';
import { ISystemConfig } from '../cms/models/system-config';
import { VisEventService } from '../visEvent/vis-event.service';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { EventService } from '@sb/services/event/event.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

/**
 * All necessary data for visualisation to be rendered and handled.
 */
@Injectable()
export class VisDataHandlerService {
  constructor(
    private eventFactory: EventService,
    private visEventService: VisEventService,
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private route: ActivatedRoute,
    private routingState: RoutingState
  ) {}

  init(eventEntity?: ISportEvent): Observable<any> {
    const configObj: any = {};
    configObj.eventId = this.routingState.getRouteParam('id', this.route.snapshot);
    const event = eventEntity;
    if (event) {
      return this.getConfig(configObj, event);
    } else {
      return fromPromise(this.eventFactory.getEvent(configObj.eventId)).pipe(map(data => this.getConfig(configObj, data)));
    }
  }

  private getVisEndpoint(event: ISportEvent): Observable<{ visEndpoint: string; timeout: number }> {
    return this.cmsService.getSystemConfig().pipe(
      map((sysConfig: ISystemConfig) => {
        const visConfig = sysConfig.VisualisationConfig;
        const timeout = Number(visConfig.timeout);
        let visEndpoint: string;

        if (!Boolean(visConfig.disabled)) {
          switch (event.categoryId) {
            case visConfig.footballId:
              visEndpoint = environment.VISUALIZATION_ENDPOINT;
              break;
            case visConfig.tennisId:
              visEndpoint = environment.VISUALIZATION_TENNIS_ENDPOINT;
              break;
          }
        }

        return { visEndpoint, timeout };
      }));
  }

  private getConfig(configObj: any, event: ISportEvent): Observable<any> {
    return this.getVisEndpoint(event).pipe(concatMap((data) => {
      if (!data.visEndpoint) {
        return throwError('Not football or tennis vis');
      }
      return this.visEventService.checkForEventsWithAvailableVisualization(configObj.eventId, data.visEndpoint, data.timeout);
    }), map((visEventFactoryResp) => {
      configObj.eventIsLive = event.eventIsLive;
      configObj.eventsWithVisualizationParams = visEventFactoryResp;
      return configObj;
    }), concatMap((res) => {
      return this.visEventService.checkPreMatchWidgetAvailability(res.eventId);
    }), map((visEventFactoryResp) => {
      configObj.eventsWithPrematchData = visEventFactoryResp;
      const isVisData = configObj.eventsWithVisualizationParams && configObj.eventsWithVisualizationParams.length;
      const isPreMatchData = configObj.eventsWithPrematchData;
      const isLive = configObj.eventIsLive;
      const isPastEvent = !_.keys(event).length;
      // When pre-match widget is available it should be hidden for:
      // - past events;
      // - live events without visualisation.
      if (isPastEvent || (!isPreMatchData && !isLive) || (isPreMatchData && isLive && !isVisData)) {
        this.pubSubService.publish(this.pubSubService.API.DISPLAY_WIDGET, [{ name: 'match-centre' }]);
      }

      return configObj;
    }));
  }
}

