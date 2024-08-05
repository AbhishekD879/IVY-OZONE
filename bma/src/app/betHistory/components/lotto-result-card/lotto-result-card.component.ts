import { Component, Input, OnInit } from '@angular/core';
import { IBall, ILotteryResult } from '@app/betHistory/models/lotto.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { UserService } from '@app/core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';
import { TimeService } from '@core/services/time/time.service';



@Component({
  selector: 'lotto-result-card',
  templateUrl: './lotto-result-card.component.html',
  styleUrls: ['./lotto-result-card.component.scss']
})
export class LottoResultCardComponent implements OnInit {

  @Input() lottoResult: ILotteryResult = {} as ILotteryResult;
  @Input() index: number  = null;
  @Input() settled: string ;

  returned:string;
  drawResults:string;
  currency :string;
  isBrandLadbrokes: boolean;
  drawAt :Date |number | string;
  
  constructor(
    private locale: LocaleService,
    private userService: UserService,
    private timeService: TimeService
  ) { }

  trackByBall(index: number, item: IBall): string {
    return `${index}${item.ballNo}`;
  }

  ngOnInit(): void {
    this.returned =  this.locale.getString(bma.returned);
    this.drawResults = this.locale.getString(bma.drawresults);
    this.currency = this.userService.currencySymbol
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
     this.drawAt = this.settled == "Y" ? this.timeService.convertDateStr(this.lottoResult.settledAt) : this.timeService.convertDateStr(this.lottoResult.drawAt);
  }

}
