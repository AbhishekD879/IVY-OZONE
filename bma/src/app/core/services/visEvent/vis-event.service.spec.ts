import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { VisEventService } from './vis-event.service';
import environment from '@environment/oxygenEnvConfig';

describe('VisEventService', () => {
  let service: VisEventService;

  let cms;
  let http;
  let windowRef;
  let timeService;

  beforeEach(() => {
    cms = {
      getFootball3DBanners: jasmine.createSpy().and.returnValue(of([])),
      getSystemConfig: jasmine.createSpy('getSystemConfig')
    };
    http = {
      get: jasmine.createSpy().and.returnValue(of({
        id: '123456',
        providerName: 'img',
        sportName: 'football'
      }))
    };
    windowRef = {
      nativeWindow: {
        frames: {
          visWidget: {
            postMessage: jasmine.createSpy()
          }
        }
      }
    };
    timeService = {
      oneSecond: 1000
    };

    service = new VisEventService(cms, http, windowRef, timeService);
  });

  describe('checkForEventsWithAvailableVisualization', () => {
    it('event is string', () => {
      service.checkForEventsWithAvailableVisualization('123456', 'https://vis-symphony-solutions.eu').subscribe();
      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(`https://vis-symphony-solutions.eu/is-available/123456`, jasmine.anything());
    });
    it('event is array', () => {
      service.checkForEventsWithAvailableVisualization([{id: '123456'}], 'https://vis-symphony-solutions.eu').subscribe();
      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(`https://vis-symphony-solutions.eu/is-available/123456`, jasmine.anything());
    });
  });

  it('checkPreMatchWidgetAvailability', fakeAsync(() => {
    http.get = jasmine.createSpy().and.returnValue(of([{
      id: '123456',
      stats: true
    }]));
    cms.getSystemConfig.and.returnValue(of({
      VisualisationConfig: {
        disabled: false
      }
    }));
    service.checkPreMatchWidgetAvailability('123456').subscribe(() => {},
    (err) => {
      expect(err.message).toContain(`undefined`);
    });
    tick();
    expect(http.get).toHaveBeenCalledWith(`${environment.VISUALIZATION_ENDPOINT}/is-stats/123456`, jasmine.anything());
  }));

  it('checkPreMatchWidgetAvailability (disabled)', fakeAsync(() => {
    cms.getSystemConfig.and.returnValue(of({
      VisualisationConfig: {
        disabled: true
      }
    }));
    service.checkPreMatchWidgetAvailability('123456').subscribe(() => {},
    (err) => {
      expect(err.message).toBeUndefined();
    });
    tick();
    expect(http.get).not.toHaveBeenCalled();
  }));

  it('visListener, false case', fakeAsync(() => {
    service.visListener(<MessageEvent>{ data: { type: 'vis_not_ready' } });
    tick();
    expect(cms.getFootball3DBanners).not.toHaveBeenCalled();
    expect(windowRef.nativeWindow.frames.visWidget.postMessage).not.toHaveBeenCalled();
  }));

  it('visListener, empty array', fakeAsync(() => {
    service.visListener(<MessageEvent>{ data: { type: 'vis_ready' } });
    tick();
    expect(cms.getFootball3DBanners).toHaveBeenCalledTimes(1);
    expect(windowRef.nativeWindow.frames.visWidget.postMessage).toHaveBeenCalledTimes(1);
    expect(windowRef.nativeWindow.frames.visWidget.postMessage).toHaveBeenCalledWith({ type: 'vis_banners_ready', fbanners: [] }, '*');
  }));

  it('visListener and filter conditions', fakeAsync(() => {
    cms.getFootball3DBanners = jasmine.createSpy('spyyyy').and.returnValue(of(
        [{ 'uriMedium': null }, { 'uriMedium': 'https://' }, { 'uriMediumm': 'wrong' }]
    ));
    service.visListener(<MessageEvent>{ data: { type: 'vis_ready' } });
    tick();
    expect(cms.getFootball3DBanners).toHaveBeenCalledTimes(1);
    expect(windowRef.nativeWindow.frames.visWidget.postMessage).toHaveBeenCalledTimes(1);
    expect(windowRef.nativeWindow.frames.visWidget.postMessage).toHaveBeenCalledWith({
      type: 'vis_banners_ready',
      fbanners: [{ 'uriMedium': 'https://' }]
    }, '*');
  }));
});
