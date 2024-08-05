import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { MarketSelectorEditComponent } from './market-selector-edit.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { MarketSelectorExt } from '@app/client/private/models/marketselector.model';
import { fakeAsync, tick } from '@angular/core/testing';

describe('MarketSelectorEditComponent', () => {
  let component: MarketSelectorEditComponent;
  let marketSelector: MarketSelectorExt;

  let activatedRoute: Partial<ActivatedRoute>;
  let apiClientService;
  let dialogService: Partial<DialogService>;
  let globalLoaderService: Partial<GlobalLoaderService>;
  let router: Partial<Router>;

  beforeEach(() => {
    router = {
      navigate: jasmine.createSpy('navigate')
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };

    marketSelector = {
      id: '465',
      title: 'Title1',
      header: ['head1', 'head2'],
      headerStr: 'head1, head2'
    } as any;

    activatedRoute = {
      params: Observable.of({ id: '465' })
    };

    apiClientService = {
      marketSelector: jasmine.createSpy('marketSelector').and.returnValue({
        getById: jasmine.createSpy('getById').and.returnValue(Observable.of({ body: marketSelector })),
        edit: jasmine.createSpy('edit').and.returnValue(Observable.of({ body: marketSelector })),
        delete: jasmine.createSpy('delete').and.returnValue(Observable.of({})),
        getUsedMarketTemplateNames: jasmine.createSpy('getUsedMarketTemplateNames').and.returnValue(Observable.of(['a', 'b']))
      })
    };

    component = new MarketSelectorEditComponent(
      router as any,
      activatedRoute as any,
      apiClientService as any,
      dialogService as any,
      globalLoaderService as any
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should call #loadInitData', () => {
    spyOn(component, 'loadInitData');
    component.ngOnInit();
    expect(component.loadInitData).toHaveBeenCalled();
  });

  it('#loadInitData should get market selector by id', () => {
    component['setBreadcrumbsData'] = jasmine.createSpy('setBreadcrumbsData');
    spyOn<any>(component, 'availableMarketTemplateNames');
    component.loadInitData();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().getById).toHaveBeenCalledWith('465');
    expect(component.marketSelector).toEqual(marketSelector);
    expect(component['availableMarketTemplateNames']).toHaveBeenCalled();
    expect(component['setBreadcrumbsData']).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#loadInitData should handle error response', () => {
    apiClientService.marketSelector().getById.and.returnValue(Observable.throw({}));
    component['setBreadcrumbsData'] = jasmine.createSpy('setBreadcrumbsData');
    component.loadInitData();

    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().getById).toHaveBeenCalledWith('465');
    expect(component['setBreadcrumbsData']).not.toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#availableMarketTemplateNames should get used templateMarketNames and exclude them from dropdown box', () => {
    const compStub = {
      marketTemplateNames: ['a', 'b', 'c'],
      marketSelector: {
        templateMarketName: 'b'
      },
      apiClientService: apiClientService,
      allUsedTemplateNames: null
    };
    component['availableMarketTemplateNames'].call(compStub);
    expect(apiClientService.marketSelector().getUsedMarketTemplateNames).toHaveBeenCalled();
    expect(compStub.marketTemplateNames).toEqual(['c', 'b']);
    expect(compStub.allUsedTemplateNames).toEqual(['a']);
  });

  it('#setBreadcrumbsData should set breadcrumbs', () => {
    component.marketSelector = marketSelector;
    component['setBreadcrumbsData']();

    const expectResult = [
      { label: 'Coupon Market Selectors', url: '/football-coupon/coupon-market-selectors' },
      { label: 'Title1', url: '/football-coupon/coupon-market-selectors/465' }
    ];

    expect(component.breadcrumbsData).toEqual(expectResult);
  });

  it('#save should send request', () => {
    component.actionButtons = jasmine.createSpyObj([
      'extendCollection'
    ]);
    component.marketSelector = marketSelector;
    component.save();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().edit).toHaveBeenCalledWith(component.marketSelector);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.marketSelector);
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Coupon Market Selector',
      message: 'Market Selector is Saved.'
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#save should handle error response', () => {
    apiClientService.marketSelector().edit.and.returnValue(Observable.throw({}));
    component.actionButtons = jasmine.createSpyObj([
      'extendCollection'
    ]);
    component.marketSelector = marketSelector;
    component.save();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().edit).toHaveBeenCalledWith(component.marketSelector);
    expect(component.actionButtons.extendCollection).not.toHaveBeenCalledWith();
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#revert should call #loadInitData', () => {
    spyOn(component, 'loadInitData');
    component.revert();
    expect(component.loadInitData).toHaveBeenCalled();
  });

  it('#remove should send request and redirect user', () => {
    component.marketSelector = marketSelector;
    component.remove();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().delete).toHaveBeenCalledWith(component.marketSelector.id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['/football-coupon/coupon-market-selectors/']);
  });

  it('#remove should handle request error', () => {
    apiClientService.marketSelector().delete.and.returnValue(Observable.throw({}));
    component.marketSelector = marketSelector;
    component.remove();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().delete).toHaveBeenCalledWith(component.marketSelector.id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(router.navigate).not.toHaveBeenCalledWith(['/football-coupon/coupon-market-selectors/']);
  });

  it('#actionsHandler should call correct method', () => {
    spyOn(component, 'remove');
    spyOn(component, 'save');
    spyOn(component, 'revert');

    component.actionsHandler('remove');
    expect(component.remove).toHaveBeenCalled();

    component.actionsHandler('save');
    expect(component.save).toHaveBeenCalled();

    component.actionsHandler('revert');
    expect(component.revert).toHaveBeenCalled();
  });

  it('#actionsHandler should do nothing if wrong event', () => {
    spyOn(component, 'remove');
    spyOn(component, 'save');
    spyOn(component, 'revert');

    component.actionsHandler('test');
    expect(component.remove).not.toHaveBeenCalled();
    expect(component.save).not.toHaveBeenCalled();
    expect(component.revert).not.toHaveBeenCalled();
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

  it('#isValidHeaders should validate headers', () => {
    expect(component.isValidHeaders('h1, h2, h3')).toBeTruthy();
    expect(component.isValidHeaders('h1,, h3')).toBeFalsy();
    expect(component.isValidHeaders('h1, h2, h3, h4')).toBeFalsy();
    expect(component.isValidHeaders(undefined)).toBeTruthy();
    expect(component.isValidHeaders('')).toBeTruthy();
  });

  it('#isValidForm should validate form and return boolean', () => {
    let market: MarketSelectorExt;
    expect(component.isValidModel(market)).toBeFalsy();

    market = { title: 'title2', templateMarketName: '', headerStr: 'h1, h2' } as any;
    expect(component.isValidModel(market)).toBeFalsy();

    market = { title: 'title2', templateMarketName: 'templ name', headerStr: 'h1, h2' } as any;
    expect(component.isValidModel(market)).toBeTruthy();

    market = { templateMarketName: 'templ name', headerStr: 'h1, h2' } as any;
    expect(component.isValidModel(market)).toBeTruthy();
  });
});
