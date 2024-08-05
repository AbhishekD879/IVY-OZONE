// import { of as observableOf } from 'rxjs';
// import { LottoResultsService } from '@app/lotto/services/lottoResults/lotto-results.service';
// import environment from '@environment/oxygenEnvConfig';
// import { ILotteryResultsMap, ILottoResultDraw } from '@app/lotto/models/lotto.model';
// import { tick, fakeAsync } from '@angular/core/testing';


// describe('LottoResultsService', () => {
//   let lottoResultsService;

//   let locale, siteServerLottoService, timeService;
//   const LOTTERIES_CONFIG = environment.LOTTERIES_CONFIG;
//   const lottoResults = {
//     lottoResults: {
//       sortDate: 'sortDate',
//       resultedDraw: [{
//         prop1: 'resultedDraw1',
//         sortDate: '2'
//       }, {
//         prop1: 'resultedDraw2',
//         sortDate: '1'
//       }, {
//         prop1: 'resultedDraw3',
//         sortDate: '1'
//       }, {
//         prop1: 'resultedDraw4',
//         sortDate: '3'
//       }],
//       ballColor: 'ballColor',
//       results: 'results 1 2 3 result',
//       country: 'country',
//       description: 'description',
//       draw: [],
//       hasOpenDraw: true,
//       id: 'id',
//       limits: 100,
//       lotteryPrice: [],
//       maxLines: '4',
//       maxNumber: '4',
//       maxPicks: 4,
//       minNumber: '2',
//       minPicks: '2',
//       name: 'name',
//       siteChannels: 'siteChannels',
//       sort: 'sort',
//       normal: {
//         name: 'name'
//       },
//       boosterBall: {
//         name: 'name'
//       },
//       uri: 'uri',
//       shutAtTime: 'shutAtTime'
//     } as ILottoResultDraw
//   } as ILotteryResultsMap;
//   const lottoResult = {
//     betOdds: 'betOdds',
//     betSelections: 'betSelections',
//     betStake: 2,
//     betStakePerLine: 'betStakePerLine',
//     betTypeDesc: 'betTypeDesc',
//     currency: 'currency',
//     draws: [],
//     name: 'name',
//     description: 'Lottery description',
//   };
//   const lottoMap = {
//     'Lottery description': {
//       betOdds: 'betOdds',
//       betSelections: 'betSelections',
//       betStake: 2,
//       betStakePerLine: 'betStakePerLine',
//       betTypeDesc: 'betTypeDesc',
//       currency: 'currency',
//       description: 'Lottery description',
//       draws: [],
//       ids: 'undefined,undefined',
//       lotteryName: 'Lottery description',
//       name: 'name',
//       page: 0,
//       resultedDraw: []
//     }
//   } as any;

//   beforeEach(() => {
//     locale = {
//       getString: jasmine.createSpy('getString')
//     };

//     siteServerLottoService = {
//       getLottoResults: jasmine.createSpy('getLottoResults').and.returnValue(observableOf([]))
//     };

//     timeService = {
//       getHoursRageFromNow: jasmine.createSpy('getHoursRageFromNow').and.returnValue({
//         start: 'start',
//         end: 'end'
//       })
//     };

//     lottoResultsService = new LottoResultsService(locale, siteServerLottoService, timeService);
//   });

//   it('Tests if LottoResultsService Service Created', () => {
//     expect(lottoResultsService).toBeTruthy();
//     expect(lottoResultsService.LOTTERIES_CONFIG).toEqual(LOTTERIES_CONFIG);
//   });

//   it('#getLottoResultsByLotto', () => {
//     const actualResult = lottoResultsService.getLottoResultsByLotto();

//     expect(actualResult).toEqual(lottoResultsService['lottoResults']);
//   });

//   it('#getLottoResultsById', fakeAsync(() => {
//     const data = {
//       lottoIds: [
//         'lottoId1', 'lottoId2'
//       ],
//       page: 1
//     };

//     lottoResultsService['arrangeByLottoResults'] = jasmine.createSpy('arrangeByLottoResults').and.returnValue([]);
//     lottoResultsService['addToResults'] = jasmine.createSpy('addToResults');

//     lottoResultsService.getLottoResultsById(data).subscribe();
//     tick();

//     expect(siteServerLottoService.getLottoResults).toHaveBeenCalledWith(data);
//     expect(lottoResultsService['arrangeByLottoResults']).toHaveBeenCalledWith([]);
//     expect(lottoResultsService['addToResults']).toHaveBeenCalledWith([]);
//   }));

