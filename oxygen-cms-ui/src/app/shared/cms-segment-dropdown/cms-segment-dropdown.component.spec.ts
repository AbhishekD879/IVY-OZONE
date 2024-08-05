import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { CmsSegmentDropdownComponent } from './cms-segment-dropdown.component';
import { CSPSegmentConstants } from '@app/app.constants';
import { SharedModule } from '@app/shared/shared.module';
import { ApiClientService } from '@app/client/private/services/http';
import { of } from 'rxjs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('CmsSegmentDropdownComponent', () => {
  let component: CmsSegmentDropdownComponent,
    fixture: ComponentFixture<CmsSegmentDropdownComponent>;
  let apiClientService, globalLoaderService;

  beforeEach(async(() => {
    apiClientService = {
      segmentMethods: jasmine.createSpy('segmentMethods').and.returnValue({
        getSegments: jasmine.createSpy('getSegments').and.returnValue(of({ body: [{ 'name': 'Universal' },{'name': 'Cricket'}] })),
      })
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    TestBed.configureTestingModule({
      imports: [ BrowserAnimationsModule, SharedModule ],
      providers: [
        { provide: ApiClientService, useValue: apiClientService }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA]
    }).compileComponents();

    component = new CmsSegmentDropdownComponent(
      apiClientService, globalLoaderService
    );

    fixture = TestBed.createComponent(CmsSegmentDropdownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    component.ngOnInit();
  }));

  describe('#ngOnInit', () => {
    it('should create', () => {
      expect(component).toBeTruthy();
    });
  });

  it('should get the default segment selected as Universal', () => {
    component.activeSegment = CSPSegmentConstants.UNIVERSAL_TITLE;
    component.ngOnInit();
    expect(component.selectedValue).toBe(CSPSegmentConstants.UNIVERSAL_TITLE);
  });

  it('should get segments list onInIt', () => {
    component.ngOnInit();
    expect(apiClientService.segmentMethods().getSegments).toHaveBeenCalled();
    expect(component.segmentsList.length).toBe(2);
    expect(component.segmentsFilteredList.length).toBe(2);
  })

  it('should filter the data based on search string', () => {
    component.ngOnInit();
    const segmentSearch = 'Cri';
    component['onSearch'](segmentSearch);
    expect(component.segmentsList.length).toBe(2);
    expect(component.segmentsFilteredList.length).toBe(1);
  })

  it('should filter the universal data when search string is empty', () => {
    component.ngOnInit();
    const segmentSearch = '';
    component['onSearch'](segmentSearch);
    expect(component.segmentsList.length).toBe(2);
    expect(component.segmentsFilteredList.length).toBe(2);
  })
});
