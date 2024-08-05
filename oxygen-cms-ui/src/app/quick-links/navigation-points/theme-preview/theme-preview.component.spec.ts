import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ThemePreviewComponent } from './theme-preview.component';

describe('ThemePreviewComponent', () => {
  let component: ThemePreviewComponent;
  let fixture: ComponentFixture<ThemePreviewComponent>;
  let brandServiceRef: Partial<BrandService>;

  beforeEach(async(() => {
    brandServiceRef = {
      brand: 'ladbrokes'
    };
    TestBed.configureTestingModule({
      declarations: [ThemePreviewComponent],
      providers: [
        { provide: BrandService, useValue: brandServiceRef }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ThemePreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create component Theme Preview Component', () => {
    expect(component).toBeTruthy();
  });

  it('should set isBrandLads variable to be true if the brand is "LADBROKES"', () => {
    expect(component.isBrandLads).toBeTrue();
  });

  it('should set isBrandLads to false if the brand is not "CORAL"', () => {
    brandServiceRef.brand = 'CORAL';
    fixture.detectChanges();
    expect(component.isBrandLads).toBeFalse();
  });

  it('should initialize the component properties during componenet loading', () => {
    expect(component.themeValueFromParent).toBeUndefined();
    expect(component.alignmentFromParent).toBeUndefined();
    expect(component.titleOptionsFromParent).toBeUndefined();
    expect(component.rightTopClass).toBe('');
    expect(component.rightBtnClass).toBe('');
    expect(component.centerTopClass).toBe('');
    expect(component.centerBtnClass).toBe('');
    expect(component.defaultFormConfig).toBeUndefined();
  });

  describe('ngDoCheck', () => {
    beforeEach(() => {
      component.titleOptions = [
      {
        key: 'center', value: 'Center Alignment', config: {
          title: { maxLength: 40 },
          description: { maxLength: 65 }
        }
      },
      {
        key: 'right', value: 'Right Alignment', config: {
          title: { maxLength: 12 },
          description: { maxLength: 25 },
          shortDescription: { coral: { maxLength: 38 }, lads: { maxLength: 42 } }
        }
      }
    ];
      component.alignment = 'center';
      component.themeValue = 'theme_1';
    });

    it('should update the component properties', () => {
      component.ngDoCheck();
      expect(component.titleOptionsFromParent).toEqual(component.titleOptions);
      expect(component.alignmentFromParent).toEqual(component.alignment);
      expect(component.themeValueFromParent).toEqual(component.themeValue);
      expect(component.defaultFormConfig).toEqual({
        key: 'center', value: 'Center Alignment', config: {
          title: { maxLength: 40 },
          description: { maxLength: 65 }
        }
      });
    });

    it('should set the CSS classes for different cases, LADBROKES and aligment as center with different themes', () => {
      component.isBrandLads = true;
      component.alignment = 'center';
      component.themeValue = 'theme_1';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme1-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme1-top');

      component.isBrandLads = true;
      component.alignment = 'center';
      component.themeValue = 'theme_2';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme2-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme2-top');

      component.isBrandLads = true;
      component.alignment = 'center';
      component.themeValue = 'theme_3';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme3-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme3-top');

      component.isBrandLads = true;
      component.alignment = 'center';
      component.themeValue = 'theme_4';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme4-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme4-top');

    });

    it('should set the CSS classes for different cases, LADBROKES and aligment as Right with different themes', () => {
      component.isBrandLads = true;
      component.alignment = 'right';
      component.themeValue = 'theme_1';
  
      component.ngDoCheck();

      
      expect(component.centerBtnClass).toBe('right-theme1-btn');
      expect(component.centerTopClass).toBe('row right-theme1-top');

      component.isBrandLads = true;
      component.alignment = 'right';
      component.themeValue = 'theme_2';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme2-btn');
      expect(component.centerTopClass).toBe('row right-theme2-top');

      component.isBrandLads = true;
      component.alignment = 'right';
      component.themeValue = 'theme_3';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme3-btn');
      expect(component.centerTopClass).toBe('row right-theme3-top');

      component.isBrandLads = true;
      component.alignment = 'right';
      component.themeValue = 'theme_4';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme4-btn');
      expect(component.centerTopClass).toBe('row right-theme4-top');

    });

    it('should set the CSS classes for different cases, CORAL and aligment as center with different themes', () => {
      component.isBrandLads = false;
      component.alignment = 'center';
      component.themeValue = 'theme_1';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme1-corl-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme1-corl-top');

      component.isBrandLads = false;
      component.alignment = 'center';
      component.themeValue = 'theme_2';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme2-corl-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme2-corl-top');

      component.isBrandLads = false;
      component.alignment = 'center';
      component.themeValue = 'theme_3';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme3-corl-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme3-corl-top');

      component.isBrandLads = false;
      component.alignment = 'center';
      component.themeValue = 'theme_4';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme4-corl-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme4-corl-top');

      component.isBrandLads = false;
      component.alignment = 'center';
      component.themeValue = 'theme_5';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme5-corl-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme5-corl-top');

      component.isBrandLads = false;
      component.alignment = 'center';
      component.themeValue = 'theme_6';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('center-theme6-corl-btn text-center');
      expect(component.centerTopClass).toBe('row center-theme6-corl-top');

    });

    it('should set the CSS classes for different cases, CORAL and aligment as right with different themes', () => {
      component.isBrandLads = false;
      component.alignment = 'right';
      component.themeValue = 'theme_1';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme1-corl-btn');
      expect(component.centerTopClass).toBe('row right-theme1-corl-top');

      component.isBrandLads = false;
      component.alignment = 'right';
      component.themeValue = 'theme_2';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme2-corl-btn');
      expect(component.centerTopClass).toBe('row right-theme2-corl-top');

      component.isBrandLads = false;
      component.alignment = 'right';
      component.themeValue = 'theme_3';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme3-corl-btn');
      expect(component.centerTopClass).toBe('row right-theme3-corl-top');

      component.isBrandLads = false;
      component.alignment = 'right';
      component.themeValue = 'theme_4';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme3-corl-btn');
      expect(component.centerTopClass).toBe('row right-theme3-corl-top');

      component.isBrandLads = false;
      component.alignment = 'right';
      component.themeValue = 'theme_5';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme5-corl-btn');
      expect(component.centerTopClass).toBe('row right-theme5-corl-top');

      component.isBrandLads = false;
      component.alignment = 'right';
      component.themeValue = 'theme_6';
  
      component.ngDoCheck();

      expect(component.centerBtnClass).toBe('right-theme6-corl-btn');
      expect(component.centerTopClass).toBe('row right-theme6-corl-top');

    });
  });
});
