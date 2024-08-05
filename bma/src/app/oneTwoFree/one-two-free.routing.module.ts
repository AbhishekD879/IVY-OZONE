import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { OneTwoFreeDialogComponent } from '@app/oneTwoFree/components/one-two-free-dialog.component';

const routes: Routes = [{
    path: '',
    component: OneTwoFreeDialogComponent,
    children: []
}];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
export class OneTwoFreeRoutingModule {}