//   describe('getLottoResults', () => {
//     it('#getLottoResults when there is no lottoResults', () => {
//       const oldS = lottoResultsService;
//       const loadMore = true;
//       lottoResultsService = {
//         locale,
//         siteServerLottoService,
//         timeService,
//         lottoResults: {},
//         resultsPage: oldS.lottoResultsService,
//         getLottoResults: oldS.getLottoResults
//       };
//       lottoResultsService['getLottoIds'] = jasmine.createSpy('getLottoIds').and.returnValue(observableOf([]));
//       lottoResultsService['arrangeByLottoResults'] = jasmine.createSpy('arrangeByLottoResults').and.returnValue([]);
//       lottoResultsService['addToResults'] = jasmine.createSpy('addToResults').and.returnValue([]);

//       const resultsPage = lottoResultsService['resultsPage'];
//       lottoResultsService.getLottoResults(loadMore).subscribe();

//       expect(lottoResultsService['resultsPage']).toEqual(resultsPage + 1);
//       expect(lottoResultsService['getLottoIds']).toHaveBeenCalledWith(lottoResultsService['resultsPage']);
//       expect(siteServerLottoService.getLottoResults).toHaveBeenCalledWith([]);
//       expect(lottoResultsService['arrangeByLottoResults']).toHaveBeenCalledWith([]);
//       expect(lottoResultsService['addToResults']).toHaveBeenCalledWith([]);
//     });

//     it('should return observable of lottoResults',  () => {
//       lottoResultsService.lottoResults = [{}];

//       const successHandler = jasmine.createSpy('successHandler');

//       lottoResultsService.getLottoResults(false).subscribe(successHandler);

//       expect(successHandler).toHaveBeenCalledWith(lottoResultsService.lottoResults);
//     });
//   });

//   it('#getLottoResultsByTime', () => {
//     lottoResultsService['lottoResults']['lottoResult1'] = lottoResults.lottoResults;
//     lottoResultsService['lottoResults']['lottoResult2'] = lottoResults.lottoResults;
//     lottoResultsService['sortObject'] = jasmine.createSpy('sortObject');
//     const draws = {
//       '1': [
//         {
//           prop1: 'resultedDraw2',
//           sortDate: '1'
//         },
//         {
//           prop1: 'resultedDraw3',
//           sortDate: '1'
//         }],
//       '2': [
//         {
//           prop1: 'resultedDraw1',
//           sortDate: '2'
//         }],
//       '3': [{
//           prop1: 'resultedDraw4',
//           sortDate: '3'
//       }]
//     };
//     lottoResultsService['getLottoResultsByTime']();

//     expect(lottoResultsService['sortObject']).toHaveBeenCalledWith(draws, true);
//   });

//   it('#is7BallLottery when it is not', () => {
//     const actualResult = lottoResultsService['is7BallLottery']('lotteryName');

//     expect(actualResult).toEqual(false);
//   });

//   it('#is7BallLottery when it is', () => {
//     const actualResult = lottoResultsService['is7BallLottery']('7 ball lotteryname');

//     expect(actualResult).toEqual(true);
//   });

//   describe('arrangeByLottoResults', () => {
//     it('#arrangeByLottoResults', () => {
//       const lottoResultsArr = [];
//       lottoResultsArr.push(lottoResult);
//       lottoResultsArr.push(lottoResult);
//       lottoResultsService['sortObject'] = jasmine.createSpy('sortObject');
//       lottoResultsService['arrangeByLottoResults'](lottoResultsArr);

//       expect(lottoResultsService['sortObject']).toHaveBeenCalled();
//     });

//     it('should arrangeByLottoResults with bonus lottoType and modify draw if description is Irish', () => {
//       const lottoResultsArr = [];
//       const lottoResultWithDraw = {
//         betOdds: 'betOdds',
//         betSelections: 'betSelections',
//         betStake: 2,
//         betStakePerLine: 'betStakePerLine',
//         betTypeDesc: 'betTypeDesc',
//         currency: 'currency',
//         draws: [],
//         name: '7 ball',
//         description: 'Lottery description',
//         resultedDraw: [
//           {
//             drawAtTime: '10-11-2019',
//             description: 'Description',
//             results: 'asd'
//           }
//         ]
//       };
//       const lottoResultWithDraw2 = {
//         betOdds: 'betOdds',
//         betSelections: 'betSelections',
//         betStake: 2,
//         betStakePerLine: 'betStakePerLine',
//         betTypeDesc: 'betTypeDesc',
//         currency: 'currency',
//         draws: [],
//         name: '7 ball',
//         description: 'Irish',
//         resultedDraw: [
//           {
//             drawAtTime: '10-11-2019',
//             description: 'Description',
//             results: 'asd'
//           }
//         ]
//       };

//       lottoResultsArr.push(lottoResultWithDraw);
//       lottoResultsArr.push(lottoResultWithDraw);
//       lottoResultsArr.push(lottoResultWithDraw2);
//       lottoResultsArr.push(lottoResultWithDraw2);
//       lottoResultsService['sortObject'] = jasmine.createSpy('sortObject');

