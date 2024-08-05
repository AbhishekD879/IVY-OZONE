import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';

import { TimeService } from '@core/services/time/time.service';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ILottoBet, ILottoModel, IBall } from '@app/betHistory/models/lotto.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { BetHistoryMainService } from './../../services/betHistoryMain/bet-history-main.service';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { CurrencyPipe } from '@angular/common';
import { betHistoryConstants } from '@app/betHistory/constants/bet-history.constant';
import { ICelebration } from '@app/betHistory/models/bet-history.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISvgItem } from '@app/core/services/cms/models';

@Component({
  selector: 'lotto-bets',
  styleUrls: ['./lotto-bets.component.scss'],
  templateUrl: './lotto-bets.component.html'
})
export class LottoBetsComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnChanges {
  @Input() lottoBets: ILottoBet[];
  @Input() isMyBetsInCasino: boolean;
  @Input() isSportIconEnabled: boolean;
  @Input() isBetHistoryTab: boolean;
  @Input() settled: string = 'N';
  lottoHistory: ILottoModel[] = [];
  noBetsMessage: string;
  emptyBalls = new Array(5).fill({ ballNo: '-' } as IBall);
  sportIconSvgId: string = '';
  isBrandLadbrokes: boolean;
  celebration: ICelebration = {
    congratsBannerImage: '',
    displayCelebrationBanner: false,
    celebrationMessage: '',
    winningMessage: '',
    cashoutMessage: '',
    duration: 0
  };
  readonly env = environment;
  readonly LADBROKES: string = bma.brands.ladbrokes;
  private readonly cashoutStatus: string = betHistoryConstants.celebratingSuccess.cashoutStatus;

  constructor(
    private betHistoryMainService: BetHistoryMainService,
    private timeService: TimeService,
    private userService: UserService,
    private filtersService: FiltersService,
    private locale: LocaleService,
    private pubSub: PubSubService,
    private cmsService: CmsService,
    private currencyPipe: CurrencyPipe
  ) {
    super();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.lottoBets === undefined) { return; }
    this.generateLottoHistory();
  }

  ngOnInit(): void {
    if(this.isBetHistoryTab) {
      this.celebration = this.betHistoryMainService.getCelebrationBanner();
    }
    this.noBetsMessage = this.locale.getString('bethistory.noLottoBets');
    this.pubSub.publish('UPDATE_SETTLED_BETS_HEIGHT', this.lottoBets.length);
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  trackByBall(index: number, item: IBall): string {
    return `${index}${item.ballNo}`;
  }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  trackByBet(index: number, item: ILottoModel): string {
    return `${index}${item.id}${item.betReceiptId}`;
  }

  /**
   * Generate Lotto History
   * @private
   */
  calcStakeAndEstRetuns(Amt , numSubs){
    return (Number(Amt.value) * (numSubs.numSubs)).toFixed(2);
  }
  
  private generateLottoHistory(): void {
    this.cmsService.getItemSvg('Lotto')
      .subscribe((icon: ISvgItem) => {
        this.sportIconSvgId = icon.svgId ? icon.svgId : "icon-generic";
      });

    this.lottoHistory = _.map(this.lottoBets, (bet: any) => {
      const estReturns = Number(bet.lotterySub.outstandingSubs) == 0  ?  (Number(bet.potentialPayout.value) * bet.lotteryDraws.length).toFixed(2) : this.calcStakeAndEstRetuns(bet.potentialPayout , bet.lotterySub);
      const returns = bet.lotteryDraws.reduce((current, item) => current + parseFloat(item.winnings.value),0.00).toFixed(2);
      const openBetsStake = Number(bet.lotterySub.outstandingSubs) == 0  ? (Number(bet.stake.value) * bet.lotteryDraws.length).toFixed(2) : this.calcStakeAndEstRetuns(bet.stake , bet.lotterySub);
      const settledBetStake = (Number(bet.stake.value) * bet.lotteryDraws.length).toFixed(2);
      const betStatus = this.settled === 'Y' ? this.betHistoryMainService.getLottoBetStatus(bet.lotteryDraws.filter(item => item.settled === this.settled)) : 'open';
      const lottoModel: ILottoModel = {
        id: bet.id,
        name: this.filtersService.removeLineSymbol(bet.lotteryName),
        balls: bet.pick,
        drawName: this.filtersService.removeLineSymbol(bet.drawName),
        settledAt:'', 
        betDate: bet.date,
        betReceiptId: bet.lotterySub.subReceipt,
        outstandingSubs : Number(bet.lotterySub.outstandingSubs) > 0,
        stake: this.settled === 'Y' ? settledBetStake : openBetsStake,
        currency: this.userService.currencySymbol,
        status: betStatus,
        settled: this.settled,
        drawDate: bet.lotteryDraws[0].drawAt,
        totalReturns: this.settled === 'Y' ? returns : estReturns,
        lotteryResults: bet.lotteryDraws.filter(lotteryDraw => lotteryDraw.settled === this.settled).map(draw => {
          return {
            ...draw,
            lotteryDrawResult:draw.lotteryDrawResult && draw.lotteryDrawResult.length > 0 ? draw.lotteryDrawResult.map(result => ({
              ...result,
              matched: bet.pick.some(pick => pick.ballNo === result.ballNo)
            })) : this.emptyBalls
          }
        }),
        isShowMore: betStatus === 'won'
      };
      return lottoModel;
    });
  }

  /**
   * Tells whether to show congrats banner or not
   * @param bet 
   */
  isCongratsBannerShown(bet: ILottoModel): boolean {
    const currentDate = new Date(),
    compareDateValue = new Date(this.timeService.getLocalDateFromString(bet.lotteryResults[0].settledAt)),
    timeDiff = Math.abs(currentDate.getTime() - compareDateValue.getTime());
    const hrs = timeDiff/(1000 * 3600);
    return this.celebration?.displayCelebrationBanner && hrs<=this.celebration.duration && Number(bet.stake)<Number(bet.totalReturns);
  }
  /**
   * Returns the winning message with the totalreturns on the bet
   * @param bet 
   */
  getReturnValue(bet: ILottoModel): string {
    return this.celebration?.winningMessage.replace("{amount}", this.currencyPipe.transform(bet.totalReturns, bet.currency, 'code'));
  }
  /**
   * Returns the cashout message with the cashedout amount
   * @param bet
   */
  getCashoutReturnValue(bet: ILottoModel): string {
    return this.celebration?.cashoutMessage.replace("{amount}", this.currencyPipe.transform(bet.totalReturns, bet.currency, 'code'));
  }

  handleToggleMore(bet:any){
    bet.isShowMore = !bet.isShowMore
  }
}


