import { NgModule } from '@angular/core';
import { SplashPageComponent } from '@app/free-ride/splash-page/splash-page.component';
import { FreeRideRoutingModule } from './free-ride-routing.module';
import { SharedModule } from '@app/shared/shared.module';
import { FreeRideAPIService } from './services/free-ride.api.service';
import { PostModule } from '../timeline/post/post.module';
import { ViewPotTableComponent } from './view-pot-table/view-pot-table.component';
import { CampaignCreateComponent } from './campaign-create/campaign-create.component';
import { CampaignListComponent } from './campaign-list/campaign-list.component';
import { CampaignEditComponent } from './campaign-edit/campaign-edit.component';

@NgModule({
    imports: [FreeRideRoutingModule, SharedModule, PostModule],
    declarations: [
        CampaignCreateComponent,
        CampaignListComponent,
        CampaignEditComponent,
        ViewPotTableComponent,
        SplashPageComponent
    ],
    providers: [
        FreeRideAPIService
    ],
    exports: []
})
export class FreeRideModule { }
