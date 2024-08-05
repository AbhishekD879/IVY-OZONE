import { of } from 'rxjs/observable/of';
import { fakeAsync, tick } from '@angular/core/testing';

import { IMAGE_MANAGER_ROUTES } from '@app/image-manager/constants/image-manager.constant';
import { DetailsPageComponent } from '@app/image-manager/details-page/details-page.component';

describe('DetailsPageComponent', () => {
  let component: DetailsPageComponent;

  let
    activatedRoute,
    locationService,
    dialogService,
    globalLoaderService,
    imageManagerService,
    router;

  beforeEach(() => {
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue('abc')
        }
      }
    };
    locationService = {
      path: jasmine.createSpy('path').and.returnValue('/foo')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(opt => {
        if (opt.closeCallback) {
          opt.closeCallback();
        }
      })
    };
    globalLoaderService = jasmine.createSpyObj(['showLoader', 'hideLoader']);
    imageManagerService = {
      getSpriteList: jasmine.createSpy('getSpriteList').and.returnValue(of([])),
      getSingleImage: jasmine.createSpy('getSingleImage').and.returnValue(of({})),
      sendImageData: jasmine.createSpy('sendImageData').and.returnValue(of('abcd')),
      deleteAndOpenList: jasmine.createSpy('deleteAndOpenList')
    };
    router = jasmine.createSpyObj(['navigate']);

    component = new DetailsPageComponent(
      activatedRoute,
      locationService,
      dialogService,
      globalLoaderService,
      imageManagerService,
      router
    );
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  describe('ngOnInit', () => {

    it('should get sprite list', () => {
      spyOn(component, 'getOrCreateImage').and.returnValue(of({svgId: ''} as any));
      component.ngOnInit();

      expect(imageManagerService.getSpriteList).toHaveBeenCalled();
    });
  });

  describe('getOrCreateImage', () => {
    beforeEach(() => {
      component.appSprites = ['1', '2'];
    });

    it('should get image data', () => {
      component.getOrCreateImage('123abc');

      expect(imageManagerService.getSingleImage).toHaveBeenCalledWith('123abc');
    });

    it('should return new image data', () => {
      component.getOrCreateImage(undefined).subscribe(res => {
        expect(res).toEqual(jasmine.any(Object));
        expect(imageManagerService.getSingleImage).not.toHaveBeenCalled();
      });
    });
  });

  describe('buildBreadcrumbs', () => {

    it('should build breadcrumbs data (add mode)', () => {
      expect(component.breadcrumbsData).not.toBeDefined();

      component.image = {} as any;
      component.buildBreadcrumbs();

      expect(component.breadcrumbsData).toEqual([
        {
          label: `image manager`,
          url: IMAGE_MANAGER_ROUTES.base
        }, {
          label: 'new image',
          url: '/foo'
        }
      ]);
    });
  });

  describe('validateAndUpdateFileFields', () => {
    let transformNameSpy, validateFileSizeSpy;

    beforeEach(() => {
      transformNameSpy = spyOn(component, 'transformName');
      validateFileSizeSpy = spyOn(component, 'validateFileSize');
    });

    it('should autofill id and run validation', () => {
      component.image = {svgFilename: {}} as any;
      component.validateAndUpdateFileFields({target: {files: [{name: 'fooName', type: 'image/svg'}]}});

      expect(transformNameSpy).toHaveBeenCalledWith('fooName');
      expect(validateFileSizeSpy).toHaveBeenCalledWith({name: 'fooName', type: 'image/svg'});
    });
  });

  describe('validateFileSize', () => {

    it('should add form errors if file size is too big', fakeAsync(() => {
      const setErrorsSpy = jasmine.createSpy('setErrors');
      component.imageForm = {
        controls: {
          originalname: {
            setErrors: setErrorsSpy
          }
        }
      } as any;
      component.validateFileSize({size: 21000} as any);
      tick();

      expect(setErrorsSpy).toHaveBeenCalledWith({'size': true});
    }));
  });

  describe('actionsHandler', () => {

    it('should delegate removing to service', () => {
      component.image = {id: 'abc'} as any;
      component.actionsHandler('remove');

      expect(imageManagerService.deleteAndOpenList).toHaveBeenCalledWith('abc');
    });

    it('should call submit method', () => {
      const submitImageFormSpy = spyOn(component, 'submitImageForm');
      component.actionsHandler('save');

      expect(submitImageFormSpy).toHaveBeenCalled();
    });
  });

  describe('transformName', () => {

    it('should apply transformations', () => {
      expect(component.transformName('Svg-Image #file.svg')).toBe('svg-imagefile');
    });
  });

  describe('submitImageForm', () => {

    beforeEach(() => {
      component.image = {id: 'abc'} as any;
      component.imageForm = {value: {}} as any;
    });

    it('should delegate saving to service', () => {
      component.submitImageForm();

      expect(imageManagerService.sendImageData).toHaveBeenCalledWith('abc', jasmine.any(Object));
    });

    it('should call callback after saving', () => {
      const successfulSaveCallbackSpy = spyOn(component, 'successfulSaveCallback');
      component.submitImageForm();

      expect(successfulSaveCallbackSpy).toHaveBeenCalledWith('abcd');
    });
  });

  describe('successfulSaveCallback', () => {

    beforeEach(() => {
      component.image = {sprite: 'initial'} as any;
    });

    it('should call dialog', () => {
      component.successfulSaveCallback('abc');

      expect(dialogService.showNotificationDialog).toHaveBeenCalled();

      const argOptions = dialogService.showNotificationDialog.calls.argsFor(0)[0];
      expect(argOptions.title).toEqual(jasmine.any(String));
      expect(argOptions.message).toEqual(jasmine.any(String));
      expect(argOptions.message.includes('initial')).toBe(true);
      expect(argOptions.closeCallback).toEqual(jasmine.any(Function));
    });
  });
});
