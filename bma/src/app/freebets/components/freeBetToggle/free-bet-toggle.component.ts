import { Component, Input, Output, EventEmitter, ComponentFactoryResolver, ChangeDetectorRef } from '@angular/core';

import { DialogService } from '@core/services/dialogService/dialog.service';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { FreeBetSelectDialogComponent } from '../freeBetSelectDialog/free-bet-select-dialog.component';
import { IFreebetToken } from '@bpp/services/bppProviders/bpp-providers.model';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import { FiltersService } from '@core/services/filters/filters.service';
import { DeviceService } from '@core/services/device/device.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';

@Component({
  selector: 'free-bet-toggle',
  templateUrl: './free-bet-toggle.component.html',
  styleUrls: ['./free-bet-toggle.component.scss']
})
export class FreeBetToggleComponent {
  @Input() freeBets: IFreebetToken[];
  @Input() selected: IFreeBet;
  @Input() freebetsConfig: IFreebetsPopupDetails;
  @Input() isBoostEnabled: boolean;
  @Input() isSelectionBoosted: boolean;
  @Input() canBoostSelection: boolean;
  @Input() showOnDigitKeyborad: boolean;
  @Input() isBetslip: boolean;
  @Input() betPackList: IFreebetToken[];
  @Input() selection?: IQuickbetSelectionModel;
  @Input() fanzoneList : IFreebetToken[];
  @Input() freeBetImageName:string;
  @Input() categoryName: string = '';
  @Input() eventName: string = '';

  @Output() readonly selectedChange = new EventEmitter();
  freeBetVal: string;
  isDesktop: boolean;
  isMobile: boolean;
  isStreamAndBet = false;
  freeBetImageNameSvg:string;

  constructor(
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private filtersService: FiltersService,
    private deviceService: DeviceService,
    protected freeBetsFactory: FreeBetsService,
    protected gtmService: GtmService,
    private changeDetectorRef: ChangeDetectorRef,
    private eventVideoStreamProviderService: EventVideoStreamProviderService
  ) {
    this.isMobile = this.deviceService.getDeviceViewType().mobile && !this.deviceService.isTabletOrigin;
    this.isStreamAndBet = this.eventVideoStreamProviderService.isStreamAndBet;
  }

  get dialogComponent() {
    return FreeBetSelectDialogComponent;
  }
  set dialogComponent(value: any) { }

  useFreeBet(): void {
    if(this.isStreamAndBet && this.selection.disabled) {
      return;
    }
     if ( (!this.freeBets || !this.freeBets.length ) && (!this.betPackList || !this.betPackList.length)&& (!this.fanzoneList || !this.fanzoneList.length)) {
      return;
    }
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.dialogService.openDialog(DialogService.API.selectFreeBetDialog, componentFactory, true, {
      dialogClass: 'free-bet-select-dialog',
      freeBets: this.freeBets,
      freebetsConfig: this.freebetsConfig,
      fanzoneList : this.fanzoneList,
      isBoostEnabled: this.isBoostEnabled,
      isSelectionBoosted: this.isSelectionBoosted,
      canBoostSelection: this.canBoostSelection,
      betPackList:this.betPackList,
      categoryName: this.categoryName,
      eventName: this.eventName,
      onSelect: (freeBet: IFreeBet) => {
        this.selectedChange.emit(freeBet);
        this.dialogService.closeDialog(DialogService.API.selectFreeBetDialog);
      }
    });
    const  freebetsdata = this.freeBets && this.freeBets.length;
    const  betPackdata = this.betPackList && this.betPackList.length;
    const  fanzonedata = this.fanzoneList && this.fanzoneList.length;
    const freebetText = (freebetsdata> 0 && betPackdata> 0) ? 'add bet token and free bet': ((freebetsdata > 0)||(fanzonedata > 0)) ? 'add free bet' : 'add bet token';
    this.triggerGtmService(this.isStreamAndBet, freebetText);
    this.changeDetectorRef.detectChanges();
  }

