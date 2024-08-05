import { Component, OnInit, Input, AfterViewInit, Output, EventEmitter } from "@angular/core";
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from "@core/models/sport-event.model";
import { QuickbetService } from "@app/quickbet/services/quickbetService/quickbet.service";
import { UserService } from "@core/services/user/user.service";
import { EventVideoStreamProviderService } from "@eventVideoStream/components/eventVideoStream/event-video-stream-provider.service";
import { StorageService } from "@core/services/storage/storage.service";
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from "@app/core/services/communication/pubsub/pubsub.service";

@Component({
  selector: 'stream-bet-overlay-provider-racing',
  templateUrl: '../overlay-provider/stream-bet-overlay-provider.component.html',
  styleUrls: ['../overlay-provider/stream-bet-overlay-provider.component.scss']
})
export class StreamBetOverlayProviderRacingComponent implements OnInit, AfterViewInit {
  @Input() eventEntity: ISportEvent;
  @Output() readonly sbOverlayLoaded = new EventEmitter();
  @Input() isHR: boolean;

  outcomeSelected = false;
  betPlaced = false;
  showQuickBet = false;
  showMarkets = true;
  showReceipt = false;
  selectedMarket: IMarket;
  allMarkets: IMarket[] = [];
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

  constructor(
    private quickbetService: QuickbetService,
    private userService: UserService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService,
    private storageService: StorageService,
    private gtmService: GtmService,
    private pubSubService: PubSubService,
    ) { }

    ngOnInit() {
      const isValidSiteChannel = this.eventEntity.siteChannels?.split(',').includes('M');
      if(isValidSiteChannel && this.eventEntity.liveStreamAvailable) {
        this.allMarkets = this.eventEntity.markets?.filter((market: IMarket) => market.siteChannels?.split(',').includes('M') && 
          market.isMarketBetInRun === "true" && market.isDisplayed?.toString() === "true")
      }
      if(this.allMarkets && this.allMarkets.length) {          
        this.gtmService.push('contentView', {
          'event': 'contentView',         
          'component.CategoryEvent': 'video streaming',      
          'component.LabelEvent': 'stream and bet',      
          'component.ActionEvent': 'load',      
          'component.PositionEvent': this.eventEntity.categoryName,       
          'component.LocationEvent': this.eventEntity.originalName || this.eventEntity.name, 
          'component.EventDetails': 'view_markets',      
          'component.URLClicked': 'not applicable' ,      
          'component.ContentPosition':'not applicable'      
        });
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
    }
    ngAfterViewInit(){
     this.sbOverlayLoaded.emit();
    }

    handleSelectionClick(market: IMarket) {
        this.selectedMarket = market;
        this.showQuickBet = true;
    }

    showHideClick(){
      if(!this.showQuickBet) {
        this.showHideText = this.showHideText === 'HIDE' ? 'SHOW' : 'HIDE';
        this.showMarkets = !this.showMarkets;
        this.gtmService.push('Event.Tracking',{
          'event': 'Event.Tracking',        
          'component.CategoryEvent': 'video streaming',        
          'component.LabelEvent': 'stream and bet',        
          'component.ActionEvent': this.showHideText === 'HIDE' ? 'expand' : 'collapse',        
          'component.PositionEvent': this.eventEntity.categoryName,       
          'component.LocationEvent':this.eventEntity.originalName || this.eventEntity.name,       
          'component.EventDetails': this.eventEntity.originalName || this.eventEntity.name,       
          'component.URLClicked': 'not applicable',        
          'component.ContentPosition':'not applicable' 
        });
      }
    }

    ngOnDestroy(): void {
      this.eventVideoStreamProviderService.isStreamAndBet = false;
    }
}
