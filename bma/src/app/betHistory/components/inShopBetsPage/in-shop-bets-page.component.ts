import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';

@Component({
  selector: 'in-shop-bets-page',
  templateUrl: 'in-shop-bets-page.component.html'
})
export class InShopBetsPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  errorMsg: string;
  @Input() betType?: string;
  @Input() fromDate?: string;
  @Input() toDate?: string;

  isMyBetsInCasino: boolean = false;
  isBrandLadbrokes: boolean;
  private cmpName = 'InShopBetsPageComponent';

  constructor(private pubsubService: PubSubService,
              private userService: UserService,
              private localeService: LocaleService,
              private ezNavVanillaService: EzNavVanillaService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.init();
    this.pubsubService.subscribe(this.cmpName, this.pubsubService.API.SESSION_LOGIN, this.init);
    this.isMyBetsInCasino = this.ezNavVanillaService.isMyBetsInCasino;
    this.isBrandLadbrokes = environment.brand === this.localeService.getString(bma.brands.ladbrokes).toLowerCase();
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.cmpName);
  }

  get userStatus(): boolean {
    return this.userService.status;
  }

  set userStatus(value:boolean){}

  private init = () => {
    if (this.userStatus) {
      this.hideSpinner();
      this.hideError();
    } else {
      const page: string = this.localeService.getString('app.betslipTabs.inShopBets').toLowerCase();
      this.errorMsg = this.localeService.getString('app.loginToSeePageMessage', { page });
      this.showError();
    }
  }
}