  removeFreeBet(): void {
    if(this.isStreamAndBet && this.selection.disabled) {
      return;
    }
    let freeBetOfferCategory = '';
    
    if(this.selected && this.selected.freeBetOfferCategories && this.selected.freeBetOfferCategories.freebetOfferCategory) {
      freeBetOfferCategory = this.selected.freeBetOfferCategories.freebetOfferCategory;
    }
    if(!freeBetOfferCategory && (this.selection && this.selection.freeBetOfferCategory)) {
      freeBetOfferCategory = this.selection.freeBetOfferCategory;
    }
    this.triggerGtmService(this.isStreamAndBet,this.freeBetsFactory.isBetPack(freeBetOfferCategory)? 'remove bet token' : 'remove free bet');
    this.selectedChange.emit(null);
  }

  get value() {
    const fbCategory = this.freeBetsFactory.isBetPack(this.selected.freeBetOfferCategories?.freebetOfferCategory) ? this.selected.freeBetOfferCategories.freebetOfferCategory : '';
    const fanzoneCategory = this.freeBetsFactory.isFanzone(this.selected.freeBetOfferCategories?.freebetOfferCategory) ? this.selected.freeBetOfferCategories.freebetOfferCategory : '';
    return (this.filtersService.setFreebetCurrency(this.selected.value) + ' ' + (fbCategory ? this.freebetsConfig.betTokenAdded :fanzoneCategory?  this.freebetsConfig.fanZoneAdded : this.freebetsConfig.freeBetAdded));
  }

  /**
   *
   * @returns {string}
   * This value displays in Desktop & Tablet betslip underneath input stake
   */

  freebetImage(){
    if(this.selected){
      this.freeBetImageNameSvg= this.freeBetsFactory.isFanzone(this.selected&& this.selected.freebetOfferCategories?.freebetOfferCategory) ? 'fanzone-bet-label' : 'free-bet-label';
    }else{
      this.freeBetImageNameSvg = (!(this.freeBets && this.freeBets.length> 0) && (this.fanzoneList && this.fanzoneList.length > 0)  )?'fanzone-bet-label':'free-bet-label'
    }

  }
  /**
   * @returns {string}
   * This value displays in Mobile (betslip & Quickbet) & Tablet Quickbet
   */
freebetButtonText(isMobile:boolean=false):string{
  const  freebetsdata = this.freeBets && this.freeBets.length;
  const  betPackdata = this.betPackList && this.betPackList.length;
  const  fanzonedata = this.fanzoneList && this.fanzoneList.length;
  this.freebetImage();
  if(isMobile){
    return (freebetsdata> 0 && betPackdata> 0) ? this.freebetsConfig.plusTokenAndFreeBet : ((freebetsdata > 0)||(fanzonedata > 0)) ? this.freebetsConfig.plusFreeBet : (betPackdata> 0) ? this.freebetsConfig.plusToken : '';
  }  
  return (freebetsdata > 0 && betPackdata> 0) ? this.freebetsConfig.addTokenAndFreeBet : ((freebetsdata > 0)||(fanzonedata > 0)  ) ? this.freebetsConfig.addFreeBet : (betPackdata> 0) ? this.freebetsConfig.addBetToken : '';
}
  /**
   * @return  {string}
   * @memberof FreeBetToggleComponent
   */
  removeFreebetButtonText(): string{
    this.freebetImage();
    return this.freeBetsFactory.isBetPack(this.selected?.freebetOfferCategories?.freebetOfferCategory) ? this.freebetsConfig.betTokenAdded : this.freebetsConfig.freeBetAdded;
   }

  /**
  * 
  * @returns frebbet button title {String}
  */
  private getEventdetails(): string {
    
    if (!this.showOnDigitKeyborad && !this.selected && !this.isMobile) {
      return this.freebetButtonText();
    }

    if (this.showOnDigitKeyborad) {
      return this.selected ? this.removeFreebetButtonText() : this.freebetButtonText(true);
    }

    if (!this.showOnDigitKeyborad && this.selected) {
      return this.value;
    }

    return '';
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
}
