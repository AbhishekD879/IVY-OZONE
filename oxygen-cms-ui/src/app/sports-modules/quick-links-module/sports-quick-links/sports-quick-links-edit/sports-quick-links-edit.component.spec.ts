import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Observable, of } from 'rxjs';
import { NavigationPoint } from '@app/client/private/models/navigationpoint.model';
import { SportsQuickLinksEditComponent } from './sports-quick-links-edit.component';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { SportQuickLinksService } from '../sport-quick-links.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NotificationDialogComponent } from '@app/shared/dialog/notification-dialog/notification-dialog.component';
import { BrowserDynamicTestingModule } from '@angular/platform-browser-dynamic/testing';
import { FormControl, FormGroup } from '@angular/forms';
import { CSPSegmentLSConstants } from '@app/app.constants';

describe('SportsQuickLinksEditComponent', () => {
    let component: SportsQuickLinksEditComponent,
        fixture: ComponentFixture<SportsQuickLinksEditComponent>;

    let router,
        activatedRoute,
        apiClientService,
        sportQuickLinksService,
        sportsModulesBreadcrumbsService,
        globalLoaderService,
        snackBar,
        segmentStoreService,
        brandService,
        dialogService;

    beforeEach(async(() => {
        router = {};
        activatedRoute = {
            params: of({
                id: 'mockId'
            })
        };

        sportQuickLinksService = {
            getHubIndex: jasmine.createSpy('getHubIndex').and.returnValue(of([{}, {}, {}]))
        };

        apiClientService = {
            sportsQuickLink: jasmine.createSpy('sportsQuickLink').and.returnValue({
                findOne: jasmine.createSpy('findOne').and.returnValue(of({
                    body: {}
                })),
                update: jasmine.createSpy('update').and.returnValue(of({ body: { title: '1234' } })),
            }),
        }

        dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog']);

        brandService = {
            isIMActive: jasmine.createSpy('isIMActive')
        };
    
        segmentStoreService = {
          validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
          validateHomeModule: jasmine.createSpy('validateHomeModule').and.returnValue(of('homepage')),
          getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.SPORTS_QUICK_LINK }),
          updateSegmentMessage: jasmine.createSpy('updateSegmentMessage'),
          setSegmentValue: jasmine.createSpy('setSegmentValue')
        };

        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        component = new SportsQuickLinksEditComponent(
            router,
            activatedRoute,
            apiClientService,
            sportQuickLinksService,
            sportsModulesBreadcrumbsService,
            dialogService,
            globalLoaderService,
            snackBar,
            brandService,
            segmentStoreService
        );

        TestBed.configureTestingModule({
            declarations: [SportsQuickLinksEditComponent, NotificationDialogComponent, ConfirmDialogComponent],
            imports: [MatDialogModule, HttpClientTestingModule, BrowserAnimationsModule],
            providers: [
                { provide: SportQuickLinksService, useValue: sportQuickLinksService },
                { provide: GlobalLoaderService, useValue: globalLoaderService },
                { provide: DialogService, useValue: dialogService },
                { provide: ApiClientService, useValue: apiClientService },
                { provide: MatSnackBar, useValue: snackBar },
                { provide: SegmentStoreService, useValue: segmentStoreService },
                { provide: Router, useValue: router },
                { provide: MatDialogRef, useValue: <MatDialogRef<ConfirmDialogComponent>>{} },
                { provide: SportsModulesBreadcrumbsService, useValue: sportsModulesBreadcrumbsService },
                { provide: BrandService, useValue: brandService },
                { provide: ActivatedRoute, useValue: activatedRoute }
            ],
            schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA]
        })
            .overrideModule(BrowserDynamicTestingModule, {
                set: {
                    entryComponents: [NotificationDialogComponent, ConfirmDialogComponent],
                }
            })
            .compileComponents();

        fixture = TestBed.createComponent(SportsQuickLinksEditComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();

        component.ngOnInit();

    }));

    it('should create', () => {
        expect(component.isLinkVlid).toBeDefined();

        expect(component.breadcrumbsData).toBeUndefined();
        expect(component.maxLinksAmount).toBeUndefined();
        expect(component.sportsQuickLink).toBeUndefined();
        expect(component.form).toBeUndefined();
    });

    describe('#save', () => {
        it('should save and open dialog', () => {
            component.actionButtons = { extendCollection: jasmine.createSpy('extendCollection') };
            component.save();
            expect(apiClientService.sportsQuickLink().update).toHaveBeenCalled();
            expect(component.sportsQuickLink).toEqual(<NavigationPoint>{ title: '1234' });
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.sportsQuickLink);
        });
    });

    describe('#form validator and emitted data handler', () => {

        beforeEach(() => {
            component.sportsQuickLink = <any>{
                id: 'id',
                title: 'title',
                sportId: 'targetUri',
                disabled: true
            };
            component.form = new FormGroup({
                linkTitle: new FormControl(component.sportsQuickLink.title),
                targetUri: new FormControl(component.sportsQuickLink.sportId),
                mobile: new FormControl(component.sportsQuickLink.disabled)
            });
        });

        it('should handle form valid and check validation to true', () => {
            expect(component.form).toBeDefined();
            component.isSegmentValid = true;
            expect(component.validationHandler()).toBeTruthy();
        });

        it('check validation to true', () => {
            component.isSegmentValid = false;
            expect(component.validationHandler()).toBeFalsy();
        });

        it('should check if segment is valid', () => {
            let flag = true;
            component.isSegmentFormValid(flag);
            expect(component.isSegmentValid).toBeTrue();
        })

        it('should check if segment is valid', () => {
            let flag = false;
            component.isSegmentFormValid(flag);
            expect(component.isSegmentValid).toBeFalse();

        })
    });
});
