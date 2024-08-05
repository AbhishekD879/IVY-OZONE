import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { UserService } from '@core/services/user/user.service';
import { BetSummaryComponent } from '@app/quickbet/components/betSummary/bet-summary.component';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';

@Component({
  selector: 'bet-summary',
  templateUrl: './bet-summary.component.html',
  styleUrls: ['./bet-summary.component.scss']
})
export class LadbrokesBetSummaryComponent extends BetSummaryComponent implements OnInit, OnDestroy {
  @Input() isQuickdeposit?: boolean;
  isGermanUser: boolean;

  constructor(user: UserService,
              currencyPipe: CurrencyPipe,
              bppProviderService: BppProvidersService,
              private germanSupportService: GermanSupportService,
              private pubSubService: PubSubService) {
    super(user, currencyPipe, bppProviderService);
  }

  ngOnInit(): void {
    this.isGermanUser = this.germanSupportService.isGermanUser();
    this.pubSubService.subscribe('QuickbetSummary',
      [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
        this.isGermanUser = this.germanSupportService.isGermanUser();
      }
    );
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('QuickbetSummary');
  }

  /**
   * Set specific color for quickbet-info-spot background
   */
  get quickdepositClass(): string {
    return this.isQuickdeposit ? 'quickdeposit-info-spot' : '';
  }
  set quickdepositClass(value:string){}
}
