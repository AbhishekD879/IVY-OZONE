import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@root/app/shared/shared.module';
import { CommonModule } from '@angular/common';
import { TopSportsListComponent } from '@app/virtual-sports/top-sports/top-sports-list/top-sports-list.component';
import { TopSportsCreateAndUpdateComponent } from '@app/virtual-sports/top-sports/top-sports-create-and-update/top-sports-create-and-update.component';
import { TopSportsRoutingModule } from '@app/virtual-sports/top-sports/top-sports-routing.module';

@NgModule({
    imports: [
        CommonModule,
        SharedModule,
        FormsModule,
        ReactiveFormsModule,
        TopSportsRoutingModule
    ],
    declarations: [
        TopSportsListComponent,
        TopSportsCreateAndUpdateComponent
    ],
    entryComponents: [
    ],
    providers: []
})


export class TopSportsModule {}
