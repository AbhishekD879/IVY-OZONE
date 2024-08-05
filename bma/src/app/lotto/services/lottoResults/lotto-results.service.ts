
// import { of as observableOf,  Observable } from 'rxjs';

// import { concatMap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';

// import { TimeService } from '@core/services/time/time.service';
// import { SiteServerLottoService } from '../siteServerLotto/site-server-lotto.service';
// import { LocaleService } from '@core/services/locale/locale.service';
// import environment from '@environment/oxygenEnvConfig';
// import { ILotteriesConfig } from '../../models/lotteries-config.model';
// import { ILottoResult } from '@app/lotto/models/lotto-result.model';
// import { ILotteryMap, ILottoResultDraw, ILotto, ILotteryResultsMap } from '../../models/lotto.model';

@Injectable()
export class LottoResultsService {

  // readonly LOTTERIES_CONFIG: ILotteriesConfig;
  // private resultsPage: number = 0;
  // private readonly lottoResults: ILotteryResultsMap = {};

  constructor(
    // private locale: LocaleService,
    // private siteServerLottoService: SiteServerLottoService,
    // private timeService: TimeService
  ) {
    // this.LOTTERIES_CONFIG = environment.LOTTERIES_CONFIG;
  }

  /**
   * get cached Lotto Results.
   *
   * @returns {object} - Lotto results object arrange by lotto.
   */
  // getLottoResultsByLotto(): ILotteryResultsMap {
  //   return this.lottoResults;
  // }

  /**
   * get Lotto Results from SS for specific lotteries and then arrange them By Lotto.
   *
   * @param {object} - lottery ids and page number.
   * @returns {object} - Lotto results object arrange by lotto.
   */
  // getLottoResultsById(data): Observable<ILotteryMap> {
  //   return this.siteServerLottoService.getLottoResults(data).pipe(
  //   map((res) => {
  //     return this.arrangeByLottoResults(res);
  //   }), map((res) => {
  //     return this.addToResults(res);
  //   }));
  // }

  /**
   * get Lotto Results from SS and then arrange them By Lotto.
   *
   * @param {boolean} optional - return cached results when this parameter is not supplied.
   * @returns {object} - Lotto results object arrange by lotto.
   */
  // getLottoResults(loadMore: boolean): Observable<ILotteryResultsMap> {
  //   if (!_.isEmpty(this.lottoResults) && !loadMore) {
  //     return observableOf(this.lottoResults);
  //   }
  //   this.resultsPage += 1;
  //   return this.getLottoIds(this.resultsPage).pipe(
  //   concatMap((idsAndPage) => {
  //     return this.siteServerLottoService.getLottoResults(idsAndPage);
  //   }), map((data) => {
  //     return this.arrangeByLottoResults(data);
  //   }), map((data) => {
  //     return this.addToResults(data);
  //   }));
  // }

  /**
   * Arrange Lotto Results by Draw date.
   *
   * @returns {object} - Lotto results object arrange by time
   */
  // getLottoResultsByTime(): ILotteryResultsMap {
  //   let draws: ILottoResultDraw[] = [];

  //   _.each(this.lottoResults, (lotto: ILotto) => {
  //     draws = _.union(draws, lotto.resultedDraw);
  //   });
  //   draws = (_.groupBy(draws, 'sortDate') as any); // OrderBy Bug typings

  //   return this.sortObject(draws, true);
  // }
  /**
   * get Lotto ids for Connect app from configuration.
   *
   * @param page number.
   * @returns Promise.
   */
  // private getLottoIds(page): Observable<{ lottoIds: string[], page: number}> {
  //   const lottoIds = _.compact(_.map(this.LOTTERIES_CONFIG, (lottery, key) => lottery.inConnect ? key : ''));

  //   return observableOf({ lottoIds, page: page || 1 });
  // }

