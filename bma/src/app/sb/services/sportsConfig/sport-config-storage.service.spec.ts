import { SportsConfigStorageService } from './sport-config-storage.service';
import { ReplaySubject } from 'rxjs';
import { ISportInstance } from '@app/core/services/cms/models';

describe('SportsConfigStorageService', () => {
  let service: SportsConfigStorageService;

  beforeEach(() => {
    service = new SportsConfigStorageService();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#storeSport', () => {
    it('should call storeSport method', () => {
      const sportInstane =  new ReplaySubject<ISportInstance>(1);

      service.storeSport('football', sportInstane);

      expect(service['sportInstanceStore']['football']).toEqual(sportInstane);
    });
  });

  describe('#getSport', () => {
    it('should call getSport method if no sport instance', () => {
      const result = service.getSport('football');

      expect(result).toEqual(undefined);
    });

    it('should call getSport method with instance', () => {
      const sportInstane = new ReplaySubject<ISportInstance>(1);

      service.storeSport('football', sportInstane);

      const result = service.getSport('football');

      expect(service['sportInstanceStore']['football']).toEqual(sportInstane);
      expect(result).toEqual(sportInstane);
    });
  });

  describe('#getSports', () => {
    it('should call getSports method if no sport instances and no sportNames', () => {
      const result = service.getSports(undefined);

      expect(result).toEqual({});
    });

    it('should call getSports method if no sport instances', () => {
      const result = service.getSports(['football']);

      expect(result).toEqual({});
    });

    it('should call getSport method with instance', () => {
      const sportInstane = new ReplaySubject<ISportInstance>(1);

      service.storeSport('football', sportInstane);
      service.storeSport('basketball', sportInstane);
      service.storeSport('cricket', sportInstane);

      const result = service.getSports(['football']);

      expect(service['sportInstanceStore']['football']).toEqual(sportInstane);
      expect(result).toEqual({
        football: sportInstane
      });
    });
  });
});
