import { YcStaticBlocksEditComponent } from './yc-static-blocks-edit.component';
import { of } from 'rxjs';

describe('YcStaticBlocksEditComponent', () => {
  let component, staticBlockAPIService, globalLoaderService, activatedRoute, dialogService, router;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    staticBlockAPIService = {
      getSingleStaticBlock: jasmine.createSpy('getSingleStaticBlock').and.returnValue(of({ body: {} }))
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    component = new YcStaticBlocksEditComponent(
      staticBlockAPIService,
      globalLoaderService,
      activatedRoute,
      dialogService,
      router
    );
    component.ngOnInit();
  });

  it('should show loader', () => {
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  });
});
