import { ExternalLinksPageComponent } from './external-links-page.component';
import { of } from 'rxjs';

describe('Object', () => {
  let component: ExternalLinksPageComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let externalLinksService;

  beforeEach(() => {
    apiClientService = {
      externalLinks: () => externalLinksService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    externalLinksService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: [] }))
    };

    component = new ExternalLinksPageComponent(
      apiClientService, globalLoaderService, dialogService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(externalLinksService.findAllByBrand).toHaveBeenCalled();
  });
});
