import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { SplashPageComponent } from '../free-ride/splash-page/splash-page.component';
import { CampaignListComponent } from './campaign-list/campaign-list.component';
import { CampaignCreateComponent } from './campaign-create/campaign-create.component';
import { CampaignEditComponent } from './campaign-edit/campaign-edit.component';

const splashRoutes: Routes = [
    { path: 'splash', component: SplashPageComponent },
    { path: 'campaign', component: CampaignListComponent },
    { path: 'campaign/create', component: CampaignCreateComponent },
    { path: 'campaign/:id', component: CampaignEditComponent }
];

@NgModule({
    imports: [
        RouterModule.forChild(splashRoutes)
    ],
    exports: [RouterModule]
})
export class FreeRideRoutingModule { }
