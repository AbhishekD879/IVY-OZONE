import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';

import { InplayMainService } from '@app/inPlay/services/inplayMain/inplay-main.service';
import { InplayHelperService } from '@coralDesktop/inPlay/services/inPlayHelper/inplay-helper.service';
import { UserService } from '@core/services/user/user.service';
import { IGtmEvent } from '@core/models/gtm.event.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { GamingService } from '@core/services/sport/gaming.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'in-play-sport-tab',
  templateUrl: './in-play-sport-tab.component.html',
  styleUrls: ['./in-play-sport-tab.component.scss']
})
export class InPlaySportTabComponent implements OnInit, OnDestroy, OnChanges {
  @Input() eventsBySports: ISportSegment[];
  @Input() liveStreamTab: boolean;
  @Input() gtmDataLayer: IGtmEvent;
  @Input() activeEvent: ISportEvent;
  @Input() sport: GamingService;

  @Output() readonly update: EventEmitter<ISportEvent> = new EventEmitter();

  expandedFlags: boolean[] = [true, true, true, true];
  HREvents = [];
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private inplayHelperService: InplayHelperService,
    private inplayMainService: InplayMainService,
    public userService: UserService
  ) { }

  ngOnInit(): void {
    this.gtmDataLayer = {
      eventAction: this.liveStreamTab ? 'live stream' : 'in-play',
      eventLabel: 'more markets'
    };
    if(this.eventsBySports && this.eventsBySports[0]?.events[0]?.categoryId.toString() === this.HORSE_RACING_CATEGORY_ID) {
      this.processInitialData();
    }
  }

  /**
   * set Expanded flag to manage subscription
   */
  private processInitialData(): void {
    if (this.eventsBySports) {
      this.eventsBySports.forEach((competitionSection: ISportSegment, competitionIndex: number) => {
        this.setExpandedFlag(competitionSection, competitionIndex);
      });
    }
  }

  /**
   * set Expanded flag to manage loading data when section being expanded
   */
   private setExpandedFlag(competitionSection: ISportSegment, index: number): void {     
      competitionSection.events.map((eventData :ISportEvent)=> {
        eventData.compIndex= index;
        this.HREvents.push(eventData);
      })
      this.HREvents.sort((event: ISportEvent, nextEvent: ISportEvent) => new Date(event.startTime).getTime() - new Date(nextEvent.startTime).getTime());     
  }

  ngOnDestroy(): void {
    this.eventsBySports = [];
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.expandedFlags = [true, true, true, true];
  }

  updateActiveEvent(event: ISportEvent): void {
    this.activeEvent = event;
    this.update.emit(event);
  }

  trackById(index: number, event: ISportEvent) {
    return event.id;
  }

  trackByCategoryId(index: number, typeSegment: ITypeSegment) {
    return typeSegment.categoryId;
  }

  /**
   * subscribe/unsubscribe on colapse/expand
   * @param {Array} events
   * @param {Number} index
   */
  toggleCompetitionSection(events: ISportEvent[], index: number): void {
    this.expandedFlags[index] = !this.expandedFlags[index];
    if (this.expandedFlags[index]) {
      this.inplayHelperService.subscribeForLiveUpdates(events);
    } else {
      this.inplayHelperService.unsubscribeForLiveUpdates(events);
    }
  }

  /**
   * Check if to show cashout label
   * @param {Array} events
   * @returns {Boolean}
   */
  isCashoutAvailable(events: ISportEvent[]): boolean {
    return !!this.inplayMainService.isCashoutAvailable(events);
  }
}