//       lottoResultsService['arrangeByLottoResults'](lottoResultsArr);

//       expect(lottoResultsService['sortObject']).toHaveBeenCalled();
//     });

//     it('should get draw with bonus ball', () => {
//       const lottoResultsArr = [];
//       const lottoResultWithDraw = {
//         betOdds: 'betOdds',
//         betSelections: 'betSelections',
//         betStake: 2,
//         betStakePerLine: 'betStakePerLine',
//         betTypeDesc: 'betTypeDesc',
//         currency: 'currency',
//         draws: [],
//         name: '7 ball',
//         description: 'Lottery description',
//         resultedDraw: [
//           {
//             drawAtTime: '10-11-2019',
//             description: 'Description',
//             results: 'asd'
//           }
//         ]
//       };
//       const lottoResultWithDraw2 = {
//         betOdds: 'betOdds',
//         betSelections: 'betSelections',
//         betStake: 2,
//         betStakePerLine: 'betStakePerLine',
//         betTypeDesc: 'betTypeDesc',
//         currency: 'currency',
//         draws: [],
//         name: '7 ball',
//         description: 'Lottery description',
//         resultedDraw: [
//           {
//             drawAtTime: '19-11-2019',
//             description: 'Description2',
//             results: 'asd'
//           }
//         ]
//       };

//       lottoResultsService['getDrawWithBonusBall'] = jasmine.createSpy('getDrawWithBonusBall');

//       lottoResultsArr.push(lottoResultWithDraw);
//       lottoResultsArr.push(lottoResultWithDraw2);
//       lottoResultsService['arrangeByLottoResults'](lottoResultsArr);

//       expect(lottoResultsService['getDrawWithBonusBall']).toHaveBeenCalled();
//     });
//   });

//   describe('addToResults', () => {
//     it('#addToResults', () => {
//       lottoResultsService['lottoResults']['lottoResult1'] = lottoResults.lottoResults;
//       lottoResultsService['lottoResults']['lottoResult2'] = lottoResults.lottoResults;
//       const actualResult = lottoResultsService['addToResults'](lottoMap);
//       const expectedResult = Object.assign({}, lottoResultsService['lottoResults']);
//       expectedResult['Lottery description'] = lottoMap['Lottery description'];

//       expect(actualResult).toEqual(expectedResult);
//     });

//     it('should set resultedDraw to lotto', () => {
//       const lotto = {
//         'Lottery description': {
//           betOdds: 'betOdds',
//           betSelections: 'betSelections',
//           betStake: 2,
//           betStakePerLine: 'betStakePerLine',
//           betTypeDesc: 'betTypeDesc',
//           currency: 'currency',
//           description: 'Lottery description',
//           draws: [],
//           ids: 'undefined,undefined',
//           lotteryName: 'Lottery description',
//           name: 'name',
//           page: 0,
//           resultedDraw: [
//             {date: 'lotto date', description: 'lotto description'}
//           ]
//         }
//       } as any;
//       const expectedResult = {
//         'Lottery description': {
//           resultedDraw: [
//             {date: 'lotto date1', description: 'lotto description1'},
//             {date: 'lotto date', description: 'lotto description'}
//           ]
//         }
//       };

//       lottoResultsService.lottoResults = {
//         'Lottery description': {
//           resultedDraw: [
//             {date: 'lotto date1', description: 'lotto description1'}
//           ]
//         }
//       };
//       const actualResult = lottoResultsService['addToResults'](lotto);

//       expect(actualResult).toEqual(expectedResult);
//     });

//     it('should push add draw', () => {
//       const lotto = {
//         'Lottery description': {
//           betOdds: 'betOdds',
//           betSelections: 'betSelections',
//           betStake: 2,
//           betStakePerLine: 'betStakePerLine',
//           betTypeDesc: 'betTypeDesc',
//           currency: 'currency',
//           description: 'Lottery description',
//           draws: [],
//           ids: 'undefined,undefined',
//           lotteryName: 'Lottery description',
//           name: 'name',
//           page: 0,
//           resultedDraw: [
//             {date: 'lotto date', description: 'lotto description'}
//           ]
//         }
//       } as any;
//       const expectedResult = {
//         'Lottery description': {
//           resultedDraw: [
//             {date: 'lotto date', description: 'lotto description'}
//           ]
//         }
//       };

//       lottoResultsService.lottoResults = {
//         'Lottery description': {
//           resultedDraw: [
//             {date: 'lotto date', description: 'lotto description'}
//           ]
//         }
//       };
//       const actualResult = lottoResultsService['addToResults'](lotto);

//       expect(actualResult).toEqual(expectedResult);
//     });
//   });

