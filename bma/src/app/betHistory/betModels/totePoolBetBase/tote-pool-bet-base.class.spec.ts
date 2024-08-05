import TotePoolBetBase from './TotePoolBetBaseClass';
import quadpodBet from './../../mocks/quadpotBet.mock';

describe('TotePoolBetBase', () => {
  let bet;
  let betHistoryMainService;
  let userService;
  let localeService;
  let timeService;
  let cashOutMapIndexService;
  let instance: TotePoolBetBase;
  let currencyPipe;

  beforeEach(() => {
    bet = Object.assign({}, quadpodBet);

    betHistoryMainService = {
      getBetStatus: jasmine.createSpy('getBetStatus').and.returnValue('pending')
    };
    userService = {
      currencySymbol: '$'
    };
    localeService = {};
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('15:10')
    };
    cashOutMapIndexService = {
      create: jasmine.createSpy('cashOutMapIndexService.create')
    };

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    instance = new TotePoolBetBase(
      bet,
      betHistoryMainService,
      userService,
      localeService,
      timeService,
      cashOutMapIndexService,
      currencyPipe
    );
  });

  describe('constructor', () => {
    it('should properly init scoop6 bet type', () => {
      expect(instance.isScoop6Pool).toBeFalsy();
      expect(instance.isUkToteBet).toBeTruthy();
    });
    it('should properly init scoop6 bet type', () => {
      bet.poolType = 'Scoop6';
      bet.poolSource = 'PGI';
      instance = new TotePoolBetBase(
        bet,
        betHistoryMainService,
        userService,
        localeService,
        timeService,
        cashOutMapIndexService,
        currencyPipe
      );
      expect(instance.isScoop6Pool).toBeTruthy();
      expect(instance.isUkToteBet).toBeFalsy();
    });
  });

  describe('addLiveUpdatesProperties', () => {
    it('should call proper methods and set toteEventId property of each leg', () => {
      spyOn(instance, '_fillIdsProperties').and.callThrough();
      spyOn(instance, '_updateCashoutMapIndex').and.callThrough();
      instance.extendWithLinkedEvents({});
      instance.addLiveUpdatesProperties();
      expect(instance._fillIdsProperties).toHaveBeenCalled();
      expect(instance._updateCashoutMapIndex).toHaveBeenCalled();
      const legsToteEventIdProperty = instance.leg.map(leg => leg.toteEventId);
      expect(legsToteEventIdProperty).toEqual([ '9771687', '9771688', '9771689', '9771690' ]);
    });
  });

  describe('extendWithLinkedEvents', () => {
    it('should`nt change ids of outcomes, markets and events to linked Fixed events ones if they don`t match', () => {
      instance.extendWithLinkedEvents({});
      const outcomes = instance.leg.map(leg => leg.part)
        .reduce((x, y) => x.concat(y), [])
        .map(x => x.outcome);

      expect(outcomes.map(x => x.id)).toEqual([ '542164253', '542164254', '542164264', '542164279', '542164288' ] as any);
      expect(outcomes.map(x => x.market.id)).toEqual([ '145099699', '145099699', '145099700', '145099701', '145099702' as any]);
      expect(outcomes.map(x => x.event.id)).toEqual([ '9771687', '9771687', '9771688', '9771689', '9771690' as any]);
      expect(outcomes.map(x => x.event.toteEventId)).toEqual([ '9771687', '9771687', '9771688', '9771689', '9771690' as any]);
      expect(instance.fixedEventLinked).toEqual(true);
    });
    it('should change ids of outcomes, markets and events to linked Fixed events ones', () => {
      instance.extendWithLinkedEvents({
        '9771687': 'NON-TOTE-9771687',
        '145099699': 'NON-TOTE-145099699',
        '542164253': 'NON-TOTE-542164253'
      });
      const outcomes = instance.leg.map(leg => leg.part)
        .reduce((x, y) => x.concat(y), [])
        .map(x => x.outcome);

      expect(outcomes.map(x => x.id)).toEqual([ 'NON-TOTE-542164253', '542164254', '542164264', '542164279', '542164288' as any]);
      expect(outcomes.map(x => x.market.id)).toEqual([ 'NON-TOTE-145099699', 'NON-TOTE-145099699',
        '145099700', '145099701', '145099702' as any]);
      expect(outcomes.map(x => x.event.id)).toEqual([ 'NON-TOTE-9771687', 'NON-TOTE-9771687', '9771688', '9771689', '9771690' as any]);
      expect(outcomes.map(x => x.event.toteEventId)).toEqual([ '9771687', '9771687', '9771688', '9771689', '9771690' as any]);
      expect(instance.fixedEventLinked).toEqual(true);
    });
  });

  describe('_setFavourites', () => {
    it('should set isFavourite property for Favourite horses', () => {
      const outcomes = [
        {
          outcomeMeaningMinorCode: 1
        },
        {
          outcomeMeaningMinorCode: 2
        },
        {}
      ] as any;
      instance._setFavourites(outcomes);
      expect(outcomes).toEqual([
        {
          outcomeMeaningMinorCode: 1,
          isFavourite: true
        },
        {
          outcomeMeaningMinorCode: 2,
          isFavourite: true
        },
        {
          isFavourite: false
        }
      ]);
    });
  });

  describe('getScoop6TrackName', () => {
    it('should parse string with name of Scoop6 race, and receive name from it', () => {
        expect(instance.getScoop6TrackName('Clone Race of Aintree Racecourse Race 5')).toEqual('Aintree Racecourse');
    });
    it('should handle edge cases', () => {
      expect(instance.getScoop6TrackName(undefined)).toEqual('');
      expect(instance.getScoop6TrackName('some name')).toEqual('');
    });
  });

  describe('getRaceTitle', () => {
    it('should return correct track title for non scoop6 event', () => {
      instance.isScoop6Pool = false;
        expect(instance.getRaceTitle({
          track: 'Chepstow',
          startTime: '2019-05-15 15:10:00'
        } as any)).toEqual('15:10 Chepstow');
        expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date('2019-05-15 15:10:00'), 'HH:mm');
    });
    it('should return correct track title for scoop6 event', () => {
      instance.isScoop6Pool = true;
      expect(instance.getRaceTitle({
        track: 'scoop6', // for Scoop6 track field is not correct
        startTime: '2019-05-15 15:15:00',
        name: 'Clone Race of Chepstow Race 5'
      } as any)).toEqual('15:10 Chepstow');
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date('2019-05-15 15:15:00'), 'HH:mm');
    });
  });

});
