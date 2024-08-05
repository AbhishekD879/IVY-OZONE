import { SessionStorageService } from './session-storage.service';

describe('SessionStorageService', () => {
  let service: SessionStorageService;

  const windowRefService = {} as any;

  beforeEach(() => {
    service = new SessionStorageService(windowRefService);
  });

  it('init', () => {
    expect(service).toBeDefined();
  });

  it('#init', () => {
    service['init']();
    expect(service['storageType']).toBe('sessionStorage');
  });
});
