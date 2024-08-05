import { BetModelService } from '@app/betHistory/services/betModelService/bet-model.service';

describe('test BetModelService', () => {
  let service: BetModelService;
  let timeService: any;
  let filterService: any;

  beforeEach(() => {
    timeService = {
      getLocalDateFromString: arg => arg
    };

    filterService = {
      makeHandicapValue: arg => arg
    };

    service = new BetModelService(timeService as any, filterService as any);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#getBetTimeString should call time service date format transform and return formatted time for today', () => {
    const today = new Date();
    spyOn(timeService, 'getLocalDateFromString').and.returnValue(today);
    service.getBetTimeString('randomString');
    expect(timeService.getLocalDateFromString).toHaveBeenCalledWith('randomString');
    expect(service.getBetTimeString('randomString'))
      .toEqual( `${today.getHours() < 10 ? '0' : ''}${today.getHours()}:${today.getMinutes() < 10 ? '0' : ''}${today.getMinutes()}`);
  });

  it('#getBetTimeString should call time service date format transform and return formatted time for future', () => {
    const tomorrow = new Date;
    tomorrow.setDate(tomorrow.getDate() + 1);
    spyOn(timeService, 'getLocalDateFromString').and.returnValue(tomorrow);
    service.getBetTimeString('randomFutureString');
    expect(timeService.getLocalDateFromString).toHaveBeenCalledWith('randomFutureString');
    /*@ts-ignore*/
    expect(service.getBetTimeString('randomString'))
      .toEqual(
        `${tomorrow.getDate() < 10 ? '0' : ''}${tomorrow.getDate()}/${tomorrow.getMonth() + 1 < 10 ? '0' : ''}${tomorrow.getMonth() + 1}`);
  });

  it('#getPotentialPayout should return potential payout from bet', () => {
    let bet: any = {
      potentialPayout: '10',
      betTermsChange: [{
          potentialPayout: {
            value: '20'
          }
      }]
    };
    expect(service.getPotentialPayout(bet as any)).toEqual('20');
    bet.betTermsChange = [];
    expect(service.getPotentialPayout(bet as any)).toEqual('10');
    bet = {};
    expect(service.getPotentialPayout(bet as any)).toEqual('N/A');

  });

  it('#createOutcomeName should create correct outcome name', () => {
    spyOn(filterService, 'makeHandicapValue').and.callThrough();
    const parts: any = [{
      eventInfo: true,
      handicap: '10',
      description: 'test '
    }];
    const partsWithDesk: any = [{
      eventInfo: true,
      handicap: '10',
      description: 'test 1010'
    }];

    service.createOutcomeName(parts as any);
    expect(filterService.makeHandicapValue).toHaveBeenCalledWith('10', undefined);
    expect(service.createOutcomeName(parts as any)).toEqual(partsWithDesk);
  });

  it('#getDefaultErrorMessage should call locale service for default error message', () => {
    expect(service['changeStringFormat'](8)).toEqual('08');
    expect(service['changeStringFormat'](12)).toEqual('12');
  });
});
