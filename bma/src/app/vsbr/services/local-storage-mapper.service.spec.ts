import { LocalStorageMapperService } from './local-storage-mapper.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LocalStorageMapperService', () => {
  let service: LocalStorageMapperService;

  let windowRefService;
  let pubSubService;
  let pubSubCbMap;
  let storageService;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        localStorage: {
          getItem: jasmine.createSpy('getItem'),
          setItem: jasmine.createSpy('setItem'),
          removeItem: jasmine.createSpy('removeItem')
        },
        vsmobile: {
          instance: {
            deselectBet: jasmine.createSpy('deselectBet')
          }
        }
      }
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((ch, name, cb) => pubSubCbMap[name] = cb),
      API: pubSubApi
    };
    pubSubCbMap = {};

    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove')
    };

    service = new LocalStorageMapperService(
      windowRefService,
      pubSubService,
      storageService
    );
  });

  describe('init', () => {
    it('handle REMOVE_VS_STORAGE event', () => {
      storageService.get.and.returnValue('{ "1": "key1" }');
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue('[{}]');

      service.init();
      pubSubCbMap['REMOVE_VS_STORAGE'](1);

      expect(storageService.get).toHaveBeenCalledWith('vsbr-selection-map');
      expect(windowRefService.nativeWindow.localStorage.getItem)
        .toHaveBeenCalledWith('vsm-betmanager-coralvirtuals-en-selections');
      expect(windowRefService.nativeWindow.vsmobile.instance.deselectBet).toHaveBeenCalledWith('key1');
      expect(storageService.set).toHaveBeenCalledWith('vsbr-selection-map', '{}');
      expect(windowRefService.nativeWindow.localStorage.setItem)
        .toHaveBeenCalledWith('vsm-betmanager-coralvirtuals-en-selections', '[{}]');
    });

    it('handle REMOVE_VS_STORAGE event (no data in storage)', () => {
      storageService.get.and.returnValue('null');
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(null);
      windowRefService.nativeWindow.vsmobile = null;

      service.init();
      pubSubCbMap['REMOVE_VS_STORAGE'](1);

      expect(storageService.get).toHaveBeenCalledWith('vsbr-selection-map');
      expect(windowRefService.nativeWindow.localStorage.getItem)
        .toHaveBeenCalledWith('vsm-betmanager-coralvirtuals-en-selections');
      expect(storageService.set).toHaveBeenCalledWith('vsbr-selection-map', '{}');
      expect(windowRefService.nativeWindow.localStorage.setItem)
        .toHaveBeenCalledWith('vsm-betmanager-coralvirtuals-en-selections', '[]');
    });

    it('handle FLUSH_VS_STORAGE event', () => {
      service.init();
      pubSubCbMap['FLUSH_VS_STORAGE']();
      expect(storageService.remove).toHaveBeenCalledWith('vsbr-selection-map');
      expect(windowRefService.nativeWindow.localStorage.removeItem).toHaveBeenCalledWith(
        'vsm-betmanager-coralvirtuals-en-selections' );
    });
  });
});
