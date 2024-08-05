import { FiveasideWidgetOddsviewComponent
} from '@lazy-modules/fiveASideShowDown/components/fiveASideWidgetOddsview/fiveaside-widget-oddsview.component';

describe('FiveasideWidgetOddsviewComponent', () => {
  let component: FiveasideWidgetOddsviewComponent;
  let fractoDecimalService;

  beforeEach(() => {
    fractoDecimalService = {
      getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('10/8')
    };
    component = new FiveasideWidgetOddsviewComponent(fractoDecimalService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('#ngOnChanges', () => {
      it('should call oddsFormat when change is summary', () => {
          spyOn(component as any, 'oddsFormat');
          const change = {
            summary: {}
          } as any;
          component.ngOnChanges(change);
          expect(component['oddsFormat']).toHaveBeenCalled();
      });
      it('should not call oddsFormat when change is not summary', () => {
        spyOn(component as any, 'oddsFormat');
        const change = {
          fact: {}
        } as any;
        component.ngOnChanges(change);
        expect(component['oddsFormat']).not.toHaveBeenCalled();
    });
  });
});
