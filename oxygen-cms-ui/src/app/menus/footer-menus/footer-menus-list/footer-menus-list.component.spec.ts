import { fakeAsync, tick, TestBed } from '@angular/core/testing';
import { Observable, of } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { FooterMenusListComponent } from './footer-menus-list.component';
import { ApiClientService } from '@app/client/private/services/http';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { FooterMenu } from '@app/client/private/models';
import { FooterMenusCreateComponent } from '../footer-menus-create/footer-menus-create.component';
import { SegmentStoreService } from '@root/app/client/private/services/segment-store.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

describe('FooterMenusListComponent', () => {
  let component: FooterMenusListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;
  let footerMenu;
  let footerMenusListMock;
  let segmentsMock;
  let segmentStoreService;

  beforeEach(() => {
    footerMenusListMock = [
      {
        "id": "60f959ae3fd85f2be7bfbb06",
        "segments": ["Cricket"],
        "segmentsExcl": ["Rugby"]
      }
    ];

    segmentsMock = [
      { "id": 101, "name": "Universal" },
      { "id": 201, "name": "Cricket" }
    ];

    apiClientService = {
      footerMenu: jasmine.createSpy('footerMenu').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
          body: {}
        })),
        getFooterMenus: jasmine.createSpy('getFooterMenusBySegment').and.returnValue(of(
          footerMenusListMock
        )),
        getFooterMenusBySegment: jasmine.createSpy('getFooterMenusBySegment').and.returnValue(of(
          { body: footerMenusListMock }
        )),
        getSegments: jasmine.createSpy('getSegments').and.returnValue(of(
          segmentsMock
        )),
        reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: {} })),
        delete: jasmine.createSpy('delete').and.returnValue(of({ body: {} })),
        save: jasmine.createSpy('save').and.returnValue(of({ body: { id: '1' } }))
      }),
    };
    
    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.SURFACE_BET_TAB }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        .and.callFake(({ title, message, yesCallback }) => yesCallback()),
      showCustomDialog: jasmine.createSpy('showCustomDialog')
        .and.callFake((footerMenusCreateComponent, { width, title, yesOption, noOption, yesCallback }) => yesCallback()),
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = jasmine.createSpyObj('snackBarSpy', ['open']);
    router = { navigate: jasmine.createSpy('navigate'), };

    component = new FooterMenusListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router,
      segmentStoreService);

    TestBed.configureTestingModule({
      declarations: [FooterMenusListComponent],
      providers: [
        { provide: ApiClientService, useValue: apiClientService },
        { provide: Router, useValue: router },  
        { provide: SegmentStoreService, useValue: segmentStoreService },
        { provide: MatSnackBar, useValue: snackBar },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA]
    }).compileComponents();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.footerMenu);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
    expect(component.selectedSegment).toEqual(CSPSegmentConstants.UNIVERSAL_TITLE);
  }));

  it('should call segmentHandler method', () => {
    const segment = "Cricket";
    component.segmentHandler(segment);
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
    expect(apiClientService.footerMenu().getFooterMenusBySegment).toHaveBeenCalledTimes(1);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(1);
  });

  it('should get footerMenusList by segment', () => {
    const segment = "Cricket";
    component['segmentHandler'](segment);
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
    expect(apiClientService.footerMenu().getFooterMenusBySegment).toHaveBeenCalledWith("Cricket");
    expect(apiClientService.footerMenu().getFooterMenusBySegment).toHaveBeenCalledTimes(1);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(1);
  });

  it('should not get footerMenusList if there is no segment matching', () => {
    const segment = null;
    component['segmentHandler'](segment);
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
    expect(apiClientService.footerMenu().getFooterMenusBySegment).toHaveBeenCalledWith(null);
    expect(apiClientService.footerMenu().getFooterMenusBySegment).toHaveBeenCalledTimes(1);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  describe('#create footerMenu', () => {
    beforeEach(() => {
      footerMenu = { id: '1' };
      component.footerMenus = [{ id: '1' }] as FooterMenu[];
    });
    it('should create footerMenu and add to the list', () => {
      component.createFooterMenu();
      expect(dialogService.showCustomDialog).toHaveBeenCalledWith(
        FooterMenusCreateComponent, {
        width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
        title: 'Add New Footer Menu',
        yesOption: 'Save',
        noOption: 'Cancel',
        yesCallback: jasmine.any(Function)
      });
      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.footerMenu);
      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().save).toHaveBeenCalled();
      expect(component.footerMenus.length).toBe(2);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith([`/menus/footer-menus/${footerMenu.id}`]);
    });
    it('should throw error', () => {
      component.createFooterMenu();
      apiClientService.footerMenu().save.and.returnValue(Observable.throwError);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#removehandler', () => {
    beforeEach(() => {
      footerMenu = { id: '1' };
      component.footerMenus = [{ id: '1' }] as FooterMenu[];
    });
    it('should delete the footerMenu data from the list', () => {
      component.removeHandler(footerMenu);
      expect(dialogService.showConfirmDialog).toHaveBeenCalledWith(
        {
          title: 'Footer Menu',
          message: 'Are You Sure You Want to Remove Footer Menu?',
          yesCallback: jasmine.any(Function)
        });
      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.footerMenu);
      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().delete).toHaveBeenCalledWith(footerMenu.id);
      expect(component.footerMenus.length).toBe(0);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    it('should throw an error', () => {
      component.removeHandler(footerMenu);
      apiClientService.footerMenu().delete.and.returnValue(Observable.throwError);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  it('#reorderhandler', () => {
    const newOrder = { id: '1', order: ['first', 'second'] };
    component.reorderHandler(newOrder);
    expect(apiClientService.footerMenu).toHaveBeenCalled();
    expect(apiClientService.footerMenu().reorder).toHaveBeenCalledWith(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith(`Footer menu order saved!`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION
    });
  });
});
