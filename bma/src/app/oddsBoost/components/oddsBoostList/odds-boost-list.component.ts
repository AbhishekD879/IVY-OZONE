import { Component, EventEmitter, Input, OnChanges, OnDestroy, Output, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { OddsBoostService } from '@oddsBoostModule/services/odds-boost.service';

import { CurrencyPipe } from '@angular/common';
import { IFreebetToken, IFreebetExpiredTokenIds } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { map } from 'rxjs/operators';
import { UserService } from '@core/services/user/user.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';


@Component({
  selector: 'odds-boost-list',
  templateUrl: './odds-boost-list.component.html',
  styleUrls: ['./odds-boost-list.component.scss']
})
export class OddsBoostListComponent implements OnChanges, OnDestroy {
  
  sortedBoosts: {[categoryId: string]: IFreebetToken[]} = {};
  tokenExpired: {[key: string]: boolean} = {};
  nextBoost: IFreebetToken;
  timerValue = false;
  
  @Input() tab: boolean;
  @Input() oddsBoosts: IFreebetToken[];
  @Input() type: string;
  @Input() isLads: boolean;
  @Input() timerStart:string;
  @Input() sortedTokensData:IFreebetToken[];
  @Input() expireTokenDetails:{[key: string]: boolean} = {};
  @Output() readonly oddsBoostTokensPills: EventEmitter<{[categoryId: string]: IFreebetToken[]}> = new EventEmitter();
  @Output() readonly leastTimeToken: EventEmitter<string> = new EventEmitter();
  dateValue: number;

  constructor(
    public freeBetsService: FreeBetsService,
    public oddsBoostService: OddsBoostService,
    public userService: UserService,
    public currencyPipe: CurrencyPipe,
    public cmsService: CmsService,
    private windowRef: WindowRefService,
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.oddsBoosts?.currentValue) {
      this.tokenExpired = this.expireTokenDetails;
      this.sortedTokensData = [];
      this.nextBoost = null as IFreebetToken;
      this.freeBetsService
          .getOddsBoostsWithCategories(this.oddsBoosts)
          .pipe(map((data: IFreebetToken[] = []) => {
            const formattedTokens =  data.map((token: IFreebetToken) => {
              const displayArr: string[] = token.freebetTokenDisplayText.split('|');
              token.freebetOfferName = displayArr[0];
              token.freebetOfferDesc = displayArr[1];
              if ((typeof token.freebetMaxStake === 'string' && !token.freebetMaxStake.includes(this.userService.currencySymbol)) ||
                typeof token.freebetMaxStake === 'number') {
                token.freebetMaxStake = this.currencyPipe.transform(
                  Number(token.freebetMaxStake).toFixed(2),
                  this.userService.currencySymbol,
                  'code'
                );
              }
              return token;
            });
            const sortedBoosts = _.groupBy(formattedTokens, oddsBoost => oddsBoost.categoryId ? oddsBoost.categoryId : '0');
            _.each(sortedBoosts, (tokens: IFreebetToken[]) => {
              this.oddsBoostService.sortPageTokens(tokens);
            });
            return sortedBoosts;
          }))
          .subscribe((data: {[categoryId: string]: IFreebetToken[]}) => {
            this.sortedBoosts = data;
            this.oddBoostTokens(data);
            this.oddsBoostTokensPills.emit(data);  
      });
    }
    if(changes['sortedTokensData'] && !changes.sortedTokensData.isFirstChange()){ 
      this.sortedTokensData = changes.sortedTokensData.currentValue;
    }
  }

  objectKeys(obj: Object): string[] {
    return _.keys(obj);
  }

  trackByOddsBoosts(index: number, oddsBoost: IFreebetToken): string {
    return `${index}${oddsBoost.freebetTokenId}`;
  }

  trackByCategory(index: number, category: string) {
    return `${index}_${category}`;
  }
  
  /* get oddsboost token info based on categaory Id **/
  public oddBoostTokens(data: { [categoryId: string]: IFreebetToken[] }) {
    for (const key in data) {
      const sportTokens = data[key];
      sportTokens.forEach((sportToken: IFreebetToken) => {
        this.leastTimeTokenInfo(sportToken);
      });
    }
  }

  /* return oddBoost token date **/
  countDownTimer(oddBoost: IFreebetToken): Date {
    const date = this.tab ? 'freebetTokenExpiryDate' : 'freebetTokenStartDate';
    return new Date(oddBoost[date]);
  }
  
  /* enit expired oddsboost tokens id's **/
  expireTokenInfo(event:IFreebetExpiredTokenIds): void {
    const tokenExpire = event.freebetTokenId;
    this.tokenExpired[tokenExpire] = event.tokenExpire;
  }
  
  /* find least time oddsboost token **/
  leastTimeTokenInfo(oddBoost: IFreebetToken) {
    const date = this.tab ? 'freebetTokenExpiryDate' : 'freebetTokenStartDate';
    if (!this.nextBoost) {
      this.nextBoost = oddBoost;
    }
    const oddsBoostStartDate = new Date(oddBoost[date]);
    const nextBoostStartDate = new Date(this.nextBoost[date]);

    this.nextBoost = oddsBoostStartDate < nextBoostStartDate ? oddBoost : this.nextBoost;
    if (this.nextBoost.freebetTokenId == oddBoost.freebetTokenId) {
      const dateValue = this.windowRef.nativeWindow.setInterval(() => {
        if (this.timerValue) {
          this.windowRef.nativeWindow.clearInterval(dateValue);
        }
        this.leastTimeToken.emit(this.nextBoost[date]);
      }, 400);
    }
  }

  /* clear time interval **/
  public clearTimer() {
    this.timerValue = true;
  }

  ngOnDestroy(): void {
    this.clearTimer();
  }
}
