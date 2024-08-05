import { PAY_TABLE_DATA } from '@app/five-a-side-showdown/components/pay-table/pay-table.component.mock';
import { AddEditPrizeComponent } from '@app/five-a-side-showdown/components/add-edit-prize/add-edit-prize.component';

describe('AddEditPrizeComponent', () => {
  let component: AddEditPrizeComponent;
  let dialogRef;
  let dialog;
  let dialogService;
  let brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    dialog = {
      title: 'Add New Prize',
      data: {
      } as any
    };
    brandService = {
      brand: 'bma'
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(opt => {
        if (opt.closeCallback) {
          opt.closeCallback();
        }
      })
    };
    component = new AddEditPrizeComponent(dialogRef, dialogService, brandService, dialog);
    component.prizeForm = {
      form: {
        markAsDirty: jasmine.createSpy('markAsDirty')
      }
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit should initilize title', () => {
    spyOn(component as any, 'validateSvgFile');
    component.ngOnInit();
    expect(component.title).toBe('Add New Prize');
  });

  describe('#validateAndUpdateFileFields', () => {
    let transformNameSpy;

    beforeEach(() => {
      transformNameSpy = spyOn(component as any, 'transformName');
    });

    it('should validate file size if it matches the supported type (Case 1)', () => {
      component.prize = PAY_TABLE_DATA[1] as any;
      const event = {target: {files: [{name: 'fooName', type: 'image/svg'}]}} as any;
      component.validateAndUpdateFileFields(event, 'icon');

      expect(transformNameSpy).toHaveBeenCalledWith('fooName');
    });

    it('should not validate file size if it does not matche the supported type', () => {
      component.prize = PAY_TABLE_DATA[0] as any;
      const event = {target: {files: [{name: 'fooName', type: 'image/png'}]}} as any;
      component.validateAndUpdateFileFields(event, 'icon');

      expect(transformNameSpy).not.toHaveBeenCalled();
    });

    it('should not proceed further, if there is no file', () => {
      const event = {target: {files: []}} as any;
      component.validateAndUpdateFileFields(event, 'icon');

      expect(transformNameSpy).not.toHaveBeenCalled();
    });
  });

  it('should return prize when savechanges is called', () => {
    component.prize = PAY_TABLE_DATA[2] as any;
    const response = component.saveChanges();
    expect(response).not.toBeNull();
  });

  it('should close dialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
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

  describe('#transformName', () => {
    it('should apply transformations', () => {
      expect(component['transformName']('Svg-Image #file.svg')).toBe('svg-imagefile');
    });
    it('should apply transformations (Case 2)', () => {
      expect(component['transformName']('Svg-Image #file')).toBe('svg-imagefile');
    });
  });

  describe('#updatePrizeImages', () => {
    it('should update prize images when fieldName is icon', () => {
      component.prize = PAY_TABLE_DATA;
      component['updatePrizeImages']({name: 'icon.svg'} as any, 'icon');
      expect(component.prize.prizeIcon).not.toBeNull();
    });
    it('should update prize images when fieldName is signposting', () => {
      component.prize = PAY_TABLE_DATA;
      component['updatePrizeImages']({name: 'signposting.svg'} as any, 'signPosting');
      expect(component.prize.prizeIcon).not.toBeNull();
    });
  });

  describe('#setSVGImage', () => {
    it('should not set if no dialog data', () => {
      component.prize = {
        icon: null,
        signPosting: null
      } as any;
      dialog.data = null;
      component['setSVGImage']('prizeIcon', 'icon');
      expect(component.prize.prizeIcon).toBeUndefined();
    });
    it('should not set if no dialog data(case 2)', () => {
      component.prize = {
        icon: null,
        signPosting: null
      } as any;
      dialog.data = {
        icon: null
      };
      component['setSVGImage']('prizeIcon', 'icon');
      expect(component.prize.prizeIcon).toBeUndefined();
    });
    it('should not set if no dialog data(case 3)', () => {
      component.prize = {
        icon: null,
        signPosting: null
      } as any;
      dialog.data = {
        icon: {
          filename: null
        }
      };
      component['setSVGImage']('prizeIcon', 'icon');
      expect(component.prize.prizeIcon).toBeUndefined();
    });
    it('should not set if no dialog data(case 3)', () => {
      component.prize = {
        icon: null,
        signPosting: null
      } as any;
      dialog.data = {
        icon: {
          filename: 'ping.svg'
        }
      };
      component['setSVGImage']('prizeIcon', 'icon');
      expect(component.prize.prizeIcon).toEqual({
        filename: 'ping.svg'
      } as any);
    });
  });
  describe('#removeImage', () => {
    it('should remove icon svg file', () => {
      const fieldName = 'icon';
      component.iconSvgFileInput = {
        nativeElement : {
          value: 'file'
        }
      } as any;
      component.prize = {...PAY_TABLE_DATA[1]} as any;
      component.removeImage(fieldName);
      expect(component.iconSvgFileInput.nativeElement.value).toBe('');
    });
    it('should remove signposting svg file', () => {
      const fieldName = 'signPosting';
      component.signpostingSvgFileInput = {
        nativeElement : {
          value: 'file'
        }
      } as any;
      component.prize = {...PAY_TABLE_DATA[1]} as any;
      component.removeImage(fieldName);
      expect(component.signpostingSvgFileInput.nativeElement.value).toBe('');
    });
  });
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
  describe('#validateSvgFile', () => {
    it('should set default properties, if data is null', () => {
      component.prize = { icon: null} as any;
      component['validateSvgFile']('icon');
      expect(component.prize.icon).toEqual({
        originalname: ''
      } as any);
    });
    it('should not set default properties, if data exists', () => {
      component.prize = { icon: { originalName: 'welcome'}} as any;
      component['validateSvgFile']('icon');
      expect(component.prize.icon).not.toBeNull();
    });
  });

  describe('#handleWhiteSpaces', () => {
    it('should remove spaces for numberOfEntries field if isEntries is true', () => {
      component.prize = { numberOfEntries: 'test abc'} as any;
      component['handleWhiteSpaces'](true);
      expect(component.prize.numberOfEntries).toEqual('testabc');
    });
    it('should remove spaces for percentageOfField field if isEntries is true', () => {
      component.prize = { percentageOfField: 'test bcd '} as any;
      component['handleWhiteSpaces'](false);
      expect(component.prize.percentageOfField).toEqual('testbcd');
    });
  });
});
