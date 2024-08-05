import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BannerComponent } from '@app/betpack-market-place/banner/banner.component';
import { BetPackTokenComponent } from '@app/betpack-market-place/betpack-token/betpack-token.component';
import { BetPackCreateComponent } from '@app/betpack-market-place/create-betpack/bet-pack-create.component';
import { BetPackEditComponent } from '@app/betpack-market-place/edit-betpack/bet-pack-edit.component';
import { EditFilterComponent } from '@app/betpack-market-place/filter/edit-filter/edit-filter.component';
import { FilterComponent } from '@app/betpack-market-place/filter/filter.component';
import { BetPackListComponent } from '@app/betpack-market-place/list-betpack/bet-pack-list.component';
import { StaticFieldComponent } from '@app/betpack-market-place/static-fields/betpack-static-fields.component';
import { CreateOnboardComponent } from './onboarding-betpack/create-onboard/create-onboard.component';
import { EditOnboardComponent } from './onboarding-betpack/edit-onboard/edit-onboard.component';
import { OnboardingBetpackComponent } from './onboarding-betpack/onboarding-betpack.component';

const route: Routes = [
  {
    path: '',
    component: BetPackListComponent,
    children: []
  },
  { path: 'filter/:id', component: EditFilterComponent },
  { path: 'banner', component: BannerComponent },
  { path: 'filter', component: FilterComponent },
  { path: 'static-field', component: StaticFieldComponent },
  { path: 'betpack-list', component: BetPackListComponent },
  { path: 'betpack-list/create', component: BetPackCreateComponent },
  { path: 'betpack-list/:id', component: BetPackEditComponent },
  { path: 'betpack-token', component: BetPackTokenComponent },
  { path: 'onboarding-betpack', component:OnboardingBetpackComponent},
  { path: 'onboarding-betpack/create-onboard', component:CreateOnboardComponent},
  { path: 'onboarding-betpack/:id', component:EditOnboardComponent}
];

@NgModule({
  imports: [
    RouterModule.forChild(route)
  ],
  exports: [
    RouterModule
  ]
})
export class BetPackRoutingModule { }
