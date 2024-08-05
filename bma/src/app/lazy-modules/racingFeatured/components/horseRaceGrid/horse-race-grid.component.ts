import * as _ from 'underscore';
import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IClassTypeName, IRaceGridMeeting } from '@core/models/race-grid-meeting.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRacingGroup } from '@racing/models/racing-ga.model';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { DRILLDOWNTAGNAMES } from '@promotions/constants/tag-names-config.constant';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IMarket } from '@core/models/market.model';
import { NEXT_RACES_HOME_CONSTANTS } from '@app/lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';
import { DeviceService } from '@core/services/device/device.service';
@Component({
  selector: 'horse-race-grid',
  templateUrl: './horse-race-grid.component.html'
})

export class HorseRaceGridComponent implements OnInit, OnChanges {
  @Input() raceType: string;
  @Input() eventsData: IRaceGridMeeting; // or & IRaceGridMeetingTote[] (lacks classesTypeNames)?
  @Input() eventsOrder: string[];
  @Input() racingGroup: ISportEvent[];
  @Input() racingGroupFlag: string;
  @Input() sportName: string;
  @Input() showSwitcher?: boolean = true;
  @Input() filterDay?: string;
  @Input() groupFlagText?: string;
  @Input() isEventOverlay?: boolean;
  @Input() showSignPost: boolean = false;
  groupedRaces: IRacingGroup[] = [];
  switchers: ISwitcherConfig[] = [];
  isHR: boolean;
  filter: string;
  public isMobile: boolean;
  public isDesktop: boolean;
  
  constructor(
    private locale: LocaleService,
    private lpAvailabilityService: LpAvailabilityService,
    private racingGaService: RacingGaService,
    protected routingHelperService: RoutingHelperService,
    protected racingService: RacingService,
    protected pubsub: PubSubService,
    protected gtmService: GtmService,
    public deviceService: DeviceService
  ) {  }

  ngOnInit(): void {
    this.createSwitchers();
    this.filter = this.filterDay ? this.filterDay : this.switchers.length && this.switchers[0].viewByFilters;
    this.validateRacesForToday();
    this.getRacesForDay(this.eventsData);
    this.filterResultedEvents();
    this.isMobile = this.deviceService.isMobile;
    this.isDesktop = this.deviceService.isDesktop;
  }

  ngOnChanges(changes: SimpleChanges): void {
    const eventsData = changes && changes.eventsData && changes.eventsData.currentValue;
    if (eventsData) {
      this.eventsData = eventsData;
      this.ngOnInit();
    }
  }

  /**
   * Check if Live Price available
   * @param {Object} event
   * @returns {Boolean}
   */
  isLpAvailable(event: ISportEvent): boolean {
    return this.lpAvailabilityService.check(event);
  }

  /**
   * #OZONE-8265 Story
   * displays the early price sign post
   * Horse racing - Only tommorow && not resulted && not race off && lpAvailable
   * GreyHound - only today and tommorow and not resulted && not race off && lpAvailable
   * @param - events
   * @return - boolean
   */
  isEarlyPricesAvailable(events: ISportEvent[]): boolean {
    const checkIsDayValue = events.every((event) => this.raceType === 'horseracing' ?  (event.correctedDayValue  !== 'racing.today' ) : true);
    const isLpAvailable = events.filter((event) => {
      if (event.isStarted || event.isLiveNowEvent || event.isResulted || event.rawIsOffCode === 'Y') {
        return false;
      }
      return event.markets.some(market => market.isLpAvailable);
    });
    return (checkIsDayValue  && isLpAvailable.length > 0);
  }
 
  /**
   * #OZONE-8265 Story
   * align early price sign post when first event is resulted      
   * @param - events
   * @return - boolean
   */
  hasResult(events: ISportEvent[]): boolean {
    return events[0].isResulted || events[0].rawIsOffCode === 'Y' ? true  : false;
  }

  /**
   * #OZONE-8265 Story
   * get early price sign post title from locale    
   * @param - none
   * @return - string
   */
  earlySignPostTitle(): string {
    return this.locale.getString(`sb.earlyPricesAvailable`);
  }


