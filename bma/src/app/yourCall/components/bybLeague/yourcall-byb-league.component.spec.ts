import { fakeAsync, tick } from '@angular/core/testing';
import { YourcallBybLeagueComponent } from '@yourcall/components/bybLeague/yourcall-byb-league.component';
import { of, throwError } from 'rxjs';

describe('YourcallBybLeagueComponent', () => {
  let component: YourcallBybLeagueComponent;

  let interval;
  let timeServiceStub;
  let date;
  let routerStub;
  let yourcallBybLeagueServiceStub;
  let localeStub,seoDataService;

  beforeEach(() => {
    interval = {
      dateFrom: '2019-01-28T22:00:00.000Z',
      dateTo: '2019-01-29T22:00:00.000Z'
    },
    timeServiceStub = {
      getEventTime: jasmine.createSpy('getEventTime')
    },
    date = new Date(),
    routerStub = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    },
    yourcallBybLeagueServiceStub = {
      getLeagueEvents: jasmine.createSpy('getLeagueEvents').and.returnValue(Promise.resolve([])),
      parse: () => [{
        date
      }],
      getEventPath: jasmine.createSpy('getEventPath').and.returnValue(of('event')),
      getInterval: jasmine.createSpy('getInterval').and.returnValue(interval)
    },
    localeStub = {
      getString: jasmine.createSpy().and.returnValue('build-your-bet')
    };

    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };

    component = new YourcallBybLeagueComponent(
      localeStub,
      routerStub,
      yourcallBybLeagueServiceStub,
      timeServiceStub,
      seoDataService
    );

    component.filter = 'Upcoming';
    component.league = {
      obTypeId: 12312312,
      title: 'Premier League'
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#initData', () => {
    it('should call init data with error', fakeAsync(() => {
      yourcallBybLeagueServiceStub.getLeagueEvents.and.returnValue(Promise.reject());
      component.ngOnInit();

      tick();

      expect(yourcallBybLeagueServiceStub.getLeagueEvents).toHaveBeenCalledWith(component.league, interval);
      expect(yourcallBybLeagueServiceStub.getInterval).toHaveBeenCalledWith('Upcoming');
      expect(timeServiceStub.getEventTime).not.toHaveBeenCalled();
    }));

    afterEach(() => {
      yourcallBybLeagueServiceStub.getLeagueEvents.and.returnValue(Promise.resolve([]));
    });
  });

  it('should test ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(timeServiceStub.getEventTime).toHaveBeenCalledWith(date);
    expect(yourcallBybLeagueServiceStub.getLeagueEvents).toHaveBeenCalledWith(component.league, interval);
    expect(yourcallBybLeagueServiceStub.getInterval).toHaveBeenCalledWith('Upcoming');
  }));

  describe('#ngOnChanges', () => {
    it('should test ngOnChanges for first change', fakeAsync(() => {
      const changes = {
        filter: {
          firstChange: true
        }
      } as any;
      component.ngOnChanges(changes);

      tick();

      expect(yourcallBybLeagueServiceStub.getLeagueEvents).not.toHaveBeenCalled();
      expect(yourcallBybLeagueServiceStub.getLeagueEvents).not.toHaveBeenCalled();
      expect(yourcallBybLeagueServiceStub.getInterval).not.toHaveBeenCalled();
    }));

    it('should test ngOnChanges not for first change', fakeAsync(() => {
      const changes = {
        filter: {
          firstChange: false
        }
      } as any;
      component.ngOnChanges(changes);

      tick();

      expect(yourcallBybLeagueServiceStub.getLeagueEvents).toHaveBeenCalledWith({
        obTypeId: 12312312,
        title: 'Premier League',
        eventsLoaded: true
      } as any, interval);
      expect(yourcallBybLeagueServiceStub.getInterval).toHaveBeenCalledWith('Upcoming');
      expect(yourcallBybLeagueServiceStub.getLeagueEvents).toHaveBeenCalledTimes(1);
      expect(yourcallBybLeagueServiceStub.getInterval).toHaveBeenCalledTimes(1);
    }));
  });

  it('trackById', () => {
    const result = component.trackById(1, {id: '123'} as any);

    expect(result).toEqual('123 1');
  });

  it('goToEvent', fakeAsync(() => {
    routerStub.navigateByUrl.and.returnValue('url');
    component.goToEvent({} as any);
    tick();
    expect(yourcallBybLeagueServiceStub.getEventPath).toHaveBeenCalledWith({}, component.league);
    expect(routerStub.navigateByUrl).toHaveBeenCalledWith('/event/build-your-bet');
    expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ },'event');
  }));

  it('initData should handle error response', () => {
    yourcallBybLeagueServiceStub.getLeagueEvents = jasmine.createSpy('getLeagueEvents').and.returnValue(throwError('error'));
    spyOn(console, 'warn');

    component.initData();

    expect(console.warn).toHaveBeenCalledWith('error');
  });
});
