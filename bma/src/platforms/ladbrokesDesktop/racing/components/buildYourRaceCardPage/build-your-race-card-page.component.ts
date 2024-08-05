import { Component, OnInit, OnDestroy } from '@angular/core';
import { BuildYourRaceCardPageService } from '@ladbrokesDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ISportEvent } from '@core/models/sport-event.model';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { from, Subscription } from 'rxjs';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { HRTabs } from '@app/lazy-modules/racingFeatured/components/racingFeatured/constant';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { IDelta } from '@app/core/models/delta-object.model';


@Component({
  selector: 'build-your-race-card-page',
  templateUrl: 'build-your-race-card-page.component.html'
})
export class BuildYourRaceCardPageComponent implements OnInit, OnDestroy {
  events: ISportEvent[];
  eventsIds: string;
  sport: string = 'horseracing';
  racingDefaultPath: string;
  readonly HR_TABS = HRTabs;
  activeUserTab = this.HR_TABS.MARKETS;
  delta: IDelta;

  protected eventsSubscription: Subscription;
  
  private editMyAccaUnsavedOnEdp: boolean;
  private readonly tagName = 'BuildYourRaceCardPage';

  constructor(
    private buildYourRaceCardPageService: BuildYourRaceCardPageService,
    private routingState: RoutingState,
    private route: ActivatedRoute,
    private router: Router,
    private routingHelperService: RoutingHelperService,
    private pubSubService: PubSubService
  ) {
  }

  ngOnInit(): void {
    this.routingHelperService.formSportUrl('horseracing', 'featured').subscribe((url: string) => {
      this.racingDefaultPath = url;
    });
    this.eventsIds = this.routingState.getRouteParam('ids', this.route.snapshot);
    this.eventsSubscription = from(this.buildYourRaceCardPageService.getEvents(this.eventsIds))
    .subscribe((events: ISportEvent[]) => {
      // Subscription from liveServe PUSH updates
      this.buildYourRaceCardPageService.subscribeForUpdates(events);
      this.events = events;
    });
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EMA_UNSAVED_ON_EDP, (unsaved: boolean) => {
      this.editMyAccaUnsavedOnEdp = unsaved;
    });
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT, (updateEventId: string, delta: IDelta) => {
      if (delta.originalName === 'Win or Each Way') {
        this.events?.forEach((event: ISportEvent) => {
          if(updateEventId.toString() === event.id.toString()) {
            event.delta = delta;
            event.delta.updateEventId = updateEventId;
          }
        });
      }
    });
  }
  /**
   * Check for market with antepost flag
   * @param event
   * @return {boolean}
   */
  isAntepostMarket(event): boolean {
    return event &&
      event.markets &&
      event.markets[0] &&
      event.markets[0].isAntepost === 'true';
  }

  trackById(index: number, event: ISportEvent): string {
    return `${index}${event.id}`;
  }

  ngOnDestroy(): void {
    // unSubscription from liveServe PUSH updates
    this.eventsSubscription && this.eventsSubscription.unsubscribe();
    this.buildYourRaceCardPageService.unSubscribeForUpdates();
  }

  goToDefaultPage(): void {
    this.router.navigateByUrl(this.racingDefaultPath);
  }

  /**
   * process the updates from racing mybets
   * @param {ILazyComponentOutput} event 
   */
  handleRacingMybetsUpdates(event: ILazyComponentOutput): void {
    if (event.output === 'tabUpdated') {
      this.activeUserTab = event.value;
    }
  }

  /**
   * Check if edit my acca is in progress for changing route
   * @returns {boolean}
   */
  canChangeRoute(): boolean {
    this.pubSubService.publish(this.pubSubService.API.ROUTE_CHANGE_STATUS, !this.editMyAccaUnsavedOnEdp);
    return !this.editMyAccaUnsavedOnEdp;
  }

  /**
  * open edit my acca pop-up if edit is in progress while changing route
  */
  onChangeRoute(): void {
    this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  }

  /**
   * Click on Horse Block.
   *
   * Toggle Horse Information Area.
   *
   * param {array} summary of expanded and collapsed areas.
   * param {number} market index.
   * param {number} outcome index.
   *
   */
  onExpand(expandedSummary, mIndex, oIndex) {
    const temp = !expandedSummary[mIndex][oIndex];

    for (let i = 0; i < expandedSummary[mIndex].length; i++) {
      expandedSummary[mIndex][i] = false;
    }

    expandedSummary[mIndex][oIndex] = temp;
  }
}
