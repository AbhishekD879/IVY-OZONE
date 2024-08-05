import { EnhancedMultiplesTabComponent } from '@lazy-modules/enhancedMultiplesTab/components/enhanced-multiples-tab.component';
import { of, throwError } from 'rxjs';

describe('EnhancedMultiplesTabComponent', () => {
  let component: EnhancedMultiplesTabComponent;
  let enhancedMultiplesService: any;
  let filterSerice: any;


  beforeEach(() => {
    enhancedMultiplesService = jasmine.createSpyObj('enhancedMultiplesService', ['getAllEnhancedMultiplesEvents']);
    filterSerice = jasmine.createSpyObj('filterSerice', ['orderBy']);

    component = new EnhancedMultiplesTabComponent(enhancedMultiplesService, filterSerice);

    spyOn(component, 'getAllEnhancedMultiplesEvents');
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit should call methods with correct params', () => {
    component.ngOnInit();
    expect(component['getAllEnhancedMultiplesEvents']).toHaveBeenCalled();
  });

  it('trackByIndex should return passed index', () => {
    expect(component.trackByIndex(2)).toEqual(2);
  });

  describe('isNoEvents', () => {
    it('isNoEvents should return true if events are missing', () => {
      component['eventsCategories'] = undefined;
      component['showLoader'] = undefined;
      component['ssDown'] = undefined;

      expect(component.isNoEvents()).toEqual(true);
    });

    it('should return true if events are missing, but eventsCategories.length is more than 0', () => {
      component['eventsCategories'] = [];
      component['showLoader'] = undefined;
      component['ssDown'] = undefined;

      expect(component.isNoEvents()).toEqual(true);
    });

    it('should return false if events are missing, but eventsCategories.length is more than 0', () => {
      component['eventsCategories'] = new Array(2);
      component['showLoader'] = undefined;
      component['ssDown'] = undefined;

      expect(component.isNoEvents()).toEqual(false);
    });
  });

  describe('isRequestError', () => {
    it('should return true if ssDown is true and showLoader is false', () => {
      component['ssDown'] = true;
      component['showLoader'] = false;

      expect(component.isRequestError()).toBeTruthy();
    });

    it('should return false if ssDown is false and showLoader is true', () => {
      component['ssDown'] = false;
      component['showLoader'] = true;

      expect(component.isRequestError()).toBeFalsy();
    });
  });

  it('reloadComponent should set showLoader and ssDown, call getAllEnhancedMultiplesEvents method', () => {
    component.reloadComponent();

    expect(component['showLoader']).toBeTruthy();
    expect(component['ssDown']).toBeFalsy();
    expect(component['getAllEnhancedMultiplesEvents']).toHaveBeenCalled();
  });

  describe('ge)tAllEnhancedMultiplesEvents', () => {
    it('should set showLoader and eventsCategories properties', () => {
      (component['getAllEnhancedMultiplesEvents'] as any).and.callThrough();

      enhancedMultiplesService.getAllEnhancedMultiplesEvents.and.returnValue(of('someData'));
      spyOn<any>(component, 'sortCategoriesAndEvents').and.returnValue(12345);

      component.getAllEnhancedMultiplesEvents();

      expect(component.showLoader).toBeFalsy();
      expect(component.eventsCategories as any).toEqual(12345);
      expect(component['sortCategoriesAndEvents']).toHaveBeenCalledWith('someData' as any);
    });

    it('should set showLoader and eventsCategories properties after error', () => {
      enhancedMultiplesService.getAllEnhancedMultiplesEvents.and.returnValue(throwError('some message'));

      (component['getAllEnhancedMultiplesEvents'] as any).and.callThrough();

      component.getAllEnhancedMultiplesEvents();

      expect(component.showLoader).toBeFalsy();
      expect(component.ssDown).toBeTruthy();
    });
  });

  it('sortCategoriesAndEvents should return correct result', () => {
    spyOn<any>(component, 'reOrderEvents').and.returnValue(12);

    const data = [
      {
        displayOrder: 'c'
      },
      {
        displayOrder: 'a'
      },
      {
        displayOrder: 'b'
      }
    ] as any;

    expect(component['sortCategoriesAndEvents'](data)[0].displayOrder as any).toEqual('a');
    expect(component['sortCategoriesAndEvents'](data)[0].events as any).toEqual(12);
    expect(component['sortCategoriesAndEvents'](data).length).toEqual(3);
  });

  it('reOrderEvents should filter data and return correct result', () => {
    filterSerice.orderBy.and.returnValue([
      {
        markets: [
          {outcomes: [1, 2, 3]}
        ]
      },
      {
        markets: [
          {outcomes: []}
        ]
      }
    ]);

    expect(component['reOrderEvents']('events' as any).length).toEqual(1);
  });
});
