import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  OnInit,
  Output
} from '@angular/core';
import {
  forkJoin,
  from as observableFrom,
  Observable,
  Subscription
} from 'rxjs';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { RegularBetBase } from '@app/betHistory/betModels/regularBetBase/regular-bet-base.class';
import { ICashoutBetsMap, ICashoutMapItem } from '@app/betHistory/models/cashout-map-item.model';
import { map, mergeMap, reduce } from 'rxjs/operators';
import { CommandService } from '@core/services/communication/command/command.service';
import { CashOutMapService } from '@app/betHistory/services/cashOutMap/cash-out-map.service';
import { UserService } from '@core/services/user/user.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { StreamTrackingService } from '@sb/services/streamTracking/stream-tracking.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { SortByOptionsService } from '@app/racing/services/sortByOptions/sort-by-options.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { AREAS } from '@app/lazy-modules/racingFeatured/components/racingFeatured/constant';
import * as _ from 'underscore';
import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import { StorageService } from '@core/services/storage/storage.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'racing-mybets',
  templateUrl: './racing-mybets.component.html'
})
export class RacingMyBetsComponent extends RacingEventComponent implements OnInit {
  @Input() eventId: number;
  @Input() eventEntity: ISportEvent;
  @Input() events: ISportEvent[] = [];
  @Input() isRaceCard = false;
  @Output() tabUpdated: EventEmitter<any> = new EventEmitter();
  
  isBetsStreamLoading: boolean = false; 
  
  private cashoutDataSubscription: Subscription;
  private betsStreamOpened: boolean = false;
  private cashoutIds: ICashoutMapItem[];
  private placedBets: RegularBetBase[];
  private editMyAccaUnsavedOnEdp: boolean;
  private isLoggedIn: boolean;
  private tagName: string = 'RacingMyBetsComponent';
  private readonly HORSE_RACING_EDP = AREAS.HREDP;
  private myBetsTabLabel: string;
  private myBetsAvailable: boolean;
  private raceCardEventIds: number[] = [];
  private signPostEventIds: number[] = [];
  private combineEventIds: number[] = [];
  public showSignPosting: boolean;
  public tempBets = [];
  public cashoutBets: RegularBetBase[];
  public myBetsCounter: number;
  isCoral: boolean;
  
