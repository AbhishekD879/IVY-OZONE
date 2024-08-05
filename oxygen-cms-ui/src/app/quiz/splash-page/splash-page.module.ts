import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { SplashPageRoutingModule } from './splash-page-routing.module';
import { SplashPageListComponent } from './splash-page-list/splash-page-list.component';
import { SplashPageCreateComponent } from './splash-page-create/splash-page-create.component';
import { SplashPageEditComponent } from './splash-page-edit/splash-page-edit.component';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    SplashPageRoutingModule
  ],
  declarations: [SplashPageListComponent, SplashPageCreateComponent, SplashPageEditComponent],
  entryComponents: [SplashPageCreateComponent],
  providers: [SplashPageApiService, QuizApiService]
})
export class SplashPageModule { }
