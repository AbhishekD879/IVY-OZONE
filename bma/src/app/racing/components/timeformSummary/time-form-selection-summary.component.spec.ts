import { TimeFormSelectionSummaryComponent } from '@racing/components/timeformSummary/time-form-selection-summary.component';

describe('TimeFormSelectionSummaryComponent', () => {
  let component: TimeFormSelectionSummaryComponent,
    locale,
    gtmService;

  beforeEach(() => {
    locale = {} as any;
    gtmService = {} as any;

    component = new TimeFormSelectionSummaryComponent(gtmService, locale);
  });

  describe('ngOnInit', () => {
    let parentNgOnInit;

    beforeEach(() => {
      parentNgOnInit = spyOn(TimeFormSelectionSummaryComponent.prototype['__proto__'], 'ngOnInit');
    });

    it('should set summary text as empty if no outcome data', () => {
      component.outcome = {} as any;

      component.ngOnInit();

      expect(component.summaryText).toEqual('');
    });

    it('should set summary text from outcome', () => {
      component.outcome = {
        timeformData: {
          oneLineComment: 'oneLineComment'
        }
      } as any;

      component.ngOnInit();

      expect(component.summaryText).toEqual('oneLineComment');
    });

    afterEach(() => {
      expect(parentNgOnInit).toHaveBeenCalled();
    });
  });
});
