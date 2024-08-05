import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyBetsRoutingModule } from './my-bets-routing.module';
import { OpenBetsComponent } from './open-bets/open-bets.component';
import { SharedModule } from "../shared/shared.module";
import { MyBetsService } from './my-bets.service';


@NgModule({
    declarations: [OpenBetsComponent],
    imports: [
        CommonModule,
        MyBetsRoutingModule,
        SharedModule
    ],
    providers:[MyBetsService]
})
export class MyBetsModule { }
