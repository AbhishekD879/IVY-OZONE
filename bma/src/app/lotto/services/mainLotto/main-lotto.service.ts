import { of as observableOf, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { SiteServerLottoService } from '../siteServerLotto/site-server-lotto.service';
import { ILotto, ILottoPrice, ILotteryMap, ILottonMenuItem, ILottoDraw, ILottoCms, ILottoCmsPage } from '../../models/lotto.model';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { IDateRangeObject } from '@root/app/betHistory/models/date-object.model';
import { IPageBets } from '@root/app/betHistory/models/bet-history.model';
import { IGetBetHistoryRequest } from '@root/app/bpp/services/bppProviders/bpp-providers.model';
import { ILottoResult } from '../../models/lotto-result.model';
@Injectable()
export class MainLottoService {

  lotteryData: ILotteryMap;
  activeLotto: string;
  lottoCmsBanner: ILottoCms;
  lottoInfoDialog: ILottoCmsPage;
  finalData: ILotto;

  constructor(
    private siteServerLottoService: SiteServerLottoService,
    private betHistoryMainService: BetHistoryMainService,
  ) {
    this.lotteryData = {};
  }

  cmsLotto() {
    const lottoFinal = {};
    this.lottoCmsBanner.lottoConfig.forEach((data) => {
      this.lotteryData && Object.values(this.lotteryData).forEach((lottoValue: any) => {
        if (data.enabled) {
          const mappingIds: string[] = data.ssMappingId.split(',');
          mappingIds.forEach(id => {
            if (id === lottoValue.boosterBall?.id || id === lottoValue.normal?.id) {
              lottoValue.sortCode = data['svgId'];
              lottoFinal[lottoValue.uri] = lottoValue;
            }
          })
        }
      })
    })
    return lottoFinal;
  }

  getLotteryData(lotteryName: string): Observable<ILotto> {
    const active: ILotto[] = _.toArray(this.cmsLotto());
    const activeLotto = active.length && active[0].uri;
    if (lotteryName && this.lotteryData[lotteryName]) {
      return observableOf(this.lotteryData[lotteryName]);
    } else if (this.lotteryData[activeLotto]) {
      return observableOf(this.lotteryData[activeLotto]);
    }

    return this.getLotteriesByLotto().pipe(map((lottoMap) => {
      return lottoMap[activeLotto];
    }));
  }

  getMenuItems(lotteriesByLotto: ILotto | ILotteryMap): ILottonMenuItem[] {
    const lottoArray = _.toArray(lotteriesByLotto);
    return lottoArray.map(({ name, uri, sortCode }) => ({
      imageTitle: name,
      uri,
      svg: name,
      svgId: sortCode,
      inApp: true,
      targetUri: `/lotto/${uri}`,
      targetUriCopy: uri
    }));

  }

  setLottoCmsBanner(lottoBanner: ILottoCms) {
    this.lottoCmsBanner = lottoBanner;
  }

  public getLottoCmsBanner(): ILottoCms {
    return this.lottoCmsBanner;
  }

  getLotteriesByLotto(): Observable<ILotteryMap> {
    return this.siteServerLottoService.getLotteries().pipe(map((data) => {
      return this.arrangeByLotto(data);
    }));
  }

  getLottoType(lottoEntity, is7Ball) {
    return (!is7Ball && _.has(lottoEntity, 'normal')) ? 'normal' : 'boosterBall';
  }

  getShutAtTime(lotteryEntity: ILotto): string {
    return _.min(lotteryEntity.draw, (item: ILottoDraw) => {
      const currentTime = Date.now(),
        endTime = Date.parse(item.shutAtTime);
      if (endTime >= currentTime) {
        return Date.parse(item.shutAtTime);
      }

      return undefined;
    }).shutAtTime;
  }

  /**
   * Check if lottery is 7ball lottery
   *
   * @param lotteryName
   * @returns {boolean}
   */
  private is7BallLottery(lotteryName) {
    return new RegExp('7 ball', 'i').test(lotteryName);
  }

  private sortLotteryPrices(lotteryEntityPrices: ILottoPrice[]) {
    return _.sortBy(lotteryEntityPrices, 'numberPicks');
  }

  /**
   * return Lotteries packed in Lotto Entity
   *
   * @param lotteriesArray
   * @returns {{}}
   */
  private arrangeByLotto(lotteriesArray: ILotto[]): ILotteryMap {
    let lotteryName;
    let lottoType;
    let sortCode;
    let propName;
    const lottoMap = {};

    _.forEach(lotteriesArray, (lotteryEntity: ILotto) => {
      const shutAtTime = this.getShutAtTime(lotteryEntity);
      if (shutAtTime) {
        lotteryEntity.lotteryPrice = this.sortLotteryPrices(lotteryEntity.lotteryPrice);
        sortCode = this.filterSortCode(lotteryEntity.sort);
        lotteryName = lotteryEntity.description.replace(/\sLottery|\sLotto/g, '')
          .replace(/(\d\s(ball|Ball))/g, '');
        propName = this.filterLottoDesc(lotteryName);
        lottoType = !this.is7BallLottery(lotteryEntity.name) ? 'normal' : 'boosterBall';
        if (!_.has(lottoMap, propName)) {
          lottoMap[propName] = {
            limits: lotteryEntity.limits,
            active: false,
            name: lotteryName,
            sortCode: sortCode,
            description: lotteryEntity.description,
            country: lotteryEntity.country,
            uri: propName
          };
        }
        lottoMap[propName][lottoType] = lotteryEntity;
        lottoMap[propName][lottoType].shutAtTime = shutAtTime;
        if (!lottoMap[propName].shutAtTime ||
          Date.parse(lottoMap[propName].shutAtTime) > Date.parse(lottoMap[propName][lottoType].shutAtTime)) {
          lottoMap[propName].shutAtTime = lottoMap[propName][lottoType].shutAtTime;
        }
      }
    });
    this.activeLotto = _.min(_.toArray(lottoMap), (item: any) => Date.parse(item.shutAtTime)).uri;
    if (this.activeLotto) {
      lottoMap[this.activeLotto].active = true;
    }
    this.lotteryData = lottoMap;

    return lottoMap;
  }

  private filterSortCode(sortCode: string): string {
    const firstNumRegex = /(^\d.)/; // Match First Numbers: [0-9]
    const code = firstNumRegex.test(sortCode) ? sortCode.replace(/(\D)/g, '') :
      sortCode.replace(/(\d)/g, '');
    return `${code.toLowerCase()}-lotto`;
  }

  /**
   * filterLottoDesc (Example: |Lotto USA| ==> lotto-usa; |69s| ==> lotto-69s)
   * Filter lotto description (lottoData.description).
   */
  private filterLottoDesc(input: string): string {
    const symbolRegex = /[\|.,']/g; // Match Symbols: |.,',
    const spaceRegex = /\b(\s+)\b/g; // Match Spaces between words: ' '
    const firstNumRegex = /(^\d.)/; // Match First Numbers: [0-9]
    const text = input
      .replace(symbolRegex, '')
      .replace(spaceRegex, '-')
      .toLowerCase()
      .trim(); // |Lotto USA | ==> lotto-usa

    // add text 'lotto-' if first symbol is number in input
    return firstNumRegex.test(text) ? `lotto-${text}` : text;
  }

  setLottoDialog(lottodialog: ILottoCmsPage) {
    this.lottoInfoDialog = lottodialog;
  }

  getLottoDialog() {
    return this.lottoInfoDialog;
  }
  getHistory(date: IDateRangeObject | string): Observable<IPageBets> {
    const reqObject = {
      detailLevel: 'DETAILED',
      fromDate: (date as IDateRangeObject).startDate || date,
      toDate: (date as IDateRangeObject).endDate,
      group: 'LOTTERYBET',
      pagingBlockSize: '20'
    };

    return this.betHistoryMainService.createRequest((reqObject as IGetBetHistoryRequest),
      response => this.betHistoryMainService.normalizeResponse(response)) as Observable<IPageBets>;
  }

  getBetHistoryForTimePeriod(dateObject): Observable<IPageBets> {
    return this.getHistory(dateObject);

  }

  getPreviousResult(dateObject , id): Observable<ILottoResult[]> {
    return this.getPreviousResultOf(dateObject , id)

  }
  getPreviousResultOf(date: IDateRangeObject | string ,id:string ): Observable<ILottoResult[]> {
    const fromDate = (date as IDateRangeObject).startDate.toString() || date.toString();
    const toDate = (date as IDateRangeObject).endDate.toString();
    const lottoid = id;
    const data = { lottoId: lottoid, page: 1, startDate: fromDate, endDate: toDate  };
    return this.siteServerLottoService.getLottoPreviousResultsFromDate(data).pipe(
      map((res) => {
        return res;
      }));
  }

}
