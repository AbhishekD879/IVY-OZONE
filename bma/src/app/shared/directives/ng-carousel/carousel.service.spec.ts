import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';

describe('CarouselService', () => {
  let service: CarouselService;

  const domTools = {} as any;

  beforeEach(() => {
    spyOn(console, 'error');
    service = new CarouselService(domTools);
  });

  describe('add', () => {
    it('should error if no name specified', () => {

      service.add(null, undefined, {}, {} as any);

      expect(console.error).toHaveBeenCalledWith('Error: no carousel name specified');
    });

    it('should set default slides count', () => {
      const instance = new Carousel(0, {}, {} as any, domTools);

      expect(service.add(null, 'carousel1', {}, {} as any)).toEqual(instance);
      expect(console.error).not.toHaveBeenCalled();
      expect(service.instances.hasOwnProperty('carousel1')).toBeTruthy();
      expect(service.instances.carousel1).toEqual(instance);
    });

    it('should set slides count', () => {
      const instance = new Carousel(10, {}, {} as any, domTools);

      expect(service.add(10, 'carousel2', {}, {} as any)).toEqual(instance);
      expect(console.error).not.toHaveBeenCalled();
      expect(service.instances.hasOwnProperty('carousel2')).toBeTruthy();
      expect(service.instances.carousel2).toEqual(instance);
    });
  });

  describe('get', () => {
    it('should return null if no instance is present', () => {
      expect(service.get('superInstance')).toBeNull();
    });

    it('should get instance if it exists', () => {
      service.instances = {
        superInstance: {}
      } as any;

      expect(service.get('superInstance')).toEqual({} as any);
    });
  });

  it('remove', () => {
    service.instances = {
      myInstance: {} as any
    };

    service.remove('myInstance');
    expect(service.instances.hasOwnProperty('myInstance')).toBeFalsy();
  });
});
