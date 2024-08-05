
import { of as observableOf } from 'rxjs';
import { ITimeHydraModel } from './timeModel';
import { TimeSyncService } from './time-sync.service';

describe('TimeSyncService', () => {
  let service: TimeSyncService;

  let http;

  const timeHydraModel: ITimeHydraModel = {
    timestamp: new Date().getTime(),
    'x-forward-for': '192.168.3.45'
  };
  beforeEach(() => {
    http = {
      get: jasmine.createSpy().and.returnValue(observableOf({
        body: timeHydraModel
      }))
    };

    service = new TimeSyncService(http);
  });

  it('getUserSessionTime', () => {
    service.getUserSessionTime();

    expect(http.get).toHaveBeenCalledTimes(2);
  });

  it('getTimeDelta', () => {
    service['timeDelta'] = null;
    expect(service.getTimeDelta()).toEqual(0);

    service['timeDelta'] = 100;
    expect(service.getTimeDelta()).toEqual(100);
  });

  it('ip', () => {
    service['customerIp'] = null;
    expect(service.ip).toEqual('91.232.241.59');
  });
});
