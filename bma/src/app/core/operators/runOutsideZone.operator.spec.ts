import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { runOutsideZone } from '@core/operators/runOutsideZone.operator';

describe('runOutsideZone', () => {
  it('should run out of angular Zone', fakeAsync(() => {
    const zone: any = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular').and.callFake(cb => cb())
    };
    const source = of(null);

    runOutsideZone(zone)(source).subscribe();
    tick();

    expect(zone.runOutsideAngular).toHaveBeenCalledTimes(1);
  }));
});
