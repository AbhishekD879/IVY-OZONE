import { Component, Output, EventEmitter, Input, OnChanges, ViewEncapsulation, OnDestroy, SimpleChanges } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router } from '@angular/router';

import * as _ from 'underscore';

@Component({
  selector: 'build-race-card',
  templateUrl: 'build-race-card.component.html',
  styleUrls: ['build-race-card.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class BuildRaceCardComponent implements OnChanges, OnDestroy {
  @Input() cardIdObj: { id: string };
  @Output() readonly updatedState = new EventEmitter<boolean>();
  @Output() readonly updatedLimitState = new EventEmitter<boolean>();
  @Output() readonly clearBuildCardState = new EventEmitter<boolean>();

  cardIds = [];
  isEnabledCardState: boolean = false;
  cardState = {
    isLimitReached: false,
    eventsList: undefined
  };

  isBuildCardButtonActive: boolean;

  constructor(
    private router: Router,
    private pubsubService: PubSubService
    ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.cardIdObj && this.cardIdObj) {
      // TODO: need to investigate this logic. It looks strange
      this.toggle(this.cardIdObj.id);
    }
  }

  ngOnDestroy(): void {
    this.cardIds = [];
    this.isEnabledCardState = false;
    this.updatedState && this.updatedState.emit(this.isEnabledCardState);
  }

  /**
   * toggle card ids
   * @param {Number} id
   */
  toggle(id: string): void {
    const cardIdIndex = this.cardIds.indexOf(id);
    if (cardIdIndex > -1) {
      this.cardIds.splice(cardIdIndex, 1);
    } else {
      this.sendGTM('select race');
      this.cardIds.push(id);
    }
    this.cardState.isLimitReached = this.cardIds.length >= 10;
    this.clearBuildCardState && this.clearBuildCardState.emit(false);
    this.updatedLimitState && this.updatedLimitState.emit(this.cardState.isLimitReached);
    this.isBuildCardButtonActive = this.cardIds.length >= 1;
  }

  /**
   * Toggle card state
   */
  toggleBuildCardState(): void {
    this.isEnabledCardState = !this.isEnabledCardState;
    const eventLabel = this.isEnabledCardState ? 'create' : 'close';
    this.sendGTM(eventLabel);
    this.clearBuildCard();
    this.updatedState && this.updatedState.emit(this.isEnabledCardState);
  }

  /**
   * Clear card ids
   */
  clearBuildCard(): void {
    this.cardState.isLimitReached = false;
    this.isBuildCardButtonActive = false;
    this.cardIds = [];
    this.updatedLimitState && this.updatedLimitState.emit(this.cardState.isLimitReached);
    this.clearBuildCardState && this.clearBuildCardState.emit(true);
    this.cardState.eventsList = undefined;
  }

  /**
   * Build card, redirect to build card page
   */
  buildCard(): void {
    if (!_.isEmpty(this.cardIds)) {
      const path = `/horse-racing/build-your-own-race-card/${this.cardIds}`;
      this.router.navigateByUrl(path);
    }
  }

  private sendGTM(eventLabel: string): void {
    this.pubsubService.publish(this.pubsubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'build race card',
      eventLabel
    }]);
  }
}
