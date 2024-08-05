import { FeaturedEventsModuleComponent } from './featured-events-module.component';
import { of } from 'rxjs';

describe('FeaturedEventsModuleComponent', () => {
  let component,
    activatedRoute,
    sportsModulesService,
    sportsModulesBreadcrumbsService,
    snackBar;

  beforeEach(() => {
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    sportsModulesService = {
      getSingleModuleData: jasmine.createSpy('getSingleModuleData').and.returnValue(of([{}]))
    };
    sportsModulesBreadcrumbsService = {
      getBreadcrubs: jasmine.createSpy('getBreadcrubs').and.returnValue(of([]))
    };
    snackBar = {};

    component = new FeaturedEventsModuleComponent(
      activatedRoute,
      sportsModulesService,
      sportsModulesBreadcrumbsService,
      snackBar
    );

    component.ngOnInit();
  });

  it('should init Module', () => {
    expect(component.routeParams).toBeDefined();
    expect(component.module).toBeDefined();
    expect(component.breadcrumbsData).toBeDefined();
  });
});
