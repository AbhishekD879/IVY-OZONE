import { ToteEventsByTimeComponent } from './tote-events-by-time.component';

describe('ToteEventsByTimeComponent', () => {
  let component: ToteEventsByTimeComponent, router;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('router.navigateByUrl')
    };
    component = new ToteEventsByTimeComponent(router);
  });

  it('ngOnInit', () => {
    component.events = [{id: 1}] as any;
    component.ngOnInit();

    expect(component.expanded).toBeTruthy();
    expect(component.limit).toBe(10);
    expect(component.eventsOrder).toEqual(['localTime']);
    expect(component.events).toEqual([{id: 1}] as any);
  });

  it('ngOnInit (no events)', () => {
    component.ngOnInit();
    expect(component.events).toEqual([]);
  });

  it('goToUrl', () => {
    component.goToUrl('test_url');
    expect(router.navigateByUrl).toHaveBeenCalledWith('test_url');
  });
});
