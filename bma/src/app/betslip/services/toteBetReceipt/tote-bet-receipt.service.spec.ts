import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { ToteBetReceiptService } from './tote-bet-receipt.service';

describe('ToteBetReceiptService', () => {
  let bppService;
  let service: ToteBetReceiptService;

  beforeEach(() => {
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of({
        response: {
          poolBetDetail: {
            poolBet: {}
          }
        }
      }))
    };

    service = new ToteBetReceiptService(
      bppService
    );
  });

  it('getToteBetReceipt ', fakeAsync(() => {
    service.getToteBetReceipt().subscribe();
    tick();

    service.id = '1';
    service.getToteBetReceipt().subscribe();
    tick();

    expect(bppService.send).toHaveBeenCalledTimes(1);
  }));
});
