import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('LoadByPortionsService', () => {
  let service: LoadByPortionsService;
  let ssUtility;

  beforeEach(() => {
    ssUtility = {
      stripResponse: jasmine.createSpy('stripResponse'),
      filterEventsWithPrices: jasmine.createSpy('filterEventsWithPrices'),
      queryService: jasmine.createSpy('queryService'),
      addResponseCreationTime: jasmine.createSpy('addResponseCreationTime')
    };

    service = new LoadByPortionsService(ssUtility);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('concatResponses should call stripResponse', () => {
    const data = [{
      SSResponse: {
        children: [{
          responseFooter: {
            cost: 'cost',
            creationTime: 'creationTime'
          }
        }],
        xmlns: 'xmlns'
      }
    }];

    service['concatResponses'](data);

    expect(ssUtility.stripResponse).toHaveBeenCalled();
  });

  describe('chunkArray', () => {
    it('should return array of arrays', () => {
      const ids = [1, 2, 3],
        result = service['chunkArray'](ids, service['maxClassesInRequest']);

      expect(result).not.toBe([ids]);
      expect(result).toEqual([ids]);
    });

    it('should contain arrays of maxlength 100 each', () => {
      const ids = Array.from(Array(200), (item, index) => index + 1),
        result = service['chunkArray'](ids, service['maxClassesInRequest']);

      expect(result).toEqual([ids.slice(0, 100), ids.slice(100, 201)]);
    });

    it('should return array if ids is empty', () => {
      const ids = [],
        result = service['chunkArray'](ids, service['maxClassesInRequest']);

      expect(result.length).toEqual(0);
    });
  });

  it('loadPortion should call passed service', () => {
    const loadPortion = {
      service: () => {
      }
    };

    const spy = spyOn(loadPortion, 'service');

    service['loadPortion'](loadPortion.service, {}, 'typeId', []);

    expect(spy).toHaveBeenCalled();
  });

  describe('get', () => {
    const serviceFunction = () => {
    };

    beforeEach(() => {
      service['chunkArray'] = jasmine.createSpy('chunkArray').and.returnValue([]);
      service['concatResponses'] = jasmine.createSpy('concatResponses');
    });

    it('should be called with typeId key', () => {
      const spy = spyOn(service, 'get');

      spy(serviceFunction, {}, 'typeId', [1, 2]);

      expect(spy).toHaveBeenCalledWith(serviceFunction, {}, 'typeId', [1, 2]);
    });

    it('should be called with eventsIds key', () => {
      const spy = spyOn(service, 'get');

      spy(serviceFunction, {}, 'eventsIds', [1, 2]);

      expect(spy).toHaveBeenCalledWith(serviceFunction, {}, 'eventsIds', [1, 2]);
    });

    it('should call chunkArray once', fakeAsync(() => {
      service.get(serviceFunction, {}, 'typeId', [1, 2]);

      tick();

      expect(service['chunkArray']).toHaveBeenCalledTimes(1);
    }));

    it('should call concatResponses once', fakeAsync(() => {
      service.get(serviceFunction, {}, 'typeId', [1, 2]);

      tick();

      expect(service['concatResponses']).toHaveBeenCalledTimes(1);
    }));
  });
});
