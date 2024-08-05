import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { fakeAsync, tick } from '@angular/core/testing';

const MOCK_EVENT_ARRAY: any = [
  {
    markets: [
      {
        outcomes: [
          {
            prices: [1, 2, 3]
          }
        ]
      }
    ]
  },

  {
    markets: [
      {
        outcomes: [
          {
            prices: [1, 2, 3]
          }
        ]
      }
    ]
  },

  {
    markets: [
      {
        outcomes: [
          {
            prices: []
          }
        ]
      }
    ]
  }
];

const MOCK_SS_RESPONSE_ENTITY: any = {
  SSResponse: {
    children: [1, 2, 3, 4, 5]
  }
};

describe('SiteServerUtilityService', () => {
  let service: SiteServerUtilityService;

  beforeEach(() => {
    service = new SiteServerUtilityService();
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  describe('filterEventsWithPrices', () => {
    it('Should return correct events if all conditions true', () => {
      expect(service.filterEventsWithPrices(MOCK_EVENT_ARRAY).length).toEqual(2);
    });
  });

  describe('stripResponse', () => {
    it('Should call addResponseCreationTime with correct params and return correct result', () => {
      spyOn(service, 'addResponseCreationTime').and.returnValue('result' as any);

      expect('result').toEqual(service.stripResponse(MOCK_SS_RESPONSE_ENTITY));
      expect(service.addResponseCreationTime).toHaveBeenCalledWith(
        MOCK_SS_RESPONSE_ENTITY.SSResponse.children.slice(0, -1), 5 as any
      );
    });

    it('should return empty list if there is no data', () => {
      expect(service.stripResponse({ SSResponse: {} } as any)).toEqual([]);
      expect(service.stripResponse({} as any)).toEqual([]);
    });
  });

  describe('queryService', () => {
    it('Shoulf call service which return promise and call stripResponse method after promise will resolve', fakeAsync(() => {
      spyOn(service, 'stripResponse');

      service.queryService(
        () => Promise.resolve(MOCK_SS_RESPONSE_ENTITY),
        {a: 1, b: 2}
      );

      tick();

      expect(service.stripResponse).toHaveBeenCalledWith(MOCK_SS_RESPONSE_ENTITY);
    }));
  });

  describe('addResponseCreationTime', () => {
    it('Should add response creation time and return entities array', () => {
      const responseFooter = {
        responseFooter: { creationTime: 1563448833 }
      } as any;

      expect(MOCK_EVENT_ARRAY).toEqual(service.addResponseCreationTime(MOCK_EVENT_ARRAY, responseFooter));
    });
  });
});
