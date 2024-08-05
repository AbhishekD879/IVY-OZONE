import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SeasonViewComponent } from './season-view/season-view.component';
import { SeasonEditComponent } from './season-edit/season-edit.component';
import { OtfSeasonsRoutingModule } from './otf-seasons-routing.module';
import { SharedModule } from '@root/app/shared/shared.module';
import { SeasonsApiService } from '@root/app/one-two-free/service/seasons.api.service';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    SeasonViewComponent,
    SeasonEditComponent
  ],
  imports: [
    CommonModule,
    OtfSeasonsRoutingModule,
    SharedModule, FormsModule
  ],
  providers: [SeasonsApiService]
})
export class OtfSeasonsModule { }
