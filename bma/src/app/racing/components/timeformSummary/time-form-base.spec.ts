import { TimeFormBaseComponent } from '@racing/components/timeformSummary/time-form-base';

describe('TimeFormBase', () => {
  let component: TimeFormBaseComponent,
    gtmService,
    locale;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };
    locale = {
      getString: jasmine.createSpy('getString').and.callFake((token: string) => {
        return token.indexOf('showLess') > -1 ? 'showLess' : token.indexOf('showMore') > -1 ? 'showMore' : '';
      })
    };

    component = new TimeFormBaseComponent(gtmService, locale);
  });

  it('constructor', () => {
    expect(component.details).toEqual({ text: '', expanded: false, expandable: true, expandedText: '' });
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.summaryText = 'summaryText';
      spyOn(component, 'getExpandedText').and.callThrough();
    });

    it('should expand text', () => {
      component.ngOnInit();

      expect(component.getExpandedText).toHaveBeenCalledWith(true);
      expect(component.details.text).toEqual(component.summaryText);
      expect(component.details.expandedText).toEqual('showLess');
      expect(component.details.expanded).toBeTruthy();
      expect(component.details.expandable).toBeFalsy();
    });

    it('should not expand text', () => {
      const spy = spyOnProperty(TimeFormBaseComponent, 'SUMMARY_MAX_LENGTH', 'get').and.returnValue(2);

      component.ngOnInit();

      expect(spy).toHaveBeenCalled();
      expect(component.getExpandedText).toHaveBeenCalledWith(false);
      expect(component.details.text).toEqual('su...');
      expect(component.details.expandedText).toEqual('showMore');
      expect(component.details.expanded).toBeFalsy();
      expect(component.details.expandable).toBeTruthy();
    });
  });

  it('SUMMARY_MAX_LENGTH should return number', () => {
    expect(TimeFormBaseComponent.SUMMARY_MAX_LENGTH).toEqual(100);
  });

  describe('toggleSummary', () => {
    beforeEach(() => {
      component.summaryText = 'summaryText';
      spyOn(component, 'getExpandedText').and.callThrough();
      spyOn(component, 'truncateSummaryText' as any).and.callThrough();
    });

    it('should toggle summary with expanded false', () => {
      const spy = spyOnProperty(TimeFormBaseComponent, 'SUMMARY_MAX_LENGTH', 'get').and.returnValue(2);

      component.details.expanded = true;

      component.toggleSummary();

      expect(spy).toHaveBeenCalled();
      expect(component.details.text).toEqual('su...');
      expect(component.getExpandedText).toHaveBeenCalledWith(false);
    });

    it('should toggle summary with expanded true', () => {
      component.toggleSummary();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'greyhounds',
        eventAction: 'race card',
        eventLabel: 'show more'
      });

      expect(component.details.expanded).toBeTruthy();
      expect(component.details.text).toEqual('summaryText');
      expect(component.getExpandedText).toHaveBeenCalledWith(true);
    });
  });

  describe('getExpandedText', () => {
    it('should show less', () => {
      expect(component.getExpandedText(true)).toEqual('showLess');
      expect(locale.getString).toHaveBeenCalledWith('racing.showLess');
    });

    it('should show more', () => {
      expect(component.getExpandedText(false)).toEqual('showMore');
      expect(locale.getString).toHaveBeenCalledWith('racing.showMore');
    });
  });

  it('trackByIndex should return index', () => {
    expect(component.trackByIndex(10)).toEqual(10);
  });

  it('truncateSummaryText should truncate summary text', () => {
    const spy = spyOnProperty(TimeFormBaseComponent, 'SUMMARY_MAX_LENGTH', 'get').and.returnValue(2);

    expect(component['truncateSummaryText']('randomtext')).toEqual('ra...');
    expect(spy).toHaveBeenCalled();
  });
});
