import { finalize } from 'rxjs/operators';
import { Component, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { Router } from '@angular/router';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IFreebetToken, IFreebetGroup } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IStaticBlock } from '@core/services/cms/models';
import { Subscription } from 'rxjs';
import { StorageService } from '@core/services/storage/storage.service';

@Component({
  selector: 'freebets',
  templateUrl: './freebets.component.html'
})
export class FreebetsComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  freebets: IFreebetToken[];
  Fanzonefreebets : IFreebetToken[];
  freebetsGroup: IFreebetGroup;
  fanzonegroup : IFreebetGroup;
  totalFreeBetsAmount: string;
  totalFreeBets: string;
  sportBalance: string;
  totalBalance: string;
  readonly sports = 'ALL SPORTS';

  freeBetText: string = this.localeService.getString('bma.freeBet');
  validOn: string = this.localeService.getString('bma.validOn');
  freebetsHelperText: IStaticBlock;

  private freebetsSubscription: Subscription;

  constructor(
    protected userService: UserService,
    protected filtersService: FiltersService,
    protected freeBetsService: FreeBetsService,
    protected router: Router,
    private localeService: LocaleService,
    private cmsService: CmsService,
    private storageService: StorageService
  ) {
    super();
  }

  ngOnInit(): void {
    this.freeBetsService.getFreeBets().pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((data: IFreebetToken[]) => {
        this.freebets = data ? data.filter(bet => {
          return (bet.tokenPossibleBetTags && bet.tokenPossibleBetTags.tagName) ? bet.tokenPossibleBetTags.tagName !== 'FRRIDE' : bet;
        }) : [];
        this.availableTotefreebets(this.freebets);
        this.totalFreeBetsAmount = this.getTotalFreeBetsBalance();
        this.totalFreeBets = this.addCurrencySymbol(this.totalFreeBetsAmount);
        this.totalBalance = this.getTotalBalance();
        this.freebets.length && this.groupByName();
        this.extendFreebetsData();
        this.sportBalance = this.addCurrencySymbol(this.userService.sportBalance);
      }, () => {
        if (!this.userService.status) {
          this.router.navigate(['/']);
        } else {
          this.showError();
        }
      });

      this.cmsService.getFreebetsHelperText()
      .subscribe((data: IStaticBlock) => this.freebetsHelperText = data);
  }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  indexNumber(index: number): number {
    return index;
  }

  navigateToEvent(freeBet: IFreebetToken): void {
    freeBet.pending = true;
    this.freeBetsService.getFreeBetWithBetNowLink(freeBet).pipe(
      finalize(() => {
        freeBet.pending = false;
      })).subscribe((freeBetItem: IFreebetToken ) => {
      this.router.navigateByUrl(freeBetItem.betNowLink);
    }, () => {});
  }

  stopOuterAction($event: Event): void {
    $event.stopPropagation();
  }

  trackByTokenId(index: number, item: IFreebetToken): number {
    return +item.freebetTokenId;
  }

  ngOnDestroy(): void {
    this.freebetsSubscription && this.freebetsSubscription.unsubscribe();
  }

  /**
   * Returns total user's total balance combined with sport and free bets balances.
   * @return {string}
   */
  private getTotalBalance(): string {
    return this.addCurrencySymbol(Number(this.userService.sportBalance) + Number(this.totalFreeBetsAmount));
  }

  /**
   * Formats given value with currency filter.
   * @param {string|number} value
   * @return {string}
   * @private
   */
  private addCurrencySymbol(value: string | number): string {
    return this.filtersService.setCurrency(value, this.userService.currencySymbol);
  }

  /**
   * Extends free bets list with redirection url and formatted freebet value.
   * @param {Array} freebets The list of freebet objects.
   * @return {Array}
   * @private
   */
  private extendFreebetsData() {
    _.each(this.freebets, (freebet: IFreebetToken) => {
      freebet.redirectUrl = `/freebets/${freebet.freebetTokenId}`;
      freebet.amount = this.addCurrencySymbol(freebet.freebetTokenValue);
    });
  }

  /**
   * Format freebets based on sports it's applicable
   * @param {Array} freebets the lis of freebet objects
   * @return {IFreebetGroup}
   */
  private groupByName() {
     this.freebetsSubscription = this.freeBetsService.groupByName(this.freebets,false).subscribe((groupedFreeBets: IFreebetGroup) => this.freebetsGroup = groupedFreeBets);
  }

  /**
   * Calculates total free bets balance.
   * @param {Array} freeBets
   * @returns {string}
   * @private
   */
  private getTotalFreeBetsBalance(): string {
    const totalPrize = _.reduce(this.freebets || [], (sum, bet) => sum + parseFloat(bet.freebetTokenValue), 0);
    return totalPrize.toFixed(2);
  }
  /**
   * get labeltext value 
   * @param freeBetType 
   * @returns {string}
   */
  public getLabelText(freeBetType:string):string{
    return (this.freeBetsService.isFanzone(freeBetType))?this.localeService.getString('bma.fanZoneFreebet'):freeBetType;
  } 
  /**
   * get available totefreebets
   * @param freebets
   */
  private availableTotefreebets(freebets){
    const usedTotes = this.storageService.get('usedToteFreebets') || [];
    this.freebets = freebets ? freebets.filter(bet => {
      return (!usedTotes.includes(bet.freebetTokenId));
    }) : [];
  }
}
