
import { SortByOptionsService } from './sort-by-options.service';

describe('SortByOptionsService', () => {
  let service: SortByOptionsService;

  beforeEach(() => {
    service = new SortByOptionsService();
  });

  it('get default option', () => {
    expect(service.get()).toEqual('Price');
  });

  it('set option', () => {
    service.set('Racecard');
    expect(service.get()).toEqual('Racecard');
  });

  it('get default option isGreyHound true', () => {
    service.isGreyHound = true;
    expect(service.get()).toEqual('Price');
  });

  it('set option isGreyHound true', () => {
    service.isGreyHound = true;
    service.set('Racecard');
    expect(service.get()).toEqual('Racecard');
  });
});
