import { SliderPanelComponent } from '@lazy-modules/timeline/components/sliderPanel/slider-panel.component';
import { of, Observable, ReplaySubject } from 'rxjs';

describe('SliderPanelComponent', () => {
  let sliderComponent;
  const event = {
    stopPropagation: jasmine.createSpy('stopPropagation')
  };

  const changeDetectorRef = {
    markForCheck: jasmine.createSpy('markForCheck')
  } as any;

  beforeEach(() => {
    sliderComponent = new SliderPanelComponent(changeDetectorRef);
    sliderComponent.stateChange.emit = jasmine.createSpy('stateChangeEmit');
    sliderComponent.reloadTimeline.emit = jasmine.createSpy('reloadTimelineEmit');
    sliderComponent.loadMore.emit = jasmine.createSpy('loadMoreEmit');
  });

  it('#ngOnInit scroll end', () => {
    sliderComponent.allPostsLoaded = true;
    sliderComponent['isPanelScrolledEnd'] = jasmine.createSpy('isPanelScrolledEnd').and.returnValue(true);
    sliderComponent['getScrollObservable'] = jasmine.createSpy('getScrollEnd').and.returnValue(of(null));

    sliderComponent.ngOnInit();

    expect(sliderComponent.loadMore.emit).not.toHaveBeenCalled();
    expect(sliderComponent.bounce$).toEqual(jasmine.any(Observable));
  });

  it('#ngOnInit not all posts are loaded', () => {
    sliderComponent['isPanelScrolledEnd'] = jasmine.createSpy('isPanelScrolledEnd').and.returnValue(false);
    sliderComponent.allPostsLoaded = false;
    sliderComponent['getScrollObservable'] = jasmine.createSpy('getScrollEnd').and.returnValue(of(null));

    sliderComponent.ngOnInit();

    expect(sliderComponent.loadMore.emit).not.toHaveBeenCalled();
    expect(sliderComponent.bounce$).toEqual(jasmine.any(Observable));
  });

  it('#ngOnInit scroll end and not all posts are loaded', () => {
    sliderComponent['isPanelScrolledEnd'] = jasmine.createSpy('isPanelScrolledEnd').and.returnValue(true);
    sliderComponent.allPostsLoaded = false;
    sliderComponent['getScrollObservable'] = jasmine.createSpy('getScrollEnd').and.returnValue(of(null));

    sliderComponent.ngOnInit();

    expect(sliderComponent.loadMore.emit).toHaveBeenCalled();
    expect(sliderComponent.bounce$).toEqual(jasmine.any(Observable));
  });

  it('#ngOnDestroy', () => {
    sliderComponent['subscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    sliderComponent.ngOnDestroy();
    expect(sliderComponent['subscription']['unsubscribe']).toHaveBeenCalled();
  });

  it('#getScrollObservable', () => {
    sliderComponent.sliderPanel = {
      nativeElement: {}
    };
    const scrollEnd = sliderComponent['getScrollObservable']();
    expect(scrollEnd).toEqual(jasmine.any(Observable));
  });

  it('#isScrollEnd scroll is not ended', () => {
    sliderComponent.allPostsLoaded = true;
    expect(sliderComponent['isScrollEnd'](false)).toBeFalsy();
  });

  it('#isScrollEnd not all posts are loaded', () => {
    sliderComponent.allPostsLoaded = false;
    expect(sliderComponent['isScrollEnd'](true)).toBeFalsy();
  });

  it('#isScrollEnd scroll is ended all posts are loaded', () => {
    sliderComponent.allPostsLoaded = true;
    expect(sliderComponent['isScrollEnd'](true)).toBeTruthy();
  });

  it('#isPanelScrolledEnd panel is not scrolled to the end', () => {
    sliderComponent.sliderPanel = {
      nativeElement: {
        scrollHeight: 450,
        scrollTop: 20,
        clientHeight: 300
      }
    };
    expect(sliderComponent['isPanelScrolledEnd']()).toBeFalsy();
  });

  it('#isPanelScrolledEnd panel is scrolled to the end', () => {
    sliderComponent.sliderPanel = {
      nativeElement: {
        scrollHeight: 450,
        scrollTop: 150,
        clientHeight: 300
      }
    };
    expect(sliderComponent['isPanelScrolledEnd']()).toBeTruthy();
  });

  it('#getBounceObservable', () => {
    const scrollEnd$ = new ReplaySubject<boolean>(2);
    const scrollEndObservable$ = scrollEnd$.asObservable();
    scrollEnd$.next(true);
    scrollEnd$.next(true);
    sliderComponent['isScrollEnd'] = jasmine.createSpy('isScrollEnd').and.returnValue(true);
    sliderComponent.sliderPanel = {
      nativeElement: {
        scrollHeight: 450,
        scrollTop: 150,
        clientHeight: 300
      }
    };
    sliderComponent['getBounceObservable'](scrollEndObservable$).subscribe();
    expect(sliderComponent['isScrollEnd']).toHaveBeenCalledWith(true);
  });

  it('should hide panel', () => {
    sliderComponent.show(event, false);

    expect(sliderComponent.visible).toBeFalsy();
    expect(event.stopPropagation).toHaveBeenCalled();
    expect(sliderComponent.stateChange.emit).toHaveBeenCalledWith(false);
    expect(sliderComponent.changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it('should show panel', () => {
    sliderComponent.show(event, true);

    expect(sliderComponent.visible).toBeTruthy();
    expect(event.stopPropagation).toHaveBeenCalled();
    expect(sliderComponent.stateChange.emit).toHaveBeenCalledWith(true);
    expect(sliderComponent.changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it('should test callToReload()', () => {
    sliderComponent.callToReload(event);

    expect(event.stopPropagation).toHaveBeenCalled();
    expect(sliderComponent.reloadTimeline.emit).toHaveBeenCalledWith(true);
  });

  it('should trackByPost', () => {
    expect(sliderComponent.trackByPost(1, { id: '2' })).toEqual('2');
  });

  it('should emit event when state changes', () => {
    sliderComponent.onStateChange(true);
    expect(sliderComponent.stateChange.emit).toHaveBeenCalled();
  });
});
