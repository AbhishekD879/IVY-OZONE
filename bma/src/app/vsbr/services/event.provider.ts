
import { map } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';



import { IEventWithRacingFormResponse, ISsResponse, IEventSSResponse } from '../models/virtuals-ss-respose.model';
import { IEventForClassRequestParams } from './../models/request-params.model';
import { IOutcomeEntity } from '@core/models/outcome-entity.model';
import { IMarketEntity } from '@core/models/market-entity.model';
import { IOutcome } from '@core/models/outcome.model';


/**
 * Service which provide fetching event functionality
 */
@Injectable()
export class EventProvider {
  private SITESERVER_ENDPOINT: string;

  constructor(private http: HttpClient) {
    this.SITESERVER_ENDPOINT = environment.SITESERVER_ENDPOINT;
  }

  /**
   * Get event by Id
   * @param {string} id - id of event
   * @returns {Observable<ISportEvent>}
   */
  getEvent(id: string): Observable<ISsResponse> {
    const endpoint = `${this.SITESERVER_ENDPOINT}/EventToOutcomeForEvent/${id}?racingForm=outcome&prune=market`;

    return this.http.get<IEventWithRacingFormResponse>(endpoint, {
      observe: 'response'
    }).pipe(map((data: HttpResponse<IEventWithRacingFormResponse>) => {
      return this.buildEvent(data.body);
    }));
  }

  /**
   * Get event by Id
   * @param {string} idsJoined - id of event
   * @returns {Observable<ISportEvent>}
   */
  getEventsGroup(idsJoined: string): Observable<ISsResponse[]> {
    const endpoint = `${this.SITESERVER_ENDPOINT}/EventToOutcomeForEvent/${idsJoined}?racingForm=outcome&prune=market`;

    return this.http.get<IEventWithRacingFormResponse>(endpoint, {
      observe: 'response'
    }).pipe(map((data: HttpResponse<IEventWithRacingFormResponse>) => {
      return this.buildEventsGroup(data.body);
    }));
  }

  /**
   * Get events for specific classes
   * @param {IEventForClassRequestParams} options - classIds, startTime, endTime, brTypes of event
   * @returns {Observable<IEventSSResponse>}
   */
  getEventForClass(options: IEventForClassRequestParams): Observable<IEventSSResponse> {
    const { classId, startTime, endTime, brTypes } = options;
    const endpoint = `${this.SITESERVER_ENDPOINT}/EventForClass/${classId}?simpleFilter=class.isActive:isTrue&` +
        `simpleFilter=class.siteChannels:contains:M&${brTypes}&` +
        `simpleFilter=event.isResulted:isFalse&` +
        `simpleFilter=event.startTime:lessThanOrEqual:${endTime}&` +
        `simpleFilter=event.startTime:greaterThan:${startTime}`;

    return this.http.get<IEventSSResponse>(endpoint, {
      observe: 'response'
    }).pipe(map((data: HttpResponse<IEventSSResponse>) => {
      return data.body;
    }));
  }

  /**
   * Extend event with racingFormOutcome Info
   * @param {ISsResponse} eventData - event data
   * @param {ISsResponse[]} racingFormOutcomes - racingFormOutcome objects array
   * @returns {ISsResponse}
   */
  private extendEventWithRacingFormOutcome(eventData: ISsResponse, racingFormOutcomes: ISsResponse[]): ISsResponse {
    const extendedEventContainerArray = this.extendEventsWithRacingFormOutcome([eventData], racingFormOutcomes);
    return extendedEventContainerArray && extendedEventContainerArray[0];
  }

