import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BetpackReviewHomepageComponent } from '@app/betpackReview/components/betpackReviewHomePage/betpack-review-homepage.component';

export const routes: Routes = [
    {
        path: '',
        component: BetpackReviewHomepageComponent
    }
];

@NgModule({
    imports: [
        RouterModule.forChild(routes)
    ],
    exports: [
        RouterModule
    ]
})
export class BetpackReviewRoutingModule { }
