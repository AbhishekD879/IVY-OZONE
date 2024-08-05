import { CardViewWidgetComponent } from '@app/bigCompetitions/components/cardViewWidget/card-view-widget.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';

describe('CardViewWidgetComponent', () => {
  let component: CardViewWidgetComponent;

  let events;
  let carousel;
  let carouselService;
  let changeDetectorRef;

  beforeEach(() => {
    events = [
      {
        cashoutAvail: '',
        categoryCode: '',
        categoryId: '',
        categoryName: 'Football',
        displayOrder: 0,
        drilldownTagNames: '',
        eventIsLive: true,
        eventSortCode: '',
        eventStatusCode: '',
        id: 10,
        isUS: true,
        liveServChannels: '',
        liveServChildrenChannels: '',
        liveStreamAvailable: true,
        typeId: '',
        typeName: '',
        name: '',
        originalName: '',
        responseCreationTime: '',
        markets: [],
        racingFormEvent: {
          class: ''
        },
        startTime: ''
      },
      {
        cashoutAvail: '',
        categoryCode: '',
        categoryId: '',
        categoryName: 'Football',
        displayOrder: 0,
        drilldownTagNames: '',
        eventIsLive: true,
        eventSortCode: '',
        eventStatusCode: '',
        id: '12',
        isUS: true,
        liveServChannels: '',
        liveServChildrenChannels: '',
        liveStreamAvailable: true,
        typeId: '',
        typeName: '',
        name: '',
        originalName: '',
        responseCreationTime: '',
        markets: [],
        racingFormEvent: {
          class: ''
        },
        startTime: ''
      }
    ] as IBigCompetitionSportEvent[];

    carousel = {
      currentSlide: 3,
      slidesCount: 4,
      next: jasmine.createSpy('next').and.returnValue(2),
      previous: jasmine.createSpy('previous').and.returnValue(1),
    };
    carouselService = {
      get: jasmine.createSpy('get').and.returnValue(carousel)
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new CardViewWidgetComponent(carouselService, changeDetectorRef);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', fakeAsync(() => {
    const chunkEvents = [];
    component.maxDisplay = 5;
    component.viewType = '';
    component.events = [];
    component.viewType = 'prematch';
    component.getChunk = jasmine.createSpy('getChunk').and.returnValue(chunkEvents);
    component.ngOnInit();
    expect(component.loadChunkStep).toBe(5);
    expect(component.carouselName).toBe('card-widget-carousel-prematch');
    expect(component.showLoader).toBeTruthy();
    expect(component.getChunk).toHaveBeenCalledWith(0, component.loadChunkStep);
    expect(component.chunkEvents).toBe(chunkEvents);

    tick();

    expect(component.showLoader).toBeFalsy();
  }));

  it('#ngOnChanges', () => {
    const chunkEvents = [];
    const changes = {
      events: {
        currentValue: {},
        firstChange: false
      }
    };
    component.loadChunkStep = 10;
    component.getChunk = jasmine.createSpy('getChunk').and.returnValue(chunkEvents);
    component['isPaginationRequired'] = jasmine.createSpy('isPaginationRequired').and.returnValue(false);
    component['isSingleEvent'] = jasmine.createSpy('isSingleEvent').and.returnValue(true);
    component.ngOnChanges(changes);
    expect(component.getChunk).toHaveBeenCalledWith(0, component.loadChunkStep);
    expect(component['isPaginationRequired']).toHaveBeenCalled();
    expect(component['isSingleEvent']).toHaveBeenCalled();
    expect(component.chunkEvents).toBe(chunkEvents);
    expect(component.showPaginationSlide).toBeFalsy();
    expect(component.singleEvent).toBeTruthy();
  });

  it('#ngOnChanges', () => {
    const chunkEvents = [];
    const changes = {
      events: {
        currentValue: {},
        firstChange: true
      }
    };
    component.loadChunkStep = 10;
    component.getChunk = jasmine.createSpy('getChunk').and.returnValue(chunkEvents);
    component['isPaginationRequired'] = jasmine.createSpy('isPaginationRequired');
    component['isSingleEvent'] = jasmine.createSpy('isSingleEvent');
    component.ngOnChanges(changes);
    expect(component.getChunk).not.toHaveBeenCalled();
    expect(component['isPaginationRequired']).not.toHaveBeenCalled();
    expect(component['isSingleEvent']).not.toHaveBeenCalled();
  });

  it('should return correct result', () => {
    component.events = events;
    const result = component.getChunk(0, 0);
    expect(result).toBe(component.events);
  });

  it('should return correct result', () => {
    component.events = events;
    const result = component.getChunk(0, 1);
    expect(result.length).toBe(1);
    expect(result[0]).toBe(component.events[0]);
  });

  it('should return correct result', () => {
    component.events = events;
    const result = component.getChunk(1, 5);
    expect(result.length).toBe(1);
    expect(result[0]).toBe(component.events[1]);
  });

  it('should return correct value', () => {
    const result = component.trackByEventId(1, events[0]);
    expect(result).toBe(10);
  });

  it('should call correct method', () => {
    const chunkEvents = [];
    component.chunkEvents = [];
    component.loadChunkStep = 5;
    component.getChunk = jasmine.createSpy('getChunk').and.returnValue(chunkEvents);
    component['isPaginationRequired'] = jasmine.createSpy('isPaginationRequired').and.returnValue(true);
    component.loadChunk();
    expect(component.getChunk).toHaveBeenCalledWith(0, component.chunkEvents.length + component.loadChunkStep);
    expect(component['isPaginationRequired']).toHaveBeenCalled();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    expect(component.chunkEvents).toBe(chunkEvents);
    expect(component.showPaginationSlide).toBeTruthy();
  });

  it('should return true', () => {
    component.events = [events[0]];
    expect(component['isSingleEvent']()).toBeTruthy();
  });

  it('should return false', () => {
    component.events = [];
    expect(component['isSingleEvent']()).toBeFalsy();
  });

  it('should return true', () => {
    component.viewType = 'inplay';
    component['isPaginationRequired'] = jasmine.createSpy('isPaginationRequired').and.returnValue(false);
    component.ngOnInit();
    expect(component.isInPlay).toBeTruthy();
    expect(component.showPaginationSlide).toBeFalsy();
    expect(component['isPaginationRequired']).toHaveBeenCalled();
  });

  it('should return false', () => {
    component.viewType = 'prematch';
    component['isPaginationRequired'] = jasmine.createSpy('isPaginationRequired').and.returnValue(false);
    component.ngOnInit();
    expect(component.isInPlay).toBeFalsy();
    expect(component.showPaginationSlide).toBeFalsy();
    expect(component['isPaginationRequired']).toHaveBeenCalled();
  });

  it('#nextSlide should scroll carousel', () => {
    component.slidesAvailable = jasmine.createSpy('slidesAvailable');
    component.nextSlide();
    expect(carousel.next).toHaveBeenCalled();
    expect(component.slidesAvailable).toHaveBeenCalled();
  });

  it('#prevSlide should scroll carousel', () => {
    component.slidesAvailable = jasmine.createSpy('slidesAvailable');
    component.prevSlide();
    expect(carousel.previous).toHaveBeenCalled();
    expect(component.slidesAvailable).toHaveBeenCalled();
  });

  it('#isPrevSlideAvailable checks if arrow prev is shown', () => {
    carousel.currentSlide = 5;
    component.slidesAvailable();
    expect(component.isPrevSlideAvailable).toBe(true);
  });

  it('#isPrevSlideAvailable checks if arrow prev is not shown', () => {
    carousel.currentSlide = 0;
    component.slidesAvailable();
    expect(component.isPrevSlideAvailable).toBe(false);
  });

  it('#isNextSlideUnAvailable checks if arrow next is shown', () => {
    carousel.currentSlide = 5;
    carousel.slidesCount = 6;

    component.slidesAvailable();
    expect(component.isNextSlideUnAvailable).toBe(true);
  });

  it('#isNextSlideUnAvailable checks if arrow next is not shown', () => {
    carousel.currentSlide = 1;
    carousel.slidesCount = 3;
    component.slidesAvailable();
    expect(component.isNextSlideUnAvailable).toBe(false);
  });

  it('init carousel', () => {
    const getCarousel = {
      currentSlide: 1,
      slidesCount: 4
    };
    carouselService.get.and.returnValue(getCarousel);

    expect(component['carousel']).toEqual(jasmine.objectContaining(getCarousel));
  });
});
