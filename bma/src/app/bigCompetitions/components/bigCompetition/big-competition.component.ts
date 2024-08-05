import { finalize } from 'rxjs/operators';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { IBCData, ICompetitionModules } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import {
  BigCompetitionsLiveUpdatesService
} from '@app/bigCompetitions/services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { BigCompetitionsService } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.service';
import { ParticipantsService } from '@app/bigCompetitions/services/participants/participants.service';

import { EVENTS } from '@core/constants/websocket-events.constant';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@app/core/services/user/user.service';

@Component({
  selector: 'big-competition',
  templateUrl: 'big-competition.html',
  styleUrls: ['big-competition.component.scss']
})
export class BigCompetitionComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  activeTab: { id: string; };
  defaultTabName: string;
  activeTabName: string;
  participantsFlags: string;
  competitionName: string;
  competitionTabs: any;
  subscriptionName: string;
  competition: IBCData;
  bchPageName: string;
  brand = {brand:'Coral', device: 'Mobile'};
  public bigCompetitionBgImageUrl: string = ''; /*** Sets background image for big competition ***/
  private cmsRootUri: string = environment.CMS_ROOT_URI; /*** This is default initialisation to get domain URI ***/
  subscription2$: Subscription;
  subscription$: Subscription;
  subsPat$: Subscription;
  subscriptions: Subscription[] = [];
  aemBanner: ICompetitionModules[];
  surfaceBets: string[];
  highlightCarousels: string[];
  private routeUrlSubscription: Subscription;

  constructor(
    private competitionsService: BigCompetitionsService,
    public participantsService: ParticipantsService,
    private pubsubService: PubSubService,
    private liveUpdatesService: BigCompetitionsLiveUpdatesService,
    private routingState: RoutingState,
    private route: ActivatedRoute,
    private router: Router,
    protected user: UserService,
    // eslint-disable-next-line
    private updateEventService: UpdateEventService // for events subscription (done in service init)
  ) {
    super();
  }

  /*
   * Init function.
   */
  ngOnInit(): void {
    this.routeUrlSubscription = this.route.url.subscribe(() => {
      this.highlightCarousels = null;
      this.surfaceBets = null;
      const competitionName = this.route.snapshot.paramMap.get('name');
      if(!this.router.getCurrentNavigation()?.extras?.state?.isloaded) {
        this.getTabsData(competitionName);
      }
    }, () => {
      this.showError();
    });
    this.subscription$ = this.competitionsService.aemBanner.subscribe(
      (gmodules) => {
        this.aemBanner = gmodules.filter((aembanner) => aembanner.type === 'AEM');
        const hc = gmodules.filter((aembanner) => aembanner.type === 'HIGHLIGHT_CAROUSEL');
        const sb = gmodules.filter((aembanner) => aembanner.type === 'SURFACEBET' && aembanner);
        this.highlightCarousels = hc[0]?.highlightCarousels || null;
        this.surfaceBets = sb[0]?.surfaceBets || null;
      }
    );
    this.subscriptions.push(this.subscription$);
    this.subscriptions.push(this.routeUrlSubscription);
  }
  getTabsData(competitionName) {
    this.subscription2$ = this.competitionsService.getTabs(competitionName).pipe(
      finalize(() => {
        this.hideSpinner();
        this.subscribe();
      })).subscribe((competition: IBCData) => {
          this.bchPageName = 'Competitions'
          this.competition = competition;
          this.competitionName = this.competition?.title;
          this.competitionTabs = this.competition?.competitionTabs;
          if (this.user.bonusSuppression && this.competition) {
            this.competitionTabs = this.competition.competitionTabs.filter(tab => tab.uri !== '/promotions');
          }
          this.bigCompetitionBgImageUrl = this.competition?.background ? this.cmsRootUri + this.competition?.background : '';
          this.competitionsService.storeCategoryId(this.competition?.categoryId.toString());
          this.setActiveTab();
          this.getParticipant(competition?.uri);
          this.competitionsService.brand = this.brand;
      });
      this.subscriptions.push(this.subscription2$);
  }
  getParticipant(path): void {
    this.subsPat$ = this.competitionsService.getParticipants(path).subscribe(
      (competitionParticipants) => {
        this.participantsService.store(competitionParticipants || []);
        this.participantsFlags = this.participantsService.getFlagsList();
      }
    );
    this.subscriptions.push(this.subsPat$);
  }
  ngOnDestroy(): void {
    this.subscriptions.forEach((subscription) => subscription.unsubscribe());
    this.pubsubService?.unsubscribe(this.subscriptionName);
  }

  /**
   * Subscribes for pubsub and router events.
   * @private
   */
  subscribe(): void {
    this.subscriptionName = 'BigCompetitionCtrl';
    const reloadEvents: Array<string> = [`liveServe.${EVENTS.SOCKET_RECONNECT_SUCCESS}`, this.pubsubService.API.RELOAD_COMPONENTS];

    this.pubsubService.subscribe(this.subscriptionName, reloadEvents, () => {
      this.reloadComponent();
    });
  }

  /*
   * Set active tab, and compare route with data, for proper redirections.
   * @param {Object} params - route segment params
   */
  setActiveTab(): void {
    const tabName = this.routingState.getRouteParam('tab', this.route.snapshot),
      tab = this.competitionsService.findTab();

    if (!tab) {
      return;
    }

    // Needs for tabs panel component
    this.activeTab = { id: tab.id };
    this.activeTabName = tab.name;
    // if tab not specified we should redirect to the tab
    this.defaultTabName = !tabName ? tab.name : "";
  }

  /**
   * Reloads component when LiveServe connetction is reestablised.
   * @protected
   */
  reloadComponent(): void {
    this.liveUpdatesService.reconnect().subscribe(() => {
      super.reloadComponent();
    });
  }
}
