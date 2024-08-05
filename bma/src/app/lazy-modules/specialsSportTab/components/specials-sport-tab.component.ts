import { Component, Input, OnInit, OnDestroy } from '@angular/core';

import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { from, Observable, Subscription } from 'rxjs';
import { GamingService } from '@core/services/sport/gaming.service';

@Component({
  selector: 'specials-sport-tab',
  templateUrl: 'specials-sport-tab.component.html'
})
export class SpecialsSportTabComponent implements OnInit, OnDestroy {
  @Input() sport: GamingService;
  @Input() display: string;

  eventsBySections: ITypeSegment[] = [];
  isExpanded: boolean[] = [];
  isResponseError: boolean = false;
  isLoaded: boolean = false;
  private loadSubscription: Subscription;
  private readonly COMPONENT_NAME: string = 'SpecialsSportTabComponent';

  constructor(
    private sportTabsService: SportTabsService,
    private pubsubService: PubSubService
  ) {}

  ngOnInit(): void {
    this.isExpanded[0] = true;

    this.loadSpecialsData();

    this.pubsubService.subscribe(this.COMPONENT_NAME, this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.sportTabsService.deleteEvent(eventId, this.eventsBySections);
    });
  }

  ngOnDestroy(): void {
    // unSubscribe LS Updates via WS
    this.sport.unSubscribeLPForUpdates();
    this.pubsubService.unsubscribe(this.COMPONENT_NAME);
    this.loadSubscription && this.loadSubscription.unsubscribe();
  }

  isEnhancedMultiplesSection(sportSection: ITypeSegment): boolean {
    return sportSection.events.length > 0 && sportSection.typeName === 'Enhanced Multiples';
  }

  trackByTypeId(index: number, sportSection: ITypeSegment): string {
    return sportSection.typeId;
  }

  trackById(index: number, sportEvent: ISportEvent): number {
    return sportEvent.id;
  }

  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Load Sport Specials Data
   */
  public loadSpecialsData(): void {
    this.isLoaded = false;
    this.isResponseError = false;
    const specialLoader$: Observable<ISportEvent[]> = from(this.sport.getByTab(this.display));
    this.loadSubscription = specialLoader$.subscribe((events: ISportEvent[]) => {
      this.eventsBySections = events && events.length ? this.sportTabsService.eventsBySections(events, this.sport) : [];
      this.isLoaded = true;
      this.isResponseError = false;
      // Subscribe LS Updates via PUSH updates! unSubscribe will be automatically invoked on next subscribe!
      this.sport.subscribeLPForUpdates(events);
    }, (error) => {
      this.isLoaded = true;
      this.isResponseError = true;
      console.warn('Specials Data:', error && error.error || error);
    });
  }
}