  /**
   * Extend event with racingFormOutcome Info
   * @param {ISsResponse} eventDataArray - event data
   * @param {ISsResponse[]} racingFormOutcomeArray - racingFormOutcome objects array
   * @returns {ISsResponse}
   */
  private extendEventsWithRacingFormOutcome(eventDataArray: ISsResponse[], racingFormOutcomeArray: ISsResponse[]): ISsResponse[] {
    for (const eventData of eventDataArray) {
      const marketChildren = this.getMarketChildrenIfExist(eventData);
      if (marketChildren && marketChildren.length) {
        marketChildren.forEach((elem, index) => {
          const eventMarketOutcome = marketChildren[index].outcome,
            eventMarketOutcomeId = eventMarketOutcome.id;

          const suitableOutcomesElements = racingFormOutcomeArray
            .filter(racingFormOutcomeElement => racingFormOutcomeElement.racingFormOutcome.refRecordId === eventMarketOutcomeId);
          const racingFormOutcome = suitableOutcomesElements
            && suitableOutcomesElements[0] && suitableOutcomesElements[0].racingFormOutcome;

          if (racingFormOutcome) {
            eventMarketOutcome.silkName = racingFormOutcome.silkName;
            eventMarketOutcome.racerId = racingFormOutcome.id;
            eventMarketOutcome.drawNumber = racingFormOutcome.draw;
            eventMarketOutcome.jockey = racingFormOutcome.jockey || racingFormOutcome.trainer;
          }
        });
      }
    }

    return eventDataArray;
  }

  private getMarketChildrenIfExist(eventData: ISsResponse): { outcome: IOutcome }[] {
    return eventData.event &&
      eventData.event.children &&
      eventData.event.children[0] &&
      eventData.event.children[0].market &&
      eventData.event.children[0].market.children;
  }

  /**
   * Prepare event data with correct data formats
   * @param {ISsResponse} eventData - event data
   * @returns {ISsResponse}
   */
  private prepareEventData(eventData: ISsResponse): ISsResponse {
    return this.prepareEventsData([eventData])[0];
  }

  private prepareEventsData(eventsData: ISsResponse[]): ISsResponse[] {
    // Time removed from title because of service timezone bug.
    // Removed time before title and after '-'
    eventsData.forEach(eventData => {
      eventData.event.name = eventData.event.name.replace(/^\d*:\d\d\s/, '').split('-').shift();
      eventData.event.startTimeUnix = Date.parse(eventData.event.startTime);
      eventData.event.children && eventData.event.children.forEach((market: IMarketEntity) => {
        market.market.children && market.market.children.forEach((item: IOutcomeEntity) => {
          if (item.outcome.children) {
            item.outcome.children[0].price.priceDec = parseFloat(item.outcome.children[0].price.priceDec.toString());
          }
        });
      });
    });
    return eventsData;
  }

  /**
   * Build events according to response
   * @param {IEventWithRacingFormResponse} ssEvent - event from SS response
   * @returns {ISsResponse} - prepared event entity
   */
  private buildEvent(ssEvent: IEventWithRacingFormResponse): ISsResponse {
    const arrResponse = ssEvent.SSResponse.children,
      racingFormOutcomes = _.filter(arrResponse, (responseItem: ISsResponse): boolean => !!responseItem.racingFormOutcome);
    let eventData = _.find(arrResponse, responseItem => responseItem.event);
    eventData = this.extendEventWithRacingFormOutcome(eventData, racingFormOutcomes);
    eventData = this.prepareEventData(eventData);
    return eventData;
  }

  /**
   * Build and enrich events according to response
   * @param {IEventWithRacingFormResponse} ssEvent - event from SS response
   * @returns {ISsResponse} - prepared event entities array
   */
  private buildEventsGroup(ssEvent: IEventWithRacingFormResponse): ISsResponse[] {
    const arrResponse = ssEvent.SSResponse.children,
      racingFormOutcomes = arrResponse && arrResponse.filter((responseItem: ISsResponse): boolean => !!responseItem.racingFormOutcome);
    let events = arrResponse && arrResponse.filter((responseItem: ISsResponse): boolean => !!responseItem.event);
    events = this.extendEventsWithRacingFormOutcome(events, racingFormOutcomes);
    events = this.prepareEventsData(events);

    return events;
  }
}
