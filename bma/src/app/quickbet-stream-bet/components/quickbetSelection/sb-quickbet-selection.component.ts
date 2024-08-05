import {
  Component, ChangeDetectorRef, Input
} from '@angular/core';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetUpdateService } from '@app/quickbet/services/quickbetUpdateService/quickbet-update.service';
import { QuickbetDepositService } from '@quickbetModule/services/quickbetDepositService/quickbet-deposit.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { TimeService } from '@app/core/services/time/time.service';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';

import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { QuickbetSelectionComponent } from '@app/quickbet/components/quickbetSelection/quickbet-selection.component';
import { CurrencyPipe } from '@angular/common';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'sb-quickbet-selection',
  templateUrl: 'sb-quickbet-selection.component.html',
  styleUrls: ['sb-quickbet-selection.component.scss']
})

export class SbQuickbetSelectionComponent extends QuickbetSelectionComponent {

  @Input() isStreamAndBet?: boolean;
  @Input() isBrandLadbrokes: boolean;
  @Input() categoryName: string;
  @Input() eventName: string;

  prevMaxPayout = false;
  showKeyboard = true;

  constructor(pubsub: PubSubService,
    user: UserService,
    locale: LocaleService,
    filtersService: FiltersService,
    quickbetDepositService: QuickbetDepositService,
    quickbetService: QuickbetService,
    quickbetUpdateService: QuickbetUpdateService,
    freeBetsFactory: FreeBetsService,
    quickbetNotificationService: QuickbetNotificationService,
    commandService: CommandService,
    cmsService: CmsService,
    gtmService: GtmService,
    cdr: ChangeDetectorRef,
    windowRef: WindowRefService,
    timeService: TimeService,
    bppProviderService: BppProvidersService,
    fiveASideContestSelectionService: FiveASideContestSelectionService,
    serviceClosureService: ServiceClosureService,
    sessionStorageService: SessionStorageService,
    storageService: StorageService,
    private currencyPipe: CurrencyPipe,
    protected bonusSuppressionService: BonusSuppressionService
    ) {
      super(pubsub, user, locale, filtersService, quickbetDepositService, quickbetService, quickbetUpdateService,
        freeBetsFactory, quickbetNotificationService, commandService, cmsService, gtmService, cdr, windowRef,
        timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService,
        sessionStorageService, storageService, bonusSuppressionService);
    }
  ngOnInit(): void {
    super.ngOnInit();
    this.pubsub.subscribe('this.uuid', this.pubsub.API.DIGIT_KEYBOARD_KEY_PRESSED,
      (value)=> { // refine this later
        if (!this.selection.stake && value !== 'delete') {
          if(value === '.'){
            this.selection.stake = '0.';
          }else if(value.includes('qb-')) {
            this.selection.stake = value.slice(3);
          } else {
            this.selection.stake = value;
          }
        } else if(value === 'delete') {
          if(this.selection.stake.length === 0)
            return;

          this.selection.stake = this.selection.stake.slice(0,-1);
        } else if(value.includes('qb-')) {
          this.selection.stake = (Number.parseFloat(this.selection.stake) + Number.parseFloat(value.slice(3))).toString();
        } else if(this.selection.stake.includes('.')) {
          if (value === '.' || (this.selection.stake.length && this.selection.stake[this.selection.stake.length - 3] === '.')){
            return;
          }  
          this.selection.stake += value;
        } else {
          if (this.selection.stake === '0' && value !== '.') {
            this.selection.stake = value;
            return;
          } else if(this.selection.stake.length >= 5 && value !== '.'){
            return;
          }

          this.selection.stake += value;
        }

        this.onStakeChange();
    });

    this.quickbetService.quickBetOnOverlayCloseSubj.subscribe(qbStatusMsg => {
      if(qbStatusMsg === 'fullscreen exit') {
        this.closeFnHandler();
      }
    });
  }

  /**
   * @param  {boolean} newItem
   * @returns void
   */
  addItem(newItem: boolean): void {
    let snbMaxPayoutMsg = this.maxPayMsg.split(',')[0];
    snbMaxPayoutMsg = snbMaxPayoutMsg + ` & Max Payout value is ${this.currencyPipe.
      transform(this.selection.maxPayout, this.user.currencySymbol, 'code')}`;
    if (this.prevMaxPayout !== newItem && snbMaxPayoutMsg) {
      if (newItem)
        this.quickbetNotificationService.snbMaxPayoutMsgSub.next(snbMaxPayoutMsg);
      else
        this.quickbetNotificationService.snbMaxPayoutMsgSub.next('');

      this.prevMaxPayout = newItem;
    }
  }

  showFreeBet(){
    return (this.freebetsList && this.freebetsList.length > 0 || this.betPackList && this.betPackList.length > 0);
  }

  placeBetFnHandler(): void {
    this.showKeyboard = false;
    super.placeBetFnHandler();
  }

  onStakeElemClick(){
    if(!this.showKeyboard)
      this.showKeyboard = true;
  }
}
