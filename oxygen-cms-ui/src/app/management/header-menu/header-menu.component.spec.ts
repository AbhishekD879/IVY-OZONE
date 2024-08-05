import { async, ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { HeaderMenuComponent } from './header-menu.component';
import { AuthService } from '@app/auth/auth.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Brand } from '@app/client/private/models';

describe('HeaderMenuComponent', () => {
  let component: HeaderMenuComponent;
  let fixture: ComponentFixture<HeaderMenuComponent>;
  let auth, brandService, route, router;

  const brandList: Brand[] = [
    { id: 1, disabled: true, title: 'bma' },
    { id: 2, disabled: false, title: 'ladbrokes' }
  ] as any;

  beforeEach(async(() => {
    auth = {
      logOut: jasmine.createSpy('logOut')
    };
    brandService = {
      brand: 'ladbrokes'
    };
    route = {
      snapshot: {
        data: {
          mainData: [
            {},
            {
              body: brandList
            }
          ]
        }
      }
    };
    router = {
      navigate: jasmine.createSpy('navigate').and.returnValue(Promise.resolve())
    };

    TestBed.configureTestingModule({
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ],
      declarations: [HeaderMenuComponent],
      providers: [
        { provide: AuthService, useValue: auth },
        { provide: BrandService, useValue: brandService },
        { provide: ActivatedRoute, useValue: route },
        { provide: Router, useValue: router },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HeaderMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should set brandList', () => {
      component.ngOnInit();
      expect(component.brandsList).toEqual([{ id: 2, disabled: false, title: 'ladbrokes' }] as any);
    });

    it('should not set brandList', () => {
      component.brandsList = undefined;
      component['route'] = {
        snapshot: {
          data: {
            mainData: [
              {},
              {}
            ]
          }
        }
      } as any;
      component.ngOnInit();
      expect(component.brandsList).toEqual(undefined);
    });
  });


  describe('#onBrandSelect', () => {
    it('should navigate to home page and set brand', fakeAsync(() => {
      component.onBrandSelect('bma');
      tick();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
      expect(component['brandService'].brand).toEqual('bma');
    }));
    it('should ignore select if brand is not changed', fakeAsync(() => {
      component.onBrandSelect('ladbrokes');
      tick();
      expect(router.navigate).not.toHaveBeenCalled();
      expect(component['brandService'].brand).toEqual('ladbrokes');
    }));
  });

  it('#logPut should log out user', () => {
    component.logOut();
    expect(auth.logOut).toHaveBeenCalledTimes(1);
  });
});
