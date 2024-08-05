import { BetService } from './bet.service';
import { Bet } from '@betslip/services/bet/bet';

describe('BetService', () => {
  let service;
  let freeBetService;
  let betStakeService;
  let sportsLegPriceService;
  let overaskService;
  let localeService;
  let fracToDec;
  let filters;
  let betslipFilters;
  let storageService;
  let user;
  let pubSubService;
  let params;

  beforeEach(() => {
    params = {
      isMocked: true,
      uid: '1',
      placed: {
        id: '1'
      },
      docId: '11',
      type: 'single',
      betOffer: {},
      errs: [],
      freeBets: [],
      payout: [{
        legType: 'Y',
        potential: '1.00'
      }],
      winPlace: '1/4',
      lines: 1,
      stake: {
        doc: 'Y'
      },
      allLegs: []
    };
    freeBetService = {
      parse: jasmine.createSpy('parse'),
      construct: jasmine.createSpy('construct')
    };
    betStakeService = jasmine.createSpyObj('betStakeService', ['construct', 'parse']);
    sportsLegPriceService = jasmine.createSpyObj('sportsLegPriceService', ['convert']);
    overaskService = {};
    storageService = {};
    localeService = jasmine.createSpyObj('localeService', ['getString']);
    fracToDec = jasmine.createSpyObj('fracToDec', ['getDecimal']);
    filters = jasmine.createSpyObj('filters', ['filterAddScore', 'filterPlayerName']);
    betslipFilters = jasmine.createSpyObj('betslipFilters', ['handicapValueFilter']);
    user = { currencySymbol: '$' };
    pubSubService = jasmine.createSpyObj('pubSubService', ['publish', 'subscribe', 'unsubscribe']);
    service = new BetService(freeBetService, betStakeService, sportsLegPriceService, overaskService, localeService,
      fracToDec, filters, betslipFilters, storageService, user, pubSubService);
  });

  it('should construct bet', () => {
    const result = service.construct(params);

    expect(result).toEqual(jasmine.any(Bet));
  });

  describe('parse', () => {
    let rootBetDoc;
    let legs;

    beforeEach(() => {
      rootBetDoc = {
        id: '11',
        documentId : '1',
        timeStamp: 1541074570003,
        stake : {
          maxAllowed : '16000.00',
          currencyRef : {
            id : 'GBP'
          },
          minAllowed : '0.01'
        },
        payout : [{
          legType : 'W',
          potential : '1.125'
        }],
        legRef : [{
          documentId : '1'
        }],
        leg: {
          documentId: '12'
        },
        lines : {
          number : 1
        },
        betTypeRef : {
          id: 'SGL',
          ordering: '1'
        },
        freebet: [],
        eachWayAvailable: 'Y'
      };
      legs = [];
    });

    it('should parse non receipt or BIR bet', () => {
      spyOn(service, 'construct').and.callThrough();

      const result = service.parse(rootBetDoc, legs);

      expect(betStakeService.parse).toHaveBeenCalledWith(rootBetDoc.stake, rootBetDoc.lines.number);
      expect(freeBetService.parse).toHaveBeenCalledWith(rootBetDoc.freebet);
      expect(service.construct).toHaveBeenCalledWith(jasmine.objectContaining({
        betOffer: {},
        docId: rootBetDoc.documentId,
        type: rootBetDoc.betTypeRef.id,
        lines: rootBetDoc.lines.number,
        legIds: ['1'],
        allLegs: legs,
        payout: rootBetDoc.payout,
        eachWayAvailable: 'Y'
      }));
      expect(result).toEqual(jasmine.any(Bet));
    });

    it('should parse receipt bet', () => {
      rootBetDoc['receipt'] = { receiptId: '123' };
      rootBetDoc.legRef = null;
      rootBetDoc.isConfirmed = 'Y';
      rootBetDoc.isSettled = 'Y';
      rootBetDoc.provider = 'OpenBet';

      spyOn(service, 'construct').and.callThrough();

      const result = service.parse(rootBetDoc, legs);

      expect(service.construct).toHaveBeenCalledWith(jasmine.objectContaining({
        legIds: rootBetDoc.leg.documentId,
        eachWayAvailable: rootBetDoc.eachWayAvailable,
        placed: jasmine.objectContaining({
          id: rootBetDoc.id,
          docId: rootBetDoc.documentId,
          time: jasmine.any(Date),
          confirmed: true,
          settled: true,
          provider: rootBetDoc.provider,
          receipt: rootBetDoc.receipt,
        })
      }));
      expect(result).toEqual(jasmine.any(Bet));
    });

    it('should parse OpenBetBir bet', () => {
      rootBetDoc.isConfirmed = 'N';
      rootBetDoc.provider = 'OpenBetBir';
      rootBetDoc.confirmationExpectedAt = 60;

      spyOn(service, 'construct').and.callThrough();

      const result = service.parse(rootBetDoc, legs);

      expect(service.construct).toHaveBeenCalledWith(jasmine.objectContaining({
        placed: jasmine.objectContaining({
          id: rootBetDoc.id,
          docId: rootBetDoc.documentId,
          confirmed: false,
          provider: rootBetDoc.provider,
          expectedAt: rootBetDoc.confirmationExpectedAt,
        }),
        eachWayAvailable: rootBetDoc.eachWayAvailable
      }));
      expect(result).toEqual(jasmine.any(Bet));
    });

    it('should parse (freeBets)', () => {
      rootBetDoc.freebet = [{ type: 'SPORTS' }];

      spyOn(service, 'construct').and.callThrough();
      freeBetService.parse.and.returnValue([rootBetDoc.freebet[0]]);
      const result = service.parse(rootBetDoc, legs);

      expect(service.construct).toHaveBeenCalledWith(jasmine.objectContaining({
        freeBets: [rootBetDoc.freebet[0]],
      }));
      expect(result).toEqual(jasmine.any(Bet));
    });

    it('should parse (oddsBoosts)', () => {
      rootBetDoc.freebet = [{ type: 'BETBOOST' }];

      spyOn(service, 'construct').and.callThrough();
      freeBetService.parse.and.returnValue([]);
      const result = service.parse(rootBetDoc, legs);

      expect(service.construct).toHaveBeenCalledWith(jasmine.objectContaining({
        oddsBoosts: [rootBetDoc.freebet[0]]
      }));
      expect(result).toEqual(jasmine.any(Bet));
    });

    it('should parse (no oddsBoosts)', () => {
      rootBetDoc.freebet = undefined;

      spyOn(service, 'construct').and.callThrough();
      freeBetService.parse.and.returnValue([]);
      const result = service.parse(rootBetDoc, legs);

      expect(service.construct).toHaveBeenCalledWith(jasmine.objectContaining({
        oddsBoosts: []
      }));
      expect(result).toEqual(jasmine.any(Bet));
    });

    it('should parse lotto bet data', () => {
      rootBetDoc = {
        id: '11',
        isLotto: true,
        payout : [{
          legType : 'W',
          potential : '1.125'
        }],
        legRef : [{
          documentId : '1'
        }],
        leg: {
          documentId: '12'
        },
        type: 'SGL',
        freebet: [],
        eachWayAvailable: 'Y'
      };
      legs = [];
      spyOn(service, 'construct').and.callThrough();

      const result = service.parse(rootBetDoc, legs);

      expect(result).toEqual(jasmine.any(Bet));
    });
  });
});
