import { of } from 'rxjs/internal/observable/of';
import { fakeAsync, tick } from '@angular/core/testing';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { FanzoneOptinEmailDialogComponent } from './fanzone-optin-email-dialog.component';
import * as fanzoneConst from '@lazy-modules/fanzone/fanzone.constant';
import { RML_REQUEST, cmsEmailData, getEmailOptinRMLStorage, getEmailOptinStorage, getEmailOptinStorage1, params } from '@app/lazy-modules/fanzone/components/fanzoneOptinEmailDialog/mockData/fanzone-optin-email-dialog.component.mock';
import { ICmsEmailOptin } from '@app/lazy-modules/fanzone/models/fanzone-email-optin.model';

describe('FanzoneOptinEmailDialogComponent', () => {
  let component: FanzoneOptinEmailDialogComponent;
  let deviceService, windowRef, router, fanzoneStorageService, fanzoneSharedService, timeService, loc,elementRef;
  beforeEach(() => {
    deviceService = {
      isIos : true,
      isWrapper: true
    };
    windowRef = {
      nativeWindow: {
        location: {
          href: '/fanzone/sport-football/Arsenal/now-next',
          origin: 'https://qa2.sports.ladbrokes.com',
          pathname: '/fanzone/sport-football/Arsenal/now-next'
        }
      },
      document: {
        body: {
          classList: {
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    router = {
      url: '/fanzone/sport-football'
    };
    fanzoneStorageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    fanzoneSharedService = {
      getFanzoneEmailOptin: jasmine.createSpy('getFanzoneEmailOptin').and.returnValue(of(cmsEmailData)),
      postEmailOptinDetails: jasmine.createSpy('postEmailOptinDetails').and.returnValue(of({})),
      showFanzoneGamesPopup: jasmine.createSpy('showFanzoneGamesPopup').and.returnValue(of(params.data.fanzoneDetailResponse)),
      addDaysToCurrentDate: jasmine.createSpy('addDaysToCurrentDate').and.returnValue(of({}))
    };
    timeService = {
      getHydraDaysDifference: jasmine.createSpy('getHydraDaysDifference').and.returnValue(of(14)),
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue(of({}))
    };
    loc = {
      onPopState: jasmine.createSpy('onPopState')
    };
    elementRef = {
      nativeElement : { contains : jasmine.createSpy('element.contains').and.returnValue(false)},
    };
    component = new FanzoneOptinEmailDialogComponent(
      deviceService,
      windowRef,
      router,
      fanzoneStorageService,
      fanzoneSharedService,
      timeService,
      loc,
      elementRef);
    component.dialog = {
      closeOnOutsideClick: jasmine.createSpy("closeOnOutsideClick"),
      open: jasmine.createSpy('open'),
      close: jasmine.createSpy('close'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
  });


  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('clickOutside', ()=>{
    elementRef.nativeElement.contains.and.returnValue(false);
  })

  it('open dialog when user has not opted in to emails', () => {
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage);
    AbstractDialogComponent.prototype.setParams(params);
    const openSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'open');
    component.open();
    expect(openSpy).toHaveBeenCalled();
  });

  it('open dialog when user has not opted in to emails', () => {
    fanzoneStorageService.get.and.returnValue(undefined);
    AbstractDialogComponent.prototype.setParams(params);
    const openSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'open');
    component.open();
    expect(openSpy).toHaveBeenCalled();
  });

  it('to not open dialog when user is outside fanzone page', () => {
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage);
    AbstractDialogComponent.prototype.setParams(params);
    router.url = "/home";
    const openSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'open')
    component.open();
    expect(openSpy).not.toHaveBeenCalled();
  });

  it('to not open dialog when user is outside fanzone page when user clicks on rml', () => {
    getEmailOptinStorage.remindMeLaterCount = 0;
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage);
    timeService.getHydraDaysDifference = jasmine.createSpy('getHydraDaysDifference').and.returnValue(of(-14));
    AbstractDialogComponent.prototype.setParams(params);
    const openSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'open')
    component.open();
    expect(openSpy).not.toHaveBeenCalled();
  });

  it('to not open dialog when user is outside fanzone page when user clicks on dsme', () => {
    getEmailOptinStorage.dontShowMeAgainPref = true;
    timeService.getHydraDaysDifference = jasmine.createSpy('getHydraDaysDifference').and.returnValue(of(-14));
    AbstractDialogComponent.prototype.setParams(params);
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage);
    const openSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'open')
    component.open();
    expect(openSpy).not.toHaveBeenCalled();
  });

  it('to not open dialog and open fanzone games popup', () => {
    getEmailOptinStorage.dontShowMeAgainPref = true;
    timeService.getHydraDaysDifference = jasmine.createSpy('getHydraDaysDifference').and.returnValue(of(-14));
    AbstractDialogComponent.prototype.setParams(params);
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage);
    const openSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'open')
    component.open();
    expect(openSpy).not.toHaveBeenCalled();
    expect(fanzoneSharedService.showFanzoneGamesPopup).toHaveBeenCalledWith(params.data.fanzoneDetailResponse);
  });

  it('closePopupDialog', () => {
    const closeSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    component.closePopupDialog(RML_REQUEST as any);
    expect(fanzoneSharedService.postEmailOptinDetails).toHaveBeenCalledWith(RML_REQUEST, true);
    expect(closeSpy).toHaveBeenCalled();
    expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('ios-modal-opened');
    expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('ios-modal-opened');
    expect(fanzoneSharedService.showFanzoneGamesPopup).toHaveBeenCalledOnceWith(params.data.fanzoneDetailResponse);
  });

  it('checkDialogButtonClick remind me later', () => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    component.getRemindMeLaterRequest = jasmine.createSpy('getRemindMeLaterRequest');
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    component.checkDialogButtonClick(fanzoneConst.BUTTONS.rml);
    expect(component.getRemindMeLaterRequest).toHaveBeenCalled();
  });

  it('checkDialogButtonClick on remind me later click ', () => {
    component.getRemindMeLaterRequest = jasmine.createSpy('getRemindMeLaterRequest');
    AbstractDialogComponent.prototype.setParams(params);
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage);
    component.checkDialogButtonClick(fanzoneConst.BUTTONS.dsme);
    expect(component.getRemindMeLaterRequest).toHaveBeenCalled();
  });

  it('getRemindMeLaterRequest when storage is empty', () => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    fanzoneStorageService.get.and.returnValue({});
    component.getRemindMeLaterRequest(fanzoneConst.BUTTONS.dsme);
    expect(component.closePopupDialog).not.toHaveBeenCalled();
  });

  it('getRemindMeLaterRequest when storage is undefined', fakeAsync(() => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    fanzoneStorageService.get.and.returnValue(undefined);
    component.getRemindMeLaterRequest(fanzoneConst.BUTTONS.dsme);
    tick();
    expect(component.optInData).toBe(params.data);
    expect(component.closePopupDialog).not.toHaveBeenCalled();
  }));

  it('getRemindMeLaterRequest when user clicks on DSME', fakeAsync(() => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage1);
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    timeService.formatByPattern = jasmine.createSpy('timeService.formatByPattern').and.returnValue('2023-07-14T15:53:47');
    component.getRemindMeLaterRequest(fanzoneConst.BUTTONS.dsme);
    tick();
    expect(component.optInData).toBe(params.data);
    expect(component.closePopupDialog).toHaveBeenCalledWith({
      dontShowMeAgainPref: true,
      remindMeLaterPrefDate: '2023-07-14T15:53:47Z',
      remindMeLaterCount: 2
    });
  }));

  it('getRemindMeLaterRequest when user clicks on DSME when CMS has no data', fakeAsync(() => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    component.fanzoneOptinCmsData = {} as ICmsEmailOptin;
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage1);
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    timeService.formatByPattern = jasmine.createSpy('timeService.formatByPattern').and.returnValue('2023-07-14T15:53:47');
    component.getRemindMeLaterRequest(fanzoneConst.BUTTONS.dsme);
    tick();
    expect(component.optInData).toBe(params.data);
    expect(component.closePopupDialog).toHaveBeenCalledWith({
      dontShowMeAgainPref: true,
      remindMeLaterPrefDate: '2023-07-14T15:53:47Z',
      remindMeLaterCount: 2
    });
  }));

  it('onoutsideclick on document click',  fakeAsync(() => {
    const closeSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'closeDialog');
    const event = { target: { tagName: 'target '},
    stopPropagation: jasmine.createSpy('stopPropagation') } as any;
    component.clickOutside(event as any);
    tick(100);
    expect(event.stopPropagation).toHaveBeenCalled();
    expect(closeSpy).toHaveBeenCalled(); 
    expect(fanzoneSharedService.showFanzoneGamesPopup).toHaveBeenCalled();
  }));


  it('getRemindMeLaterRequest when user clicks on RML for 2nd time', fakeAsync(() => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    fanzoneStorageService.get.and.returnValue(getEmailOptinStorage1);
    AbstractDialogComponent.prototype.setParams(params);
    component.optInData = params.data;
    fanzoneSharedService.addDaysToCurrentDate = jasmine.createSpy('fanzoneSharedService.addDaysToCurrentDate').and.returnValue('2023-07-14T15:53:47');
    timeService.formatByPattern = jasmine.createSpy('timeService.formatByPattern').and.returnValue('2023-07-14T15:53:47');
    component.getRemindMeLaterRequest(fanzoneConst.BUTTONS.rml);
    tick();
    expect(component.optInData).toBe(params.data);
    expect(component.closePopupDialog).toHaveBeenCalledWith({
      dontShowMeAgainPref: false,
      remindMeLaterPrefDate: '2023-07-14T15:53:47Z',
      remindMeLaterCount: 3
    });
  }));

  it('getRemindMeLaterRequest when user clicks on RML for 1st time', fakeAsync(() => {
    component.closePopupDialog = jasmine.createSpy('closePopupDialog');
    AbstractDialogComponent.prototype.setParams(params);
    fanzoneStorageService.get.and.returnValue(getEmailOptinRMLStorage);
    component.optInData = params.data;
    fanzoneSharedService.addDaysToCurrentDate = jasmine.createSpy('fanzoneSharedService.addDaysToCurrentDate').and.returnValue('2023-07-14T15:53:47');
    timeService.formatByPattern = jasmine.createSpy('timeService.formatByPattern').and.returnValue('2023-07-14T15:53:47');
    component.getRemindMeLaterRequest(fanzoneConst.BUTTONS.rml);
    tick();
    expect(component.optInData).toBe(params.data);
    expect(component.closePopupDialog).toHaveBeenCalledWith({
      dontShowMeAgainPref: false,
      remindMeLaterPrefDate: '2023-07-14T15:53:47Z',
      remindMeLaterCount: 1
    });
  }));

  it('when user wants to optin to emails', () => {
    const closeSpy = spyOn(FanzoneOptinEmailDialogComponent.prototype['__proto__'], 'closeDialog');
    component.communicationUrl = 'https://test.myaccount.ladbrokes.com/en/mobileportal/communication';
    component.checkDialogButtonClick(fanzoneConst.BUTTONS.optin);
    expect(windowRef.nativeWindow.location.href).toBe('https://test.myaccount.ladbrokes.com/en/mobileportal/communication?source=fanzone&redirectionUrl=https://qa2.sports.ladbrokes.com/fanzone/sport-football/Arsenal/now-next');
    expect(closeSpy).toHaveBeenCalled();
  });

  it('when user wants to default', () => {
    component.checkDialogButtonClick('default');
  });
});