  /**
   * Generate URL for event details page or results page
   * @param {string} eventEntity
   */
  genEventDetailsUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }

  /*
   * TODO before here was also check `&& this.ocLazyLoad.isLoaded('uktote')`
   */
  showUKToteIndicators(): boolean {
    return this.racingGroupFlag === 'UK';
  }

  trackByGroupName(index: number, group: IRacingGroup): string {
    return `${index}${group.groupName}${group.events[0].id}`;
  }

  trackById(index: number, event: ISportEvent): number {
    return event.id;
  }

  /**
   * Ga track day switch
   * @param day
   */
  trackSwitchDayEvent(day: string): void {
    this.racingGaService.trackEvent({
      eventCategory: this.sportName,
      eventAction: this.locale.getString(`sb.flag${this.racingGroupFlag}`),
      eventLabel: this.locale.getString(day)
    });
  }

  /**
   * Create day switchers
   */
  protected createSwitchers(): void {
    const uniqDays = _.chain(this.racingGroup)
      .sortBy('startTime')
      .pluck('correctedDayValue')
      .uniq()
      .value();

    this.switchers = [];
    this.isHR = this.raceType === 'horseracing';
    _.each(uniqDays, (day: string) => {
      this.switchers.push({
        name: day,
        onClick: () => this.selectDay(day),
        viewByFilters: day
      });
    });

    if (this.racingGroupFlag === 'VR') {
      this.switchers = this.switchers.slice(0, 2);
    }
  }

  /**
   * Check today races and map filter accordingly
   */
  protected validateRacesForToday(): void {
    if(this.showSwitcher){
      this.filter = this.racingService.validateRacesForToday(this.racingGroup, this.filter, this.switchers);
    }
  }

  /**
   * Create groups of filtered and sorted races
   */
  protected getRacesForDay(eventsData: IRaceGridMeeting): void {
    let classes: IClassTypeName[]; // TODO cuz of `typeDisplayOrder` prop - should it be IRaceGridMeetingTote[] ???

    this.groupedRaces = [];
    const sortedGroupedRaces = [];
    let activeGroupedRaces = [];

    classes = (eventsData.classesTypeNames[this.racingGroupFlag] && eventsData.classesTypeNames[this.racingGroupFlag].length) ?
      [...eventsData.classesTypeNames[this.racingGroupFlag]].sort(this.compareFunction('name')) : [];
    classes = classes.sort(this.compareFunction('typeDisplayOrder'));
    classes.forEach((meeting: IClassTypeName) => {
      const filteredRaces = this.getFilteredRacesGroup(meeting);
      if (filteredRaces.length) {
        const sortedRacesGroup = this.sortRacesGroup(filteredRaces);
        const activeEvent = this.racingService.getFirstActiveEventFromGroup(sortedRacesGroup, this.racingGroupFlag);
        const streamPresented = this.isStreamPresented(sortedRacesGroup);
        const cashoutPresented = this.isCashoutPresented(sortedRacesGroup);
        const bogPresented = this.isHR && this.isBogPresented(sortedRacesGroup);
        const isHeaderBIRAvailable = this.isHR && this.isBIRSignpostPresented(sortedRacesGroup);

        const groupedRace = {
          groupName: sortedRacesGroup[0].typeName,
          liveStreamAvailable: streamPresented,
          cashoutAvailable: cashoutPresented,
          events: sortedRacesGroup,
          bogAvailable: bogPresented,
          isHeaderBIRAvailable
        };
        if (activeEvent) {
          activeGroupedRaces.push({
            ...groupedRace,
            typeDisplayOrder: meeting.typeDisplayOrder
          });
        }
        sortedGroupedRaces.push(groupedRace);
      }
    });
    activeGroupedRaces = this.sortActiveGroupedRaces(activeGroupedRaces);
    this.groupedRaces = this.setGroupedRacesByType(sortedGroupedRaces, activeGroupedRaces);
  }

  protected filterResultedEvents(): void {
    const indexes = this.getIndexesOfResultedEvents();
    const arrLength = this.groupedRaces.length;
    if (arrLength > 1) {
      this.sortEvents(this.groupedRaces, indexes);
    }
  }

  /**
   * Get group of racing filtered by meeting and filter property
   * @param meeting
   */
  private getFilteredRacesGroup(meeting: IClassTypeName): ISportEvent[] {
    return this.racingGroup.filter((race: ISportEvent) => {
      return ((race.typeName === meeting.name) && (race.correctedDayValue === this.filter));
    });
  }

  /**
   * Sort racing group by eventsOrder
   * @param racingGroup
   */
  private sortRacesGroup(racingGroup: ISportEvent[]): ISportEvent[] {
    return _.sortBy(racingGroup, (race: ISportEvent) => {
      return _.reduce(this.eventsOrder, (res, field) => {
        return `${res}_${race[field]}`;
      }, '');
    });
  }

  /**
   * Checks if at least one event of group has liveStream available
   * @param {ISportEvent[]} races
   * @returns {boolean}
   */
  private isStreamPresented(races: ISportEvent[]): boolean {
    return _.some(races, (race: ISportEvent) => race.liveStreamAvailable);
  }

  /**
   * Checks if at least one event of group has isGpAvailable true
   * @param {ISportEvent[]} races
   * @returns {boolean}
   */
  private isBogPresented(races: ISportEvent[]): boolean {
    return races.some((race: ISportEvent): boolean => {
        return !!race.effectiveGpStartTime && new Date().getTime() >= new Date(race.effectiveGpStartTime).getTime() && race.markets.some((market: IMarket) => market.isGpAvailable);
    });
  }

  /**
   * Checks if at least one event of group has cashout available
   * @param {ISportEvent[]} races
   * @returns {boolean}
   */
  private isCashoutPresented(races: ISportEvent[]): boolean {
    return _.some(races, (race: ISportEvent) => race.cashoutAvail === 'Y');
  }

    /**
   * Checks if at least one event of group has inplay signpost available
   * @param {ISportEvent[]} races
   * @returns {boolean}
   */
     private isBIRSignpostPresented(races: ISportEvent[]): boolean {
      return races.some((race: ISportEvent) => race.drilldownTagNames?.split(',').includes(DRILLDOWNTAGNAMES.HR_BIR));
    }

  /**
   * Select day on race grid
   * @param day
   * @private
   */
  private selectDay(day: string): void {
    this.filter = day;
    this.getRacesForDay(this.eventsData);
    this.filterResultedEvents();
    this.trackSwitchDayEvent(day);
  }

  /**
   * Get indexes of events which are resulted
   * @private
   */
  private getIndexesOfResultedEvents(): number[] {
    return this.groupedRaces.map((el: IRacingGroup) => this.checkIfEventIsResulted(el)).filter((el: number | null) => el !== null);
  }

  /**
   * Move resulted events to the end
   * @private
   * @param {IRacingGroup[]} arr Array to be modified
   * @param {number[]} indexes Array of indexes of resulted events
   */
  private sortEvents(arr: IRacingGroup[], indexes: number[]): void {
    const arrLength: number = arr.length - 1;
    let counter: number = 0;

    for (let i = arrLength; i >= 0; i--) {
      if (indexes.indexOf(i) > -1) {
        const elem: IRacingGroup = arr[i],
          indexToMove: number = arrLength - counter;

        arr.splice(i, 1);
        arr.splice(indexToMove, 0, elem);
        counter++;
      }
    }
  }

  /**
   * Check if event is resulted
   * @private
   * @param {IRacingGroup} el Passed event
   * @returns {number|null}
   */
  private checkIfEventIsResulted(el: IRacingGroup): number | null {
    const isResulted = el.events.every((elem: ISportEvent) => elem.isResulted);
    return isResulted ? this.groupedRaces.indexOf(el) : null;
  }

  /**
   * Sort Meetings and remove display order
   * @param {IRacingGroup[]} events
   */
  private sortMeetings(events: IRacingGroup[]): IRacingGroup[] {
    const sortedMeetings = [...events].sort(this.compareFunction('typeDisplayOrder'));
    return sortedMeetings.map((meeting: IRacingGroup) => {
      delete meeting.typeDisplayOrder;
      return meeting;
    });
  }

  /**
   * Sort Active Grouped races based on groupname and typeDisplayOrder
   * @param {IRacingGroup[]} activeGroupedRaces
   */
  private sortActiveGroupedRaces(activeGroupedRaces: IRacingGroup[]): IRacingGroup[] {
    activeGroupedRaces = activeGroupedRaces.length ? [...activeGroupedRaces].sort(this.compareFunction('groupName')) : [];
    return this.sortMeetings(activeGroupedRaces);
  }

  /**
   * Set grouped races based on type
   * @param {IRacingGroup[]} sortedGroupedRaces
   * @param {IRacingGroup[]} activeGroupedRaces
   * @returns {IRacingGroup[]}
   */
  private setGroupedRacesByType(sortedGroupedRaces: IRacingGroup[], activeGroupedRaces: IRacingGroup[]): IRacingGroup[] {
    let groupedRaces = [];
    if (this.raceType === 'horseracing') {
      [...activeGroupedRaces, ...sortedGroupedRaces].forEach((race: IRacingGroup) => {
          if (groupedRaces.length) {
            const index = groupedRaces.findIndex((group) => group.groupName === race.groupName);
            if (index === -1) {
              groupedRaces.push(race);
            }
          } else {
            groupedRaces.push(race);
          }
        });
    } else {
      groupedRaces = sortedGroupedRaces;
    }
    return groupedRaces;
  }

  /**
   * To sort the array of objects based on compareValue
   * @param {string} compareValue
   */
  private compareFunction(compareValue: string):
    (a: IRacingGroup | IClassTypeName, b: IRacingGroup | IClassTypeName) => number {
    return (a: IRacingGroup | IClassTypeName, b: IRacingGroup | IClassTypeName): number => {
      if (a[compareValue] > b[compareValue]) {
        return 1;
      } else if (b[compareValue] > a[compareValue]) {
        return -1;
      } else {
        return 0;
      }
    };
  }

  overlayMenuClose(event) {
    if(!this.showSwitcher) {
      if(event) { 
        this.eventRacesGATracker(event);
      }
      this.pubsub.publish('MEETING_OVERLAY_FLAG',{id:event?.id,flag: false});
    }
  }

  eventRacesGATracker(event: ISportEvent) {
    this.gtmService.push('trackEvent', {    
        eventAction: 'meetings',
        eventCategory: event.categoryId == '21' ? NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE,
        eventLabel: `navigation – ${this.groupFlagText.toLowerCase()}`,
        categoryID: event.categoryId,
        typeID: event.typeId,
        eventID: event.id
      });
  } 

}
