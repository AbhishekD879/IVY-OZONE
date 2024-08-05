import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ExternalLinksRoutingModule} from './external-links-routing.module';
import {ExternalLinksPageComponent} from './external-links-page/external-links-page.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from '../shared/shared.module';
import {AddExternalLinkComponent} from './add-external-link/add-external-link.component';
import {EditExternalLinkComponent} from './edit-external-link/edit-external-link.component';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    ExternalLinksRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [ExternalLinksPageComponent, AddExternalLinkComponent, EditExternalLinkComponent],
  entryComponents: [
    AddExternalLinkComponent
  ]
})
export class ExternalLinksModule { }
