import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DesktopBetpackReviewHomepageComponent } from '@coralDesktop/betpackReview/components/betpackReviewHomePage/betpack-review-homepage.component';

export const routes: Routes = [
    {
        path: '',
        component: DesktopBetpackReviewHomepageComponent
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
export class BetpackReviewRoutingModule { }
