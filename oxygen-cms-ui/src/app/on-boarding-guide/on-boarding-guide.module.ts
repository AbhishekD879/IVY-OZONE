import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {OnBoardingGuideListComponent} from './on-boarding-guide-list/on-boarding-guide-list.component';
import {OnBoardingGuideEditComponent} from './on-boarding-guide-edit/on-boarding-guide-edit.component';
import {OnBoardingGuideCreateComponent} from './on-boarding-guide-create/on-boarding-guide-create.component';
import {OnBoardingGuideRoutingModule} from './on-boarding-guide-routing.modules';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    OnBoardingGuideRoutingModule
  ],
  declarations: [OnBoardingGuideListComponent, OnBoardingGuideEditComponent, OnBoardingGuideCreateComponent]
})
export class OnBoardingGuideModule {
}
