import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SecretsPageComponent } from './secrets-page/secrets-page.component';
import { SecretsRoutingModule } from '@app/secrets/secrets-routing.module';
import { SharedModule } from '@app/shared/shared.module';
import { SecretEntryComponent } from '@app/secrets/secret-entry/secret-entry.component';
import { EditSecretEntryComponent } from '@app/secrets/edit-secret-entry/edit-secret-entry.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SecretsRoutingModule
  ],
  declarations: [
    SecretsPageComponent,
    SecretEntryComponent,
    EditSecretEntryComponent
  ],
  entryComponents: [
    EditSecretEntryComponent
  ]
})
export class SecretsModule { }
