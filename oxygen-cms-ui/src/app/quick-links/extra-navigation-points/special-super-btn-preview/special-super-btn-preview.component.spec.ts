import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SpecialSuperBtnPreviewComponent } from './special-super-btn-preview.component';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { Brand } from '@root/app/app.constants';

describe('SpecialSuperBtnPreviewComponent', () => {
  let component: SpecialSuperBtnPreviewComponent;
  let fixture: ComponentFixture<SpecialSuperBtnPreviewComponent>;
  let brandService: BrandService;

  beforeEach(async () => {
    const brandServiceSpy = jasmine.createSpyObj('BrandService', ['brand']);

    await TestBed.configureTestingModule({
      declarations: [ SpecialSuperBtnPreviewComponent ],
      providers: [
        { provide: BrandService, useValue: brandServiceSpy }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpecialSuperBtnPreviewComponent);
    component = fixture.componentInstance;
    brandService = TestBed.inject(BrandService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set isBrandLads to true if brand is LADBROKES', () => {
    brandService.brand = Brand.LADBROKES;
    component.ngOnInit();
    expect(component.isBrandLads).toBeTrue();
  });

  it('should set isBrandLads to false if brand is not LADBROKES', () => {
    brandService.brand = 'someOtherBrand';
    component.ngOnInit();
    expect(component.isBrandLads).toBeFalse();
  });

  it('should set class properties based on the condition in ngDoCheck', () => {
    component.titleOptions = [{ key: 'bgImage', value: 'testValue' }];
    component.bgImage = 'testImage';
    component.isBrandLads = true;

    component.ngDoCheck();

    expect(component.rightBtnClass).toBe('bg-align-right-theme1-btn');
    expect(component.rightTopClass).toBe('row bg-align-right-theme1');
  });

  it('should set defaultFormConfig correctly in ngDoCheck', () => {
    const titleOption = { key: 'bgImage', value: 'testValue' };
    component.titleOptions = [titleOption];
    
    component.ngDoCheck();

    expect(component.defaultFormConfig).toEqual(titleOption);
  });
});
