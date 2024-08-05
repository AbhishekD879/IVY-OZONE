import { BsDocService } from './bs-doc.service';
import { IBuildBetResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('BsDocService', () => {
  let service;
  let betFactoryService;
  let legFactoryService;
  let betErrorService;

  beforeEach(() => {
    betFactoryService = {
      constructBets: jasmine.createSpy('constructBets').and.returnValue('constructedBets')
    };
    legFactoryService = {
      parseLegs: jasmine.createSpy('parseLegs').and.returnValue('parsedLegs')
    };
    betErrorService = {
      parseErrors: jasmine.createSpy('parseErrors').and.returnValue('parsedErrors')
    };

    service = new BsDocService(betFactoryService, legFactoryService, betErrorService);
  });

  it('should parse json element', () => {
    expect(service['el']('firstName', 'Robert')).toEqual({ firstName: 'Robert' });
  });

  it('should return abstract content', () => {
    expect(service.content({ id: '1' })).toEqual({});
  });

  it('should build request param', () => {
    service.action = 'id';
    expect(service.buildRequest({ test: 'data' })).toEqual({ id: { } });
  });

  describe('setResponse', () => {
    it('should parse response with only legs', () => {
      const response = {
        legs: []
      };
      service.setResponse(response as IBuildBetResponse);

      expect(legFactoryService.parseLegs).toHaveBeenCalledWith(response.legs);
      expect(betErrorService.parseErrors).toHaveBeenCalledWith([]);
      expect(betFactoryService.constructBets).toHaveBeenCalledWith([], 'parsedLegs', 'parsedErrors');
    });

    it('should parse response with legs and response bet', () => {
      const response = {
        legs: [],
        bet: [{ id: '1' }]
      };
      service.setResponse(response as IBuildBetResponse);

      expect(legFactoryService.parseLegs).toHaveBeenCalledWith(response.legs);
      expect(betErrorService.parseErrors).toHaveBeenCalledWith([]);
      expect(betFactoryService.constructBets).toHaveBeenCalledWith(response.bet, 'parsedLegs', 'parsedErrors');
    });

    it('should parse response with only isLotto', () => {
      const response =[
        {
            isLotto:true,                    
        },
    ]as any;
      service.setResponse(response as IBuildBetResponse);
      expect(response[0].isLotto).toEqual(true);
     });

    it('should parse response with legs and response bets', () => {
      const response = {
        legs: [],
        bet: [{ id: '1' }],
        bets: [{ id: '1', documentId: '12' }],
        betErrors: [{ code: '500' }],
        betOfferRef: 'Some offer'
      };
      const result = service.setResponse(response as IBuildBetResponse);

      expect(legFactoryService.parseLegs).toHaveBeenCalledWith(response.legs);
      expect(betErrorService.parseErrors).toHaveBeenCalledWith(response.betErrors);
      expect(betFactoryService.constructBets).toHaveBeenCalledWith(response.bets, 'parsedLegs', 'parsedErrors');
      expect(Object.keys(result)).toEqual(['legs', 'bets', 'errs', 'betOffers']);
    });
  });
});
