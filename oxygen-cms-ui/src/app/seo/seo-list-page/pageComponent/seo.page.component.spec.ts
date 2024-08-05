import { SeoPagesListPageComponent } from './seo.page.component';
import { of } from 'rxjs';

describe('SeoPagesListPageComponent', () => {
  let component,
    dialogService,
    seoAPIService;

  beforeEach(() => {
    dialogService = {};
    seoAPIService = {
      getSeoListData: jasmine.createSpy('getSeoListData').and.returnValue(of({
        body: []
      }))
    };

    component = new SeoPagesListPageComponent(
      dialogService,
      seoAPIService
    );

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.seoPagesData).toBeDefined();
  });
});
