import { timeout, map, catchError, switchMap } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import * as _ from 'underscore';

import { IVisEventAvailability, IPreMatchAvailability, IEventVisParams } from './vis-event.model';
import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IFootball3DBanner, ISystemConfig } from '../cms/models';
import { WindowRefService } from '../windowRef/window-ref.service';
import { TimeService } from '@core/services/time/time.service';

/**
 * Service for visualization related API calls.
 */
@Injectable()
export class VisEventService {

  private requestTimeout: number;
  private readonly DEFAULT_TIMEOUT: number = 10;

  constructor(
    private cms: CmsService,
    private http: HttpClient,
    private windowRef: WindowRefService,
    private timeService: TimeService
  ) {
    this.visListener = this.visListener.bind(this);
  }

  /**
   * Return array of params for events which have available visualization
   * @param {string | { id: string }[]} events array or eventid string, or comma separated string of event ids
   * @returns {Promise<IEventVisParams[] | void>}
   */
  checkForEventsWithAvailableVisualization(
    events: string | { id: string }[],
    endpoint?: string,
    timeOut?: number
  ): Observable<IEventVisParams[] | void> {
    this.requestTimeout = timeOut;
    const eventIdsString: string = typeof events === 'string' ? events : _.map(events, event => event.id).join(',');
    // Check visualization availability for all event id's
    return this.isVisualizationAvailable(endpoint, eventIdsString).pipe(
    map((response: HttpResponse<IVisEventAvailability[]>) =>
      _.reduce(response.body, (params: IEventVisParams[], event: IVisEventAvailability) => {
        // If providerName is present and sport is football, visualization is available for this event
        // In all other cases we assume that visualization is not available
        // If provider is OpenBet we can't display castro widget, cause it will not display match results,
        // so we need to set parameter canDisplayCastro = false for those events
        // Please contact Visualization team if you need more information about castro widget
        const { id, providerName, sportName } = event;
        providerName && params.push({ id, sportName, canDisplayCastro: providerName !== 'openBet' });
        return params;
      }, [])),
      catchError(err => {
        events ? console.warn('Can\'t get visualization params (checkForEventsWithAvailableVisualization) ', err)
          : console.warn('Please pass events to checkForEventsWithAvailableVisualization method');
        return throwError(err);
      }));
  }

  /**
   * Checks pre-match stats widget availability
   * @param {string} eventId
   * @returns {Promise<boolean | void>}
   */
  checkPreMatchWidgetAvailability(eventId: string): Observable<boolean> {
    return this.isPreMatchDataAvailable(eventId).pipe(
      map((data: HttpResponse<IPreMatchAvailability[]>) => data.body[0].stats),
      catchError(err => {
        console.warn('Pre-match availability error (checkPreMatchWidgetAvailability)', err);
        return throwError(err);
      }));
  }

  /**
   * Post message with banners data to visualisation iFrame
   * @param {MessageEvent} event
   */
  visListener(event: MessageEvent): void {
    if (event.data.type === 'vis_ready') {
      const { visWidget } = this.windowRef.nativeWindow.frames;
      this.cms.getFootball3DBanners()
        .subscribe((banners: IFootball3DBanner[]) => {
          const fbanners = banners.filter((banner: IFootball3DBanner) => banner['uriMedium'] && banner['uriMedium'].length);
          visWidget.postMessage({ type: 'vis_banners_ready', fbanners }, '*');
        });
    }
  }

  /**
   * Check the visualization availability for event/events
   * @param {string} endpoint - endpoint depends on environment, is set in Gruntfile
   * @param {string} eventIds
   * @returns {Observable<HttpResponse<IVisEventAvailability[]>>}
   */
  private isVisualizationAvailable(endpoint: string, eventIds: string): Observable<HttpResponse<IVisEventAvailability[]>> {
    return this.getData<IVisEventAvailability[]>(`${endpoint}/is-available/${eventIds}`);
  }

  /**
   * Check whether pre match data is available for event
   * @param {string} eventId
   * @returns {Observable<HttpResponse<IPreMatchAvailability[]>>}
   */
  private isPreMatchDataAvailable(eventId: string): Observable<HttpResponse<IPreMatchAvailability[]>> {
    return this.cms.getSystemConfig(false).pipe(
      map((sysConfig: ISystemConfig) => {
        const visConfig = sysConfig.VisualisationConfig;
        return !Boolean(visConfig.disabled);
      }),
      switchMap(enabled => {
        return enabled ? this.getData<IPreMatchAvailability[]>(`${environment.VISUALIZATION_ENDPOINT}/is-stats/${eventId}`)
          : throwError('VisualisationConfig disabled');
      })
    );
  }

  /**
   * Generic method for HTTP-request
   * @param {string} endpoint
   * @param {object} params
   * @return {Observable<HttpResponse<T>>}
   */
  private getData<T>(endpoint: string): Observable<HttpResponse<T>> {
    const timeoutAmount = this.requestTimeout ?
      this.requestTimeout * this.timeService.oneSecond : this.DEFAULT_TIMEOUT * this.timeService.oneSecond;
    return this.http.get<T>(endpoint, { observe: 'response' }).pipe(timeout(timeoutAmount));
  }
}

