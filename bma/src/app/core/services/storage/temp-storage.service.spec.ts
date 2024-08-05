import { TempStorageService } from './temp-storage.service';
describe('TempStorageService', () => {
  let service: TempStorageService;

  beforeEach(() => {
    service = new TempStorageService();
  });

  it('set', () => {
    service.set('test', {});
    expect(service['map']).toEqual({
      test: {}
    });
  });

  it('get', () => {
    service.set('test', {});
    expect(service.get('test')).toEqual({});
  });
});