  /**
   * Check if lottery is 7ball lottery
   *
   * @param lotteryName
   * @returns {boolean}
   */
  // private is7BallLottery(lotteryName: string): boolean {
  //   return new RegExp('7 ball', 'i').test(lotteryName);
  // }

  /**
   * return Lotto Results arranged by Lotto
   *
   * @param lotteriesArray
   * @returns {object} - Lotto results object arrange by lotto.
   */
  // private arrangeByLottoResults(lotteriesArray: ILottoResult[]): ILotteryResultsMap {
  //   const lottoMap = {};

  //   _.forEach(lotteriesArray, (lotteryEntity: any) => {
  //     const propName = lotteryEntity.description.replace(/\sLottery|\sLotto/g, '')
  //       .replace('N.Y.', 'New York');
  //     const lottoType = !this.is7BallLottery(lotteryEntity.name) ? 'normal' : 'bonus';
  //     if (!_.has(lottoMap, propName)) {
  //       lottoMap[propName] = lotteryEntity;
  //       lottoMap[propName].page = this.resultsPage;
  //       lottoMap[propName].lotteryName = propName;

  //       this.parseParamsForDraw(lotteryEntity, propName);
  //     } else {
  //       _.each(lottoMap[propName].resultedDraw, (draw: any) => {
  //         _.each(lotteryEntity.resultedDraw, (bonusDraw: any) => {
  //           const drawTime = propName === 'Irish' ? draw.drawAtTime.substring(0, 10) : draw.drawAtTime;
  //           const bonusDrawTime = propName === 'Irish' ? bonusDraw.drawAtTime.substring(0, 10) : bonusDraw.drawAtTime;

  //           if (drawTime === bonusDrawTime && draw.description === bonusDraw.description) {
  //             this.getDrawWithBonusBall(draw, bonusDraw, lottoType === 'bonus', lotteryEntity.ballColor);
  //           }
  //         });
  //       });
  //       lottoMap[propName].ids = `${lotteryEntity.id},${lottoMap[propName].id}`;
  //       lottoMap[propName].resultedDraw = _.chain(lottoMap[propName].resultedDraw)
  //         .sortBy('description')
  //         .reverse()
  //         .sortBy('drawAtTime')
  //         .reverse()
  //         .value();
  //     }
  //   });

  //   return this.sortObject(lottoMap);
  // }

  /**
   * Parse date and description params for a draw.
   *
   * @param {object} lotteryEntity - single lotto object.
   * @param {string} propName - simplified lotto name.
   */
  // private parseParamsForDraw(lotteryEntity: ILottoResultDraw, propName: string): void {
  //   const currentDate = new Date().toJSON()
  //     .slice(0, 10);
  //   const yesterdayDate = this.timeService.getHoursRageFromNow(-24).end.slice(0, 10);

  //   _.each(lotteryEntity.resultedDraw, (draw: any) => {
  //     let date = draw.drawAtTime.slice(0, 10);
  //     let sortDate;
  //     const shortDescription = draw.description.replace('Daily Million', '');

  //     if (date === currentDate) {
  //       date = this.locale.getString('lotto.today');
  //       sortDate = `__${this.locale.getString('lotto.today')}`;
  //     } else if (date === yesterdayDate) {
  //       date = this.locale.getString('lotto.yesterday');
  //       sortDate = `_${this.locale.getString('lotto.yesterday')}`;
  //     } else {
  //       sortDate = date;
  //       date = date.split('-')
  //         .reverse()
  //         .join('/');
  //     }

  //     draw.date = date;
  //     draw.sortDate = sortDate;
  //     draw.fullDescription = `${propName} ${shortDescription}`;
  //     this.getDrawWithBonusBall(draw, { results: '' }, false, lotteryEntity.ballColor);
  //   });
  // }

