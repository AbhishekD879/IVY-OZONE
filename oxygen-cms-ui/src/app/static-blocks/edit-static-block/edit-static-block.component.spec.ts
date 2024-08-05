import { EditStaticBlockComponent } from './edit-static-block.component';
import { of } from 'rxjs';

describe('EditStaticBlockComponent', () => {
  let component: EditStaticBlockComponent;
  let globalLoaderService, apiClientService, activatedRoute, dialogService, router;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      staticBlocks: jasmine.createSpy('staticBlocks').and.returnValue({
        getById: jasmine.createSpy('getById').and.returnValue(of({
          body: {
            test: ''
          }
        }))
      })
    };

    component = new EditStaticBlockComponent(
      globalLoaderService, apiClientService, activatedRoute, dialogService, router
    );
    component.ngOnInit();
  });

  it('should load init data', () => {
    const res = {test: ''} as any;
    expect(apiClientService.staticBlocks).toHaveBeenCalled();
    expect(component.staticBlock).toEqual(res);
  });
});
