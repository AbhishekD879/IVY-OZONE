import { JackpotReceiptPageService } from './jackpot-receipt-page.service';

describe('JackpotReceiptPageService', () => {
  let service: JackpotReceiptPageService;

  beforeEach(() => {
    service = new JackpotReceiptPageService();
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('get getTotalStake should return correct value', () => {
    service['totalStake'] = 12;

    expect(service.getTotalStake).toEqual(12);
  });

  it('get getTotalLines should return correct value', () => {
    service['totalLines'] = 13;

    expect(service.getTotalLines).toEqual(13);
  });

  it('get getBetReceiptNumber should return correct value', () => {
    service['betReceiptNumber'] = 14 as any;

    expect(service.getBetReceiptNumber as any).toEqual(14);
  });

  it('getTotalLines should set correct data', () => {
    service.setReceiptData('events' as any, 'outcomesIds' as any, 11, 2, 'num');

    expect(service['jackpotEvents'] as any).toEqual('events');
    expect(service['selectedOutcomesIds'] as any).toEqual(['outcomesIds']);
    expect(service['totalStake']).toEqual(11);
    expect(service['totalLines']).toEqual(2);
    expect(service['betReceiptNumber']).toEqual('num');
  });

  describe('get getReceiptData', () => {
    let data: any;

    beforeEach(() => {
      data = [
        {
          markets: [
            {
              outcomes: ['first', 'second'],
              classDisplayOrder: 2
            },
            {
              outcomes: ['third', 'fourth', 'fifth'],
              classDisplayOrder: 1
            }
          ],
        }
      ];
    });

    it('should iterate and mutate data', () => {
      service['jackpotEvents'] = data;

      spyOn(service['selectedOutcomesIds'], 'indexOf').and.returnValue(-1);

      expect(service.getReceiptData[0].markets[0].outcomes).toEqual([]);
    });

    it('should iterate and mutate data and call else statement', () => {
      service['jackpotEvents'] = data;

      spyOn(service['selectedOutcomesIds'], 'indexOf').and.returnValue(1);

      expect(service.getReceiptData[0].markets[0].outcomes.length).toEqual(2);
    });
  });
});
