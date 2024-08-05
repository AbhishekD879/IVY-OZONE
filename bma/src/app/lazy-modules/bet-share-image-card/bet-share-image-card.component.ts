import { Component, ComponentFactoryResolver, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { ShareToSocialMediaDialogComponent } from './shareToSocialMediaDialog/share-to-social-media-dialog.component';
import { ICashOutData } from '@app/betHistory/models/cashout-section.model';
import { CmsService } from '@core/services/cms/cms.service';
import { DeviceService } from '@core/services/device/device.service';
import { IBetHistoryPoolBet } from '@app/betHistory/models/bet-history.model';
import TotePoolBet from '@app/betHistory/betModels/totePoolBet/tote-pool-bet.class';
import { BetShareImageCardService } from './services/bet-share-image-card.service';
import { IBetShare } from '@app/betHistory/models/bet-share.model';
import { BetShareGTAService } from './services/bet-share-gta-tracking.service';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'bet-share-image-card',
  templateUrl: './bet-share-image-card.component.html',
  styleUrls: ['./bet-share-image-card.component.scss']
})
export class BetShareImageCardComponent implements OnInit {

  @Input() bets: ICashOutData[] | IBetHistoryPoolBet[] | TotePoolBet[];
  // need to add type ICashOutData | IBetHistoryPoolBet in bet
  @Input() bet: any;
  @Input() sportType: string;
  @Input() currencySymbol: string;
  openBetStatus: boolean;
  wonBetStatus: boolean;
  betId: string;
  betDate: string;
  betSettled: boolean;
  time: string[] = [];
  selectionNamesData: string[] = [];
  showSettledShareIcon: boolean;
  showOpenBetsShareIcon: boolean;
  cmsData: IBetShare;
  dataForming: string;
  params: any;
  shareData: any;
  loading: boolean;
  dialog: ShareToSocialMediaDialogComponent;
  settledBetsCheck: boolean;
  betStatusControlData: string;
  betDataToShare: any;
  flags: any = {};
  brand: string;
  bridge: any;
  isNativeBetSharingAllowed: boolean = true;
  legType: boolean;

  constructor(
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected dialogService: DialogService,
    private cmsService: CmsService,
    protected deviceService: DeviceService,
    private betShareImageCardService: BetShareImageCardService,
    private betShareGTAService: BetShareGTAService,
    private windowRef: WindowRefService) {
      this.brand = environment && environment.brand;
      this.bridge = this.windowRef.nativeWindow.NativeBridge;
  }

  ngOnInit(): void {
    if (this.deviceService.isAndroid && this.deviceService.isWrapper) {
      this.isNativeBetSharingAllowed = _.isFunction(this.bridge.shareContentOnSocialMediaGroups);
    }

    this.cmsService.fetchBetShareConfigDetails().subscribe((data) => {
      this.cmsData =data;
      this.betId = this.bet.eventSource ? this.bet.eventSource.betId : this.bet.id;
      this.betDate = this.bet.eventSource ? this.bet.eventSource.date : this.bet.date;
      this.betSettled = this.bet.eventSource ? this.bet.eventSource.settled === 'Y' : this.bet.isSettled ? this.bet.isSettled : this.bet.settled === 'Y';
      this.showSettledShareIcon = this.betSettled && ['won','lost','cashed out'].includes((this.bet.eventSource && this.bet.eventSource.totalStatus) || this.bet.status) && data.wonBetShareCardStatus;
      this.showOpenBetsShareIcon = !this.betSettled && data.openBetShareCardStatus;
      this.legType = (this.sportType === 'regularBets') ? (this.bet.eventSource && this.bet.eventSource.legType === 'E') : false;
    });
  }

  shareToMedia(): void {
    this.selectionNamesData = [];
    this.time = [];
    this.sportType = this.sportType.includes('pools') ? this.bet.isTotePoolBetBetModel ? 'totePoolBet' : this.bet.isTotePotPoolBetBetModel ? 'totePotPoolBet' : 'jackPotPool' : this.sportType;
    if (this.sportType === 'totePoolBet') {
      this.bet.orderedOutcomes.forEach((outcome, index) => {
        this.selectionNamesData.push(this.betShareImageCardService.getOutcomeTitle(this.bet, outcome, index));
      })
    }
    else if (this.sportType === 'jackPotPool') {
      let timeEvent: any;
      this.bet.legs.forEach((leg) => {
        timeEvent = leg.isResulted ? 'FT' : this.betShareImageCardService.getEventStartTime(leg)
        this.time.push(timeEvent);
      })
    }
    this.onShareClicked();
    this.prepareGTMObject();
  }

  onShareClicked(): void {
    this.params = {
      betData: this.bet,
      sportType: this.sportType,
      bets: this.bets,
      marketName: this.selectionNamesData,
      eventTime: this.time,
      currencySymbol: this.currencySymbol
    };
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(ShareToSocialMediaDialogComponent);
    this.dialogService.openDialog(DialogService.API.shareToSocialMediaDialog, componentFactory, true, {
      data: this.params
    });
  }

  private prepareGTMObject(): void {
    const isSettled = ((this.bet.eventSource && this.bet.eventSource.settled ) || this.bet.settled || this.bet.bet.settled);
    const positionEvent = ( this.bet.location === "cashOutSection" ) ? 'cash out' : ( isSettled === 'Y' ? 'settled bets': 'open bets' );
    const gtaSportType = this.sportType === 'regularBets'? 'sports' : (this.sportType === 'totePotPoolBet'? 'pools': this.sportType) 
    this.betShareGTAService.setGtmData(positionEvent, gtaSportType, 'share');
  }
}
