import { Observable } from 'rxjs';

import { InplayDataService } from './inplay-data.service';
import environment from '@environment/oxygenEnvConfig';

describe('InplayDataService', () => {
  let service: InplayDataService;

  let inPlayConnectionService;
  const windowRefService: any = {
    nativeWindow: {
      setTimeout: jasmine.createSpy('setTimeout').and.returnValue(10)
    }
  };

  const MESSAGES = {
    RIBBON: {
      RESPONSE_MESSAGE: 'INPLAY_SPORTS_RIBBON'
    },
    STRUCTURE: {
      RESPONSE_MESSAGE: 'INPLAY_STRUCTURE'
    },
    LS_STRUCTURE: {
      RESPONSE_MESSAGE: 'INPLAY_LS_STRUCTURE'
    },
    COMPETITION: {
      RESPONSE_MESSAGE: 'IN_PLAY_SPORT_TYPE'
    },
    virtuals: {
      RESPONSE_MESSAGE: 'GET_VIRTUAL_SPORTS_RIBBON_RESPONSE'
    }
  };

  beforeEach(() => {
    inPlayConnectionService = {
      emitSocket: jasmine.createSpy(),
      addEventListener: jasmine.createSpy(),
      setConnectionErrorState: jasmine.createSpy()
    };

    service = new InplayDataService(
      windowRefService,
      inPlayConnectionService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('loadData', () => {
    let loadParams;

    beforeEach(() => {
      loadParams = { categoryId: '16', modifyMainMarkets: true, topLevelType: 1 } as any;
      spyOn(service, 'modifyMainMarkets');
      inPlayConnectionService.addEventListener.and.callFake((msg, cb) => cb && cb());
    });

    it('loadData', () => {
      service.dataTypes = {
        test: {
          requestMessage: 'test',
          buildResponseMessage: jasmine.createSpy().and.returnValue('TEST'),
          additionalRequestParams: {}
        }
      } as any;

      loadParams = {};

    expect(service.loadData('test', loadParams)).toEqual(jasmine.any(Observable));
    expect(service.dataTypes['test'].buildResponseMessage).toHaveBeenCalledWith(loadParams);
    expect(inPlayConnectionService.addEventListener).toHaveBeenCalledWith(
      'TEST', jasmine.any(Function), true
    );
    expect(inPlayConnectionService.emitSocket).toHaveBeenCalledWith(
      service.dataTypes['test'].requestMessage, service.dataTypes['test'].additionalRequestParams
    );

      expect(service.loadDataTimeout).toBeDefined();
    });

    describe('should modifyMainMarkets if', () => {
      it(`categoryId equal footballId`, () => {
        loadParams.categoryId = environment.CATEGORIES_DATA.footballId;
      });

      it(`marketSelector is Falthy`, () => {
        delete loadParams.marketSelector;
      });

      it(`marketSelector equal 'Main Market'`, () => {
        loadParams.marketSelector = 'Main Market';
      });


      it(`modifyMainMarket is equal true'`, () => {
        loadParams.modifyMainMarkets = true;
      });


      afterEach(() => {
        service.loadData('sports', loadParams);

        expect(service.modifyMainMarkets).toHaveBeenCalled();
      });
    });


    describe('should Not modifyMainMarkets if', () => {
      it(`Not responseMessage is Not matched`, () => {
        spyOn(service.dataTypes.sports, 'buildResponseMessage').and.returnValue('text');
      });

      it(`categoryId in Not equal footballId`, () => {
        loadParams.categoryId = '1';
      });

      it(`marketSelector in Npt equal 'Main Market'`, () => {
        loadParams.marketSelector = 'text';
      });

      it(`modifyMainMarkets is equal false`, () => {
        loadParams.modifyMainMarkets = false;
      });

      afterEach(() => {
        service.loadData('sports', loadParams);

        expect(service.modifyMainMarkets).not.toHaveBeenCalled();
      });
    });
  });

  it('modifyMainMarkets', () => {
    const data: any = [
      {
        markets: [{
          templateMarketName: 'Penalty Shoot Out Winner'
        }]
      }
    ];
    service.modifyMainMarkets(data);
    expect(data[0].markets[0].marketMeaningMinorCode).toBe(service.MATCH_RESULT_MARKET_IDENTIFICATOR);
    expect(data[0].markets[0].dispSortName).toBe(service.MATCH_RESULT_MARKET_IDENTIFICATOR);
  });

  describe('dataTypes', () => {
    it(`should return RIBBON.RESPONSE_MESSAGE`, () => {
      const response_message = service.dataTypes.ribbon.buildResponseMessage();
      expect(response_message ).toEqual(MESSAGES.RIBBON.RESPONSE_MESSAGE);
    });
    it(`should return STRUCTURE.RESPONSE_MESSAGE`, () => {
      const response_message = service.dataTypes.structure.buildResponseMessage();
      expect(response_message).toEqual(MESSAGES.STRUCTURE.RESPONSE_MESSAGE);
    });
    it(`should return LS_STRUCTURE.RESPONSE_MESSAGE`, () => {
      const response_message = service.dataTypes.ls_structure.buildResponseMessage();
      expect(response_message).toEqual(MESSAGES.LS_STRUCTURE.RESPONSE_MESSAGE);
    });
    it(`should return COMPETITION.RESPONSE_MESSAGE`, () => {
      const data = {
        categoryId: '123',
        topLevelType: '234',
        typeId: '345'
      };
      const result = `${MESSAGES.COMPETITION.RESPONSE_MESSAGE}::123::234::345`;
      expect( service.dataTypes.competition.buildResponseMessage(data)).toEqual(result);
    });
    it(`should return COMPETITION.RESPONSE_MESSAGE with marketSelector`, () => {
      const data = {
        categoryId: '123',
        topLevelType: '234',
        typeId: '345',
        marketSelector: '456'
      };
      const result = `${MESSAGES.COMPETITION.RESPONSE_MESSAGE}::123::234::456::345`;
      expect( service.dataTypes.competition.buildResponseMessage(data)).toEqual(result);
    });
    it(`should return RIBBON.RESPONSE_MESSAGE`, () => {
      const response_message = service.dataTypes.virtuals.buildResponseMessage();
      expect(response_message ).toEqual(MESSAGES.virtuals.RESPONSE_MESSAGE);
    });
  });
});
