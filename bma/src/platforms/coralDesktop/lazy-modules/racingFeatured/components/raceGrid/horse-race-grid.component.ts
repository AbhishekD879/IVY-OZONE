import {
  Component,
  OnInit,
  Input,
  EventEmitter,
  Output,
  OnChanges,
  SimpleChanges,
  ViewEncapsulation,
  OnDestroy
} from '@angular/core';
import { HorseRaceGridComponent } from '@app/lazy-modules/racingFeatured/components/horseRaceGrid/horse-race-grid.component';
import { LocaleService } from '@core/services/locale/locale.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import * as _ from 'underscore';
import { IRacingEvent } from '@app/core/models/racing-event.model';
import { IRacingGroup } from '@app/racing/models/racing-ga.model';
import { IConstant } from '@app/core/services/models/constant.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'horse-race-grid',
  templateUrl: 'horse-race-grid.component.html',
  styleUrls: ['horse-race-grid.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class DesktopHorseRaceGridComponent extends HorseRaceGridComponent implements OnInit, OnChanges, OnDestroy {
  @Input() isEnabledCardState: boolean;
  @Input() isLimitReached: boolean;
  @Input() isClearBuildCardState: boolean;
  @Input() isEventOverlay?: boolean;
  @Output() readonly toogleCheckBox = new EventEmitter<{id: string}>();


  cardState: IConstant;

  constructor(localeService: LocaleService,
              private localeServicePublic: LocaleService,
              lpAvailabilityService: LpAvailabilityService,
              racingGaService: RacingGaService,
              private racingGaServicePublic: RacingGaService,
              routingHelperService: RoutingHelperService,
              protected racingService: RacingService,
              protected pubsub: PubSubService,
              gtmService: GtmService,
              public deviceService: DeviceService) {
    super(localeService, lpAvailabilityService, racingGaService,
      routingHelperService, racingService, pubsub, gtmService,deviceService);
  }

  ngOnInit(): void {
    super.ngOnInit();
    // card state from parent controller
    this.cardState = this.isHR ? {
      eventsList: this.generateEventList()
    } : this.cardState;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.isClearBuildCardState && changes.isClearBuildCardState.currentValue) {
      this.cardState.eventsList = this.generateEventList();
    }
  }

  ngOnDestroy(): void {
    if (this.cardState) {
      this.cardState.eventsList = {};
    }
    this.isEnabledCardState = false;
    this.isLimitReached = false;
  }

  isRaceOffOrResulted(event: ISportEvent): boolean {
    return (event.isStarted || event.isLiveNowEvent || event.isResulted) as boolean;
  }

  /**
   * On checkbox change
   * Triggers parent controller function toggle
   * @param id
   */
  toggle(id: string): void {
    this.toogleCheckBox.emit({id});
    const cardIdState = this.cardState.eventsList[id];
    if (!cardIdState) {
      this.cardState.eventsList[id] = true;
    } else {
      this.cardState.eventsList[id] = false;
    }
  }

  generateEventList(): IConstant {
    const eventsList: IConstant = {};
    _.each(this.groupedRaces, (racesGroup: IRacingGroup) => {
      _.each(racesGroup.events, (event: IRacingEvent) => {
        eventsList[event.id] = false;
      });
    });
    return eventsList;
  }

  /**
   * Ga track day switch
   * @param day
   * @private
   */
  trackSwitchDayEvent(day) {
    const eventAction = this.isEnabledCardState && this.racingGroupFlag !== 'VR'
      ? 'build race card' : this.localeServicePublic.getString(`sb.flag${this.racingGroupFlag}`);
    this.racingGaServicePublic.trackEvent({
      eventCategory: this.sportName,
      eventAction,
      eventLabel: this.localeServicePublic.getString(day)
    });
  }
}
