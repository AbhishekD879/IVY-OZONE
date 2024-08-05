
import {  Observable,  throwError } from "rxjs";
import { ExtraNavigationPointsApiService } from "./extra-navigation-points-api.service";
import { fakeAsync } from "@angular/core/testing";
describe('ExtraNavigationPointsApiService', () => {
  let service,
    globalLoaderService, 
    apiClientService;
  
  beforeEach(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')

    };
    apiClientService = {
      competitions:jasmine.createSpy('competitions').and.returnValue({
        findAllCompetitions:jasmine.createSpy('findAllCompetitions').and.returnValue([{name:'c1'},{name:'c2'}]),
        getCompetitions:jasmine.createSpy('getCompetitions').and.returnValue({name:'c1'})
      }),
      sportCategoriesService:jasmine.createSpy('sportCategoriesService').and.returnValue({
        getSportCategories:jasmine.createSpy('getSportCategories').and.returnValue([{categoryId:16},{categoryId:123}])      }),
      moduleRibbonTab:jasmine.createSpy('moduleRibbonTab').and.returnValue({
        getByBrand:jasmine.createSpy('getByBrand').and.returnValue([{internalId:'123'},{internalId:'12'}])
      }),
      extraNavigationPoints: jasmine.createSpy('extraNavigationPoints').and.returnValue({
        reorderNavigationPoints: jasmine.createSpy('reorderNavigationPoints').and.returnValue({ 'id': 123 }),
        update: jasmine.createSpy('update').and.returnValue({ 'id': 123 }),
        delete: jasmine.createSpy('delete').and.returnValue({}),
        save: jasmine.createSpy('save').and.returnValue({ 'id': 123 }),
        findOne: jasmine.createSpy('findOne').and.returnValue({ 'id': 123 }),
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue([{ 'id': 123 }, { 'id': 12 }]),
        getList:jasmine.createSpy('getList').and.returnValue({categoryId:'123'})
      })
    }; 

    service = new ExtraNavigationPointsApiService(
      globalLoaderService,
      apiClientService
    );
  });

  it('should be created', () => {
    expect(service).toBeDefined();
  });

  it('getSingleNavigationPoint', () => {
    spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
    const id = '1';
    service.getSingleNavigationPoint(id);
    expect(apiClientService.extraNavigationPoints).toHaveBeenCalled();
  });

  it('deleteNavigationPoint', () => {
    const id = '1';
    spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
    service.deleteNavigationPoint(id);
    expect(apiClientService.extraNavigationPoints).toHaveBeenCalled();
  });

  it('reorderNavigationPoints', () => {
    const order = { id: '1', order: ['1', '2', '3'] };
    service.reorderNavigationPoints(order);
    expect(apiClientService.extraNavigationPoints).toHaveBeenCalled();
  });

  it('createNavigationPoint', () => {
    spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
    const n1 = { id: '123' };
    service.createNavigationPoint(n1);
    expect(apiClientService.extraNavigationPoints).toHaveBeenCalled();
  });

  it('getNavigationPointsList', () => {
    spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
  
    service.getNavigationPointsList();
    expect(apiClientService.extraNavigationPoints).toHaveBeenCalled();
  });   
  
  it('getSportCategories', () => {
    spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
   
    service.getSportCategories();
    expect(apiClientService.sportCategoriesService).toHaveBeenCalled();
  }); 
  it('getCompetitions', () => {
    spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
   
    service.getCompetitions();
    expect(apiClientService.competitions).toHaveBeenCalled();
  });
it('updateNavigationPoint',()=>
{
  spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
  const id = '123';
  service.updateNavigationPoint(id);
  
  expect(apiClientService.extraNavigationPoints).toHaveBeenCalled();

});

it('getModuleRibbonTabs',()=>
{
  spyOn(service as any, 'wrappedObservable').and.returnValue({ 'id': 123 });
  service.getModuleRibbonTabs();

  expect(apiClientService.moduleRibbonTab).toHaveBeenCalled();
});

it('filterSportCategory',()=>{
  const c1={key:'1',showInAZ:true,targetUri:'lotto',categoryId:16};
  
  expect(service.filterSportCategory(c1)).toBeFalsy();
});

it('getLandingPages',()=>

{
  const a=[{ id: '123',title:'b' },{ id: '12',title:'a' },{ id: 1,title:'c' }];
  const b=[{ 'id': 123,imageTitle:'titleB' },{ 'id': 123,imageTitle:'titleA' },{ 'id': 123,imageTitle:'titleC' }];
  const c=[{ 'id': 123 ,name:'nameB'},{ 'id': 123 ,name:'nameA'},{ 'id': 123 ,name:'name'}];
  spyOn(service as any, 'getModuleRibbonTabs').and.returnValue([{ id: '123',title:'b' },{ id: '12',title:'a' },{ id: 1,title:'c' }]);
  spyOn(service as any, 'getSportCategories').and.returnValue([{ 'id': 123,imageTitle:'titleB' },{ 'id': 123,imageTitle:'titleA' },{ 'id': 123,imageTitle:'titleC' }]);
  spyOn(service as any, 'getCompetitions').and.returnValue([{ 'id': 123 ,name:'nameB'},{ 'id': 123 ,name:'nameA'},{ 'id': 123 ,name:'name'}]);
  service.getLandingPages(a,b,c);
  expect(service.getModuleRibbonTabs).toHaveBeenCalled();
});

const mockhttp = {
};

it(' wrappedObservable hide loader to havebeen called', fakeAsync(() => {
  service.wrappedObservable(throwError(({ res: mockhttp }))).subscribe(
    );
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
}));

it('wrappedObservable',()=>
{
  service.wrappedObservable(Observable.of({ }));
  expect(globalLoaderService.showLoader).toHaveBeenCalled();
})

});
