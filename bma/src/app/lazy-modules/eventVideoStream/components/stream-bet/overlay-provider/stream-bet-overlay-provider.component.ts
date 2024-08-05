import { ChangeDetectorRef, Component, OnInit, OnDestroy, Output, EventEmitter, AfterViewInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { CmsService } from "@app/core/services/cms/cms.service";
import { PubSubService } from "@app/core/services/communication/pubsub/pubsub.service";
import { LocaleService } from "@app/core/services/locale/locale.service";
import { RoutingHelperService } from "@app/core/services/routingHelper/routing-helper.service";
import { SeoDataService } from "@app/core/services/seoData/seo-data.service";
import { WindowRefService } from "@app/core/services/windowRef/window-ref.service";
import { SportEventPageProviderService } from "@app/edp/components/sportEventPage/sport-event-page-provider.service";
import { FootballExtensionService } from "@app/edp/services/footballExtension/football-extension.service";
import { MarketsOptaLinksService } from "@app/edp/services/marketsOptaLinks/markets-opta-links.service";
import { TennisExtensionService } from "@app/edp/services/tennisExtension/tennis-extension.service";
import { SportsConfigService } from "@app/sb/services/sportsConfig/sports-config.service";
import { RoutingState } from "@app/shared/services/routingState/routing-state.service";
import { TemplateService } from "@app/shared/services/template/template.service";
import { SportEventPageComponent } from '@app/edp/components/sportEventPage/sport-event-page.component';
import { QuickbetService } from "@app/quickbet/services/quickbetService/quickbet.service";
import { IMarket } from '@core/models/market.model';
import { UserService } from "@core/services/user/user.service";
import { EventVideoStreamProviderService } from "@eventVideoStream/components/eventVideoStream/event-video-stream-provider.service";
import { StreamBetService } from '@lazy-modules/eventVideoStream/services/streamBet/stream-bet.service';
import { StorageService } from "@core/services/storage/storage.service";
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { SportEventPageService } from '@edp/services/sportEventPage/sport-event-page.service';
import { GtmService } from '@core/services/gtm/gtm.service';
@Component({
  selector: 'stream-bet-overlay-provider',
  templateUrl: './stream-bet-overlay-provider.component.html',
  styleUrls: ['./stream-bet-overlay-provider.component.scss']
})
export class StreamBetOverlayProviderComponent extends SportEventPageComponent implements OnInit, OnDestroy,AfterViewInit{
  @Output() readonly sbOverlayLoaded = new EventEmitter();
  
  outcomeSelected = false;
  betPlaced = false;
  showQuickBet = false;
  showMarkets = true;
  showReceipt = false;
  allMarkets: IMarket[] = [];
  baseMarkets: IMarket[] = [];
  selectedMarket: IMarket;
  showHideText = 'HIDE';
  balanceRefreshed = false;
  set sportBalance(value: string | number){}
  get sportBalance(): string | number {
    if(isNaN(+this.userService.sportBalance) && !this.balanceRefreshed){
      this.balanceRefreshed = true;
      this.pubSubService.publish(this.pubSubService.API.IMPLICIT_BALANCE_REFRESH);
    }
    return this.userService.sportBalanceWithSymbol;
  }

  templateMarketTypes: {};
  objectKeys = Object.keys;
  currMktContainerScrollLeft = 0;
  eventName: string = '';

  constructor(
    router: Router,
    activatedRoute: ActivatedRoute,
    sportEventPageProviderService: SportEventPageProviderService,
    templateService: TemplateService,
    footballExtension: FootballExtensionService,
    tennisExtension: TennisExtensionService,
    routingHelperService: RoutingHelperService,
    pubSubService: PubSubService,
    sportsConfigService: SportsConfigService,
    changeDetectorRef: ChangeDetectorRef,
    windowRefService: WindowRefService,
    cmsService: CmsService,
    routingState: RoutingState,
    marketsOptaLinksService: MarketsOptaLinksService,
    localeService: LocaleService,
    seoDataService: SeoDataService,
    protected isPropertyAvailableService: IsPropertyAvailableService,
    protected cashOutLabelService: CashOutLabelService,
    protected sportEventPageService: SportEventPageService,
    private quickbetService: QuickbetService,
    private userService: UserService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService,
    private streamBetService: StreamBetService,
    private storageService: StorageService,
    private gtmService: GtmService,
    ) {
      super(router, activatedRoute, sportEventPageProviderService, templateService, footballExtension, tennisExtension, routingHelperService,
        pubSubService, sportsConfigService, changeDetectorRef, windowRefService,
        cmsService, routingState, marketsOptaLinksService, localeService, seoDataService, isPropertyAvailableService, cashOutLabelService, sportEventPageService);

        super.isMobileOnly = true;
    }

    ngOnInit(){
      super.ngOnInit();
      const isValidSiteChannel = this.eventEntity.siteChannels?.split(',')?.includes('M');
      if(isValidSiteChannel && this.eventEntity.liveStreamAvailable) {
        const allMarketsData = this.marketsByCollection && this.marketsByCollection.find(market => market.name === 'All Markets');
        const allMarketsCollection = allMarketsData && allMarketsData.markets;
        const allMarkets = allMarketsCollection && allMarketsCollection.filter((market: IMarket) => market.siteChannels && market.siteChannels.split(',').includes('M')
         && market.isMarketBetInRun === "true" && market.isDisplayed && market.isDisplayed.toString() === "true" && market.viewType != "Scorecast");
        this.allMarkets = [...allMarkets];
        this.eventName = this.eventEntity.originalName || this.eventEntity.name;
        if(this.allMarkets.length) {           
          this.trackGADetails({actionEventData: 'load', 
            locationEventData: this.eventName, eventDetailsData: 'view_markets'},'contentView');
        }
        this.allMarkets.sort((m1, m2) =>  m1.displayOrder - m2.displayOrder);
        this.splitMarkets();
      }     
      this.eventVideoStreamProviderService.isStreamAndBet = true;

        this.quickbetService.quickBetOnOverlayCloseSubj.subscribe(qbStatusMsg => {
          if(qbStatusMsg === 'close qb panel'){
            this.showQuickBet = false;
            this.showReceipt = false;
          } else if(qbStatusMsg === 'qb receipt') {
            this.showQuickBet = true;
            this.showReceipt = true;
          }
        });

      this.streamBetService.lastTemplateLoadedSubj.subscribe(() => {
        document.querySelector('.markets-container').scrollLeft = this.currMktContainerScrollLeft;
      });
    }
    ngAfterViewInit(){
      this.sbOverlayLoaded.emit();
    }

     /**
      * Split markets into grouped and base markets(No grouping)
      * @returns void
      */
    splitMarkets(): void {
      this.allMarkets?.forEach((eachMarket:IMarket)=> {
        const market = {...eachMarket};
        // formatting data - START
        const result = this.streamBetService.getMarketTemplate(market, this.eventEntity);
        if(result) {
          if (market.outcomes) {
            market.outcomes = this.templateService.sortOutcomesByPriceAndDisplayOrder(market.outcomes);
          }
          if( this.templateMarketTypes && this.templateMarketTypes['template-market-type']) {
            const sbTemplateMarketTypes = this.templateMarketTypes['template-market-type'];            
            if(sbTemplateMarketTypes[market.templateMarketName]) {
              const existingMarkets = sbTemplateMarketTypes[market.templateMarketName].markets;
              const templateMarket = sbTemplateMarketTypes[market.templateMarketName];
              const lastTemplateMarket = templateMarket.markets[templateMarket.markets.length-1];
              if((result === 'price-odd-button' || result === 'special-market' || result === 'single-drop-double-odd') && (!market.templateMarketName.toLowerCase().includes('handicap')) && lastTemplateMarket.name.split(' ')[0] !== market.name.split(' ')[0]) {
                this.templateMarketTypes['template-market-type'][market.templateMarketName+'-'+market.name] = {markets : [market], template: result};
              } else {
                const updatedMarkets = [...existingMarkets, market];
                sbTemplateMarketTypes[market.templateMarketName].markets = updatedMarkets;
                this.templateMarketTypes['template-market-type'][market.templateMarketName] = sbTemplateMarketTypes[market.templateMarketName];
              }
            } else {
              this.templateMarketTypes['template-market-type'][market.templateMarketName] = {                  
                  markets: [market], 
                  template: result                 
              }
            }
          } else {
            this.templateMarketTypes = {
              'template-market-type': {
                [market.templateMarketName]: {
                  markets: [market], 
                  template: result
                }
              }
            };
          }          
        }        
        // formatting data - END        
      });
    }

  handleSelectionClick(market: IMarket, index?: number) {
    this.selectedMarket = market;
    this.currMktContainerScrollLeft = document.querySelector('.markets-container').scrollLeft;
    this.showQuickBet = true;
    this.streamBetService.multiOddMarketCounter = 0;
    const multipleOddsMarketElems = document.querySelectorAll('.multiple-odds-card-item');
    this.streamBetService.totalMultiOddMarketElemsCount = multipleOddsMarketElems.length;
  }

  showHideClick() {
    if (!this.showQuickBet) {
      this.showHideText = this.showHideText === 'HIDE' ? 'SHOW' : 'HIDE';
      this.showMarkets = !this.showMarkets;      
      this.trackGADetails({ actionEventData: this.showHideText === 'HIDE' ? 'expand' : 'collapse', 
        locationEventData: this.eventName, eventDetailsData: this.eventName });      
    }
  }

  /**
    * GA tracking
    * @returns void
    */
  trackGADetails(trackingData: object,eventTracking: string = 'Event.Tracking'): void {
    this.gtmService.push(eventTracking,{
      'event': eventTracking,        
      'component.CategoryEvent': 'video streaming',        
      'component.LabelEvent': 'stream and bet',        
      'component.ActionEvent': trackingData['actionEventData'],        
      'component.PositionEvent': this.eventEntity.categoryName,     
      'component.LocationEvent': trackingData['locationEventData'],
      'component.EventDetails': trackingData['eventDetailsData'],        
      'component.URLClicked': 'not applicable',        
      'component.ContentPosition':'not applicable' 
    });
  }

  ngOnDestroy(): void {
    this.eventVideoStreamProviderService.isStreamAndBet = false;
  }
}
