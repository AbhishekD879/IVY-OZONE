import { of } from 'rxjs/observable/of';

import { ImageManagerService } from './image-manager.service';
import { IMAGE_MANAGER_ROUTES } from '@app/image-manager/constants/image-manager.constant';

describe('ImageManagerService', () => {
  let service: ImageManagerService;

  let router;
  let sendRequestSpy;
  const brand = 'bma';

  beforeEach(() => {
    router = jasmine.createSpyObj(['navigate']);

    service = new ImageManagerService(
      {} as any,
      '',
      brand,
      {} as any,
      router
    );

    sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('sendImageData', () => {

    it('should add brand and send request', () => {
      const formData = {
        append: jasmine.createSpy('append')
      };
      service.sendImageData('abc', formData as any);

      expect(formData.append).toHaveBeenCalledWith('brand', brand);
      expect(sendRequestSpy).toHaveBeenCalledWith('post', 'svg-images/abc', formData);
    });
  });

  describe('getSpriteList', () => {

    it('should request available sprites for brand', () => {
      service.getSpriteList();

      expect(sendRequestSpy).toHaveBeenCalledWith('get', 'svg-images/brand/bma/sprites', null);
    });
  });

  describe('getSingleImage', () => {

    it('should request image data', () => {
      service.getSingleImage('abc');

      expect(sendRequestSpy).toHaveBeenCalledWith('get', 'svg-images/abc', null);
    });
  });

  describe('deleteAndOpenList', () => {

    it('should perform delete action and navigate to list', () => {
      const deleteSpy = spyOn(service as any, 'delete').and.returnValue(of({}));
      service.deleteAndOpenList('abc');

      expect(deleteSpy).toHaveBeenCalledWith('abc');
      expect(router.navigate).toHaveBeenCalledWith([IMAGE_MANAGER_ROUTES.base]);
    });
  });
});
