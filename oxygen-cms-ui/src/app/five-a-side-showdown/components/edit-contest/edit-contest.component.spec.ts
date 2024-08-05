import { of } from 'rxjs/observable/of';

import { EditContestComponent } from '@app/five-a-side-showdown/components/edit-contest/edit-contest.component';
import {  BREADCRUMBS_EDIT_MOCK,  EDIT_CONTEST_INVALID_MOCK,  EDIT_CONTEST_MOCK
} from '@app/five-a-side-showdown/components/edit-contest/edit-contest.mock';
import { throwError } from 'rxjs';
import { REMOVE_CONTEST_MOCK } from '@app/five-a-side-showdown/components/contest-manager/contests.mock';

describe('EditContestComponent', () => {
  let component: EditContestComponent;
  let router;
  let globalLoaderService;
  let apiClientService;
  let dialogService;
  let activatedRoute;
  let contestManagerService;
  let errorService;
  let brandService;
  let clipboard;

  beforeEach(() => {
    activatedRoute = {
      params: of({
        contestid: 'abc123'
      })
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/five-a-side-showdown/'
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    }
    contestManagerService = {
      getContests: jasmine.createSpy('getContests').and.returnValue(of({
        body: EDIT_CONTEST_MOCK
      })),
      saveContestChanges: jasmine.createSpy('saveContestChanges').and.returnValue(of({
        body: EDIT_CONTEST_MOCK
      })),
      getContestForId :jasmine.createSpy('getContestForId').and.returnValue(of({
        body: EDIT_CONTEST_MOCK
      })),
      uploadSvgImage :jasmine.createSpy('uploadSvgImage').and.returnValue(of({
        body: EDIT_CONTEST_MOCK
      })),
      removeContestForId : jasmine.createSpy('removeContestForId').and.returnValue(of({
        body: REMOVE_CONTEST_MOCK
      }))
    };

    clipboard = {
      copy: () => { return EDIT_CONTEST_MOCK.id }
    };

    apiClientService = {
      contestManagerService: () => contestManagerService,
      clipboard: () => clipboard
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    brandService = {
      brand: 'ladbrokes'
    };
    component = new EditContestComponent(activatedRoute,
      globalLoaderService,
      apiClientService,
      dialogService,
      router,
      errorService,
      brandService,
      clipboard
      );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should fetch contests data on init', () => {
      spyOn(component as any, 'loadContestData');
      component.ngOnInit();
      expect(component.isLoading).toBe(false);
      expect(component['loadContestData']).toHaveBeenCalled();
    });
  });

  describe('#loadContestData edit flow', () => {
    it('should load contest data based on create or edit flow', () => {
      spyOn(component as any, 'loadEditData');
      component.ngOnInit();
      expect(component['loadEditData']).toHaveBeenCalled();
    });
  });
 
  describe('#loadContestData edit flow', () => {
    it('should load contest data based on id for edit flow', () => {
      spyOn(component as any, 'showHideSpinner');
      component.ngOnInit();
      expect(component.contestManagerForm).toEqual(EDIT_CONTEST_MOCK);
      expect(component['showHideSpinner']).toHaveBeenCalled();
      expect(component.breadcrumbsData).toEqual(BREADCRUMBS_EDIT_MOCK);
    });
    it('should if the service returns error', () => {
      contestManagerService.getContestForId = jasmine.createSpy().and.returnValue(throwError({error: '401'}));
      component.ngOnInit();
      expect(component.contestManagerForm).toBeUndefined();
      expect(errorService.emitError).toHaveBeenCalled();
    });
    it('should set svg images for icon and sponsorlogo in edit flow', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      spyOn(component as any, 'showHideSpinner');
      component.contestManagerForm.icon =   {
        target: { files: [{ name: "iconsvg", size: 500001 , type: "image/svg"}] },
      } as any;
      component.contestManagerForm.sponsorLogo = {
        target: { files: [{ name: "sponsorsvg", size: 500002 , type: "image/svg"}] },
      } as any;
      component.ngOnInit();
      expect(component['showHideSpinner']).toHaveBeenCalled();
      expect(component.iconSvgFile).toEqual(null);
      expect(component.sponsorSvgFile).toEqual(null);
    });
  }); 

  
  describe('#action Handler', () => {
    it('#actionHandler should call correct method', () => {
      spyOn(component, 'removeContest');
      component.actionsHandler('remove');
      expect(component.removeContest).toHaveBeenCalled();
  
      spyOn(component, 'saveChanges');
      component.actionsHandler('save');
      expect(component.saveChanges).toHaveBeenCalled();
  
      spyOn(component, 'revertChanges');
      component.actionsHandler('revert');
      expect(component.revertChanges).toHaveBeenCalled();
    });
  
    it('#actionHandler should do nothing if wrong event', () => {
      spyOn(component, 'removeContest');
      spyOn(component, 'saveChanges');
      spyOn(component, 'revertChanges');
  
      component.actionsHandler('test-event');
      expect(component.removeContest).not.toHaveBeenCalled();
      expect(component.saveChanges).not.toHaveBeenCalled();
      expect(component.revertChanges).not.toHaveBeenCalled();
    });

    it('#removeSegment should call remove and update navigation', () => {
      spyOn(component as any, 'showHideSpinner');
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.removeContest();
      expect(router.navigate).toHaveBeenCalledWith(['/five-a-side-showdown']);
      expect(globalLoaderService['hideLoader']).toHaveBeenCalled();
    });

    it('should throw error if the service returns error', () => {
      spyOn(component as any, 'showHideSpinner');
      contestManagerService.removeContestForId = jasmine.createSpy('removeContestForId').and.returnValue(throwError({error: '401'}));
      component.removeContest();
      expect(globalLoaderService['hideLoader']).toHaveBeenCalled();
      expect(errorService['emitError']).toHaveBeenCalled();
    });
  
    it('#revertChanges should call #loadEditData', () => {
      component['loadEditData'] = jasmine.createSpy('loadEditData');
      component.revertChanges();
      expect(component['loadEditData']).toHaveBeenCalled();
    });

  });

  describe('#uploadFile', () => {
    it('#test for invalid file extension', () => {
       const uploadfile = {
         target: { files: [{ name: "foo", size: 500001 , type: "png"}] },
       } as any ;
       const fieldname =  "iconSvgFile";
       component.prepareToUploadFile(uploadfile, fieldname);
       expect(dialogService.showNotificationDialog).toHaveBeenCalled();
       expect(component.iconSvgFileName.length).toEqual(0);
    });
    it('#test for valid file upload for icon svg file for icon', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      const uploadfile = {
        target: { files: [{ name: "foo", size: 500001 , type: "image/svg"}] },
      } as any;
      const fieldname =  "iconSvgFile";
      component.prepareToUploadFile(uploadfile, fieldname);
      expect(component.iconSvgFileName).toBe('foo');
      expect(component.iconSvgFile).toEqual(uploadfile.target.files[0]);
      expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
      expect(component.sponsorSvgFile).toBeUndefined();
      expect(component.sponsorSvgFileName.length).toBe(0);
   });
   it('#test for valid file upload for icon svg file for sponsorImage', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      const uploadfile = {
        target: { files: [{ name: "foo", size: 500001 , type: "image/svg"}] },
      } as any;
      const fieldname =  "sponsorSvgFile";
      component.prepareToUploadFile(uploadfile, fieldname);
      expect(component.sponsorSvgFileName).toBe('foo');
      expect(component.sponsorSvgFile).toEqual(uploadfile.target.files[0]);
      expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
      expect(component.iconSvgFile).toBeUndefined();
      expect(component.iconSvgFileName.length).toBe(0);
    });
  });

  describe('#sendSvgImages', () => {
    it('#should send svg images for the sponsor logo and icon', () => {
      spyOn(component as any,'clearSvgImageFields');
      component._actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any; 
      component.iconSvgFile =  {
        target: { files: [{ name: "iconsvg", size: 500001 , type: "image/svg"}] },
      } as any;
       component.sponsorSvgFile = {
        target: { files: [{ name: "sponsorsvg", size: 500002 , type: "image/svg"}] },
      } as any;
      component['sendSvgImages'](); 
      expect(component['clearSvgImageFields']).toHaveBeenCalled();
    });    
    it('should return error if sending svg images is failed', () => {
      spyOn(component as any,'clearSvgImageFields');
      component._actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any; 
      component.iconSvgFile =  {
        target: { files: [{ name: "iconsvg", size: 500001 , type: "image/svg"}] },
      } as any;
       component.sponsorSvgFile = {
        target: { files: [{ name: "sponsorsvg", size: 500002 , type: "image/svg"}] },
      } as any;
      contestManagerService.uploadSvgImage = jasmine.createSpy('uploadSvgImage').and.returnValue(throwError({error: '401'}));
      component['sendSvgImages']();
      expect(errorService['emitError']).toHaveBeenCalled();
    });
  })

  describe('#handleUploadImageClick', () => {
      it('#test for file input click when click upload button', () => {
        const inputEle = {
          click: jasmine.createSpy('click')
        };
        const eventEle = 
          {
            target: {
              parentElement : {
                previousElementSibling: {
                  querySelector: jasmine.createSpy('querySelector').and.returnValue(inputEle)
                }
              }
            }
          } as any;
        component.handleUploadImageClick(eventEle);
        expect(inputEle.click).toHaveBeenCalled();
      });
  });

  describe('#getButtonName', () => {
    it('#test for button name to be upload if uploads a new file', () => {
      const fileLabel = component.getButtonName('');
      expect(fileLabel).toBe('Upload File');
    });
    it('#test for button name to be upload if changes a new file', () => {
      const fileLabel = component.getButtonName('changedFile');
      expect(fileLabel).toBe('Change File');
    });
  });

  describe('#removeImage', () => {
    it('#test for file removal for svg icon file', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      const fieldName= 'iconSvgFile';
      component.iconSvgFileInput = {
        nativeElement : {
          value: 'file'
        }
      } as any;
      component.removeImage(fieldName);
      expect(component.iconSvgFile).toBeNull();
      expect(component.iconSvgFileName).toBe('');
      expect(component.iconSvgFileInput.nativeElement.value).toBe('');
    });
    it('#test for file removal for svg sponsor file', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.sponsorSvgFileInput = {
        nativeElement : {
          value: 'file'
        }
      } as any;
      const fieldName= 'sponsorSvgFile';
      component.removeImage(fieldName);
      expect(component.sponsorSvgFile).toBeNull();
      expect(component.sponsorSvgFileName).toBe('');
      expect(component.sponsorSvgFileInput.nativeElement.value).toBe('');
    });
  });

  it('#test for alphanumeric function', () => {
    const event = {
      target: {
        value: 'test'
      }
    } as any;
    component.alphaToNumeric(event);
    expect(event.target.value).toEqual('');
  });

  it('#test for block special chars ', () => {
    const event = {
      target: {
        value: '@@@@test123%%%&****((())_'
      }
    } as any;
    component.blockSpecialChars(event);
    expect(event.target.value).toEqual('test123');
  });

  it('should change contest type to true', () => {
    component.contestManagerForm = EDIT_CONTEST_MOCK;
    component.onContestTypeChange({checked:true});
    expect(component.contestManagerForm.isPrivateContest).toEqual(true);
  })

  it('should change contest type to false', () => {
    component.contestManagerForm = EDIT_CONTEST_MOCK;
    component.onContestTypeChange({checked:false});
    expect(component.contestManagerForm.isPrivateContest).toEqual(null);
  })

  describe('#saveChanges', () => {
    it('#test for successful contest update changes', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component._actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any;
      component.iconSvgFile =  {
        target: { files: [{ name: "iconsvg", size: 500001 , type: "image/svg"}] },
      } as any;
       component.sponsorSvgFile = {
        target: { files: [{ name: "sponsorsvg", size: 500002 , type: "image/svg"}] },
      } as any;
      component.saveChanges();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
    it('#test for successful contest update changes', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component._actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
      } as any;
      component.prizePoolComponent = {
        prizePool : [{}]
      } as any;
      component.saveChanges();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
    it('should if the service returns error', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      contestManagerService.saveContestChanges = jasmine.createSpy('saveContestChanges').and.returnValue(throwError({error: '401'}));
      component.saveChanges();
      expect(errorService['emitError']).toHaveBeenCalled();
    });
  });

  describe('#showHideSpinner', () => {
    it('should show loader when we pass true', () => {
      component['showHideSpinner']();
      expect(component.isLoading).toBeTruthy();
    });
    it('should not show loader when we pass false', () => {
      component['showHideSpinner'](false);
      expect(component.isLoading).toBeFalsy();
    });
  });

  describe('#isValidModel', () => {
    it('should return true if mandatory fields in contest are entered', () => {
      const contetsMock = {...EDIT_CONTEST_MOCK};
      contetsMock.realAccount = true;
      expect(component.isValidModel(contetsMock)).toBeTruthy();
    });
    it('should return false if mandatory fields in contest are not entered', () => {
      expect(component.isValidModel(EDIT_CONTEST_INVALID_MOCK)).toBeFalsy();
    });
  });

  describe('#handleStartDate', () => {
    it('should return date in ISO Format for date Object', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.startDate = null;
      component.handleStartDate("2021-01-13T11:59:43.603Z");
      expect(component.contestManagerForm.startDate.length).not.toEqual(0);
    });
  });

  describe('#test updates for description, eventBlurb, entry confirmation', () => {
    it('should set the new description to null', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.description = 'oldvalue';
      component.updateDescription('');
      expect(component.contestManagerForm.description).toBeNull();
    });

    it('should set the new description to new value', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.description = 'oldvalue';
      component.updateDescription('newValue');
      expect(component.contestManagerForm.description).toEqual('newValue');
    });


    it('should set the new blurb to null', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.blurb = 'oldvalue';
      component.updateBlurb('');
      expect(component.contestManagerForm.blurb).toBeNull();
    });

    it('should set the new blurb to new value', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.blurb = 'oldvalue';
      component.updateBlurb('newValue');
      expect(component.contestManagerForm.blurb).toEqual('newValue');
    });

    it('should set the new entry confirmation to null', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.entryConfirmationText = 'oldvalue';
      component.updateEntryConfirmation('');
      expect(component.contestManagerForm.entryConfirmationText).toBeNull();
    });

    it('should set the new description', () => {
      component.contestManagerForm = EDIT_CONTEST_MOCK;
      component.contestManagerForm.entryConfirmationText = 'oldvalue';
      component.updateEntryConfirmation('newValue');
      expect(component.contestManagerForm.entryConfirmationText).toEqual('newValue')
    });
  });

  it('should set payTable data', () => {
    component.contestManagerForm = {} as any;
    component.onPayTableChanged([]);
    expect(component.contestManagerForm.payTable).toEqual([]);
  });

  it('should set prizePool data', () => {
    component.contestManagerForm = {} as any;
    component.onPrizePoolChanged({ cash: 1000} as any);
    expect(component.contestManagerForm.prizePool).toEqual({ cash: 1000} as any);
  });

  describe('#onDownloadCSV', () => {
    it('should handle click event (case: contest)', () => {
      const mock = {
        href: undefined, target: undefined, download: undefined,
        click: jasmine.createSpy('click')
      };
      spyOn(document, 'createElement').and.returnValue(mock as any);
      component.onDownloadCSV('contest');
      expect(mock.click).toHaveBeenCalled();
    });
    it('should handle click event (case: prize)', () => {
      const mock = {
        href: undefined, target: undefined, download: undefined,
        click: jasmine.createSpy('click')
      };
      spyOn(document, 'createElement').and.returnValue(mock as any);
      component.onDownloadCSV('prize');
      expect(mock.click).toHaveBeenCalled();
    });
  });

});


