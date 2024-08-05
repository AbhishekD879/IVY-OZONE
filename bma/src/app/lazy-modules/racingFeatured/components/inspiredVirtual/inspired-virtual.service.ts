import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { TimeService } from '@core/services/time/time.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { inspiredVirtualConfig } from './inspired-virtual.constant';
import environment from '@environment/oxygenEnvConfig';
import { ISportEvent } from '@core/models/sport-event.model';
import { SiteServerService } from '@core/services/siteServer/site-server.service';

@Injectable({
  providedIn: 'root'
})
export class InspiredVirtualService {
  config = inspiredVirtualConfig;
  BR_TYPE_ID = environment.BR_TYPE_ID;
  data = null;

  constructor(
    private siteServerService: SiteServerService,
    private timeService: TimeService,
    private cacheEventsService: CacheEventsService,
    private gtmService: GtmService) {
    this.extendCacheParams();
  }

  /**
   * send GTM tracking, when user click on "VIRTUALS" section header first time to collapse on virtual carousel
   */
  sendGTMOnFirstTimeCollapse(sportName: string): void {
    const gtmOnFirstTimeCollapseObject = _.extendOwn({ event: 'trackEvent', eventLabel: 'collapse' }, this.getGtmCommonObject(sportName));
    this.gtmService.push('trackEvent', gtmOnFirstTimeCollapseObject);
  }

  /**
   * send GTM tracking, when user click on bet now on virtual carousel
   */
  sendGTMOnGoToLiveEvent(sportName: string): void {
    const gtmOnGoToLiveEventObject = _.extendOwn({ eventLabel: 'bet now' }, this.getGtmCommonObject(sportName));
    this.gtmService.push('trackEvent', gtmOnGoToLiveEventObject);
  }

  /**
   * Get data format in mm:ss
   * @params {number} startTime(timestamp)
   */
  getStartTime(startTime: number): string {
    return this.timeService.getLocalHourMinInMilitary(startTime);
  }

  /**
   * Removes all timers from events with timers
   */
  destroyTimers(): void {
    const timers = ['countdownTimer', 'liveTimer'],
      eventsCount = this.data ? this.data.length : 0;

    for (let i = 0; i < eventsCount; i++) {
      _.each(timers, (timer: string) => {
        if (this.data && {}.hasOwnProperty.call(this.data[i], timer)) {
          this.data[i][timer].stop();
          delete this.data[i][timer];
        }
      });
    }
  }

  setupEvents(eventsArray): ISportEvent[] {
    this.data = this.addTimers(this.validEvents(_.sortBy(this.convertStartTime(eventsArray), 'startTime')));
    return this.data;
  }

  getEvents(): Promise<ISportEvent[]> {
    return this.cachedEvents(this.siteServerService.getInspiredVirtualEvents.bind(this.siteServerService),
      this.config.cacheName)(this.requestParams())
    .then(eventsArray => _.sortBy(eventsArray, 'startTime'))
    .then(this.validEvents.bind(this)).then(this.addTimers.bind(this)).then(data => {
      this.data = data || [];
      return this.data;
    });
  }

  getGtmCommonObject(sportName: string) {
    const sport = sportName.indexOf('horse') > -1 ? 'horse' : 'greyhound';
    return { eventCategory: `${sport} racing`, eventAction: `virtual ${sport} racing` };
  }

  /**
   * Extends apiDataCacheInterval and storedData params for cache
   */
  private extendCacheParams(): void {
    this.timeService.apiDataCacheInterval[this.config.cacheName] = this.config.cacheInterval;
    this.cacheEventsService.storedData[this.config.cacheName] = {};
  }

  private cachedEvents(loaderFn: Function, cacheName: string): Function {
    return params => {
      const store = _.partial(this.cacheEventsService.store, cacheName);
      const stored = this.cacheEventsService.stored(cacheName);

      // @ts-ignore
      return stored ? this.cacheEventsService.async(stored) : loaderFn(params).then(events => store(events));
    };
  }

