import { QuickbetDataProviderService } from './quickbet-data-provider.service';
import { Observable } from 'rxjs';

describe('QuickbetDataProviderService', () => {
  let service: QuickbetDataProviderService;

  beforeEach(() => {
    service = new QuickbetDataProviderService();
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should get quickbetPlaceBetListener', () => {
    expect(service.quickbetPlaceBetListener instanceof Observable).toBe(true);
  });

  it('should get quickbetReceiptListener', () => {
    expect(service.quickbetReceiptListener instanceof Observable).toBe(true);
  });
});
