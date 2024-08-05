import { CONTEST_SELECTION, ENTRY_CONFIRMATION } from '@app/fiveASideShowDown/constants/constants';
import { IAvailableContests } from '@app/fiveASideShowDown/models/available-contests.model';
import { of } from 'rxjs';
import { FiveASideContestSelectionComponent
} from '@app/lazy-modules/fiveASideShowDown/components/fiveASideContestSelection/fiveaside-contest-selection.component';
import { CONTESTS, prizeArray, prizeArray2 } from '@app/lazy-modules/fiveASideShowDown/components/fiveASideContestSelection/fiveaside-contest-selection.mock';


describe('FiveASideContestSelectionComponent', () => {

  let component: FiveASideContestSelectionComponent;
  let changeDetectorRef,
  carousel,
  carouselInstanceMock,
  carouselService,
  cmsService,
  domSanitizer;
  let contests: IAvailableContests[];

  beforeEach(() => {
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    carousel = {
      currentSlide: 3,
      slidesCount: 4,
      next: jasmine.createSpy('next').and.returnValue(2),
      previous: jasmine.createSpy('previous').and.returnValue(1),
    };
    carouselService = {
      get: jasmine.createSpy('get').and.callFake(() => carouselInstanceMock)
    };
    carouselInstanceMock = {
      next: jasmine.createSpy('next'),
      previous: jasmine.createSpy('previous'),
      toIndex: jasmine.createSpy('toIndex')
    };
    cmsService = {
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(of({
        htmlMarkup: '<HTML>'
      }))
    };
    domSanitizer = {
      sanitize: jasmine.createSpy().and.returnValue('<HTML>'),
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    contests = CONTESTS;
    component = new FiveASideContestSelectionComponent(carouselService,cmsService, domSanitizer,changeDetectorRef);
  });

  it('should create a component', () => {
    expect(component).toBeTruthy();
  });

  it('should do carousel initialisation ngOnInint', () => {
    spyOn(component as any, 'initContestSelectionCarousel');
    component.ngOnInit();
    expect(component['initContestSelectionCarousel']).toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component['staticBlockSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();
    expect(component['staticBlockSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('should get carousal data in initContestSelectionCarousel', () => {
    spyOn(component as any, 'requestContestAndCarouselInit');
    spyOn(component as any, 'getContestBetSlipToolTip');
    spyOn(component as any, 'triggerSlideUp');
    component.initContestSelectionCarousel();
    expect(component['requestContestAndCarouselInit']).toHaveBeenCalled();
    expect(component['getContestBetSlipToolTip']).toHaveBeenCalled();
    expect(component['triggerSlideUp']).toHaveBeenCalled();
  });

  describe('requestContestAndCarouselInit', () => {
    it('should set contest ID if present', () => {
      component.canShowPrevious = false;
      component.canShowNext = true;
      component.selectedContest = '12345';
      component.contests = CONTESTS;
      spyOn(component, 'emitSelctedContest');
  
      component.requestContestAndCarouselInit();
      
      expect(component.canShowPrevious).toBe(false);
      expect(component.canShowNext).toBe(true);
      expect(component.contests[0].contestId).toBe('61b2f0372cb30f010f8fa61b');
      expect(component.selectedContest).toBe('12345');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });

    it('should set contest ID to first contest in CMS order if present', () => {
      component.canShowPrevious = false;
      component.canShowNext = true;
      component.selectedContest = '';
      component.contests = CONTESTS;
      spyOn(component, 'emitSelctedContest');
  
      component.requestContestAndCarouselInit();
      
      expect(component.canShowPrevious).toBe(false);
      expect(component.canShowNext).toBe(true);
      expect(component.selectedContest).toBe('61b2f0372cb30f010f8fa61b');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });

    it('should set contest ID to default', () => {
      component.canShowPrevious = false;
      component.canShowNext = true;
      component.selectedContest = '61b2f0372cb30f010f8fa61b';
      component.contests = [];
      spyOn(component, 'emitSelctedContest');
  
      component.requestContestAndCarouselInit();
      
      expect(component.canShowPrevious).toBe(false);
      expect(component.canShowNext).toBe(true);
      expect(component.selectedContest).toBe('61b2f0372cb30f010f8fa61b');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });

    it('should set contest ID to empty if not present', () => {
      component.canShowPrevious = false;
      component.canShowNext = true;
      component.selectedContest = '';
      component.contests = [];
      spyOn(component, 'emitSelctedContest');
  
      component.requestContestAndCarouselInit();
      
      expect(component.canShowPrevious).toBe(false);
      expect(component.canShowNext).toBe(true);
      expect(component.selectedContest).toBe('');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });

    it('should set contest ID to empty if not present', () => {
      component.canShowPrevious = false;
      component.canShowNext = true;
      component.selectedContest = '';
      component.contests = undefined;
      spyOn(component, 'emitSelctedContest');
  
      component.requestContestAndCarouselInit();
      
      expect(component.canShowPrevious).toBe(false);
      expect(component.canShowNext).toBe(true);
      expect(component.selectedContest).toBe('');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });

    it('should set contest ID to value if present and contest length is 0', () => {
      component.canShowPrevious = false;
      component.canShowNext = true;
      component.selectedContest = '61b2f0372cb30f010f8fa61b';
      component.contests = undefined;
      spyOn(component, 'emitSelctedContest');
  
      component.requestContestAndCarouselInit();
      
      expect(component.canShowPrevious).toBe(false);
      expect(component.canShowNext).toBe(true);
      expect(component.selectedContest).toBe('61b2f0372cb30f010f8fa61b');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });
});

  it('#nextSlide should scroll carousel', () => {
    component.slidesAvailable = jasmine.createSpy('slidesAvailable');
    component.nextSlide();
    expect(component.bannersCarousel.next).toHaveBeenCalled();
    expect(component.slidesAvailable).toHaveBeenCalled();
  });

  it('#prevSlide should scroll carousel', () => {
    component.slidesAvailable = jasmine.createSpy('slidesAvailable');
    component.prevSlide();
    expect(component.bannersCarousel.previous).toHaveBeenCalled();
    expect(component.slidesAvailable).toHaveBeenCalled();
  });

  it('isSlidesAvailable should returns true' , () => {
    component['canShowPrevious']=false;
    component['canShowNext']=true;
    expect(component['isSlidesAvailable'](carousel)).toBe(true);
   });

   it('isSlidesAvailable should returns false' , () => {
    component['canShowPrevious']=true;
    component['canShowNext']=false;
    expect(component['isSlidesAvailable'](carousel)).toBe(false);
   });

   describe('setActiveContest', () => {
    it('should set active contest to empty when already selected', () => {
      component.selectedContest = '';
      spyOn(component, 'emitSelctedContest');
      component.setActiveContest();
      expect(component.selectedContest).toBe('');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });
    it('should set active contest', () => {
      component.selectedContest = '12345';
      spyOn(component, 'emitSelctedContest');
      component.setActiveContest('123456');
      expect(component.selectedContest).toBe('123456');
      expect(component.emitSelctedContest).toHaveBeenCalled();
    });
   });

   describe('emitSelctedContest', () => {
    it('should set active contest to empty when already selected', () => {
      component.selectedContest = '';
      spyOn(component, 'findContestName');
      spyOn(component.selectedContestChange, 'emit');
      component.emitSelctedContest();
      expect(component.selectedContest).toBe('');
      expect(component.findContestName).not.toHaveBeenCalled();
      expect(component.selectedContestChange.emit).toHaveBeenCalled();
    });
    it('should set active contest', () => {
      component.selectedContest = '123456';
      spyOn(component, 'findContestName');
      spyOn(component.selectedContestChange, 'emit');
      component.emitSelctedContest();
      expect(component.selectedContest).toBe('123456');
      expect(component.findContestName).toHaveBeenCalled();
      expect(component.selectedContestChange.emit).toHaveBeenCalled();
    });
   });

   it('findContestName should return contest name', () => {
      component.contests = CONTESTS;
      component.selectedContest = '61b2f0372cb30f010f8fa61b';
      const result = component.findContestName();
      expect(result).toEqual('1685124-contest' as string);
   });

   describe('#slidesAvailable', () => {
    it('should not check if slides are not available', () => {
      const currentcarousel = {
        currentSlide: 4,
        slidesCount: 4,
        next: jasmine.createSpy('next').and.returnValue(2),
        previous: jasmine.createSpy('previous').and.returnValue(1),
      };
      component.canShowPrevious = true;
      component.canShowNext = true;
      component.slidesAvailable(currentcarousel);
      expect(component.canShowPrevious).toBe(true);
      expect(component.canShowNext).toBe(true);
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });
    it('should check if slides are available', () => {
      const currentcarousel = {
        currentSlide: 1,
        slidesCount: 4,
        next: jasmine.createSpy('next').and.returnValue(2),
        previous: jasmine.createSpy('previous').and.returnValue(1),
      };
      component['isSlidesAvailable'](carousel);
      component.canShowPrevious = true;
      component.canShowNext = false;
      component.slidesAvailable(currentcarousel);
      expect(component.canShowPrevious).toBe(true);
      expect(component.canShowNext).toBe(true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  describe('#getContestBetSlipToolTip', () => {
    it('should call getStaticBlock', () => {
      (component as any).getContestBetSlipToolTip();
      expect(cmsService.getStaticBlock).toHaveBeenCalledWith(CONTEST_SELECTION.STATIC_BLOCK_URL);
      expect(domSanitizer.sanitize).toHaveBeenCalled();
      expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalled();
      expect(component.staticBlockContent).toEqual('<HTML>');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

   describe('#triggerSlideUp', () => {
    it('should set slideout class name after 500 ms', () => {
        component['triggerSlideUp']();
        expect(component.slideUpClass).toEqual(ENTRY_CONFIRMATION.contestSelectionClassname);
    });
  });

  describe('#activeSelCount', () => {
    it('should return 1 if selectedContest is not null', () => {
      component.selectedContest = '1533697';
      const result = component['activeSelCount']();
      expect(result).toEqual('1' as string);
    });

    it('should return 0 if selectedContest is null', () => {
      const result = component['activeSelCount']();
      expect(result).toEqual('0' as string);
    });
  });

  describe('#getPrizetypeIndex', () => {
    it('should return in pence if toBeReturned is "prizeValue" and value < 1', () => {
      const result = component.getPrizetypeIndex(prizeArray, 'prizeValue');
      expect(prizeArray[0].type).toBe("Cash");
      expect(result).toEqual('10p' as string);
    });

    it('should return in euros if toBeReturned is "prizeValue" and value >= 1', () => {
      const result = component.getPrizetypeIndex(prizeArray2, 'prizeValue');
      expect(prizeArray2[0].type).toBe("Cash");
      expect(result).toEqual('1' as string);
    });

    it('should return boolean if toBeReturned is "cash/freebet/voucher"', () => {
      const result = component.getPrizetypeIndex(prizeArray2, 'Cash');
      expect(prizeArray2[0].type).toBe("Cash");
      expect(result).toEqual(true as boolean);
    });
  });

  describe('#checkPenceorEuro', () => {
    it('should return true if prize value greater than or equal to 1', () => {
      const result = component.checkPenceorEuro(prizeArray2, 'prizeValue');
      expect(result).toEqual(true);
    });

    it('should return false if prize value less than 1', () => {
      const result = component.checkPenceorEuro(prizeArray, 'prizeValue');
      expect(result).toEqual(false);
    });
  });

  describe('#getMinEntryCurrency', () => {
    it('should return pence if value is less than 1', () => {
      const result = component.getMinEntryCurrency('0.2');
      expect(result).toEqual('20p' as string);
    });

    it('should return euro if value greater than or equal to 1', () => {
      const result = component.getMinEntryCurrency('20');
      expect(result).toEqual('20' as string);
    });
  });
});
