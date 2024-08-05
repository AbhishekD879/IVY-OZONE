import { SvgTeamKitComponent } from '@shared/components/svgTeamKit/svg-team-kit.component';
import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SvgTeamKitComponent', () => {
  let component: SvgTeamKitComponent;
  let asyncScriptLoaderService: any;
  let changeDetectorRef;

  beforeEach(() => {
    asyncScriptLoaderService = {
      loadSvgIcons: jasmine.createSpy().and.returnValue(observableOf())
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new SvgTeamKitComponent(
      asyncScriptLoaderService,
      changeDetectorRef
    );
    component.teamKitRef = {
      nativeElement: {
        append: jasmine.createSpy('append')
      }
    };

  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('#ngOnInit should load the test.svg file', () => {
      asyncScriptLoaderService.loadSvgIcons.and.returnValue(observableOf('<svg>1</svg>'));
      component.fileName = 'test';
      component.ngOnInit();
      expect(asyncScriptLoaderService.loadSvgIcons).toHaveBeenCalledWith('/assets/images/svg/team-kits/test.svg', false);
    });

    it('#ngOnInit should get svg and insert into html', fakeAsync(() => {
      asyncScriptLoaderService.loadSvgIcons.and.returnValue(observableOf('<svg>1</svg>'));
      expect(component.svgIsLoaded).toEqual(false);
      component.ngOnInit();
      tick();
      expect(component.teamKitRef.nativeElement.append).toHaveBeenCalledWith(jasmine.any(Object));
      expect(component.svgIsLoaded).toEqual(true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));

    it('#ngOnInit should get svg and insert into html', () => {
      component.isTeamKitAvailable.emit = jasmine.createSpy('component.isTeamKitAvailable.emit');
      asyncScriptLoaderService.loadSvgIcons.and.returnValue(throwError('404'));
      component.ngOnInit();

      expect(component.isTeamKitAvailable.emit).toHaveBeenCalledWith(false);
    });

    it('#ngOnInit svg is not returned', () => {
      component.isTeamKitAvailable.emit = jasmine.createSpy('component.isTeamKitAvailable.emit');
      asyncScriptLoaderService.loadSvgIcons.and.returnValue(observableOf('<svg>1</svg123>'));
      component.ngOnInit();
      expect(component.svgIsLoaded).toEqual(false);
      expect(component.isTeamKitAvailable.emit).toHaveBeenCalledWith(false);
    });
  });

  it('should use OnPush strategy', () => {
    expect(SvgTeamKitComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
