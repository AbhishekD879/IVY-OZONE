import { BannersModule } from './banners.module';

describe('BannersModule', () => {
  let bannersModule: BannersModule;

  beforeEach(() => {
    bannersModule = new BannersModule();
  });

  it('should create an instance', () => {
    expect(bannersModule).toBeTruthy();
  });
});
