import { AddNavigationGroupComponent } from '@app/promotions/add-navigation-group/add-navigation-group.component';

describe('AddNavigationGroupComponent', () => {
  let component: AddNavigationGroupComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    brandService = {
      brand: 'bma'
    };
    component = new AddNavigationGroupComponent(dialogRef, brandService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit should initialize newNavigationGroup', () => {
    const mockData = {
      brand: 'bma',
      title: '',
      status: false
    };
    component.ngOnInit();
    expect(component.newNavigationGroup).toEqual(mockData);
  });

  it('should return newNavigationGroup', () => {
    component['getNewNavigationGroup']();
    expect(component.newNavigationGroup).toBeUndefined();
  });

  it('should return false title is not present', () => {
    const valid = component['isValidNavigationGroup']();
    expect(valid).toEqual(true);
  });

  it('should close handler', () => {
    component['closeDialog']();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
