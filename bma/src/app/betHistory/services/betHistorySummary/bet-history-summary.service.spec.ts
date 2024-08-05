import { BetHistorySummaryService } from './bet-history-summary.service';

describe('BetHistorySummaryService', () => {
  let awsService, betHistoryMainService;
  let service: BetHistorySummaryService;
  let summaryData, summaryResult, calcResult;

  beforeEach(() => {
    summaryData = {
      summary: {
        totalBets: {amount: '5'},
        totalWins: {amount: '7'}
      },
      walletTransactions: [{
        actionType: 'sb_bet',
        amount: {amount: '1'}
      }, {
        actionType: 'lotto_bet',
        amount: {amount: '4'}
      }, {
        actionType: 'sb_win',
        amount: {amount: '3'}
      }, {
        actionType: 'lotto_win',
        amount: {amount: '2'}
      }, {
        actionType: 'sb_bet_cancel',
        amount: {amount: '2'}
      }]
    } as any;

    calcResult = {
      totalStakes: '$5',
      totalReturns: '$7',
      profit: '$2',
      iconClass: 'arrow-right-up',
      label: 'fooString'
    } as any;

    summaryResult = {
      allBetsGames: calcResult,
      sb: calcResult,
      lotto: calcResult
    } as any;

    awsService = {
      addAction: jasmine.createSpy('addAction')
    };

    betHistoryMainService = {
      calculateTotals: jasmine.createSpy('calculateTotals').and.returnValue(calcResult)
    };

    service = new BetHistorySummaryService(
      awsService,
      betHistoryMainService
    );
  });

  it('#getSummaryTotals should get summary total', () => {
    expect(service.getSummaryTotals(summaryData, ['sb', 'lotto'])).toEqual(summaryResult);
  });

  it('#getAllTotals should get result profit loss', () => {
    expect(service.getAllTotals(summaryData.summary, 'allBetsGames'))
      .toEqual(summaryResult.allBetsGames as any);
  });

  it('#getSpecificTotals should get profit loss values related to bet types', () => {
    expect(service.getSpecificTotals(summaryData.walletTransactions, ['sb', 'lotto'])).toEqual({
      sb: summaryResult.sb,
      lotto: summaryResult.lotto
    } as any);
  });

  it('#sendAwsData', () => {
    const awsData = {
      request: {
        requestId: '1'
      },
      requestStart: 123,
      requestEnd: 123,
      totalDuration: 1
    } as any;
    service.sendAwsData(awsData);
    expect(awsService.addAction).toHaveBeenCalled();
  });
});