  /**
   * When more results received add them to the cache object
   *
   * @param {object} lottoMap
   * @returns {object} - Lotto results object arrange by lotto.
   */
  // private addToResults(lottoMap: ILotteryResultsMap): ILotteryResultsMap {
  //   _.each(lottoMap, (lotto: ILottoResultDraw, key: string) => {
  //     if (_.has(this.lottoResults, key)) {
  //       const resultedDraw = _.clone(this.lottoResults[key].resultedDraw);
  //       _.each(lotto.resultedDraw, (draw: any) => {
  //         if (!_.findWhere(resultedDraw, { date: draw.date, description: draw.description })) {
  //           resultedDraw.push(draw);
  //         }
  //       });
  //       this.lottoResults[key].resultedDraw = _.uniq(resultedDraw);
  //     } else {
  //       this.lottoResults[key] = lotto;
  //     }
  //   });

  //   return this.lottoResults;
  // }

  /**
   * Sort Object.
   * Lotto results should be sorted by Lotto name.
   *
   * @param {object} obj - object to be sorted.
   * @param {boolean} reverse - whether object should be sorted in the reverse order.
   * @returns {object} - sorted object.
   */
  // private sortObject(obj: ILottoResultDraw[] | ILotteryResultsMap, reverse?: boolean): ILotteryResultsMap {
  //   const sorted = {};
  //   const arr = _.map((obj as any), (value, key) => key).sort((a, b) => {
  //     return a > b ? 1 : -1;
  //   });

  //   if (reverse) {
  //     arr.reverse();
  //   }

  //   _.each(arr, key => {
  //     sorted[key] = obj[key];
  //   });

  //   return sorted;
  // }

  /**
   * parse Draw Results to contain separated results and bonus ball.
   *
   * @param {object} firstDraw - first Draw with either 6 or 7 balls
   * @param {object} secondDraw - second Draw with either 6 or 7 balls
   * @param {boolean} - bonus - if true secondDraw contains bonus ball, else firstDraw contains bonus ball.
   * @param {string} - ballColor
   * @returns {object} - parsed draw with bonus ball.
   */
  // private getDrawWithBonusBall(firstDraw, secondDraw, bonus, ballColor) {
  //   const colors = ['#85d947', '#f64353', '#fd8e0b', '#f5d109', '#bd680d', '#d268e9', '#4497ec'];
  //   const results6 = bonus ? this.separateResultsNumbers(firstDraw, 6) : this.separateResultsNumbers(secondDraw, 6);
  //   const results7 = bonus ? this.separateResultsNumbers(secondDraw, 7) : this.separateResultsNumbers(firstDraw, 7);

  //   // Get Bonus Ball.
  //   const bonusBall = _.difference(results6, results7).join() || _.difference(results7, results6).join();
  //   firstDraw.bonusBall = {
  //     ballValue: bonusBall.length <= 2 ? bonusBall : '',
  //     ballColor: ballColor === 'multi' ? colors[(Number(bonusBall) - 1) % 7] : ballColor
  //   };

  //   // Get array of objects for balls.
  //   const separatedResults = results6.join() || results7.join();
  //   firstDraw.separatedResults = [];
  //   _.each(separatedResults.split(','), ballValue => {
  //     firstDraw.separatedResults.push({
  //       ballColor: ballColor === 'multi' ? colors[(Number(ballValue) - 1) % 7] : ballColor,
  //       ballValue
  //     });
  //   });

  //   return firstDraw;
  // }

  /**
   * Separate result numbers.
   * Results are received as a string, and need to be separated, to get each ball value.
   *
   * @param draw
   * @param {number} - length
   * @returns []
   */
  // private separateResultsNumbers(draw: ILottoResultDraw, length: number): string[] {
  //   let tempLength = length;
  //   let result = draw.results.replace(/\|/g, '');
  //   let arr = [];

  //   while (result.length < tempLength * 2) {
  //     arr.push(result.slice(0, 1));
  //     result = result.slice(1);
  //     tempLength -= 1;
  //   }

  //   const rest = result.match(/.{1,2}/g);
  //   arr = _.union(arr, rest);

  //   return arr;
  // }
}
