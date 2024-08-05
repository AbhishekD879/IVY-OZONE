import { of } from 'rxjs';
import { EdpListComponent } from './edp-list.component';

describe('EdpListComponent', () => {
  let component: EdpListComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let router;
  let snackBar;
  let edpService;

  beforeEach(() => {
    apiClientService = {
      edp: () => edpService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    dialogService = {};
    router = {};
    snackBar = {};
    edpService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
    };

    component = new EdpListComponent(
      apiClientService, globalLoaderService, dialogService, router, snackBar
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(edpService.findAllByBrand).toHaveBeenCalled();
  });
});
