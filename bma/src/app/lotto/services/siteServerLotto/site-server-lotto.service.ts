
import { map } from 'rxjs/operators';
// import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { ILotto } from './../../models/lotto.model';
import { HttpResponse, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { BuildLotteriesService } from '../buildLotteries/build-lotteries.service';
// import { TimeService } from '@core/services/time/time.service';
import { ILottoResult } from '@app/lotto/models/lotto-result.model';

@Injectable()
export class SiteServerLottoService {

  constructor(
    private http: HttpClient,
    private buildLotteries: BuildLotteriesService,
    // private timeService: TimeService,
    // private simpleFilters: SimpleFiltersService
  ) {
  }

  getLotteries(): Observable<ILotto[]> {
    /* eslint-disable */
    const endpointUrl =
      `${environment.SITESERVER_LOTTERY_ENDPOINT}/LotteryToDraw?simpleFilter=lottery.hasOpenDraw&translationLang=en&responseFormat=json`;
    return this.sendRequest(endpointUrl).pipe(map((response) => {
      return this.buildLotteries.build(response.body);
    }));
  }

  // getLottoResults(data: { lottoIds: string[], page: number }): Observable<ILottoResult[]> {
  //   const simpleFilter = this.simpleFilters.genFilters({
  //     resultedDrawFrom: this.timeService.getTimeWithDelta(data.page * 7),
  //     resultedDrawTo: this.timeService.getTimeWithDelta((data.page - 1) * 7)
  //   });

  //   /* eslint-disable */
  //   const endpointUrl =
  //     `${environment.SITESERVER_HISTORIC_ENDPOINT}/ResultsForLottery/${data.lottoIds.join(',')}?${simpleFilter}&translationLang=en&responseFormat=json`;
  //   /* eslint-enable */
  //   return this.sendRequest(endpointUrl).pipe(map((response: HttpResponse<ILottoResult[]>) => {
  //     return this.buildLotteries.buildLottoResults(response.body);
  //   }));
  // }

  getLottoPreviousResultsFromDate(data: { lottoId: string, page: number,startDate:string,endDate:string }): Observable<any> {
    /* eslint-disable */
    const endpointUrl =
      `${environment.SITESERVER_HISTORIC_ENDPOINT}/ResultsForLottery/${data.lottoId}/${data.startDate}/${data.endDate}&translationLang=en&responseFormat=json`;
    return this.sendRequest(endpointUrl).pipe(map((response: HttpResponse<ILottoResult[]>) => {
      return this.buildLotteries.buildLottoResults(response.body);
    }));
  }

  private sendRequest<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(url, {
      observe: 'response',
      params: params
    });
  }
}
