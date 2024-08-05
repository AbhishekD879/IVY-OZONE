import { YourCallHistoryBetBuilderService } from '@app/betHistory/services/yourCallHistoryBetBuilder/your-call-history-bet-builder.service';
import { betHistoryConstants } from '@app/betHistory/constants/bet-history.constant';

describe('Transaction history provider', () => {
  const fracToDecService: any = {
    decToFrac: jasmine.createSpy().and.returnValue('1/5')
  };

  let service: YourCallHistoryBetBuilderService;
  const historyBetMock: any = {
    manualBetDetail: [
      {
        description: 'text description and text2'
      }
    ],
    betType: {
      code: 'SGL',
      name: 'Single'
    },
    leg: []
  };

  const ycBetMock: any = {
    data: [
      {
        amount: 10.10,
        odds: 1.2,
        status: 6,
        events: [
          {
            type: 'testTYpe',
            game1: {
              date: '11111',
              homeTeam: {
                title: 'homeTeam'
              },
              visitingTeam: {
                title: 'visitingTeam'
              }
            }
          }
        ]
      }
    ]
  };

  beforeAll(() => {
    service = new YourCallHistoryBetBuilderService(fracToDecService);
  });

  it ('should test extendHistoryBet', () => {
    const result = service.extendHistoryBet(historyBetMock, ycBetMock);

    expect(result).toBeDefined();
    expect(result.potentialPayout).toBeDefined();
    expect(result.leg[0]).toBeDefined();
    expect(result.leg[0]).toBeDefined();
    expect(result.leg[0].part[0].outcome).toBeDefined();
  });

  it ('should test calculateEstReturns', () => {
    let result = service['calculateEstReturns'](ycBetMock.data[0].odds, ycBetMock.data[0].amount);

    expect(result).toBeDefined();
    expect(result).toEqual('12.12');

    result = service['calculateEstReturns'](ycBetMock.data[0].odds, null);
    expect(result).toEqual('N/A');

    result = service['calculateEstReturns'](null, ycBetMock.data[0].amount);
    expect(result).toEqual('N/A');
  });

  it ('should test parseOutcomeName', () => {
    // one spaces before and
    let result = service['parseOutcomeName']('Max and Max');

    expect(result).toEqual('Max, Max');

    // two spaces before and
    result = service['parseOutcomeName']('Max  and Max');
    expect(result).toEqual('Max, Max');
  });

  it ('should test getYCBetStatus', () => {
    const randomStatusMock = 11111;
    const statuses = betHistoryConstants.ycBetStatuses;
    let result = service['getYCBetStatus'](statuses.won);

    expect(result).toEqual('W');

    result = service['getYCBetStatus'](statuses.lost);
    expect(result).toEqual('L');

    result = service['getYCBetStatus'](statuses.void1);
    expect(result).toEqual('V');

    result = service['getYCBetStatus'](statuses.void2);
    expect(result).toEqual('V');

    result = service['getYCBetStatus'](randomStatusMock);
    expect(result).toEqual('-');
  });
});