  constructor(
    protected windowRef: WindowRefService,
    protected timeService: TimeService,
    protected pubSubService: PubSubService,
    protected nativeBridgeService: NativeBridgeService,
    protected ukToteService: UkToteService,
    protected lpAvailabilityService: LpAvailabilityService,
    protected deviceService: DeviceService,
    protected gtmService: GtmService,
    protected streamTrackingService: StreamTrackingService,
    protected dialogService: DialogService,
    protected filterService: FiltersService,
    protected localeService: LocaleService,
    protected horseracing: HorseracingService,
    protected routingHelperService: RoutingHelperService,
    protected cmsService: CmsService,
    protected tools: CoreToolsService,
    protected sbFilters: SbFiltersService,
    protected router: Router,
    protected location: Location,
    protected changeDetectorRef: ChangeDetectorRef,
    protected sortByOptionsService: SortByOptionsService,
    protected route: ActivatedRoute,
    protected watchRulesService: WatchRulesService,
    protected seoDataService: SeoDataService,
    protected elementRef: ElementRef,
    protected racingGaService: RacingGaService,
    private commandService: CommandService,
    private cashOutMapService: CashOutMapService,
    private userService: UserService,
    public cashoutWsConnectorService: CashoutWsConnectorService,
    public storageService: StorageService
  ) {
    super(windowRef
      , timeService
      , pubSubService
      , nativeBridgeService
      , ukToteService
      , lpAvailabilityService
      , deviceService
      , gtmService
      , streamTrackingService
      , dialogService
      , filterService
      , localeService
      , horseracing
      , routingHelperService
      , cmsService
      , tools
      , sbFilters
      , router
      , location
      , changeDetectorRef
      , sortByOptionsService
      , route
      , watchRulesService
      , seoDataService
      , elementRef
      , racingGaService);

    this.isLoggedIn = this.userService.status;
  }

  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.tagName = this.isRaceCard ? 'BuildRaceCardComponent' : this.tagName;
    this.pubSubService.subscribe(this.tagName, [this.pubSubService.API.SESSION_LOGIN,this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      this.raceCardEventIds = this.events.map((event: ISportEvent) => event.id);
      this.initiateCashoutBets();
    });
    if (this.isLoggedIn) {
      this.raceCardEventIds = this.events.map((event: ISportEvent) => event.id);
      this.initiateCashoutBets();
      //store event id's to show the signposting
      if(this.isRaceCard) {
        this.signPostEventIds = this.events.map((event: ISportEvent) => event.id);
      }
    // Load data from local storage when the event is same
      const signPostData = this.storageService.get('myBetsSignPostingData');
      if (signPostData) {
        if (this.eventId) {
          this.showSignPosting = signPostData.some((eventData) => Number(eventData.eventId) === Number(this.eventId) && eventData.betIds.length > 0);
        } else {
          this.raceCardEventIds.forEach((raceEventId) => {
              this.showSignPosting = signPostData.some((eventData) => Number(eventData.id) === Number(raceEventId) && eventData.betIds.length > 0);
          });
        }
      }
    }
    this.addListeners();
  }
    /**
   * sets cashoutbets and placedbets and gets cashoutbets
   */
     protected initiateCashoutBets(): void {
      this.closeCashoutStream();
      this.setPlacedBets().subscribe(() => {
        if (this.placedBets?.length) {
          this.getCashOutData();
        } else {
          this.closeCashoutStream();
        }
      });
    }
    
      /**
   * add the event listeners
   **/
  protected addListeners(): void {
    this.subscribeEditAccaChanges();
    this.subscribeForCashoutUpdates();

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.isLoggedIn = this.userService.status;
      if (this.isLoggedIn) {
        this.initiateCashoutBets();
      }
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.MY_BET_PLACED, (placedBet: any) => {
      let finalBets = this.placedBets;
        if(placedBet.isquickbet) {
          this.commandService.executeAsync(this.commandService.API.GET_PLACED_BETS_ASYNC, [this.eventId], [])
          .then(data => {
            this.placedBets = data;
            const qb = this.placedBets.filter(bet => bet.betId ===placedBet.id.toString());
            this.tempBets = [...this.tempBets, ...qb];
            this.showSignPosting = true;
            this.showMybetTab();
          });
        } else {
          this.tempBets = [...this.tempBets, ...placedBet.bets];
          this.extendCashoutBets(this.tempBets);
          if(!_.isEmpty(this.placedBets)) {
            finalBets = this.placedBets.filter((bet:any) => (bet.cashoutStatus != 'BET_CASHED_OUT' && bet.uniqueId !== "0"));
            this.placedBets = [...this.tempBets, ...finalBets];
          } else {
            this.placedBets = [...this.tempBets];
          }
          this.showSignPosting = true;
          this.showMybetTab();
        }
      });
  }

  showMybetTab() {
    this.placedBets = this.getFilteredBets();
    const uniqset = [... new Set(this.placedBets.map(bet => bet.betId))];
    this.setCashoutIds(uniqset);
    const counter = uniqset.length;
    this.myBetsAvailable = counter > 0;
    if (this.activeUserTab === 'myBets' && !this.myBetsAvailable) {
      this.setActiveUserTab('markets');
    }
    this.myBetsCounter = counter;
    this.myBetsTabLabel = this.myBetsTabName(counter);
  }

  setCashoutIds(temparr) {
    const tempCashIds = [];
    temparr.map(bet => tempCashIds.push({ id: bet, isSettled: false }));
    this.cashoutIds = [...tempCashIds];
  }
  extendCashoutBets(bets) {
    (bets || []).forEach(bet => bet.betId = bet.betId ? bet.betId : bet.id);
  }

  getFilteredBets() {
    return this.placedBets
    .filter((bet: RegularBetBase) => (this.isSameEventBet(bet) && bet.settled !== 'Y'
    && bet.cashoutStatus !== 'BET_CASHED_OUT'
    && bet.type !== 'placedBetsWithoutCashoutPossibility'));
  }
  isSameEventBet(bet): boolean {
    let filtered = false;
    if(this.isRaceCard) {
      filtered = this.raceCardEventIds.some(eventid => JSON.stringify(bet.leg).includes(eventid.toString()));
    } else {
      filtered = JSON.stringify(bet.leg).includes(this.eventId.toString());
    }
    return filtered;
  }

  isTempBetsAvailable() {
    let farr = [];
    if(this.cashoutBets) {
      farr = this.tempBets?.filter(bet =>!JSON.stringify(this.cashoutBets).includes(bet.id || bet.betId));
    } else if(!this.cashoutBets && this.tempBets) {
      farr = this.tempBets;
    }
    return farr;
  }
  updateCashoutData() {

    this.placedBets = this.getFilteredBets();
    // remove from storage when my bets section visited
    let index;
    const signPostData = this.storageService.get('myBetsSignPostingData');
    if (signPostData) {
      if (this.eventId) {
        index = signPostData.findIndex(eventData => Number(eventData.eventId) === Number(this.eventId));
        if (index !== -1) {
          signPostData.splice(index, 1);
        }
      } else {
        this.raceCardEventIds.forEach((eventId) => {
          index = signPostData.findIndex(eventData => Number(eventData.eventId) === Number(eventId));
          if (index !== -1) {
            signPostData.splice(index, 1);
          }
        });
      }
      this.showSignPosting = false;
      this.storageService.set('myBetsSignPostingData', signPostData);
    }

    if(!this.isTempBetsAvailable().length) {
      return;
    }
    if(!this.cashoutWsConnectorService.getConnection()) {
       this.openCashoutStream('onclick');
      } else  {
        this.cashoutWsConnectorService.dateChangeBet().subscribe((res: any) => {
          this.cashoutBets = res;
          if (this.cashoutBets) {
            this.cashOutMapService.createCashoutBetsMap(
              res,
              this.userService.currency,
              this.userService.currencySymbol
            );
            this.changeDetectorRef.detectChanges();
            this.pubSubService.publish(this.pubSubService.API.MY_BETS_UPDATED);
          }
        });
      }
  }
  ngOnDestroy(): void {
    this.closeCashoutStream();
  }

  /**
   * sets the placed bets
   * @returns {Observable<void>}
   */
  private setPlacedBets(): Observable<void> {
    const eventIds = this.eventId || this.raceCardEventIds.join(',');
    return observableFrom(this.commandService.executeAsync(
      this.commandService.API.GET_PLACED_BETS_ASYNC,
      [eventIds],
      [])).pipe(
        map((data: RegularBetBase[]) => {
          this.placedBets = data;
        })
      );
  }

    /**
     * gets the cashout data
     */
    private getCashOutData(): void {
      const eventsObservable = [];
      const cashOutBets = this.placedBets
          .filter((bet: RegularBetBase) => bet.settled !== 'Y' && bet.cashoutStatus !== 'BET_CASHED_OUT');
      if (!this.isRaceCard) {
        this.events = [this.eventEntity];
      }
      this.events.forEach((event: ISportEvent) => {
        const currentObservable = observableFrom(this.commandService.executeAsync(
          this.commandService.API.GET_BETS_FOR_EVENT_ASYNC,
          [
            event.id,
            cashOutBets,
            this.placedBets
          ],
          {}
        ));
        eventsObservable.push(currentObservable);
      });

      this.cashoutDataSubscription = forkJoin(eventsObservable).pipe(
        mergeMap((betsData: ICashoutBetsMap[]) => betsData),
        reduce((currentBet: ICashoutBetsMap, nextBet: ICashoutBetsMap) => {
          return {
            cashoutIds: currentBet.cashoutIds.concat(nextBet.cashoutIds),
            placedBets: currentBet.placedBets
          };
        }),
      ).subscribe((betsData: ICashoutBetsMap) => {
        const placedBets: RegularBetBase[] = betsData.placedBets
          .filter((bet: RegularBetBase) => bet.settled !== 'Y' && bet.cashoutStatus !== 'BET_CASHED_OUT');
  
        // make my bets tab available is event has placed or cash out bets
        this.cashoutIds = betsData.cashoutIds;
        this.placedBets = placedBets;
        this.updateBetsDetails();
      });
    }
  
    /**
     * update the bet details for counter, tabs visibility, stream
     */
    private updateBetsDetails(): void {
      if (this.placedBets.length) {
        const count = [... new Set(this.placedBets.map(bet => bet.betId))].length;
        this.myBetsTabLabel = this.myBetsTabName(count);
        this.openCashoutStream();
      } else {
        this.myBetsAvailable = false;
        this.closeCashoutStream();
        if (this.activeUserTab === this.HR_TABS.MYBETS) {
          this.setActiveUserTab(this.HR_TABS.MARKETS);
        }
      }
      this.changeDetectorRef.detectChanges();
      this.pubSubService.publish(this.pubSubService.API.MY_BETS_UPDATED);
    }
  
    /**
     * construct the mybets tab name with bets count
     * @param {number} counter
     * @returns {string}
     */
    private myBetsTabName(counter: number): string {
      const name = this.localeService.getString('sb.myBets');
      return Number(counter) ? `${name} (${counter})` : name;
    }
  
    /**
     * open cashout stream ws call
     */
    private openCashoutStream(source?): void {
      if (!this.betsStreamOpened) {
        this.betsStreamOpened = true;
        this.isBetsStreamLoading = true;
        this.commandService.executeAsync(this.commandService.API.OPEN_CASHOUT_STREAM).then((data: IBetDetail[]) => {
          if (data) {
            this.cashOutMapService.createCashoutBetsMap(
              data,
              this.userService.currency,
              this.userService.currencySymbol
            );
            if(source) {
              this.changeDetectorRef.detectChanges();
              this.pubSubService.publish(this.pubSubService.API.MY_BETS_UPDATED);
            }
            this.myBetsAvailable = true;
            this.isBetsStreamLoading = false;
          }
        });
      }
    }
  
    /**
     * close the ws call cashout stream
     */
    private closeCashoutStream(): void {
      if (this.cashoutDataSubscription) {
        this.cashoutDataSubscription.unsubscribe();
      }
  
      if (this.betsStreamOpened) {
        this.commandService.executeAsync(this.commandService.API.CLOSE_CASHOUT_STREAM);
        this.betsStreamOpened = false;
      }
    }
  
    /**
     * subscribes for cashout updates
     */
    private subscribeForCashoutUpdates(): void {
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.UPDATE_CASHOUT_BET, bet => {
        const isSettled = bet && (bet.cashoutStatus === 'BET_SETTLED' || bet.cashoutStatus === 'BET_CASHED_OUT');
        isSettled && this.updateBets(bet.betId);

        const signPostData = this.storageService.get('myBetsSignPostingData');
        if(signPostData && bet.isCashOutedBetSuccess) {
          if(this.isRaceCard) {
            this.showSignPosting = this.signPostEventIds.some(eventId => {
              return signPostData.some((eventData) => Number(eventData.eventId) === Number(eventId) && eventData.betIds.length > 0);
            });
          } else {
            this.showSignPosting = signPostData.some((eventData) => Number(eventData.eventId) === Number(this.eventId) && eventData.betIds.length > 0) 
          }
        }
        
      });
      
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.CASH_OUT_BET_PROCESSED, (betId: string) => {
        this.updateBets(betId);
      });
    }

    /**
     * update the bets based on betId
     * @param {string} betId 
     */
    private updateBets(betId: string): void {
      this.cashoutIds = _.filter(this.cashoutIds, (id: ICashoutMapItem) => id.id !== betId);
      this.updateCashoutBets(this.placedBets, betId);
      this.updateCashoutBets(this.cashoutBets, betId);
      const counter = this.placedBets ? this.getFilteredBets().length : 0;
      this.myBetsAvailable = counter > 0;
      if(this.myBetsAvailable) {
        this.myBetsCounter = counter;
        this.myBetsTabLabel = this.myBetsTabName(counter);
      } else {
        this.setActiveUserTab('markets');
      }
    }
    private updateCashoutBets(list: RegularBetBase[] = [], id: string): void {
      if (!Array.isArray(list)) {
        return;
      }

      list.forEach((bet: RegularBetBase) => {
        if (bet.betId === id) {
          bet.type = 'placedBetsWithoutCashoutPossibility';
        }
      });
    }
    /**
     * sets the active tab
     * @param {string} tabName
     */
    setActiveUserTab(tabName: string): void {
      if (this.editMyAccaUnsavedOnEdp) {
        this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
      } else {
        this.activeUserTab = tabName;
        this.tabUpdated.emit(this.activeUserTab);
      }
      tabName === this.HR_TABS.MYBETS && !this.isRaceCard && this.gtmService.push('trackEvent', {
        eventAction: "race card",
        eventCategory: "horse racing",
        eventLabel: this.myBetsTabLabel,
        categoryID: this.eventEntity.categoryId,
        typeID: this.eventEntity.typeId,
        eventID: this.eventEntity.id,
      });
    }
  
    /**
     * subscribe to edit acca changes
     */
    private subscribeEditAccaChanges(): void {
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EDIT_MY_ACCA, () => {
        this.initiateCashoutBets();
        const signPostData = this.storageService.get('myBetsSignPostingData');
        if(signPostData) {
          this.showSignPosting = signPostData.some((eventData) => Number(eventData.eventId) === Number(this.eventId) && eventData.betIds.length > 0);
        }
      });
  
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EMA_UNSAVED_ON_EDP, (unsaved: boolean) => {
        this.editMyAccaUnsavedOnEdp = unsaved;
      });
    }
  
    /**
     * Check if markets tab should be available
     * @returns {boolean}
     */
    isMarketsTabAvailable(): boolean {
      return this.isLoggedIn && this.myBetsAvailable;
    }
}
