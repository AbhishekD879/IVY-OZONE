import { IPoolEntity } from './../../../core/models/pool.model';
import { JackpotSportTabService } from './jackpot-sport-tab.service';
import { of } from 'rxjs';

describe('JackpotSportTabService', () => {
  let service: JackpotSportTabService;

  let deviceService;
  let storageService;
  let userService;
  let bppService;
  let clientUserAgentService;
  let timeSyncService;

  beforeEach(() => {
    deviceService = {};
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    userService = {
      currency: '$',
      status: true,
      sportBalance: 10
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of(
        {
          betError: [{
            error: { subErrorCode: 4091, errorDesc: 'error' },
          }]
        }
      ))
    };
    clientUserAgentService = {
      getId: jasmine.createSpy().and.returnValue(1)
    };
    timeSyncService = {
      ip: '192.2.2.1'
    };

    service = new JackpotSportTabService(
      deviceService,
      storageService,
      userService,
      bppService,
      clientUserAgentService,
      timeSyncService
    );
  });

  it('placeJackpotBet', () => {
    service.placeJackpotBet(10, 1, ['123', '234'], <IPoolEntity>{}, 5);
    expect(bppService.send).toHaveBeenCalled();
  });

  it('removeAllBets', () => {
    service.removeAllBets();
    expect(storageService.set).toHaveBeenCalledWith('footballJackpot', []);
  });

  it('removeStake', () => {
    service.removeStake();
    expect(storageService.set).toHaveBeenCalledWith('footballJackpotStake', 1);
  });

  it('getStake', () => {
    expect(service.getStake()).toEqual(1);
  });

  it('addStake', () => {
    service.addStake(100);
    expect(storageService.set).toHaveBeenCalledWith('footballJackpotStake', 100);
  });

  it('isSelected', () => {
    service.betsArray = ['10', '12'];
    expect(service.isSelected('12')).toEqual(true);
  });

  describe('addBet', () => {
    it('addBet (selected)', () => {
      const eventEntity = <any>{
        selected: 1
      };
      service.betsArray = ['10', '12'];

      service.addBet('10', eventEntity);
      expect(service.betsArray.length).toEqual(1);
      expect(storageService.set).toHaveBeenCalledWith('footballJackpot', ['12']);
    });

    it('addBet (!selected)', () => {
      const eventEntity = <any>{
        selected: 1
      };
      service.betsArray = ['10', '12'];

      service.addBet('11', eventEntity);
      expect(service.betsArray.length).toEqual(3);
      expect(storageService.set).toHaveBeenCalledWith('footballJackpot', ['10', '12', '11']);
    });
  });

  it('makeLuckyDip', () => {
    const initialData = <any>[
      {
        selected: 0,
        markets: [
          {
            outcomes: [
              {
                id: '1',
                outcomeStatusCode: 'S'
              },
              {
                id: '2',
                outcomeStatusCode: 'A'
              }
            ]
          }
        ]
      }
    ];

    service.makeLuckyDip(initialData);
    expect(storageService.set).toHaveBeenCalledWith('footballJackpot', ['2']);
  });

  describe('placeJackpotBet', () => {
    it('placeJackpotBet', () => {
      const pool = <any>{};

      service.placeJackpotBet(10, 2, ['1'], pool, 3).subscribe(() => {
        expect(bppService.send).toHaveBeenCalledWith(1);
      }, () => {});
    });

    it('placeJackpotBet (NOT_LOGGEDIN)', () => {
      const pool = <any>{};

      userService.status = false;

      service.placeJackpotBet(10, 2, ['1'], pool, 3).subscribe(() => {}, e => {
        expect(e.code).toEqual('NOT_LOGGEDIN');
      });
    });

    it('placeJackpotBet (INSUFFICIENT_FUNDS)', () => {
      const pool = <any>{};

      userService.sportBalance = 1;

      service.placeJackpotBet(10, 2, ['1'], pool, 3).subscribe(() => {}, e => {
        expect(e.code).toEqual('INSUFFICIENT_FUNDS');
      });
    });
  });

  it('sortJackpotData', () => {
    const data = <any>[
      {
        name: '2',
        displayOrder: 2,
        typeDisplayOrder: 1,
        classDisplayOrder: 2,
        startTime: 4
      },
      {
        name: '1',
        displayOrder: 1,
        typeDisplayOrder: 10,
        classDisplayOrder: 4,
        startTime: 1
      }
    ];

    expect(service.sortJackpotData(data)[0].name).toEqual('1');
  });

  describe('sentBetRequest', () => {
    it('sentBetRequest', () => {
      const pool = <any>{};
      const data = <any>{};

      bppService.send.and.returnValue(of(data));
      service['sentBetRequest'](10, 2, ['1'], pool, 3).subscribe(result => {
        expect(result).toEqual(data);
      });
    });

    it('sentBetRequest (error)', () => {
      const pool = <any>{};
      const data = <any>{
        betError: [
          {
            subErrorCode: 2
          }
        ]
      };

      bppService.send.and.returnValue(of(data));
      service['sentBetRequest'](10, 2, ['1'], pool, 3).subscribe(() => {}, e => {
      expect(e.code).toBeUndefined();
      });
    });
  });
});
