import { Component, Input, OnDestroy, OnInit, SimpleChanges, OnChanges } from '@angular/core';
import * as _ from 'underscore';

import { TimeService } from '@core/services/time/time.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { EventService } from '@sb/services/event/event.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { ITeams } from '@core/models/teams.model';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { greyhoundConfig } from '@core/services/racing/config/greyhound.config';
import environment from '@environment/oxygenEnvConfig';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { EventNamePipe } from '@app/shared/pipes/event-name/event-name.pipe';

@Component({
  selector: 'event-header',
  templateUrl: './event-header.component.html',
  styleUrls: ['./event-header.component.scss']
})
export class EventHeaderComponent implements OnInit, OnDestroy, OnChanges {

  @Input() event: ISportEvent;
  @Input() status: string;
  @Input() result: string;
  @Input() legType: string;
  @Input() place: string;
  @Input() totalStatus: string;
  @Input() matchTime: string;
  @Input() runningSetIndex: string;
  @Input() homeScore: string;
  @Input() awayScore: string;
  @Input() isHRLiveLabel: boolean;
  @Input() isOff: boolean;
  @Input() id: string;
  @Input() outcomeId: string;
  @Input() isLd?:string;

  animationDelay: number;
  eventStartedOrLive: boolean;
  isResultedMatch: boolean;
  isFootball: boolean;
  isTennis: boolean;
  isEventHasCurrentPoints: boolean;
  startTime: Date;
  timerLabel: string;
  isEventMatch: boolean;
  liveLabelText: string;
  todayText: string;
  isLiveEvent: boolean;
  isSpecial: boolean;
  animationClassesRemoval: number;
  componentId: string;
  isSuspendedEvent: boolean;
  eventName: string;
  placeWithFormat: string;

  private CATEGORIES_DATA = environment.CATEGORIES_DATA;
  sessionData: any = {};

  constructor(
    private timeService: TimeService,
    private coreTools: CoreToolsService,
    private locale: LocaleService,
    private eventService: EventService,
    private windowRef: WindowRefService,
    private filter: FiltersService,
    private sessionStorage: SessionStorageService,
    private eventNamePipe:EventNamePipe
  ) {

    this.animationDelay = this.timeService.animationDelay;
    this.liveLabelText = this.locale.getString('bethistory.clock.live');
    this.todayText = this.locale.getString('bethistory.today');
    this.componentId = _.uniqueId();
  }

  ngOnInit(): void {
    this.setSuspendedEventStatus();
    this.eventStartedOrLive = (this.event.isStarted || this.event.eventIsLive) && !this.event.isResulted;
    this.isResultedMatch = this.result !== '-';
    this.isFootball = this.event.categoryCode === 'FOOTBALL';
    this.isTennis = this.event.categoryCode === 'TENNIS';
    this.isEventHasCurrentPoints = this.event.comments && this.event.comments.teams &&
      this.coreTools.hasOwnDeepProperty(this.event.comments, 'teams.home.currentPoints') &&
      this.event.comments.teams.home.currentPoints !== null;
    this.isEventMatch = this.event.eventSortCode === 'MTCH';
    this.eventName = this.getEventName();
    this.setPlaceWithFormat(this.place);
    this.init();
  }

  ngOnChanges(changes: SimpleChanges): void {
    const matchTimeChanged = changes.matchTime && !changes.matchTime.firstChange,
      runningSetIndexChanged = changes.runningSetIndex && !changes.runningSetIndex.firstChange,
      statusChanged = changes.status && !changes.status.firstChange;

    if (statusChanged) {
      this.setSuspendedEventStatus();
    }

    if (matchTimeChanged || runningSetIndexChanged) {
      this.updateMatchTimerLabel();
      this.updateSession();
      this.sessionStorage.set('bs-time', this.timerLabel);
    }
  }

