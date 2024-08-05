import { of } from 'rxjs';
import { BannerPageComponent } from './banner.page.component';

describe('BannerPageComponent', () => {
  let component: BannerPageComponent;
  let dialogService;
  let route;
  let router;
  let bannersApiService;

  beforeEach(() => {
    dialogService = {};
    route = {
      snapshot: {
        paramMap: { get: jasmine.createSpy('get') }
      }
    };
    router = {};
    bannersApiService = {
      getSingleBannerData: jasmine.createSpy('getSingleBannerData').and.returnValue(of({ body: {} })),
      getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({ body: {} }))
    };

    component = new BannerPageComponent(
      dialogService, route, router, bannersApiService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(route.snapshot.paramMap.get).toHaveBeenCalled();
  });
});

