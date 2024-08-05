import { MarketSelectorCreateComponent } from './market-selector-create.component';
import { MarketSelector } from '@app/client/private/models/marketselector.model';
import { Observable } from 'rxjs/Observable';
import { fakeAsync, tick } from '@angular/core/testing';

describe('MarketSelectorCreateComponent', () => {
  let component: MarketSelectorCreateComponent;
  let dialogRef;
  let brandService;
  let apiClientService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    brandService = {
      brand: 'Test Brand'
    };
    apiClientService = {
      marketSelector: jasmine.createSpy('marketSelector').and.returnValue({
        getUsedMarketTemplateNames: jasmine.createSpy('getUsedMarketTemplateNames').and.returnValue(Observable.of(['a', 'b']))
      })
    };

    component = new MarketSelectorCreateComponent(
      dialogRef,
      apiClientService,
      brandService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should create market selector object', () => {
    component.ngOnInit();
    const expectResult = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: brandService.brand,

      title: '',
      templateMarketName: '',
      header: null,
      headerStr: '',
      sortOrder: 0
    };
    expect(component.marketSelector).toEqual(expectResult);
    expect(component.form).toBeTruthy();
  });

  it('#availableMarketTemplateNames should get used templateMarketNames and exclude them from dropdown box', () => {
    const compStub = {
      marketTemplateNames: ['a', 'b', 'c'],
      apiClientService: apiClientService,
      allUsedTemplateNames: []
    };
    component['availableMarketTemplateNames'].call(compStub);
    expect(apiClientService.marketSelector().getUsedMarketTemplateNames).toHaveBeenCalled();
    expect(compStub.marketTemplateNames).toEqual(['c']);
    expect(compStub.allUsedTemplateNames).toEqual(['a', 'b']);
  });

  it('#getMarketSelector should get marketSelector from form', () => {
    component.marketSelector = {} as any;
    component.form = {
      value: {
        title: 'Test1 title',
        templateMarketName: 'tmpl market name1',
        headers: 'h1, h2, h3'
      }
    } as any;

    const expectedResult: MarketSelector = {
      title: 'Test1 title',
      templateMarketName: 'tmpl market name1',
      header: ['h1', 'h2', 'h3']
    } as any;

    expect(component.getMarketSelector()).toEqual(expectedResult);

    component.form.value.headers = '';
    expectedResult.header = null;
    expect(component.getMarketSelector()).toEqual(expectedResult);
  });

  it('#closeDialog should call dialogRef.close', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });

  it('#checkTemplateNameFree should check if entered template name isnt used', () => {
    const compStub = {
      marketSelector: {
        templateMarketName: 'a'
      },
      allUsedTemplateNames: ['a', 'b', 'c'],
      isTemplateNameFree: true
    };
    component['checkTemplateNameFree'].call(compStub);
    expect(compStub.isTemplateNameFree).toBe(false);
    compStub.marketSelector.templateMarketName = 'f';
    component['checkTemplateNameFree'].call(compStub);
    expect(compStub.isTemplateNameFree).toBe(true);
  });

  it('#isTemplateNameValid should test delay on function call', fakeAsync(() => {
    spyOn<any>(component, 'checkTemplateNameFree');
    component.isTemplateNameValid();
    expect(component['checkTemplateNameFree']).toHaveBeenCalledTimes(0);
    tick(300);
    expect(component['checkTemplateNameFree']).toHaveBeenCalled();
  }));

  it('isValidHeaders should validate header string', () => {
    component.form = {
      value: {
        headers: 'h1, h2, h3'
      }
    } as any;
    expect(component.isValidHeaders()).toBeTruthy();

    component.form.value.headers = 'h1,, h3';
    expect(component.isValidHeaders()).toBeFalsy();

    component.form.value.headers = 'h1, h2, h3, h4';
    expect(component.isValidHeaders()).toBeFalsy();

    component.form.value.headers = undefined;
    expect(component.isValidHeaders()).toBeTruthy();

    component.form.value.headers = '';
    expect(component.isValidHeaders()).toBeTruthy();
  });

  it('#isMarketSelectorValid should validate form', () => {
    spyOn(component, 'isValidHeaders').and.returnValue(true);
    component.form = {
      valid: true
    } as any;

    expect(component.isMarketSelectorValid()).toBeTruthy();

    component.form = {
      valid: false
    } as any;
    expect(component.isMarketSelectorValid()).toBeFalsy();
  });
});
