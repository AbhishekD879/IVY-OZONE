import { QuickbetPanelWrapperComponent } from '@shared/components/quickbetPanelWrapper/quickbet-panel-wrapper.component';
import { IQuickbetSelectionResponseModel } from '@app/quickbet/models/quickbet-selection-response.model';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('QuickbetPanelWrapperComponent', () => {
  let component;
  let pubsubService;
  let changeDetectorRef;
  let cmsService;
  let remoteBsService;

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };
    remoteBsService = {
      restoreSession: jasmine.createSpy('restoreSession')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RENDER_QUICKBET_COMPONENT: 'RENDER_QUICKBET_COMPONENT'
      }
    };

    component = new QuickbetPanelWrapperComponent(pubsubService, changeDetectorRef, cmsService, remoteBsService);
  });

  it('should subscribe to pubsub event on init', () => {
    component.ngOnInit();
    expect(pubsubService.subscribe).toHaveBeenCalledWith('QuickbetPanelWrapperComponent',
      pubsubService.API.RENDER_QUICKBET_COMPONENT, component['renderQuickbet']);
  });

  it('ngOnInit should init connection if quickbet ENABLED in CMS', fakeAsync(() => {

    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({
      quickBet: {
        EnableQuickBet: true
      }
    }));

    component.ngOnInit();

    tick();

    expect(remoteBsService.restoreSession).toHaveBeenCalled();
  }));

  it('ngOnInit should NOT init connection if quickbet DISABLED in CMS', fakeAsync(() => {

    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({
      quickBet: {
        EnableQuickBet: false
      }
    }));

    component.ngOnInit();

    tick();

    expect(remoteBsService.restoreSession).not.toHaveBeenCalled();
  }));

  it('ngOnInit should NOT init connection if quickbet config is absent in CMS', fakeAsync(() => {

    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({}));

    component.ngOnInit();

    tick();

    expect(remoteBsService.restoreSession).not.toHaveBeenCalled();
  }));


  it('should unsubscribe from pubsub event on destroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('QuickbetPanelWrapperComponent');
  });

  it('should show quickbet and store selection data', () => {
    const selection = {
      typeName: 'simple'
    } as IQuickbetSelectionResponseModel;

    expect(component.selection).toBeFalsy();

    component['renderQuickbet'](selection);

    expect(component.selection).toEqual(selection);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });
});
