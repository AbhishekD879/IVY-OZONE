import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BetpackContentComponent } from '@app/betpackMarket/components/betpackContent/betpack-content.component';

export const routes: Routes = [
    {
        path: '',
        component: BetpackContentComponent
    },
];

@NgModule({
    imports: [
        RouterModule.forChild(routes)
    ],
    exports: [
        RouterModule
    ]
})
export class BetpackMarketRoutingModule { }
