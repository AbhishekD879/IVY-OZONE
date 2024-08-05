import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { BetpackReviewRoutingModule } from '@coralDesktop/betpackReview/betpack-review.routing.module';
import { DesktopBetpackReviewHomepageComponent } from '@coralDesktop/betpackReview/components/betpackReviewHomePage/betpack-review-homepage.component';
import { CommonModule } from '@angular/common';
import { BetpackCmsModule } from '@app/lazy-modules/betpackPage/betpack-cms.module';
@NgModule({
  imports: [

    SharedModule,
    BetpackCmsModule,
    CommonModule,
    BetpackReviewRoutingModule
  ],
  declarations: [
    DesktopBetpackReviewHomepageComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class BetpackReviewModule { }