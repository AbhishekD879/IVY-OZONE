import { CompetitionModuleComponent } from '@app/bigCompetitions/components/competitionModule/competition-module.component';

describe('CompetitionModuleComponent', () => {
  let component: CompetitionModuleComponent;
  beforeEach(() => {
    component = new CompetitionModuleComponent();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngAfterContentInit', () => {
    component.name = 'test';
    component.module = 'test2' as any;
    component.entry = {
      createComponent: jasmine.createSpy('createComponent').and.returnValue({
        instance: {
          moduleConfig: null
        }
      }),
      clear: () => {
        return true;
      }
    } as any;

    spyOn<any>(component, 'selectComponent');

    component.ngAfterContentInit();

    expect(component['selectComponent']).toHaveBeenCalledWith('test');
    expect(component.componentRef.instance.moduleConfig).toEqual('test2');
  });

  it('ngOnDestroy', () => {
    component.componentRef = {
      destroy: jasmine.createSpy('destroy')
    } as any;

    component.ngOnDestroy();

    expect(component.componentRef.destroy).toHaveBeenCalled();
  });

  describe('selectComponent', () => {
    it('should invoke function with default argument', () => {
      expect(component['selectComponent']()).toBeNull();
    });

    it('should invoke function without default argument', () => {
      component.competitioinComponents = {
        test: 'some result'
      };

      expect(component['selectComponent']('test')).toEqual('some result');
    });
  });
});