  private requestParams(): Object {
    return _.extendOwn({
      siteChannels: 'M',
      excludeTypeIdCodes: this.BR_TYPE_ID.join(','),
      startTime: this.timeService.selectTimeRangeStart(),
      endTime: this.timeService.selectTimeRangeEnd()
    }, this.config.request);
  }

  private convertStartTime(eventsArray: ISportEvent[]): ISportEvent[] {
    return eventsArray.map(event => {
      event.startTime = new Date(event.startTime).getTime().toString();
      return event;
    });
  }

  private validEvents(eventsArray: ISportEvent[]) {
    // check whether event 'isFinished and isFinished according to eventFinishedInterval'
    return eventsArray.filter(event => !event.isFinished && (Date.now() - Number(event.startTime) < this.config.eventFinishedInterval));
  }

  private addTimers(eventsArray: ISportEvent[]): ISportEvent[] {
    for (let i = 0; i < eventsArray.length; i++) {
      this.addTimer(eventsArray[i]);
    }
    return eventsArray;
  }

  private addTimer(eventEntity: ISportEvent): void {
    const timerFunction = this.chooseTimer(eventEntity);
    timerFunction.call(this, eventEntity);
  }

  private chooseTimer(eventEntity: ISportEvent): Function {
    return Number(eventEntity.startTime) - Date.now() > this.config.countdownTimerInterval + 1000
      ? this.beforeEventLiveTimerFunction : this.eventLiveTimerFunction;
  }

  private beforeEventLiveTimerFunction(eventEntity: ISportEvent): void {
    const that = this;
    eventEntity.countdownTimer = {
      startTime: eventEntity.startTime,
      timeLeft: null,
      minutes: null,
      seconds: null,
      start(): void {
        this.timeLeft = Math.floor((Number(this.startTime) - that.config.countdownTimerInterval - Date.now()) / 1000);
        this.timer = setInterval(this.update.bind(this), 1000);
      },
      stop(): void {
        clearInterval(this.timer);
      },
      postUpdate(): void {
        that.addTimer(eventEntity);
        delete eventEntity.countdownTimer;
      },
      update(): void {
        this.timeLeft--;
        const hours = parseInt(`${this.timeLeft / 3600}`, 10),
          minutes = parseInt(`${this.timeLeft / 60}`, 10),
          seconds = this.timeLeft % 60;

        if (minutes === 0 && seconds === 0) {
          this.stop();
          this.postUpdate();
        } else {
          this.hours = hours < 10 ? `0${hours}` : hours.toString();
          this.minutes = minutes < 10 ? `0${minutes}` : minutes.toString();
          this.seconds = seconds < 10 ? `0${seconds}` : seconds.toString();
        }
      }
    };
    eventEntity.countdownTimer.start();
  }

  private eventLiveTimerFunction(eventEntity: ISportEvent) {
    const that = this;
    eventEntity.liveTimer = {
      startTime: eventEntity.startTime,
      timeLeft: null,
      start(): void {
        this.timeLeft = Math.floor((Number(this.startTime) + that.config.eventFinishedInterval - Date.now()) / 1000);
        this.timer = setInterval(this.update.bind(this), 1000);
      },
      stop(): void {
        clearInterval(this.timer);
      },
      postUpdate(): void {
        delete eventEntity.liveTimer;
        that.data.splice(0, 1);
        if (that.data.length > 0) {
          that.addTimer(that.data[that.data.length - 1]);
        }
      },
      update(): void {
        this.timeLeft--;
        if (this.timeLeft === 0) {
          this.stop();
          this.postUpdate();
        }
      }
    };
    eventEntity.liveTimer.start();
  }

  /**
   * GA tracker for virtual sports
   * @param url : string
   */
  public virtualsGTMEventTracker(url: string, event: ISportEvent): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'virtuals sports',
      'component.LabelEvent': 'next events',
      'component.ActionEvent': 'click',
      'component.PositionEvent': event?.name,
      'component.LocationEvent': 'next events',
      'component.EventDetails': 'bet now cta',
      'component.URLclicked': url,
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
}
