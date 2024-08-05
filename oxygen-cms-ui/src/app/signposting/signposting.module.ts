import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared/shared.module';
import { SignpostingRoutingModule } from './signposting-routing.module';
import { FreebetSignpostingListComponent } from './freebet/freebet-signposting/freebet-signposting-list.component';
import { CreateFreebetSignpostingComponent } from './freebet/freebet-signposting/create-freebet-signposting/create-freebet-signposting.component';

@NgModule({
    imports: [SharedModule, SignpostingRoutingModule, FormsModule, ReactiveFormsModule],
    providers: [],
    declarations: [
        FreebetSignpostingListComponent,
        CreateFreebetSignpostingComponent
    ],
    entryComponents: [
    ]
})
export class SignpostingModule { }
