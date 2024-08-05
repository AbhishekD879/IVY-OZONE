import { FavouritesStorageService } from '@app/favourites/services/favourites-storage.service';

describe('FavouritesStorageService', () => {
  let service;
  let storageService;

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy('get').and.returnValue({}),
      set: jasmine.createSpy('get')
    };

    service = new FavouritesStorageService(storageService);
  });

  it('should create service instance', () => {
    expect(service).toBeTruthy();
  });

  describe('get', () => {
    it('should return object from storage service',  () => {
      const actualResult = service.get();

      expect(actualResult).toEqual({});
    });

    it('should return empty object',  () => {
      storageService.get.and.returnValue(null);

      const actualResult = service.get();

      expect(actualResult).toEqual({});
    });
  });

  it('should store data',  () => {
    service.store({});

    expect(storageService.set).toHaveBeenCalledWith('favourites', {});
  });
});
