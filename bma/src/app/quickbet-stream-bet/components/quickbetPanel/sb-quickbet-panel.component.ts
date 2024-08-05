import {
  Component,
  ViewEncapsulation,
  ChangeDetectorRef,
  Input
} from '@angular/core';
import { Router } from '@angular/router';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { QuickbetService, SbQbFreeBetData } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetDepositService } from '@quickbetModule/services/quickbetDepositService/quickbet-deposit.service';
import { QuickbetDataProviderService } from '@app/core/services/quickbetDataProviderService/quickbet-data-provider.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { QuickbetUpdateService } from '@app/quickbet/services/quickbetUpdateService/quickbet-update.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { YourcallMarketsService } from '@app/yourCall/services/yourCallMarketsService/yourcall-markets.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { UserService as User } from '@core/services/user/user.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { GtmService } from '@core/services/gtm/gtm.service';
import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';
import { BetReceiptService } from '@app/betslip/services/betReceipt/bet-receipt.service';

@Component({
  selector: 'sb-quickbet-panel',
  templateUrl: 'sb-quickbet-panel.component.html',
  styleUrls: ['sb-quickbet-panel.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class SbQuickbetPanelComponent extends QuickbetPanelComponent {
  @Input() isStreamAndBet?: boolean;
  @Input() market: IMarket;
  @Input() categoryName: string;
  @Input() eventName: string;

  finalStake: string;
  returns: string;
  freeBetData: SbQbFreeBetData;
  outcome: IOutcome;
  isBrandLadbrokes: boolean;
  odds: string;
  isReceiptAvailable: boolean = false;

  constructor(
    rendererService: RendererService,
    pubsub: PubSubService,
    userService: UserService,
    locale: LocaleService,
    quickbetDepositService: QuickbetDepositService,
    device: DeviceService,
    infoDialog: InfoDialogService,
    quickbetService: QuickbetService,
    quickbetDataProviderService: QuickbetDataProviderService,
    quickbetNotificationService: QuickbetNotificationService,
    cmsService: CmsService,
    windowRefService: WindowRefService,
    domToolsService: DomToolsService,
    router: Router,
    quickbetUpdateService: QuickbetUpdateService,
    changeDetectorRef: ChangeDetectorRef,
    arcUserService: ArcUserService,
    nativeBridgeService: NativeBridgeService,
    serviceClosureService: ServiceClosureService,
    yourCallMarketService: YourcallMarketsService,
    dialogService: DialogService,
    sessionStorageService: SessionStorageService,
    user: User,
    private filtersService: FiltersService,
    protected gtmService: GtmService,
    protected quickDepositIframeService: QuickDepositIframeService,
    protected betReciptService: BetReceiptService,
  ) {
    super(rendererService, pubsub, userService, locale, quickbetDepositService, device, infoDialog,
      quickbetService, quickbetDataProviderService, quickbetNotificationService, cmsService, windowRefService,
      domToolsService, router, quickbetUpdateService, changeDetectorRef, arcUserService, nativeBridgeService,
      serviceClosureService, yourCallMarketService, dialogService, sessionStorageService, user, quickDepositIframeService);
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.quickbetService.qbReceiptDataSubj.subscribe(receiptDataObj => {
      this.finalStake = receiptDataObj.stake;
      this.returns = receiptDataObj.returns;
      this.odds = receiptDataObj.odds;
      this.freeBetData = receiptDataObj.freeBetData;
      this.isReceiptAvailable = !!(this.finalStake || this.odds || this.returns);
    });
    this.outcome = this.market.outcomes.find(outcome => outcome.id === this.selection.outcomeId);
  }

  // try to refine this later
    /**
   * Filter outcome names
   * @param {string} name
   * @returns {string}
   */
    filterPlayerName(name: string): string {
      return name && this.filtersService.filterPlayerName(name);
    }

  // try to refine this later
    filterAddScore(marketName: string, outcomeName: string) {
      return marketName && outcomeName && this.filtersService.filterAddScore(marketName, outcomeName);
    }
  
      /**
   * Closes panel.
   */
  closePanel(): void {
    this.gtmService.push('Event.Tracking', {
      'event': 'Event.Tracking',
      'component.CategoryEvent': 'video streaming',      
      'component.LabelEvent': 'stream and bet',      
      'component.ActionEvent': 'close',      
      'component.PositionEvent': this.categoryName,      
      'component.LocationEvent':this.eventName,   
      'component.EventDetails': 'quick bet',      
      'component.URLClicked': 'not applicable',      
      'component.ContentPosition':'not applicable'    
    });
    super.closePanel();
    this.quickbetService.quickBetOnOverlayCloseSubj.next('close qb panel');
  }
  
}