//   it('#separateResultsNumbers', () => {
//     const lottoDraw = lottoResults.lottoResults;
//     const actualResult = lottoResultsService['separateResultsNumbers'](lottoDraw, 2);
//     const expectedResult = ['re', 'su', 'lt', 's ', '1 ', '2 ', '3 '];

//     expect(actualResult).toEqual(expectedResult);
//   });

//   describe('getLottoIds', () => {
//     it('should return observable with lottoIds and page number',  () => {
//       const successHandler = jasmine.createSpy('successHandler');

//       lottoResultsService['getLottoIds'](2).subscribe(successHandler);

//       expect(successHandler).toHaveBeenCalled();
//     });

//     it('should return observable with lottoIds and 1 page',  () => {
//       const successHandler = jasmine.createSpy('successHandler');

//       lottoResultsService['getLottoIds'](null).subscribe(successHandler);

//       expect(successHandler).toHaveBeenCalled();
//     });
//   });

//   describe('sortObject', () => {
//     it('should return sorted object',  () => {
//       const draws = {
//         'c': [
//           {
//             prop1: 'resultedDraw1',
//             sortDate: '2'
//           }],
//         'd': [{
//           prop1: 'resultedDraw4',
//           sortDate: '3'
//         }],
//         'b': [
//           {
//             prop1: 'resultedDraw2',
//             sortDate: '1'
//           },
//           {
//             prop1: 'resultedDraw3',
//             sortDate: '1'
//           }]
//       };
//       const expectedResult = {
//         'b': [
//           {
//             prop1: 'resultedDraw2',
//             sortDate: '1'
//           },
//           {
//             prop1: 'resultedDraw3',
//             sortDate: '1'
//           }],
//         'c': [
//           {
//             prop1: 'resultedDraw1',
//             sortDate: '2'
//           }],
//         'd': [{
//           prop1: 'resultedDraw4',
//           sortDate: '3'
//         }]
//       };
//       const actualResult = lottoResultsService['sortObject'](draws);

//       expect(actualResult).toEqual(expectedResult);
//     });

//     it('should return reverse sorted object',  () => {
//       const draws = {
//         '2': [
//           {
//             prop1: 'resultedDraw1',
//             sortDate: '2'
//           }],
//         '1': [
//           {
//             prop1: 'resultedDraw2',
//             sortDate: '1'
//           },
//           {
//             prop1: 'resultedDraw3',
//             sortDate: '1'
//           }],
//         '3': [{
//           prop1: 'resultedDraw4',
//           sortDate: '3'
//         }]
//       };
//       const expectedResult = {
//         '3': [{
//           prop1: 'resultedDraw4',
//           sortDate: '3'
//         }],
//         '2': [
//           {
//             prop1: 'resultedDraw1',
//             sortDate: '2'
//           }],
//         '1': [
//           {
//             prop1: 'resultedDraw2',
//             sortDate: '1'
//           },
//           {
//             prop1: 'resultedDraw3',
//             sortDate: '1'
//           }]
//       };
//       const actualResult = lottoResultsService['sortObject'](draws, true);

//       expect(actualResult).toEqual(expectedResult);
//     });
//   });

//   describe('parseParamsForDraw', () => {
//     it('should set draw date today', () => {
//       const lotteryEntity = {
//         resultedDraw: [
//           {
//             drawAtTime: new Date().toJSON(),
//             description: 'Daily Million',
//             results: ''
//           }
//         ]
//       };

//       lottoResultsService['parseParamsForDraw'](lotteryEntity, '');

//       expect(locale.getString).toHaveBeenCalledWith('lotto.today');
//     });

//     it('should set draw date yesterday', () => {
//       const yesterday = new Date(new Date().setDate(new Date().getDate() - 1)).toJSON();
//       const lotteryEntity = {
//         resultedDraw: [
//           {
//             drawAtTime: yesterday,
//             description: 'Daily Million',
//             results: ''
//           }
//         ]
//       };

//       timeService.getHoursRageFromNow.and.returnValue({
//         start: 'start',
//         end: yesterday
//       });

//       lottoResultsService['parseParamsForDraw'](lotteryEntity);

//       expect(locale.getString).toHaveBeenCalledWith('lotto.yesterday');
//     });
//   });

//   describe('getDrawWithBonusBall', () => {
//     it('should update ball color',  () => {
//       const draw = {results: ''};

//       lottoResultsService['separateResultsNumbers'] = jasmine.createSpy('separateResultsNumbers').and.returnValue(['147', '7']);

//       const actualResult = lottoResultsService['getDrawWithBonusBall'](draw, draw, false, 'multi');

//       expect(actualResult.bonusBall).toEqual({ballValue: '', ballColor: undefined});
//       expect(lottoResultsService['separateResultsNumbers']).toHaveBeenCalled();
//     });
//   });
// });
