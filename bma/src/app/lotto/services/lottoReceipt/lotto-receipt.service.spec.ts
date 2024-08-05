import { LottoReceiptService } from './lotto-receipt.service';

describe('LottoReceiptService', () => {
  let service: LottoReceiptService;

  beforeEach(() => {
    service = new LottoReceiptService();
  });

  it('getReceipt', () => {
    service.receiptData = { name: 'a' };
    expect(service.getReceipt()).toEqual({ name: 'a' });
    expect(service.receiptData).toEqual({});
  });

  it('setReceipt', () => {
    const data = { name: 'b' };
    service.setReceipt(data);
    expect(service.receiptData).toEqual(data);
  });
});