  ngOnDestroy(): void {
    this.windowRef.nativeWindow.clearTimeout(this.animationClassesRemoval);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Checks if match clock is available
   * @returns {boolean}
   * @private
   */
  get isMatchClock(): boolean {
    return this.event.clock && this.event.clock.matchTime && !this.isHalfOrFullTime;
  }
set isMatchClock(value:boolean){}
  /**
   * Checks if match time is half or full time
   * @returns {boolean}
   * @private
   */
  get isHalfOrFullTime(): boolean {
    const clock = this.event.clock;
    return clock && (clock.matchTime === 'HT' || clock.matchTime === 'FT');
  }
set isHalfOrFullTime(value:boolean){}
  /**
   * Check if to show live label
   * @return {Boolean}
   */
  get isLiveLabelShown(): boolean {
    return !this.event.isResulted && this.timerLabel === this.liveLabelText;
  }
set isLiveLabelShown(value:boolean){}
  /**
   * Check if to show stream label
   * @return {Boolean}
   */
  get isStreamLabelShown(): boolean {
    const liveStreamAvailable = this.eventService.isLiveStreamAvailable(this.event).liveStreamAvailable;
    return liveStreamAvailable;
  }
set isStreamLabelShown(value:boolean){}
  /**
   * Check if to show other label
   * @return {Boolean}
   */
  get isLabelShown(): boolean {
    return !!this.timerLabel && this.timerLabel !== this.liveLabelText;
  }
set isLabelShown(value:boolean){}
  get hasScores(): boolean {
    const event: ISportEvent = this.event;
    const teams: ITeams = event && event.comments && event.comments.teams;
    if (!teams) { return false; }

    const homeScore: string | number = teams.home && teams.home.score;
    const awayScore: string | number = teams.away && teams.away.score;

    return Boolean((homeScore || homeScore === 0) || (awayScore || awayScore === 0));
  }
set hasScores(value:boolean){}
  /**
   * return event name depending on event type
   * @return {String}
   */
  getEventName(): string {
    const {isHorseRacing, isGreyHound} = this.getSportType();
    const isRacingSport = isHorseRacing || isGreyHound;
    let eventName = this.event.name;

    if (isRacingSport) {
      eventName =  this.event.originalName || this.event.name;
    } else if (this.checkForHorse(this.event)) {
      eventName = this.checkForHorse(this.event) && this.event.originalName ?
                  `${this.event.localTime} ${this.event.name}` : `${this.event.name}`;
    }
    return eventName;
  }

  private checkForHorse(event: ISportEvent): boolean {
    const eventId = ['39'];
    return eventId.includes(event.categoryId);
  }

  /**
   * Set correct place format
   * @return {void}
   * @param place
   */
  private setPlaceWithFormat(place: string): void {
    this.placeWithFormat = `${place}${this.coreTools.getDaySuffix(place)} Place`;
  }

  private setSuspendedEventStatus(): void {
    this.isSuspendedEvent = this.status === 'suspended';
  }

  /**
   * Init function for(callbacks, watchers, scope destroying)
   * @private
   */
  private init(): void {
    // set event name
    this.event.name = this.event.nameOverride || this.event.name;

    this.setStartTime();

    this.updateMatchTimerLabel();
    this.updateSession();
    this.sessionStorage.set('bs-time', this.timerLabel);
  }
  /**
   * Format startTime for event
   * @private
   */
  private setStartTime(): void {
    this.startTime = new Date(this.event.startTime);
  }

  /**
   * Assign timer label to identify when event starts( LIVE, Live Clock, Today hours or Date)
   * @private
   */
  private updateMatchTimerLabel(): void {
    // show tennis set
    if (this.event.comments && this.event.comments.runningSetIndex) {
      const runningSetIndex = this.event.comments.runningSetIndex;
      const numberSuffix = this.locale.getString(this.filter.numberSuffix(runningSetIndex));
      this.timerLabel = `${runningSetIndex}${numberSuffix} ${this.locale.getString('sb.tennisSet')}`;
      this.isLiveEvent = true;
      return;
    }

    // if clock is available - no label
    if (this.isMatchClock) {
      this.timerLabel = '';
      this.isLiveEvent = true;
      return;
    }

    // show half or full time
    if (this.isHalfOrFullTime) {
      this.timerLabel = this.event.clock.matchTime;
      this.isLiveEvent = true;
      return;
    }

    // show live label
    if (this.eventStartedOrLive && !this.isHalfOrFullTime) {
      this.timerLabel = this.liveLabelText;
      this.isLiveEvent = true;
      return;
    }

    // show full time
    if (this.result !== '-' && this.isEventMatch && !this.isSpecial) {
      this.timerLabel = this.isFootball
        ? this.locale.getString('bethistory.clock.footballFT') : '';
      this.isLiveEvent = false;
      return;
    }

    // show event time
    if (!this.eventStartedOrLive) {
      this.timerLabel = this.timeService.getEventTime(`${this.startTime}`);
      this.isLiveEvent = false;
      return;
    }

    this.timerLabel = '';
    this.isLiveEvent = false;
  }

  /**
   * Return object with boolean types of sport
   * @private
   */
  private getSportType(): {[type: string]: boolean} {
    const eventClassId = this.event.classId && this.event.classId.toString();
    const eventCategoryId = this.event.categoryId;
    const sportsRacingConf = this.CATEGORIES_DATA.racing;
    return {
      isHorseRacing: horseracingConfig.config.request.categoryId === eventCategoryId,
      isGreyHound  : greyhoundConfig.config.request.categoryId === eventCategoryId,
      isVirtualHorseRacing: sportsRacingConf.virtualHorseRacing.id === eventCategoryId &&
              sportsRacingConf.virtualHorseRacing.specialsClassIds === eventClassId,
      isVirtualGreyHound: sportsRacingConf.virtualGreyhound.id === eventCategoryId &&
              sportsRacingConf.virtualGreyhound.specialsClassIds === eventClassId,
    };
  }

  updateSession() {
    this.sessionData = this.sessionStorage.get('betDetailsToShare');
    if(!this.sessionData) {
      return;
    }
    this.sessionData[this.event.id+'-'+this.id+'-'+ this.outcomeId].time=this.event.clock ? this.event.clock.liveTime :  this.isLabelShown && this.timerLabel;
    const eventName = this.legType === 'E' && this.place ? `${this.eventName} ${this.placeWithFormat}`: this.eventName ;
    this.sessionData[this.event.id+'-'+this.id+'-'+ this.outcomeId].eventName = this.eventNamePipe.transform(eventName);
    this.sessionData[this.event.id+'-'+this.id+'-'+ this.outcomeId].id = this.id
    this.sessionStorage.set('betDetailsToShare',this.sessionData);
  }
}
