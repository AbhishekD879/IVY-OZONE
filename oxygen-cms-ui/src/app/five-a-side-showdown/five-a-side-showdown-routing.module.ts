import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AddEditFaqComponent } from '@app/five-a-side-showdown/components/add-edit-faq/add-edit-faq.component';
import { ContestManagerComponent } from '@app/five-a-side-showdown/components/contest-manager/contest-manager.component';
import { EditContestComponent } from '@app/five-a-side-showdown/components/edit-contest/edit-contest.component';
import { FaqComponent } from '@app/five-a-side-showdown/components/faq/faq.component';
import { TermsAndConditionsComponent } from '@app/five-a-side-showdown/components/terms-and-conditions/terms-and-conditions.component';
import { WelcomeOverlayComponent } from '@app/five-a-side-showdown/components/welcome-overlay/welcome-overlay.component';

const contestRoutes: Routes = [
  {
    path: '',
    component: ContestManagerComponent,
  },
  {
    path: 'edit/:contestid',
    component: EditContestComponent
  },
  {
    path: 'faq',
    component: FaqComponent,
  },
  {
    path: 'faq/add-edit',
    component: AddEditFaqComponent
  },
  {
    path: 'faq/add-edit/:id',
    component: AddEditFaqComponent
  },
  {
    path: 'terms-and-conditions',
    component: TermsAndConditionsComponent
  },
  {
    path: 'welcome-overlay',
    component: WelcomeOverlayComponent
  }
];

@NgModule({
    imports: [
        RouterModule.forChild(contestRoutes)
    ],
    exports: [RouterModule]
})
export class FiveASideShowdownRoutingModule {
}