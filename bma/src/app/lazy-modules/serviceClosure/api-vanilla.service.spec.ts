import { apiServiceFactory, ApiVanillaService } from './api-vanilla.service';

describe('ApiVanillaService', () => {
  let service: ApiVanillaService, apiServiceFactorySer;

  beforeEach(() => {
      service = new ApiVanillaService();
      apiServiceFactorySer = { create: jasmine.createSpy('create')};
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('apiServiceFactory be called', () => {
    apiServiceFactory(apiServiceFactorySer);
    expect(apiServiceFactorySer.create).toHaveBeenCalled();
  });

  it('should call getter', () => {
    service.persistPlaybreakVal = true;
    const retVal = service.persistPlaybreak;
    expect(retVal).toBeTruthy();
  });
});
