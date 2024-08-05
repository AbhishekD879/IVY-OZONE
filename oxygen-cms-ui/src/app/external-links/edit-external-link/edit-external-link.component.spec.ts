import { EditExternalLinkComponent } from './edit-external-link.component';
import { of } from 'rxjs';

describe('EditExternalLinkComponent', () => {
  let component: EditExternalLinkComponent;
  let globalLoaderService;
  let apiClientService;
  let activatedRoute;
  let dialogService;
  let router;
  let externalLinksService;

  beforeEach(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      externalLinks: () => externalLinksService
    };
    activatedRoute = {
      params: of({})
    };
    dialogService = {};
    router = {};
    externalLinksService = {
      getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
    };

    component = new EditExternalLinkComponent(
      globalLoaderService, apiClientService, activatedRoute, dialogService, router
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(externalLinksService.getById).toHaveBeenCalled();
  });
});
