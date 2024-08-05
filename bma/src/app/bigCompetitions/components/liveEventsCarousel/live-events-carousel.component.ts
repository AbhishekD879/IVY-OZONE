import { Component, Input, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplaySubscriptionService } from '../../services/inplaySubscription/inplay-subscription-service';
import { ParticipantsService } from '../../services/participants/participants.service';
import { IConstant } from '@core/services/models/constant.model';
import { IBigCompetitionSportEvent } from '../../models/big-competitions.model';
import { BigCompetitionsService } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'live-events-carousel',
  templateUrl: 'live-events-carousel.component.html'
})
export class LiveEventsCarouselComponent implements OnInit, OnDestroy {
  @Input() carouselId: string;
  @Input() categoryId: number;
  @Input() typeId: number;

  events: IBigCompetitionSportEvent[] = [];
  name: string;

  constructor(private pubSubService: PubSubService,
              private inplaySubscriptionService: InplaySubscriptionService,
              private participantsService: ParticipantsService,
              private bigCompetitionsService: BigCompetitionsService,
              private changeDetectorRef: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.name = `liveCarousel-${this.carouselId}`;
    this.loadCompetitionEvents();
    // Add event which become inplay from next events list
    this.pubSubService.subscribe(this.name, this.pubSubService.API.MOVE_EVENT_TO_INPLAY, event => {
        const index: number = this.getEventIndex(event.id);
        const uniqueId: boolean = index === -1;

        if (uniqueId && (+event.typeId === +this.typeId)) {
          this.events = [...this.events, event];
          this.bigCompetitionsService.addOutcomeMeaningMinorCode(this.events);
          this.inplaySubscriptionService.subscribeForLiveUpdates([event.id]);
          this.events = [...this.events];
          this.changeDetectorRef.markForCheck();
        }
    });
  }
  ngOnDestroy(): void {
    const eventIds: string[] = this.getEventIds() as string[];

    if (eventIds.length) {
      this.inplaySubscriptionService.unsubscribeForLiveUpdates(eventIds);
    }

    this.pubSubService.unsubscribe(this.name);
  }

  /**
   * Load competition events from InPlay MS(inplay/upcoming)
   * @private
   */
  private loadCompetitionEvents(): void {
    this.inplaySubscriptionService.loadCompetitionEvents(true, this.categoryId, this.typeId, false)
      .then((events: IBigCompetitionSportEvent[]) => {
          if (events && events.length) {
            this.events = this.getEventsWithParticipants(events);
            this.addLiveUpdatesHandler();
            this.changeDetectorRef.markForCheck();
          }
        });
  }

  /**
   * Add listener for live updates
   * @private
   */
  private addLiveUpdatesHandler(): void {
    const eventIds = this.getEventIds() as string[];

    this.pubSubService.subscribe(this.name, this.pubSubService.API.WS_EVENT_LIVE_UPDATE, (updatedItemId: number, messageBody: string) => {
      this.handleLiveUpdate(updatedItemId, messageBody);
    });

    this.pubSubService.subscribe(this.name, this.pubSubService.API.WS_EVENT_DELETE, (cacheData: IConstant, eventId: string) => {
      this.deleteEvent(eventId);
    });

    this.inplaySubscriptionService.subscribeForLiveUpdates(eventIds);
  }
  /**
   * Handles live updates for events.
   * @param {string} updatedItemId
   * @param {Object} messageBody
   * @private
   */
  private handleLiveUpdate(updatedItemId: number, messageBody: string): void {
    const index: number = this.getEventIndex(updatedItemId);
    const eventToUpdate: IBigCompetitionSportEvent = this.events[index];

    if (eventToUpdate) {
      this.pubSubService.publish(this.pubSubService.API.WS_EVENT_UPDATE, {
        events: [eventToUpdate],
        update: messageBody
      }, false);
      this.events = [...this.events];
      this.changeDetectorRef.markForCheck();
    }
  }

  /**
   * Deletes resulted or undisplayed event.
   * @param {number} id
   * @private
   */
  private deleteEvent(id: string): void {
    const index: number = this.getEventIndex(id);
    if (index !== -1) {
      this.events = this.events.filter((event:IBigCompetitionSportEvent, i:number) => i !== index);
      this.changeDetectorRef.markForCheck();
    }
  }

  /**
   * gets event index by id
   * @param id
   */
  private getEventIndex(id: number | string): number {
    return this.events.findIndex((event:IBigCompetitionSportEvent) => Number(event.id) === Number(id));
  }

  /**
   * returns array of event ids
   */
  private getEventIds(): number[] | string[] {
    return this.events.map((event:IBigCompetitionSportEvent) => event.id);
  }

  /**
   * returns array of events with participants property
   * @param events
   */
  private getEventsWithParticipants(events: IBigCompetitionSportEvent[]): IBigCompetitionSportEvent[] {
    return events.map((event:IBigCompetitionSportEvent) => {
      return {
        ...event,
        participants: this.participantsService.parseParticipantsFromName(event.name)
      };
    });
  }
}
