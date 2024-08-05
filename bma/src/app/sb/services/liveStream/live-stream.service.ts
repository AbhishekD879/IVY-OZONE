import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import * as _ from 'underscore';
import { LIVE_STREAM_CONFIG } from '@sb/sb.constant';
import { ILiveStreamConfigObject, IStreamAvailable, IStreamProviders } from '@sb/services/liveStream/live-stream.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IStreamProvidersResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { IConstant } from '@core/services/models/constant.model';

@Injectable()
export class LiveStreamService {
  private readonly CATEGORIES_DATA: any = environment.CATEGORIES_DATA;

  constructor(
    private windowRef: WindowRefService
  ) {
    this.checkCondition = this.checkCondition.bind(this);
  }

  /**
   * Disabled/enabled live stream icon for event
   *
   * @param liveStreamConfig {array}
   *        array of stream config objects
   *        perform stream, atTheRacing stream, img stream...
   *        and returns functions that takes event to mark it
   *
   * @returns {Function}
   */
  isLiveStreamAvailable(liveStreamConfig: ILiveStreamConfigObject[]): Function {

    return ((eventObj: ISportEvent): boolean | IStreamAvailable => {
      if (!eventObj || !liveStreamConfig || _.isEmpty(eventObj) || _.isEmpty(liveStreamConfig)) {
        return false;
      }
      const result = {
        liveStreamAvailable: false,
        streamProviders: this.getStreamProviders(liveStreamConfig)
      };
      if (!this.checkCondition(liveStreamConfig, eventObj)) {
        return result;
      }
      result.liveStreamAvailable = true;
      this.setStreamProviders(result.streamProviders, liveStreamConfig, eventObj);

      return result;
    });
  }

  /**
   * Check condition for live stream
   *
   * @param liveStreamConfig {array}
   *        array of stream config objects
   *        perform stream, atTheRacing stream, img stream...
   * @param eventObj {object}
   *
   * @returns {boolean}
   */
  checkCondition(liveStreamConfig: ILiveStreamConfigObject[], eventObj: ISportEvent): boolean {
    if (!_.has(eventObj, 'drilldownTagNames')) {
      return false;
    }
    if (!this.checkForValidDrilldown(eventObj, liveStreamConfig, 'drilldownTagNames')) {
      return false;
    }

    return true;
  }

  /**
   * Add for each event custom field liveStreamAvailable, streamProviders
   *
   * @param liveStreamConfig {array}
   *        array of stream config objects
   *        perform stream, atTheRacing stream, img stream, IGameMedia stream
   *        default param LIVE_STREAM_CONFIG
   *        and returns functions that takes events array to mark them
   *
   * @returns {array}
   */
  addLiveStreamAvailability(liveStreamConfig: ILiveStreamConfigObject[] = LIVE_STREAM_CONFIG): Function {
    return ((eventsArray: Array<ISportEvent>): Array<ISportEvent> => {
      _.each(eventsArray, eventEntity => {
        if (typeof eventEntity === 'object') {
          _.extend(eventEntity, this.isLiveStreamAvailable(liveStreamConfig)(eventEntity));
        }
      });
      return eventsArray;
    });
  }

  /**
   * Check if racing event
   * {object} event
   * return {boolean}
   */
  checkIfRacingEvent(event: ISportEvent): boolean {
    // Check if racing event has live stream which is not live or pre sim
    let isLiveStream = true;
    if (this.windowRef.nativeWindow._QLGoingDown && this.windowRef.nativeWindow._QLGoingDown.status) {
      switch (this.windowRef.nativeWindow._QLGoingDown.status) {
        case 'Advert':
          isLiveStream = false;
          break;
        case 'nothing':
          isLiveStream = true;
          break;
        default:
          isLiveStream = false;
          break;
      }
    }

    return !!_.findWhere(this.CATEGORIES_DATA.racing, { id: event.categoryId }) && isLiveStream;
  }

  /**
   * Reset stream provider for event entity base on optIn response(
   * if priorityProviderCode available,
   * else remain already assigned streamProviders regarding to drilldownTagNames)
   * @param eventEntity
   * @param provider - response from optIn
   */
  prioritizeStream(eventEntity: ISportEvent, provider: IStreamProvidersResponse): void {
    if (eventEntity && eventEntity.liveStreamAvailable && provider.priorityProviderCode) {
      this.resetProviders(eventEntity);
      this.setProp(eventEntity.streamProviders, provider.priorityProviderCode, true);
    }
  }

  /**
   * Find object key case-insensitive and set value
   * @param obj - object
   * @param name - case-insensitive key
   * @param value - value
   */
  private setProp(obj: IConstant, name: string, value: boolean): void {
    for (const key in obj) {
      if (key.toLowerCase() === name.toLowerCase()) {
        obj[key] = value;
      }
    }
  }

  /**
   * Set false to all providers when error received from optIn MS
   * @param eventEntity - object
   */
  private resetProviders(eventEntity: ISportEvent): void {
    for (const i of Object.keys(eventEntity.streamProviders)) {
      eventEntity.streamProviders[i] = false;
    }
  }

  /**
   * Create object with all stream providers
   *
   * @param liveStreamConfig
   * @returns {{}}
   */
  private getStreamProviders(liveStreamConfig: ILiveStreamConfigObject[]): IStreamProviders {
    const result = {};

    _.each(liveStreamConfig, (item: {type: string}) => {
      result[item.type] = false;
    });

    return result;
  }

  /**
   * Set true/false for each stream provider
   *
   * @param streamProvidersObj {object}
   * @param liveStreamConfig
   *        array of stream config objects
   *        perform stream, atTheRacing stream, img stream...
   *
   * @param eventObj
   */
  private setStreamProviders(streamProvidersObj: IStreamProviders, liveStreamConfig: ILiveStreamConfigObject[],
                             eventObj: ISportEvent): void {
    _.each(liveStreamConfig, (configObj: ILiveStreamConfigObject) => {
      streamProvidersObj[configObj.type] = this.propertyIterator(configObj, eventObj);
    });
  }

  /**
   * Checks all wether valid drilldownTagName is present
   *
   * @param eventObj {object}
   * @param liveStreamConfig {arr}
   * @param field {string}
   * @returns {boolean}
   */
  private checkForValidDrilldown(eventObj: ISportEvent, liveStreamConfig: ILiveStreamConfigObject[],
                                 field: string): boolean {
    const validValues = _.pluck(liveStreamConfig, field),
      drilldownTagNames = eventObj[field].split(',');

    return drilldownTagNames.some(element => {
      return validValues.indexOf(element) !== -1;
    });
  }

  /**
   * Checks all field in config object
   *
   * @param configObj {object}
   * @param eventObj {object}
   * @returns {boolean}
   */
  private propertyIterator(configObj: { [key: string]: any; }, eventObj: ISportEvent): boolean {
    let hasAllProps = true;

    _.each(configObj, (value, key: string) => {
      if (key === 'type') {
        return;
      }
      hasAllProps = hasAllProps && _.has(eventObj, key) && this.hasSomeParams(value, eventObj[key].split(','));
    });

    return hasAllProps;
  }

  /**
   * Checks: has array some value
   *
   * @param value {string}
   * @param arr {array}
   * @returns {boolean}
   */
  private hasSomeParams(value: string, arr: Array<string>): boolean {
    return arr.indexOf(value) >= 0;
  }
}
