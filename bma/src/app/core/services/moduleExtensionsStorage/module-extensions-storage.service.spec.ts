import { ModuleExtensionsStorageService } from './module-extensions-storage.service';

describe('ModuleExtensionsStorageService', () => {
  let service: ModuleExtensionsStorageService;

  beforeEach(() => {
    service = new ModuleExtensionsStorageService();
  });

  it('addToList', () => {
    service.addToList(<any>{});
    expect(service['extendersList']).toEqual(<any>[{}]);
  });

  it('getList', () => {
    service.addToList(<any>{});
    expect(service.getList()).toEqual(<any>[{}]);
  });
});
