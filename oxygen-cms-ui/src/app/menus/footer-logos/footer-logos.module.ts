import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { FooterLogosRoutingModule } from './footer-logos-routing.module';
import { FooterLogosListComponent } from './footer-logos-list/footer-logos-list.component';
import { FooterLogosCreateComponent } from './footer-logos-create/footer-logos-create.component';
import { FooterLogosEditComponent } from './footer-logos-edit/footer-logos-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FooterLogosRoutingModule
  ],
  declarations: [
    FooterLogosListComponent,
    FooterLogosCreateComponent,
    FooterLogosEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class FooterLogosModule { }
