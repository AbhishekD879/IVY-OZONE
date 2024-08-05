
import { fakeAsync, tick } from "@angular/core/testing";
import { CustomFlagFilterToggleComponent } from "./custom-flag-filter-toggle.component";
import { Router } from '@angular/router';
import { of } from "rxjs";
describe("#Custom Filter Toolgle component", () => {
  let component: CustomFlagFilterToggleComponent;
  let locale;
  let gtmService;
  let ActivatedRoute;
  let windowRef;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test'),
      toLowerCase: jasmine.createSpy('toLowerCase')
     }; 
     gtmService = {
      push: jasmine.createSpy('push')
    };
    ActivatedRoute = {
      snapshot: { queryParams: { provide: Router } },
      params: of({
        sport: 'football',
        id: '12345'
      })
    };
    windowRef = {
      nativeWindow: {
        location: {
          pathname: '/greyhound-racing'
        }
      }
    };
    component = new CustomFlagFilterToggleComponent(locale, gtmService, ActivatedRoute, windowRef);
  });
  it("constructor", () => {
    expect(component).toBeTruthy();
  });
    describe("@ngOnInit", () => {
      it(" should emit onFilterSelect event", fakeAsync(() => {
         spyOn(component.filterChange, 'emit');
        component.ngOnInit();
        component.onFilterSelect({flag: "UK&IRE"});
        tick();
        expect(component.filterChange.emit).toHaveBeenCalledWith({flag: "UK&IRE"});
      })); 
    });
    it("should call ngOnChanges", () => {
      component.selectedFilter = 'VR';
      component.filters = [];
      component._filters = [{ flag: 'All' }, { flag: 'VR' }];
      component._filters = component._filters.filter((data: any) => data.flag !== 'VR');
      component.ngOnChanges({ filters: component._filters } as any);
      expect(component.selectedFilter).toEqual('All');
      expect(component.filters).toEqual(component._filters);
    });
  });