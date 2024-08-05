import {StaticBlocksPageComponent} from './static-blocks-page.component';
import { of } from 'rxjs';

describe('StaticBlocksPageComponent', () => {
  let component: StaticBlocksPageComponent;
  let apiClientService, globalLoaderService, dialogService, router;

  beforeEach(() => {
    router = {};
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      staticBlocks: jasmine.createSpy('staticBlocks').and.returnValue({
        findAllByBrand: jasmine.createSpy('getById').and.returnValue(of({
          body: {
            test: ''
          }
        }))
      })
    };

    component = new StaticBlocksPageComponent(
      apiClientService, globalLoaderService, dialogService, router
    );
    component.ngOnInit();
  });

  it('should load init data', () => {
    expect(apiClientService.staticBlocks).toHaveBeenCalled();
  });
});
