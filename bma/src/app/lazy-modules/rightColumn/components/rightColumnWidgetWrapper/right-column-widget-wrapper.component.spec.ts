import { of, throwError } from 'rxjs';
import { RightColumnWidgetWrapperComponent } from './right-column-widget-wrapper.component';

describe('#RightColumnWidgetWrapperComponent', () => {
  const statsDataMock = {
    getActiveWidgets: [
      {
        columns: 'test',
        directiveName: 'test',
        disabled: false,
        showExpanded: false,
        showOnDesktop: false,
        showOnMobile: false,
        showOnTablet: false,
        sortOrder: 1,
        title: 'test',
        type: 'test',
        type_brand: 'test',
        showOn: {
          sports: ['test', 'test'],
          routes: 'test',
        },
        componentName : 'test',
      },
      {
        columns: 'test1',
        directiveName: 'test1',
        disabled: true,
        showExpanded: false,
        showOnDesktop: true,
        showOnMobile: false,
        showOnTablet: true,
        sortOrder: 1,
        title: 'test1',
        type: 'test1',
        type_brand: 'test1',
        showOn: {
          sports: ['test1', 'test1'],
          routes: 'test1',
        },
        componentName : 'test1',
      }
    ] as any,
  };
  let component: RightColumnWidgetWrapperComponent;
  let cms;

  beforeEach(() => {
    cms = {
      getActiveWidgets: jasmine.createSpy('cms.getActiveWidgets')
    } as any;
    component = new RightColumnWidgetWrapperComponent(
      cms
    );
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
    expect(component.widgetDataStore).toBeDefined();
  });

  describe('#ngOnInit', () => {
    it('should get widget data', () => {
      spyOn(component, 'hideSpinner');
      cms.getActiveWidgets.and.returnValue(of(statsDataMock.getActiveWidgets));
      component.ngOnInit();
      expect(component.widgetDataStore.length).toEqual(2);
      expect(component.hideSpinner).toHaveBeenCalled();
    });

    it('should throw error', () => {
      spyOn(component, 'hideSpinner');
      cms.getActiveWidgets.and.returnValue(throwError('error'));
      component.ngOnInit();
      expect(component.widgetDataStore.length).toEqual(0);
      expect(component.hideSpinner).toHaveBeenCalled();
    });
  });
});
