import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {OnBoardingGuideListComponent} from './on-boarding-guide-list/on-boarding-guide-list.component';
import {OnBoardingGuideEditComponent} from './on-boarding-guide-edit/on-boarding-guide-edit.component';
import {OnBoardingGuideCreateComponent} from './on-boarding-guide-create/on-boarding-guide-create.component';

const onBoardingGuideRoutes: Routes = [
  { path: '', component: OnBoardingGuideListComponent },
  { path: 'create',  component: OnBoardingGuideCreateComponent },
  { path: ':id',  component: OnBoardingGuideEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(onBoardingGuideRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class OnBoardingGuideRoutingModule {}
