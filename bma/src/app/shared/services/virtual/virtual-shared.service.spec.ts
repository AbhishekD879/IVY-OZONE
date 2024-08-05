import { VirtualSharedService } from './virtual-shared.service';
import { ISportEvent } from '@core/models/sport-event.model';
import environment from '@environment/oxygenEnvConfig';
import { of } from 'rxjs';

describe('VirtualSharedService', () => {
  let service;
  let cmsService;

  beforeEach(() => {
    cmsService = {
      getVirtualSportAliases: jasmine.createSpy().and.returnValue(of([
        {
          'classId': '127',
          'parent': 'virtual-football',
          'child': 'football-rush',
          'events': {}
        },
        {
          'classId': '128',
          'parent': 'virtual-football',
          'child': 'epl-football',
          'events': {
            'Chelsea-MU': 'chelsea-mu',
            'Super\'s Complex le` Event~e': 'super-s-complex-le--event-e'
          }
        },
        {
          'classId': '4334',
          'parent': 'virtual-horse-racing',
          'child': 'virtual-grand-national',
          'events': {
            'Laddies Leap\'s Lane': 'laddies-leap-s-lane'
          }
        },
        {
          'classId': '123',
          'parent': 'virtual-horse-racing',
          'child': 'virtual-racing',
        }
      ]))
    };


    service = new VirtualSharedService(cmsService);
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });
  it('ngOnDestroy', () => {
    service.cmsInitialDataSubscription = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    service.ngOnDestroy();
    expect(service.cmsInitialDataSubscription.unsubscribe).toHaveBeenCalled();
  });

  describe('getVirtualSilkSrc', () => {
    it('should remove single quote from Laddies Leap\'s Lane event name', () => {
      const silkName = '1';
      const event = {
        classId: '4334',
        className: 'Virtual Grand National',
        name: 'Laddies Leap\'s Lane'
      } as ISportEvent;

      expect(service.getVirtualSilkSrc(event, silkName)).toEqual(`${environment.CMS_ROOT_URI}/images/uploads/virtuals`
        + `/virtual-horse-racing/virtual-grand-national/laddies-leap-s-lane/1.png`);
    });

    it('should generate silk name', () => {
      const silkName = '2';
      const event = {
        classId: '123',
        className: 'Virtual Racing',
        name: 'Laddies Horses'
      } as ISportEvent;

      expect(service.getVirtualSilkSrc(event, silkName)).toEqual(`${environment.CMS_ROOT_URI}/images/uploads/virtuals`
        + `/virtual-horse-racing/virtual-racing/2.png`);
    });

    it('should skip event part if none present', () => {
      const silkName = '7';
      const event = {
        classId: '127',
        className: 'Football Rush',
        name: 'Non existent Event'
      } as ISportEvent;

      expect(service.getVirtualSilkSrc(event, silkName)).toEqual(`${environment.CMS_ROOT_URI}/images/uploads/virtuals`
        + `/virtual-football/football-rush/7.png`);
    });

    it('should generate silk with formatted complex event name', () => {
      const silkName = '7';
      const event = {
        classId: '128',
        className: 'EPL',
        name: 'Super\'s Complex le` Event~e'
      } as ISportEvent;

      expect(service.getVirtualSilkSrc(event, silkName)).toEqual(`${environment.CMS_ROOT_URI}/images/uploads/virtuals`
        + `/virtual-football/epl-football/super-s-complex-le--event-e/7.png`);
    });

    it('should match alias for event with time', () => {
      const silkName = '5';
      const event = {
        classId: '4334',
        className: 'Virtual Grand National',
        name: '11:55 Laddies Leap\'s Lane'
      } as ISportEvent;

      expect(service.getVirtualSilkSrc(event, silkName)).toEqual(`${environment.CMS_ROOT_URI}/images/uploads/virtuals`
        + `/virtual-horse-racing/virtual-grand-national/laddies-leap-s-lane/5.png`);
    });

    it('should return undefined if no aliases match', () => {
      const silkName = '7';
      const event = {
        classId: 'not-configured',
        className: 'test-class',
        name: 'test-event'
      } as ISportEvent;

      expect(service.getVirtualSilkSrc(event, silkName)).toBeUndefined();
    });
  });

  describe('formVirtualEventUrl', () => {
    it('should generate event url', () => {
      const event = {
        classId: '123',
        className: 'Virtual Racing',
        name: 'Laddies Horses',
        id: 1000
      } as ISportEvent;

      expect(service.formVirtualEventUrl(event)).toEqual('virtual-sports/sports/virtual-horse-racing/virtual-racing/1000');
    });

    it('should return undefined if no aliases match', () => {
      const event = {
        classId: 'not-configured',
        className: 'test-class',
        name: 'test-event',
        id: 1000
      } as ISportEvent;

      expect(service.formVirtualEventUrl(event)).toBeUndefined();
    });

    it('should return undefined if no aliases', () => {
      const cmsServiceNoData = {
        getVirtualSportAliases: jasmine.createSpy().and.returnValue(of(''))
      } as any;
      const event = {
        classId: 'not-configured',
        className: 'test-class',
        name: 'test-event',
        id: 1000
      } as ISportEvent;

      const serviceNodata= new VirtualSharedService(cmsServiceNoData);
      expect(serviceNodata.formVirtualEventUrl(event)).toBeUndefined();
    });
  });

  describe('formVirtualTypeUrl', () => {
    it('should generate type url', () => {
      const event = {
        classId: '123',
        className: 'Virtual Racing',
        name: 'Laddies Horses',
        id: 1000
      } as ISportEvent;

      expect(service.formVirtualTypeUrl(event.classId)).toEqual('virtual-sports/sports/virtual-horse-racing/virtual-racing');
    });

    it('should generate virtual sport url', () => {
      expect(service.formVirtualTypeUrl(undefined)).toEqual('virtual-sports/sports');
    });
  });

  describe('isVirtual', () => {
    it('should check if it is Virtual Sport', () => {
      expect(service.isVirtual('39')).toBe(true);
      expect(service.isVirtual('21')).toBe(false);
    });
  });
});
