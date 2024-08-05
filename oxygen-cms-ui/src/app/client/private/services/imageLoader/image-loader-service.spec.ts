import { of } from 'rxjs';

import { ImageLoaderService } from '@app/client/private/services/imageLoader/image-loader-service';

describe('ImageLoaderService', () => {
  let service: ImageLoaderService;

  let byteToKbPipe;

  const brand = 'bma';

  beforeEach(() => {
    byteToKbPipe = {
      transform: jasmine.createSpy('transform').and.returnValue('10 kB')
    };

    service = new ImageLoaderService(
      {} as any,
      {} as any,
      brand,
      byteToKbPipe
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should define image url', () => {
    expect(service['uri']).toBe('svg-images');
  });

  describe('getData', () => {
    let sendRequestSpy;

    beforeEach(() => {
      sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    });

    it('should request data', () => {
      service.getData();
      expect(sendRequestSpy).toHaveBeenCalled();
    });
  });
});
