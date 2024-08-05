import { Component, Input, ComponentFactoryResolver,Output,EventEmitter, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { ToteFreebet } from '@betslip/services/freeBet/free-bet.model';
import { IFreebetToken} from '@bpp/services/bppProviders/bpp-providers.model';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { ToteFreeBetSelectDialogComponent } from '../tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';
import { FiltersService } from '@core/services/filters/filters.service';
import { StorageService } from '@core/services/storage/storage.service';
import { LocaleService } from '@core/services/locale/locale.service';
import * as _ from 'underscore';
import { TimeService } from '@core/services/time/time.service';
import environment from "@environment/oxygenEnvConfig";
import { GtmService } from '@core/services/gtm/gtm.service';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
@Component({
  selector: 'tote-free-bets-toggle',
  templateUrl: './tote-free-bets-toggle.component.html',
  styleUrls: ['./tote-free-bets-toggle.component.scss']
})
export class ToteFreeBetsToggleComponent {
  @Input() selected: any;
  @Input() toteFreeBetSelected: boolean;
  @Input() freeBets: IFreebetToken[];
  @Input() freebetsConfig: IFreebetsPopupDetails;
  @Input() showOnDigitKeyborad: boolean;
  @Input() betPackList: IFreebetToken[];
  @Input() digitKeyboard: boolean;
  @Input() triggeredFromToteBets?: boolean;
  @Input() selectedToteFreeBetValue? : any;
  @Input() categoryName: string = '';
  @Input() eventName: string = '';
  @Input() isBetslip: boolean;
  isMobile: boolean;
  @Output() readonly toteBet = new EventEmitter();
  @Output() readonly removetoteFreeBet = new EventEmitter();
  selectedFreebetVal: string;
  isStreamAndBet = false;
  selectedText: string;

  
  constructor(
    private componentFactoryResolver: ComponentFactoryResolver,
    private dialogService: DialogService,
    protected freeBetsFactory: FreeBetsService,
    private filtersService: FiltersService,
    private storageService: StorageService,
    private changeDetectorRef: ChangeDetectorRef,
    protected localeService: LocaleService,
    protected timeService: TimeService,
    protected gtmService: GtmService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService
  ) { 
    this.isMobile = environment.CURRENT_PLATFORM === "mobile";
    this.isStreamAndBet = this.eventVideoStreamProviderService.isStreamAndBet;
  }

  get dialogComponent() {
    return ToteFreeBetSelectDialogComponent;
  }

  set dialogComponent(value: any) { }

  /**
   * @returns {string}
   * This value displays in Mobile (betslip & Quickbet) & Tablet Quickbet
   */
  freebetButtonText(isMobile:boolean=false):string{
    const  freebetsdata = this.freeBets && this.freeBets.length;
    const  betPackdata = this.betPackList && this.betPackList.length;
    //this.freebetImage();
    if(isMobile){
      return (freebetsdata> 0 && betPackdata> 0) ? this.freebetsConfig.plusTokenAndFreeBet : (freebetsdata > 0) ? this.freebetsConfig.plusFreeBet : (betPackdata> 0) ? this.freebetsConfig.plusToken : '';
    }  
    return (freebetsdata > 0 && betPackdata> 0) ? this.freebetsConfig.addTokenAndFreeBet : (freebetsdata > 0) ? this.freebetsConfig.addFreeBet : (betPackdata> 0) ? this.freebetsConfig.addBetToken : '';
  }
    
  getText(): string {
    if(this.selected !== null && this.selected !== undefined) {
      if(this.selected[0]) {
        return (this.filtersService.setFreebetCurrency(this.selected[0].freebetTokenValue) + ' ' + ((this.selected[0].freebetOfferCategories && this.selected[0].freebetOfferCategories.freebetOfferCategory === 'Bet Pack') ? this.localeService.getString('bs.betTokenAdded') : this.freebetsConfig.freeBetAdded));
      } else {
        return (this.filtersService.setFreebetCurrency(this.selected.freebetTokenValue) + ' ' + ((this.selected.freebetOfferCategories && this.selected.freebetOfferCategories.freebetOfferCategory) === 'Bet Pack' ? this.localeService.getString('bs.betTokenAdded') : this.freebetsConfig.freeBetAdded));
      }
     }
  }
  
  useFreeBet(): void {  
    if ( (!this.freeBets) && (!this.betPackList || !this.betPackList.length)) {
      return;
    }

    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.dialogService.openDialog(DialogService.API.selectToteFreebetDialog, componentFactory, true, {
      dialogClass: 'tote-free-bet-select-dialog',
      freeBets: this.formatDate(this.storageService.get('toteFreeBets')),
      freebetsConfig: this.freebetsConfig,
      betPackList: this.formatDate(this.storageService.get('toteBetPacks')),
      categoryName: this.categoryName,
      eventName: this.eventName,
      onSelect: (freeBet: ToteFreebet) => {
        this.toteBet.emit(freeBet);
        this.dialogService.closeDialog(DialogService.API.selectToteFreebetDialog);
        this.selected = freeBet;
        this.isBetSelected();
        this.removeFreebetButtonText();
        const toteBetStorageVal = this.storageService.get('toteBet');
        toteBetStorageVal.poolBet.freebetTokenId = freeBet.freebetTokenId;
        toteBetStorageVal.poolBet.freebetTokenValue = freeBet.freebetTokenValue;
        if(freeBet.freebetOfferCategories){
          toteBetStorageVal.poolBet.betType = freeBet.freebetOfferCategories.freebetOfferCategory;
        } else {
          delete toteBetStorageVal.poolBet.betType;
        }
        this.storageService.set('toteBet', toteBetStorageVal);
      }
    });
    this.triggerGtmService(this.isStreamAndBet, this.gtmFreebetText());
    this.changeDetectorRef.detectChanges();
  }

  private gtmFreebetText(): string {
    const toteBets= this.storageService.get('toteFreeBets');
    const betPacks= this.storageService.get('toteBetPacks');
    if((toteBets && toteBets.length > 0) && (betPacks && betPacks.length > 0)) {
      return 'add bet token and free bet';
    } else if (toteBets && toteBets.length > 0) {
      return 'add free bet';
    } else if (betPacks && betPacks.length > 0) {
      return 'add bet token';
    }
  }
  private triggerGtmService(isStreamAndBet: boolean = false, freebetText: string = ''): void {    
    if(isStreamAndBet) {
      this.gtmService.push('Event.Tracking', {
        'event': 'Event.Tracking',
        'component.CategoryEvent': 'video streaming',
        'component.LabelEvent': 'stream and bet',
        'component.ActionEvent': 'click',
        'component.PositionEvent': this.categoryName,
        'component.LocationEvent': this.eventName,
        'component.EventDetails': freebetText,
        'component.URLClicked': 'not applicable' ,
        'component.ContentPosition':'not applicable'
      });
    } else {
      this.gtmService.push('trackEvent', {
        event: 'trackEvent',
        eventCategory: this.isBetslip ? 'betslip' : 'quickbet',
        eventAction: 'quick stake',
        eventLabel: 'free bet',
        eventDetails: this.getEventdetails(),
      });
    }
  }
  private getEventdetails(): string {
    if(!this.showOnDigitKeyborad && !this.isBetSelected() && !this.isMobile) {
      return this.freebetButtonText();
    }
    if (this.showOnDigitKeyborad) {
      return this.isBetSelected() ? this.removeFreebetButtonText() : this.freebetButtonText(true);
    }
    if (!this.showOnDigitKeyborad && this.isBetSelected()) {
      return this.getText() === undefined ? this.selectedText : this.getText();
    }
    return '';
  }

  removeFreeBet(): void {
    this.selectedText = this.getText();
    this.selected = null;
    const x = this.storageService.get('toteBet');
    if(x && x.poolBet && x.poolBet.freebetTokenId) {
      const removeText =  x.poolBet.betType ? 'remove bet token' : 'remove free bet';
      this.triggerGtmService(this.isStreamAndBet,removeText);
    }
    this.removetoteFreeBet.emit();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes.selectedToteFreeBetValue && changes.selectedToteFreeBetValue.currentValue === null) {
      this.selected = null;
    }
  }

  removeFreebetButtonText(): string {
    const x = this.storageService.get('toteBet');
    if(x && x.poolBet) {
      return x.poolBet.betType ? this.freebetsConfig.betTokenAdded : this.freebetsConfig.freeBetAdded;
    }
   }

  formatDate(freeBets): any {
    return _.each(freeBets, (item: any) => {
      const expDate = item.freebetTokenExpiryDate,
        tempDate = new Date(expDate.replace(/-/g, '/'));
      item.freebetTokenExpiryDate = tempDate;
    })
  }

  isBetSelected() : boolean {
    const x = this.storageService.get('toteBet');
    const tokenId = x && x.poolBet && x.poolBet.freebetTokenId;
    return tokenId ? true : false;
  }
} 
