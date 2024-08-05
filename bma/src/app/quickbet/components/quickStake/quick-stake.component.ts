import {
  Component,
  Input,
  OnInit,
  OnDestroy,
  Output,
  EventEmitter,
  ChangeDetectorRef
} from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import { CmsService } from '@app/core/services/cms/cms.service';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
@Component({
  selector: 'quick-stake',
  templateUrl: 'quick-stake.component.html',
  styleUrls: ['quick-stake.component.scss'],
})
export class QuickStakeComponent implements OnInit, OnDestroy {

  @Input() betslipType: string;
  @Input() disabled?: boolean;
  @Input() freebetsList: IFreebetToken[];
  @Input() selectedFreeBet: IFreebetToken;
  @Input() freebetsConfig: IFreebetsPopupDetails;
  @Input() isBoostEnabled: boolean;
  @Input() isSelectionBoosted: boolean;
  @Input() canBoostSelection: boolean;
  @Input() betPackList: IFreebetToken[];
  @Input() fanzoneList: IFreebetToken[];
  @Input() quickStakeVisible: boolean;

  @Output() fbChange: EventEmitter<ILazyComponentOutput> = new EventEmitter();
  @Output() readonly quickStakeSelect: EventEmitter<string> = new EventEmitter();

  quickStakePrefix: string;
  quickStakeItems: string[];

  private readonly title = 'QuickStakeController';
  private readonly globalStake = 'global_stakes';
  clicked: boolean = false;
  branchcheck: boolean;
  isStakesAvailable: boolean;


  constructor(
    private user: UserService,
    private pubsubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private cmsService: CmsService,
    private locale: LocaleService,
    private windowRef: WindowRefService
  ) {
    this.quickStakePrefix = `+${this.user.currencySymbol}`;
    this.quickStakeItems = ['5', '10', '50', '100'];

    this.reformatKrCurrency = this.reformatKrCurrency.bind(this);
  }

  ngOnInit(): void {
    this.cmsService.getQuickStakes(this.betslipType).subscribe((predefinedStakes: string[]) => {
        this.isStakesAvailable = predefinedStakes?true:false;
        this.quickStakeItems = predefinedStakes;
        this.changeDetectorRef.markForCheck();
        this.formatquickbetStakes(this.quickStakeItems);
      
    });
    this.reformatKrCurrency = this.reformatKrCurrency.bind(this);
    this.pubsubService.subscribe(this.title, [this.pubsubService.API.SESSION_LOGIN,
    this.pubsubService.API.SESSION_LOGOUT], this.reformatKrCurrency);
  }
    /**
   * @param  {string[]} quickStakeItems
   */
    formatquickbetStakes(quickStakeItems: string[]) {
      this.quickStakePrefix = `+${this.user.currencySymbol}`;
      this.quickStakeItems = quickStakeItems.map((stake: string) => {
        const dec = stake.split('.');
        if (dec.length > 1) {
          dec[1] = dec[1].substring(0, 2);
          stake = dec.join(".");
        }
        return stake;
      });
    }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.title);
  }

  setQuickStake(value: string,stakeIndex: number): void {
    this.quickStakeSelect.emit(value);
    this.clickTransition(stakeIndex);
  }
  clickTransition(stakeIndex: number) {
    this.branchcheck = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    const element = this.windowRef.document.getElementsByClassName(`price-button-${stakeIndex}`) as any;
    [].forEach.call(element, (el) => {
      el["style"].backgroundColor = this.branchcheck ? "#AAAAAA" : "#084D8D";
    })
    setTimeout(() => {
      const removeClass = this.windowRef.document.getElementsByClassName(`price-button-${stakeIndex}`);
      [].forEach.call(removeClass, (el) => {
        el["style"].backgroundColor = "#252835";
      })
    }, 250);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  onFreebetChange(event: ILazyComponentOutput): void {
    this.fbChange.emit(event);
  }

  /**
   * Reformats quick stake values for currency
   * @private
   */
  private reformatKrCurrency(): void {
    const radix = 10;

    this.quickStakePrefix = `+${this.user.currencySymbol}`;

    if (this.user.currencySymbol === 'Kr') {
      if (!this.isFormatted()) {
        this.quickStakeItems = this.quickStakeItems.map(num => (parseInt(num, radix) * 10).toString());
      }
    } else {
      this.quickStakeItems = this.quickStakeItems.map(num => (num).toString());
    }

    this.changeDetectorRef.markForCheck();
  }

  /**
   * Is quick stake already formatted
   * @private
   */
  private isFormatted(): boolean {
    return Number(this.quickStakeItems.length && this.quickStakeItems[0]) % 10 === 0;
  }
}

