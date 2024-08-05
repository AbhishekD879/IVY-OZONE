import { ToteBetReceiptService } from './tote-bet-receipt.service';

describe('ToteBetReceiptService', () => {
  let service: ToteBetReceiptService;

  let localeService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString')
    };

    service = new ToteBetReceiptService(localeService);
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  describe('betReceiptBuilder', () => {
    it('has success bets', () => {
      const eventEntity: any = {
        markets: [{ outcomes: [] }]
      };
      const betPlacementRespond: any = [{
        bet: [{
          betTypeRef: {},
          outcomeRef: {},
          leg: [{
            poolLeg: { legPart: [{ outcomeRef: {} }] }
          }]
        }],
        betslip: { stake: { currencyRef: {} } }
      }];

      const result = service.betReceiptBuilder(eventEntity, betPlacementRespond);

      expect(result.successBets.length).toBe(1);
      expect(result.failedBets.length).toBe(0);
    });

    it('has success and failed bets', () => {
      const eventEntity: any = {
        markets: [{ outcomes: [] }]
      };
      const betPlacementRespond: any = [{
        bet: [{
          betTypeRef: {},
          outcomeRef: {},
          leg: [{
            poolLeg: { legPart: [{ outcomeRef: {} }] }
          }]
        }],
        betslip: { stake: { currencyRef: {} } }
      }, {
        betError: 'error',
        bet: [{
          betTypeRef: {},
          outcomeRef: {},
          leg: [{
            poolLeg: { legPart: [{ outcomeRef: {} }] }
          }]
        }],
        betslip: { stake: { currencyRef: {} } }
      }];

      const result = service.betReceiptBuilder(eventEntity, betPlacementRespond);

      expect(result.successBets.length).toBe(1);
      expect(result.failedBets.length).toBe(1);
    });

    it('no success bets', () => {
      const result = service.betReceiptBuilder({} as any, []);
      expect(result.successBets.length).toBe(0);
      expect(result.failedBets.length).toBe(0);
    });
  });

  it('addLegDetails', () => {
    const betsReceipt: any = [{}, {}];
    const eventEntity: any = {
      localTime: '2018-03-03',
      name: 'Abc',
      markets: [{
        outcomes: {}
      }]
    };

    service.addSelectionsNames = jasmine.createSpy();
    const result = service.addLegDetails(betsReceipt, eventEntity);

    expect(service.addSelectionsNames).toHaveBeenCalledTimes(2);
    expect(result.length).toBe(2);
    expect(betsReceipt[0].leg).toBe(`${eventEntity.localTime} ${eventEntity.name}`);
    expect(betsReceipt[1].leg).toBe(`${eventEntity.localTime} ${eventEntity.name}`);
  });

  it('checkAndExcludeFailedBets', () => {
    let result;

    result = service.checkAndExcludeFailedBets([
      { betError: true }, {}, {}
    ] as any);
    expect(result.successBets.length).toBe(2);
    expect(result.failedBets.length).toBe(1);

    result = service.checkAndExcludeFailedBets({ betError: true } as any);
    expect(result.successBets.length).toBe(0);
    expect(result.failedBets.length).toBe(1);

    result = service.checkAndExcludeFailedBets({} as any);
    expect(result.successBets.length).toBe(1);
    expect(result.failedBets.length).toBe(0);
  });

  it('addSelectionsNames', () => {
    let betsReceipt: any;
    let outcomes: any[];

    betsReceipt = {
      legParts: [
        {
          outcomeRef: { id: 1 }
        }
      ]
    };
    outcomes = [{ id: 1, name: 'one' }];
    service.addSelectionsNames(betsReceipt, outcomes);
    expect(betsReceipt.legParts[0].outcomeName).toBe('one');

    betsReceipt = {
      legParts: [
        {
          outcomeRef: { id: 1 }
        },
        {
          outcomeRef: { id: 2 }
        }
      ]
    };
    outcomes = [{ id: 1, name: 'one' }, { id: 2, name: 'two' }];
    service.addSelectionsNames(betsReceipt, outcomes);
    expect(betsReceipt.legParts[0].outcomeName).toBe('(1) one');
    expect(betsReceipt.legParts[1].outcomeName).toBe('(2) two');
  });

  it('addBetDetails when bets data is an array of object', () => {
    service['buildBetReceipt'] = jasmine.createSpy();
    const bets: any = [
      {
        bet: [{
          betTypeRef: { id: 1 },
          leg: [{poolLeg: {legPart: [{outcomeRef: { id: 1 }}]}}]
        }],
        betslip: {stake: {currencyRef: { id: 1 }}}
      }
    ];
    const betsReceipt = [];
    expect(service.addBetDetails(bets, betsReceipt)).toBe(betsReceipt);
    expect(bets[0].hasOwnProperty('bet')).toBeTruthy();
    expect(service['buildBetReceipt']).toHaveBeenCalledTimes(bets.length);
    expect(betsReceipt.length).toBe(bets.length);
  });

  it('addBetDetails when bets data is an array of object of object', () => {
    service['buildBetReceipt'] = jasmine.createSpy();
    const bets: any = [
      {
        '0': {
          bet: [{
            betTypeRef: { id: 1 },
            leg: [{ poolLeg: { legPart: [{ outcomeRef: { id: 1 } }] } }]
          }],
          betslip: { stake: { currencyRef: { id: 1 } } }
        }
      }
    ];
    const betsReceipt = [];
    expect(service.addBetDetails(bets, betsReceipt)).toBe(betsReceipt);
    expect(bets[0].hasOwnProperty('bet')).toBeFalsy();
    expect(service['buildBetReceipt']).toHaveBeenCalledTimes(1);
    expect(betsReceipt.length).toBe(1);
  });

  it('addBetDetails when bets data is an not object', () => {
    service['buildBetReceipt'] = jasmine.createSpy();
    const bets: any = [
      {
        '0': {
          bet: [{
            betTypeRef: { id: 1 },
            leg: [{ poolLeg: { legPart: [{ outcomeRef: { id: 1 } }] } }]
          }],
          betslip: { stake: { currencyRef: { id: 1 } } }
        },
        'token' : 'QAWERTYg45GH'
      }
    ];
    const betsReceipt = [];
    expect(service.addBetDetails(bets, betsReceipt)).toBe(betsReceipt);
    expect(bets[0].hasOwnProperty('bet')).toBeFalsy();
    expect(service['buildBetReceipt']).toHaveBeenCalledTimes(1);
    expect(betsReceipt.length).toBe(1);
  });

  it('buildBetReceipt', () => {
    service.generatePoolTitle = jasmine.createSpy();
    const bets: any = [
      {
        bet: [{
          betTypeRef: { id: 1 },
          receipt: 'P/23124602/0000208',
          leg: [{poolLeg: {legPart: [{outcomeRef: { id: 1 }}]}}]
        }],
        betslip: {stake: {currencyRef: { id: 1 }}}
      }
    ];
    expect(service['buildBetReceipt'](bets[0]).betId).toBe('P/23124602/0000208');
    expect(service.generatePoolTitle).toHaveBeenCalled();
  });

  it('generatePoolTitle', () => {
    expect(service.generatePoolTitle('abc').startsWith('Tote')).toBeTruthy();
    expect(localeService.getString).toHaveBeenCalledWith('tt.abc');
  });

  it('calculateTotalStake', () => {
    const betsReceipt: any = [
      { stakeAmount: 1 },
      { stakeAmount: 2 }
    ];
    expect(service.calculateTotalStake(betsReceipt)).toBe(3);
  });

  it('addUnsuccessfulMsg', () => {
    const successBets: any[] = [{}];
    const failedBets: any[] = [{}, {}];
    service.addUnsuccessfulMsg(successBets, failedBets);
    expect(localeService.getString).toHaveBeenCalledWith(
      'tt.unsuccessfulBetReceiptMsg', [successBets.length, successBets.length + failedBets.length]
    );
  });

  it('getSuccessfulMsg', () => {
    const successBets: any = [{}];
    service.getSuccessfulMsg(successBets);
    expect(localeService.getString).toHaveBeenCalledWith('tt.successBetReceiptMsg');

    successBets.push({});
    service.getSuccessfulMsg(successBets);
    expect(localeService.getString).toHaveBeenCalledWith('tt.successBetsReceiptMsg');
  });
});
