import { Injectable } from '@angular/core';
import { Router, Event, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import * as _ from 'underscore';
import { ISportEvent } from '@core/models/sport-event.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Injectable()
export class StreamTrackingService {
  private second = 1000;
  // Representation of time thresholds: 5sec 30sec 2min 10min 30min 31min
  private timeThresholds = [5, 30, 120, 600, 1800, 1860];
  private trackingVideos = {};
  private trackedIds = {
    preSim: [],
    liveSim: [],
    liveStream: []
  };
  private preSimOrLiveSimId;

  constructor(
    private windowRef: WindowRefService,
    private gtmService: GtmService,
    private liveStreamService: LiveStreamService,
    private rendererService: RendererService,
    private router: Router,
    private routingState: RoutingState
  ) {}

  /**
   * Set timer for player
   * @params {object} player
   * @return {undefined}
   */
  setTrackingForPlayer(player: HTMLElement & { id_: string }, event: ISportEvent): void {
    if (!player || !event || player.id_) {
      return;
    }
    const id_ = player.getAttribute('id_');
    if (!this.trackingVideos[player.getAttribute('id_')]) {
      let id = id_;
      if (!id) {
        id = player.getAttribute('id');  // for html5 player
        if (this.trackingVideos[id]) {
          return;
        }
      }
      this.trackingVideos[id] = {
        timeWatched: 0,
        streamingEvent: event,
        isOver30MinutesPlayed: false, // needed for infinite pre sim video
        playerObj: player,
        listeners: {}
      };
      this.trackingVideos[id].listeners.play = this.rendererService.renderer.listen(player, 'playing', () => {
        this.startTimer(event);
      });
      this.trackingVideos[id].listeners.pause = this.rendererService.renderer.listen(player, 'pause', (playerEvent) => {
        const currentTarget = this.trackingVideos[this.getVideoId(event)];
        if (currentTarget && (currentTarget.wasStopped)) {
          return;
        }
        this.removeInterval(playerEvent);
        this.pushToGAPlayerStatus(event, 'pause');
      });
      this.trackingVideos[id].listeners.pauseEnded = this.rendererService.renderer.listen(player, 'ended', () => {
        const currentTarget = this.trackingVideos[this.getVideoId(event)];
        if (currentTarget.streamCompleted) {
          return;
        }
        currentTarget.streamCompleted = true;
        this.pushToGAPlayerStatus(event, 'complete');
        this.resetAllTracking();
      });
    }
    // preSimOrLiveSimId need as event object of jwplayer has no information to detect id of this player
    if (this.windowRef.nativeWindow._QLGoingDown && this.windowRef.nativeWindow._QLGoingDown.jwplayer &&
      (this.windowRef.nativeWindow._QLGoingDown.jwplayer.id === player.id)) {
      this.preSimOrLiveSimId = id_;
    }
  }

  /**
   * Removes timer on pause
   * @params {object} event
   */
  resetTimer(event: ISportEvent): void {
    const videoId = this.getVideoId(event);
    if (this.trackingVideos[videoId]) {
      this.trackingVideos[videoId].timeWatched = 0;
      clearInterval(this.trackingVideos[videoId].interval);
    }
  }

  /**
   * Check if event id has been already tracked
   * @param {number} eventId
   * @param {string} label
   * @returns {boolean}
   */
  checkIdForDuplicates(eventId: number, label: string): boolean {
    return _.contains(this.trackedIds[label], eventId);
  }

  /**
   * add id to tracked list by labels preSim, liveSim and liveStream
   * @param {number} eventId
   * @param {string} label
   */
  addIdToTrackedList(eventId: number, label: string): void {
    this.trackedIds[label].push(eventId);
  }

  /**
   * Starts timer on play
   * @params {object} event
   */
  private startTimer(event: ISportEvent): void {
    const currentTarget = this.trackingVideos[this.getVideoId(event)];
    if (currentTarget.streamCompleted) {
      return;
    }
    if (!currentTarget.interval && !currentTarget.isOver30MinutesPlayed) {
      currentTarget.interval = setInterval(() => {
        this.updateAndCheckTime(event);
      }, this.second, false);
      if (!currentTarget.startWasTracked) {
        this.subscribeForPageUnload(event);
        this.pushToGAPlayerStatus(event, 'start');
        currentTarget.startWasTracked = true;
      }
    }
  }

  /**
   * clear url from market names
   * @param {string} url
   */
  private clearURL(url: string): string {
    return url
      .split('/')
      .slice(0, 4)
      .join('/');
  }

  /**
   * Subscribes for page unload and hash change events to send "stop" status to GA
   * @param {object} event
   */
  private subscribeForPageUnload(event: ISportEvent): void {
    const currentTarget = this.trackingVideos[this.getVideoId(event)];

    this.windowRef.nativeWindow.addEventListener('beforeunload', function beforeUnloadHandler() {
      currentTarget.wasStopped = true;
      if (!currentTarget.streamCompleted) {
        this.pushToGAPlayerStatus(event, 'stop');
      }
      this.windowRef.nativeWindow.removeEventListener('beforeunload', beforeUnloadHandler);
      this.resetTimer(event);
      this.resetAllTracking();
      return null;
    }.bind(this));

    const ulrChangeListener: Subscription = this.router.events.subscribe((e: Event) => {
      if (e instanceof NavigationEnd) {
        const currentUrl = this.routingState.getCurrentUrl();
        const oldURL = this.clearURL(this.routingState.getPreviousUrl());
        const newURL = this.clearURL(currentUrl);

        if (newURL.indexOf(oldURL) === 0) {
          return;
        }
        currentTarget.wasStopped = true;
        if (!currentTarget.streamCompleted) {
          this.pushToGAPlayerStatus(event, 'stop');
        }
        ulrChangeListener.unsubscribe();
        this.resetTimer(event);
        this.resetAllTracking();
      }
    });
  }

  /**
   * Pushes updates of liveStreamProgress to GA. Acceted statuses "pause" "complete" "start" and "stop"
   * @param {object} event
   * @param {string} status
   */
  private pushToGAPlayerStatus(event: ISportEvent, status: string): void {
    const targetId = this.getVideoId(event);
    if (this.trackingVideos[targetId]) {
      const streamingEvent = this.trackingVideos[targetId].streamingEvent;
      this.gtmService.push('trackEvent', {
        eventCategory: 'streaming',
        eventAction: this.getEventAction(),
        eventLabel: this.liveStreamService.checkIfRacingEvent(streamingEvent) ? 'bet and watch' : 'watch and bet',
        sportID: streamingEvent.categoryId,
        typeID: streamingEvent.typeId,
        eventID: streamingEvent.id,
        liveStreamProgress: status
      });
    }
  }

  /**
   * Removes timer on ended
   * @params {object} event
   */
  private removeInterval(event: ISportEvent): void {
    clearInterval(this.trackingVideos[this.getVideoId(event)].interval);
    delete this.trackingVideos[this.getVideoId(event)].interval;
  }

  /**
   * Updates timer value and sends GA in time thresholds
   * @params {object} event
   */
  private updateAndCheckTime(event: ISportEvent): void {
    const targetId = this.getVideoId(event),
      streamingEvent = this.trackingVideos[targetId].streamingEvent;
    this.trackingVideos[targetId].timeWatched += this.second;
    const watchedTime = this.trackingVideos[targetId].timeWatched / this.second;

    if (_.contains(this.timeThresholds, watchedTime)) {
      this.gtmService.push('trackEvent', {
        eventCategory: 'streaming',
        eventAction: this.getEventAction(),
        eventLabel: this.liveStreamService.checkIfRacingEvent(streamingEvent) ? 'bet and watch' : 'watch and bet',
        sportID: streamingEvent.categoryId,
        typeID: streamingEvent.typeId,
        eventID: streamingEvent.id,
        liveStreamProgress: this.reformatTime(watchedTime, event)
      });
    }
  }

  /**
   * Convert milliseconds to string representation of time
   * @params {number} time
   * @return {string}
   */
  private reformatTime(time: number, event: ISportEvent): string {
    const thirtyOneMinute = 1860,
      oneMinute = 60;
    if (time === thirtyOneMinute) { // if over then 30 minutes
      this.trackingVideos[this.getVideoId(event)].isOver30MinutesPlayed = true;
      this.resetTimer(event);
      return 'over 30 minutes';
    } else if (time >= oneMinute) { // if greater then a minute
      return `${Math.round(time / oneMinute)} minutes`;
    }
    return `${time} seconds`;
  }

  /**
   * Gets video id. Function is needed for jw player as it has different
   * event object then html5 player or video js player
   * @params {object} event
   * @return {string}
   */
  private getVideoId(event: ISportEvent): string {
    if (event.target && event.target.id) {
      return event.target.id;
    } else if (event.id) {
      return this.trackingVideos[`QL_video_${event.id}`] ? this.preSimOrLiveSimId : event.id;
    }
    return this.preSimOrLiveSimId;
  }

  /**
   * Get correct event action for GA
   * @return {string}
   */
  private getEventAction(): string {
    const preSimLabel = 'watch pre sim',
      liveStreamLabel = 'watch video stream',
      liveSimLabel = 'watch live sim';
    let action = liveStreamLabel;

    if (this.windowRef.nativeWindow._QLGoingDown && this.windowRef.nativeWindow._QLGoingDown.status) {
      // "Advert" property to detect pre sim video and "Going Down" for live sim
      switch (this.windowRef.nativeWindow._QLGoingDown.status) {
        case 'Advert':
          action = preSimLabel;
          break;
        case 'nothing':
          action = liveStreamLabel;
          break;
        default:
          action = liveSimLabel;
          break;
      }
    }
    return action;
  }

  private resetAllTracking(): void {
    _.forEach(this.trackingVideos, (value, key) => {
      const eventObj = this.trackingVideos[key];
      clearInterval(eventObj.interval);
      eventObj.listeners.pause();
      eventObj.listeners.pauseEnded();
      eventObj.listeners.play();
    });
  }
}
