import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QuizPopupConfigComponent } from './quiz-popup-config.component';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {BrandService} from '@app/client/private/services/brand.service';
import {QuizPopupApiService} from '@app/quiz/service/quiz-popup.api.service';
import {EMPTY} from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';

describe('OptionsPopupConfigComponent', () => {
  let component: QuizPopupConfigComponent;
  let fixture: ComponentFixture<QuizPopupConfigComponent>;
  const quizPopupApiService: Partial<QuizPopupApiService> = {
    getQuizzes: jasmine.createSpy('getQuizzes').and.returnValue(EMPTY),
    getOneByBrand: jasmine.createSpy('getOneByBrand').and.returnValue(EMPTY)
  };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ QuizPopupConfigComponent ],
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ],
      providers: [
        { provide: DialogService, useValue: <DialogService> {} },
        { provide: BrandService, useValue: <BrandService> {} },
        { provide: QuizPopupApiService, useValue: quizPopupApiService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuizPopupConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
