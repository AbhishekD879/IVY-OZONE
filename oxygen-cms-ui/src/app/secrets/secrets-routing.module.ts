import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SecretsPageComponent } from '@app/secrets/secrets-page/secrets-page.component';

const secretsRoutes: Routes = [
  {
    path: '',
    component: SecretsPageComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(secretsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class SecretsRoutingModule { }
