import { fakeAsync, tick } from '@angular/core/testing';
import { from, throwError } from 'rxjs';

import { EuroService } from './euro.service';

describe('EuroloyaltyService', () => {
  let service: EuroService;
  let bppService;

  beforeEach(() => {
    bppService = {
      send: jasmine.createSpy().and.returnValue(from([{
        response: {
          returnStatus: {
            message: 'success'
          }
        }
      }]))
    };
    service = new EuroService(bppService);
  });

  it('should throw error ', fakeAsync(() => {
    const error = 'err';
    bppService.send = jasmine.createSpy().and.returnValue(throwError(error));

    service.getMatchRewardsBadges(true).subscribe(() => { },
      () => {
        expect(bppService.send).toHaveBeenCalled();
      });
    tick();
  }));

  it('should throw error again', fakeAsync(() => {
    const error = 'err';
    bppService.send = jasmine.createSpy().and.returnValue(throwError(error));

    service.getMatchRewardsBadges(false).subscribe(() => { },
      () => {
        expect(bppService.send).toHaveBeenCalled();
      });
    tick();
  }));

  it('should not call throwerror', fakeAsync(() => {
    service.getMatchRewardsBadges(true).subscribe(() => { },
      () => {
        expect(bppService.send).toHaveBeenCalled();
      });
    tick();
  }));

  it('should getHowItWorksData', fakeAsync(() => {
    service.getHowItWorksData().subscribe(() => { },
      () => {
        expect(bppService.send).toHaveBeenCalled();
      });
    tick();
  }));

  it('should throw error for howitworks', fakeAsync(() => {
    const error = 'err';
    bppService.send = jasmine.createSpy().and.returnValue(throwError(error));

    service.getHowItWorksData().subscribe(() => { },
      () => {
        expect(bppService.send).toHaveBeenCalled();
      });
    tick();
  }));

});

