import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';

import { HomePageComponent } from './home.page.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { Observable } from 'rxjs/Observable';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { AppConstants } from '@app/app.constants';

describe('HomePageComponent', () => {
  let component: HomePageComponent;
  let fixture: ComponentFixture<HomePageComponent>;
  let matSnackBar: Partial<MatSnackBar>,
    sportsModulesService: Partial<SportsModulesService>;

  const modules: SportsModule[] = [
    { id: '5c0a91c3c9e77c0001f54a1c' }
  ] as any;

  beforeEach(async(() => {
    matSnackBar = {
      open: jasmine.createSpy('open')
    };
    sportsModulesService = {
      getModulesData: jasmine.createSpy('getModulesData').and.returnValue(Observable.of(modules)),
      updateModulesOrder: jasmine.createSpy('updateModulesOrder').and.returnValue(Observable.of({}))
    };

    TestBed.configureTestingModule({
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ],
      declarations: [HomePageComponent],
      providers: [
        { provide: MatSnackBar, useValue: matSnackBar },
        { provide: SportsModulesService, useValue: sportsModulesService }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HomePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get all modules', () => {
    component.ngOnInit();
    expect(sportsModulesService.getModulesData).toHaveBeenCalledWith('sport', 0);
    expect(component.sportModules).toEqual([{ id: '5c0a91c3c9e77c0001f54a1c' } as any]);
  });

  it('#reorderHandler should save new order', () => {
    const newOrder = {
      'order': ['5c0a91c3c9e77c0001f54a1c', '5c0a5fa1c9e77c00013dd199', '5ab8c57bc9e77c000158a9bf'],
      'id': '5bd70b89c9e77c000101d57a'
    };

    component.reorderHandler(newOrder);
    expect(sportsModulesService.updateModulesOrder).toHaveBeenCalledWith(newOrder);
    expect(matSnackBar.open).toHaveBeenCalledWith('New Homepage Order Saved!!', 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  });
});
