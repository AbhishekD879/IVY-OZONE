import { of } from 'rxjs';

import { TemplateListComponent } from './template-list.component';

describe('TemplateListComponent', () => {
  let component: TemplateListComponent;
  let dialog;
  let dialogService;
  let templateApiService;
  let globalLoaderService;
  let router;

  beforeEach(() => {
    dialog = {};
    dialogService = {};
    templateApiService = {
      getTemplatesByBrand: jasmine.createSpy('getTemplatesByBrand').and.returnValue(of({}))
    };
    globalLoaderService = {};
    router = {};

    component = new TemplateListComponent(
      dialog, dialogService, templateApiService, globalLoaderService, router
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(templateApiService.getTemplatesByBrand).toHaveBeenCalled();
  });
});
