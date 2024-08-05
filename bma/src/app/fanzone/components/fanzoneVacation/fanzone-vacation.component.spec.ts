import { of } from 'rxjs';
import { SITECORE_PROMOTION_EMPTY_TEASER } from '@ladbrokesDesktop/bma/components/home/mockdata/home.component.mock';
import { FanzoneAppVacationComponent } from '@app/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { fanzoneVacation, fanzoneSiteCorePromotion } from '@app/fanzone/components/fanzoneVacation/mockData/fanzone-vacation.component.mock';
import { fakeAsync, tick } from '@angular/core/testing';

describe('FanzoneAppVacationComponent', () => {
  let component: FanzoneAppVacationComponent;
  let cms, changeDetectorRef, device, fanzoneModuleService, windowRef, element, smartBanner;

  beforeEach(() => {
    smartBanner = {
      scrollTop: 100
    };
    cms = {
      getFanzoneNewSeason: jasmine.createSpy('getFanzoneNewSeason').and.returnValue(of(fanzoneVacation))
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('changeDetectorRef')
    }
    element = {
      nativeElement : { contains : jasmine.createSpy('element.contains').and.returnValue(false)},
    };
    device = {
      mobileWidth : 1024
    }
    fanzoneModuleService = {
      getFanzoneImagesFromSiteCore: jasmine.createSpy('getFanzoneImagesFromSiteCore').and.returnValue(of(fanzoneSiteCorePromotion))
    }

    windowRef = {
      nativeWindow: {
        innerWidth: 1024,
        screen : {
          width: 1024
        },
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn, time) => { fn(); }),
        document : {
          querySelector: jasmine.createSpy().and.returnValue(smartBanner)
        }
      }
    }
    component = new FanzoneAppVacationComponent(cms, changeDetectorRef, device,
      fanzoneModuleService, windowRef);
  });

  it('ngOnInit - should get desktop images', () => {
    component.ngOnInit();
    expect(component.fanzoneBgImage).toBe('fzNewSeasonBgImageDesktop');
    expect(component.fanzoneVacationImage).toBe('fzNewSeasonBadgeDesktop');
    expect(component.fanzoneLightningImage).toBe('fzNewSeasonLightningDesktop');
  });

  it('ngOnInit - should get mobile images', () => {
    windowRef.nativeWindow.innerWidth = 756;
    component.getContainerHeight = jasmine.createSpy('component.getContainerHeight');
    component.ngOnInit();
    expect(component.getContainerHeight).toHaveBeenCalled(); 
    expect(component.fanzoneBgImage).toBe('fzNewSeasonBgImageMobile');
    expect(component.fanzoneVacationImage).toBe('fzNewSeasonBadgeMobile');
    expect(component.fanzoneLightningImage).toBe('fzNewSeasonLightningMobile');
  });

  it('ngOnInit - in case of empty teaser response', () => {
    fanzoneModuleService.getFanzoneImagesFromSiteCore.and.returnValue(of(SITECORE_PROMOTION_EMPTY_TEASER));
    component.ngOnInit();
    expect(component.fanzoneBgImage).toBe('');
    expect(component.fanzoneVacationImage).toBe('');
    expect(component.fanzoneLightningImage).toBe('');
  });

  it('getContainerHeight on document click',  fakeAsync(() => {
    component.getContainerHeight = jasmine.createSpy('component.getContainerHeight');
    component.clickOutside();
    tick(100);
    expect(component.getContainerHeight).toHaveBeenCalled(); 
  }));

  it('vacation content height with smart banner', () => {
    device.mobileWidth = 767;
    windowRef.nativeWindow.innerWidth = "760";
    const testObj = {someAttr: 'tra-ta-ta'};
    windowRef.nativeWindow.document.querySelector.and.returnValue(testObj);
    component.getContainerHeight();
    expect(component.containerHeight).toBe('calc(100vh - 203px)');
  })

  it('vacation content height in desktop', () => {
    device.mobileWidth = 767;
    windowRef.nativeWindow.innerWidth = "790";
    const testObj = {someAttr: 'tra-ta-ta'};
    windowRef.nativeWindow.document.querySelector.and.returnValue(testObj);
    component.getContainerHeight();
    expect(component.containerHeight).not.toBeDefined();
  })

  it('vacation content height without smart banner', () => {
    device.mobileWidth = 767;
    windowRef.nativeWindow.innerWidth = "760";
    windowRef.nativeWindow.document.querySelector.and.returnValue(null);
    component.getContainerHeight();
    expect(component.containerHeight).toBe('calc(100vh - 145px)');
  })

  it('getImage for desktop', () => {
    const result = component.getImage("desktop", "mobile");
    expect(result).toBe("desktop");
  })

  it('getImage for mobile', () => {
    device.mobileWidth = 767;
    windowRef.nativeWindow.innerWidth = "760";
    const result = component.getImage("desktop", "mobile");
    expect(result).toBe("mobile");
  })

  it('getImageWidth', () => {
    const result = component.getImageWidth('/fanzone/vacation');
    expect(result).toBe('/fanzone/vacation?w=1024')
  })
});
