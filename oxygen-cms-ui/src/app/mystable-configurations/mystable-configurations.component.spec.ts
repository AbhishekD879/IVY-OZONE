import { FormBuilder, FormControl, FormGroup} from '@angular/forms';
import { MystableConfigurationsComponent } from './mystable-configurations.component';
import { of } from 'rxjs';

describe('MystableConfigurationsComponent', () => {
  let component: MystableConfigurationsComponent;
  let brandService, apiClientService, snackBar, globalLoaderService;
  let formBuilder: FormBuilder;

  beforeEach(() => {

    const responseData = {
      body: {},
      status: 200,
      statusText: 'ssample',
      headers: null,
      url: 'abc.com',
    } as any;

    const getStableResponseData = {
      body: {
        brand: 'test',
        active: true,
        horsesRunningToday: true,

      },
      status: 200,
      statusText: 'OK',
      headers: null,
      url: 'abc.com',
    } as any;


    brandService = {
      brand: jasmine.createSpy('brand'),
    }

    apiClientService = {
      myStableService: () => {
        return {
          getMyStableData: jasmine.createSpy('getMyStableData').and.returnValue(of(getStableResponseData)),
          putMyStableData: jasmine.createSpy('putMyStableData').and.returnValue(of(responseData)),
          postMyStableData: jasmine.createSpy('postMyStableData').and.returnValue(of(responseData))
        }
      }
    }

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    }

    snackBar = {
      open: jasmine.createSpy('open'),
    }

    formBuilder = new FormBuilder();

    component = new MystableConfigurationsComponent(brandService, formBuilder, apiClientService, snackBar, globalLoaderService)
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call oninit', () => {
    spyOn(component, 'myStableformData');
    spyOn(component, 'loadIntialData');
    component.ngOnInit();
    expect(component.loadIntialData).toHaveBeenCalled();
  });

  it('should call revert', () => {
    spyOn(component, 'loadIntialData');
    component.revert();
    expect(component.loadIntialData).toHaveBeenCalled();
  });

  it('should return form controls when myStableForm', () => {
    component.myStableForm = formBuilder.group({});
    const controls = component.mystableDataControls;
    expect(controls).toBeDefined();
  });

  it('should call activeStatus if disabled is false', () => {
    component.disabled = false;
    component.activeStatus();
    expect(component.disabled).toBe(true);
  });

  it('should call activeStatus if disabled is true', () => {
    component.disabled = true;
    component.activeStatus();
    expect(component.disabled).toBe(false);
  });

  it('should call carouselStatus if carousel is false', () => {
    component.carousel = false;
    component.carouselStatus();
    expect(component.carousel).toBe(true);
  });

  it('should call carouselStatus if carousel is true', () => {
    component.carousel = true;
    component.carouselStatus();
    expect(component.carousel).toBe(false);
  });

  it('should call antepostStatus if carousel is false', () => {
    component.antepost = false;
    component.antepostStatus();
    expect(component.antepost).toBe(true);
  });

  it('should call antepostStatus if antepost is true', () => {
    component.antepost = true;
    component.antepostStatus();
    expect(component.antepost).toBe(false);
  });

  it('should call myBetsStatus if mybets is true', () => {
    component.mybets = true;
    component.myBetsStatus();
    expect(component.mybets).toBe(false);
  });

  it('should call myBetsStatus if mybets is false', () => {
    component.mybets = false;
    component.myBetsStatus();
    expect(component.mybets).toBe(true);
  });

  it('should call settledbetsStatus if settledBets is true', () => {
    component.settledBets = true;
    component.settledbetsStatus();
    expect(component.settledBets).toBe(false);
  });

  it('should call settledbetsStatus if settledBets is false', () => {
    component.settledBets = false;
    component.settledbetsStatus();
    expect(component.settledBets).toBe(true);
  });

  it('should call crcActiveStatus if crcActive is true', () => {
    component.crcActive = true;
    component.crcActiveStatus();
    expect(component.crcActive).toBe(false);
  });

  it('should call crcActiveStatus if crcActive is false', () => {
    component.crcActive = false;
    component.crcActiveStatus();
    expect(component.crcActive).toBe(true);
  });

  it('should call actionsHandler for save', () => {
    spyOn(component, 'save');
    component.actionsHandler('save');
    expect(component.save).toHaveBeenCalled();
  });

  it('should call actionsHandler for revert', () => {
    spyOn(component, 'revert');
    component.actionsHandler('revert');
    expect(component.revert).toHaveBeenCalled();
  });

  it('should call actionsHandler for log error', () => {
    spyOn(console, 'error');
    component.actionsHandler('unknown');
    expect(console.error).toHaveBeenCalledWith('Unhandled Action');
  });

  it('should show spinner and set isLoading to true', () => {
    component['showHideSpinner'](true);
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component.isLoading).toBe(true);
  });

  it('should hide spinner and set isLoading to false', () => {
    component['showHideSpinner'](false);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.isLoading).toBe(false);
  });

  it('should call myStableformData', () => {
    brandService.brand.and.returnValue('test');
    component.myStableForm = formBuilder.group({});
    component.myStableformData();
    const formControls = component.myStableForm.controls;
    expect(formControls['active'].value).toBe(false);
    expect(formControls['entryPointLabel'].value).toBe('');
    expect(formControls['entryPointLabel'].hasError('required')).toBe(true);
    expect(formControls['entryPointLabel'].hasError('maxLength')).toBe(false);
  });

  it('should set validators in ngAfterViewChecked', () => {
    component.myStableForm = new FormGroup({
      entryPointIcon: new FormControl(),
      editIcon: new FormControl(),
      saveIcon: new FormControl(),
      editNoteIcon: new FormControl(),
      signpostingIcon: new FormControl(),
      notesSignPostingIcon: new FormControl(),
      bookmarkIcon: new FormControl(),
      inProgressIcon: new FormControl(),
      unbookmarkIcon: new FormControl(),
      noHorsesIcon: new FormControl(),
      todayRunningHorsesSvg: new FormControl(),
      crcLogo: new FormControl(),
      crcSignPostingIcon: new FormControl(),
      crcWhiteBookmarkIcon: new FormControl(),
      crcBlackBookmarkIcon: new FormControl(),
    });
    component.ngAfterViewChecked();
    expect(component.myStableForm.get('entryPointIcon')?.hasError('required')).toBe(false);
    expect(component.myStableForm.get('entryPointIcon')?.hasError('minLength')).toBe(false);
    expect(component.myStableForm.get('entryPointIcon')?.hasError('pattern')).toBe(false);
  });

  it('should return mystableDataControls', () => {
    component.myStableForm = formBuilder.group({
      brand: ['test',],
      active: [true,],
    });
    const mystableDataControls = component.mystableDataControls;
    expect(mystableDataControls).toBeDefined();
    expect(mystableDataControls?.brand).toBeDefined();
    expect(mystableDataControls?.brand.value).toBe('test');
    expect(mystableDataControls?.brand.valid).toBe(true);
  });

  it('should call save when myStableData has an id', () => {
    component.myStableData = { id: 1 } as any;
    component.myStableForm = new FormGroup({
      entryPointIcon: new FormControl(),
      editIcon: new FormControl(),
      saveIcon: new FormControl(),
      editNoteIcon: new FormControl(),
      signpostingIcon: new FormControl(),
      notesSignPostingIcon: new FormControl(),
      bookmarkIcon: new FormControl(),
      inProgressIcon: new FormControl(),
      unbookmarkIcon: new FormControl(),
      noHorsesIcon: new FormControl(),
      todayRunningHorsesSvg: new FormControl(),
    });
    component.save();
    expect(component.hideAction).toBe(true);
  });

  it('should call save when no response', () => {
    component.myStableData = { id: 1 } as any;
    component.myStableForm = new FormGroup({
      entryPointIcon: new FormControl(),
      editIcon: new FormControl(),
      saveIcon: new FormControl(),
      editNoteIcon: new FormControl(),
      signpostingIcon: new FormControl(),
      notesSignPostingIcon: new FormControl(),
      bookmarkIcon: new FormControl(),
      inProgressIcon: new FormControl(),
      unbookmarkIcon: new FormControl(),
      noHorsesIcon: new FormControl(),
      todayRunningHorsesSvg: new FormControl(),
    });
    apiClientService.myStableService().putMyStableData.and.returnValue(of(null))
    component.save();
    expect(component.hideAction).toBe(true);
  });

  it('should call save when myStableData has no id', () => {
    component.myStableData = null;
    component.myStableForm = new FormGroup({
      entryPointIcon: new FormControl(),
      editIcon: new FormControl(),
      saveIcon: new FormControl(),
      editNoteIcon: new FormControl(),
      signpostingIcon: new FormControl(),
      notesSignPostingIcon: new FormControl(),
      bookmarkIcon: new FormControl(),
      inProgressIcon: new FormControl(),
      unbookmarkIcon: new FormControl(),
      noHorsesIcon: new FormControl(),
      todayRunningHorsesSvg: new FormControl(),
    });
    component.save();
    expect(component.hideAction).toBe(true);

  });

  it('should load initial data if response', () => {
    component.myStableForm = new FormGroup({
      entryPointIcon: new FormControl(),
      editIcon: new FormControl(),
      saveIcon: new FormControl(),
      editNoteIcon: new FormControl(),
      signpostingIcon: new FormControl(),
      notesSignPostingIcon: new FormControl(),
      bookmarkIcon: new FormControl(),
      inProgressIcon: new FormControl(),
      unbookmarkIcon: new FormControl(),
      noHorsesIcon: new FormControl(),
      todayRunningHorsesSvg: new FormControl(),
    });
    component.loadIntialData();
    expect(component.myStableData.brand).toBe('test');
    expect(component.carousel).toBe(true);
    expect(component.hideAction).toBe(true);
  });

  it('should load initial data if no response', () => {
    component.myStableForm = new FormGroup({
      entryPointIcon: new FormControl(),
      editIcon: new FormControl(),
      saveIcon: new FormControl(),
      editNoteIcon: new FormControl(),
      signpostingIcon: new FormControl(),
      notesSignPostingIcon: new FormControl(),
      bookmarkIcon: new FormControl(),
      inProgressIcon: new FormControl(),
      unbookmarkIcon: new FormControl(),
      noHorsesIcon: new FormControl(),
      todayRunningHorsesSvg: new FormControl(),
    });
    apiClientService.myStableService().getMyStableData.and.returnValue(of(null));
    component.loadIntialData();
    expect(component.myStableData.brand).toBe('test');
    expect(component.carousel).toBe(true);
    expect(component.hideAction).toBe(true);
  });

  it('should set maxlength error if crcLabel > 100', () => {
    component.myStableForm = formBuilder.group({
      crcLabel: ['test',],
    });
    const control = component.myStableForm.get('crcLabel');
    control.setValue('a'.repeat(101)); 
    component.crcLabelValidate();
    expect(control.hasError('maxlength')).toBeTrue();
  });

  it('should set error if crcSaveAllText length> 15', () => {
    component.myStableForm = formBuilder.group({
      crcSaveAllText: ['test',],
    });
    const crcSaveAllTextControl = component.myStableForm.get('crcSaveAllText');
    crcSaveAllTextControl?.setValue('text longer than 15 characters');
    component.crcSaveAllTextValidate();
    expect(crcSaveAllTextControl?.hasError('maxlength')).toBeTrue();
  });

  it('should set error if crcGotoRacingClubText > 30', () => {
    component.myStableForm = formBuilder.group({
      crcGotoRacingClubText: ['test',],
    }); 
    const crcGotoRacingClubTextControl = component.myStableForm.get('crcGotoRacingClubText');
    crcGotoRacingClubTextControl?.setValue('hello hello sample text longer than 30 characters');
    component.crcGotoRacingClubTextValidate();
    expect(crcGotoRacingClubTextControl?.hasError('maxlength')).toBeTrue();
  });

  it('should set error if crcGotoRacingClubUrl> 100', () => {
    component.myStableForm = formBuilder.group({
      crcGotoRacingClubUrl: ['abc.com',],
    }); 
    const crcGotoRacingClubUrlControl = component.myStableForm.get('crcGotoRacingClubUrl');
    crcGotoRacingClubUrlControl?.setValue('https://example.com/' + 'a'.repeat(95)); 
    component.crcGotoRacingClubUrlValidate();
    expect(crcGotoRacingClubUrlControl?.hasError('maxlength')).toBeTrue();
  });

  it('should create the form controls when brand is Coral', () => {
    brandService.brand = 'bma';
        component.myStableForm = formBuilder.group({
      crcActive: [false],
      crcLabel: ['abc.com',],
      crcSaveAllText: ['abc.com',],
      crcGotoRacingClubText: ['abc.com',],
      crcGotoRacingClubUrl: ['abc.com',],
    });
    component.ngOnInit();
    expect(component.isCoral).toBeTruthy();
    expect(component.myStableForm.get('crcActive')).toBeTruthy();
    expect(component.myStableForm.get('crcLabel')).toBeTruthy();
    expect(component.myStableForm.get('crcSaveAllText')).toBeTruthy();
    expect(component.myStableForm.get('crcGotoRacingClubText')).toBeTruthy();
    expect(component.myStableForm.get('crcGotoRacingClubUrl')).toBeTruthy();
  });

  it('should not create the form controls when brand is not Coral', () => {
    brandService.brand = 'lads';
    component.ngOnInit();
    expect(component.isCoral).toBeFalsy();
    expect(component.myStableForm.get('crcActive')).toBeNull();
    expect(component.myStableForm.get('crcLabel')).toBeNull();
    expect(component.myStableForm.get('crcSaveAllText')).toBeNull();
    expect(component.myStableForm.get('crcGotoRacingClubText')).toBeNull();
    expect(component.myStableForm.get('crcGotoRacingClubUrl')).toBeNull();
  });

});
