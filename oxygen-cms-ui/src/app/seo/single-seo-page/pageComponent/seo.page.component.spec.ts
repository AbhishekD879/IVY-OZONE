import { SingleSeoPageComponent } from './seo.page.component';
import { of } from 'rxjs';

describe('PromotionsPageComponent', () => {
  let component,
    dialogService,
    route,
    router,
    seoAPIService;

  beforeEach(() => {
    dialogService = {};
    route = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('paramMap.get')
        }
      }
    };
    router = {};
    seoAPIService = {
      getSingSeoItemData: jasmine.createSpy('getSingSeoItemData').and.returnValue(of({
        body: {
          id: 'pageIdMock',
          staticBlock: 'staticBlockMock',
          staticBlockTitle: ''
        }
      }))
    };

    component = new SingleSeoPageComponent(
      dialogService,
      route,
      router,
      seoAPIService
    );

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.seoPage).toBeDefined();
    expect(component.breadcrumbsData).toBeDefined();
  });

  it('should get default title', () => {
    expect(component.seoPage.staticBlockTitle).toEqual('SPORTS BETTING ONLINE');
  });
});
