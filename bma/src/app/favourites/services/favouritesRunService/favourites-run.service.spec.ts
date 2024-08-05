import { FavouritesRunService } from '@app/favourites/services/favouritesRunService/favourites-run.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';

describe('FavouritesRunService', () => {
  let service: FavouritesRunService,
    commandService,
    injector,
    callback;


  beforeEach(() => {
    commandService = {
      register: jasmine.createSpy('register').and.callFake((a, fn) => {
        callback = fn;
      }),
      API: {
        SYNC_FAVOURITES_FROM_NATIVE: 'SYNC_FAVOURITES_FROM_NATIVE'
      }
    };
    injector = {
      get: jasmine.createSpy().and.returnValue({
        syncFromNative: jasmine.createSpy('syncFromNative')
      } as any)
    };
    service = new FavouritesRunService(
      commandService as any,
      injector as any);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('run', () => {
    service.run();
    callback();

    expect(commandService.register).toHaveBeenCalledWith('SYNC_FAVOURITES_FROM_NATIVE', jasmine.any(Function));
  });

  it('favouritesService', () => {
    const favouritesService = service['favouritesService'];

    expect(injector.get).toHaveBeenCalledWith(FavouritesService);
    expect(typeof(favouritesService)).toEqual('object');
  });
});
