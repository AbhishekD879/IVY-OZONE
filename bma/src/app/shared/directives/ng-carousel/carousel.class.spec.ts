import { Carousel } from '@shared/directives/ng-carousel/carousel.class';

describe('Carousel', () => {
  let carousel: Carousel;

  const element = {
      parentElement: {},
      querySelector: jasmine.createSpy('HTMLElement.querySelector')
    },
    domTools = {
      getWidth: jasmine.createSpy('domTools.getWidth').and.callFake((el) => {
        return el ? el.clientWidth || el.innerWidth || 0 : 0;
      })
    },
    options = {} as any,
    slidesCount = 10;

  beforeEach(() => {
    carousel = new Carousel(
      slidesCount,
      options,
      element as any,
      domTools as any
    );
  });

  describe('constructor', () => {
    it('should init values', () => {
      expect(carousel.slidesCount).toEqual(10);
      expect(carousel.currentSlide).toEqual(0);
      expect(carousel['options'].looping).toBeTruthy();
      expect(carousel.onSlideChangeCallbacks).toEqual([]);
    });

    it('should not set looping to true', () => {
      options.looping = false;

      expect(carousel['options'].looping).toBeFalsy();
    });
  });

  it('getSlidesQuantity should return slides quantity', () => {
    element.querySelector.and.returnValue({ innerWidth: 1 });

    expect(carousel.getSlidesQuantity(element as any)).toEqual(9);
  });

  describe('next', () => {
    beforeEach(() => {
      carousel.toIndex = jasmine.createSpy('carousel.toIndex');
      carousel.getSlidesQuantity = jasmine.createSpy('carousel.getSlidesQuantity').and.returnValue(10);
    });

    it('should go to the next slide if its index lower than total amount of slides', () => {
      expect(carousel.next()).toEqual(1);
      expect(carousel.toIndex).toHaveBeenCalledWith(1, undefined);
    });

    it('should go the last slide if current index is higher than total amount of slides', () => {
      carousel.fluid = true;
      carousel.amount = 0;

      expect(carousel.next()).toEqual(10);
      expect(carousel.getSlidesQuantity).toHaveBeenCalledWith(element as any);
      expect(carousel.toIndex).toHaveBeenCalledWith(10, undefined);
    });

    it('should go to the first slide if current index is higher than total amount of slides and looping is enabled', () => {
      carousel.fluid = true;
      carousel.amount = 0;
      options.looping = true;

      expect(carousel.next()).toEqual(0);
      expect(carousel.getSlidesQuantity).toHaveBeenCalledWith(element as any);
      expect(carousel.toIndex).toHaveBeenCalledWith(0, 'right');
    });
  });

  describe('previous', () => {
    beforeEach(() => {
      carousel.toIndex = jasmine.createSpy('carousel.toIndex');
      carousel.getSlidesQuantity = jasmine.createSpy('carousel.getSlidesQuantity').and.returnValue(10);
    });

    it('should return to previous slide', () => {
      carousel.fluid = true;
      carousel.currentSlide = 12;

      expect(carousel.previous()).toEqual(1);
      expect(carousel.getSlidesQuantity).toHaveBeenCalledWith(element as any);
      expect(carousel.toIndex).toHaveBeenCalledWith(1, undefined);
    });

    it('should return to the beginning if current slide is already there and looping is disabled', () => {
      carousel.currentSlide = 0;
      options.looping = false;

      expect(carousel.previous()).toEqual(0);
      expect(carousel.toIndex).toHaveBeenCalledWith(0, undefined);
    });

    it('should return to the beginning if current slide is already there and looping is disabled', () => {
      carousel.currentSlide = 0;
      options.looping = true;

      expect(carousel.previous()).toEqual(9);
      expect(carousel.toIndex).toHaveBeenCalledWith(9, 'left');
    });
  });

  it('onSlideChange should store slide callback and return its index', () => {
    expect(carousel.onSlideChange(jasmine.any(Function) as any))
      .toEqual(carousel.onSlideChangeCallbacks.length - 1);
  });

  describe('unbindOnSlideChangeCallback', () => {
    it('should return if no callbacks', () => {
      expect(carousel.unbindOnSlideChangeCallback(9)).toBeUndefined();
    });

    it('should remove specified callback from a list', () => {
      carousel.onSlideChangeCallbacks.push(jasmine.any(Function) as any);

      carousel.unbindOnSlideChangeCallback(0);

      expect(carousel.onSlideChangeCallbacks.length).toBe(0);
    });
  });

  describe('toIndex', () => {
    const callback = jasmine.createSpy('onSlideChangeCallback');

    beforeEach(() => {
      carousel.onSlideChangeCallbacks.push(callback);
    });

    it('should be called with wrapping option enabled', () => {
      carousel.toIndex(2, true);

      expect(callback).toHaveBeenCalledWith(2, true);
    });

    it('should be called with wrapping option disabled', () => {
      carousel.toIndex(2, false);

      expect(callback).toHaveBeenCalledWith(2, false);
    });
  });
});
