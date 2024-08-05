import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MatchRewardsMainComponent } from '@app/euro/components/matchRewardsMain/match-rewards-main.component';

export const routes: Routes = [
    {
        path: '',
        component: MatchRewardsMainComponent
    },
];

@NgModule({
    imports: [
        RouterModule.forChild(routes)
    ],
    exports: [
        RouterModule
    ],
    providers: []
})
export class EuroRoutingModule { }
