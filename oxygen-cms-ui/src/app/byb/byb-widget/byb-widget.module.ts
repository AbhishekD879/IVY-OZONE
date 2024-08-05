import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BybWidgetRoutingModule } from './byb-widget-routing.module';
import { BybWidgetComponent } from './BYB-Widget/byb-widget.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BigCompetitionAPIService } from '@app/sports-pages/big-competition/service/big-competition.api.service';
@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BybWidgetRoutingModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    BybWidgetComponent
  ],
  providers: [
    BigCompetitionAPIService,DatePipe
  
  ]
})
export class BybWidgetModule { }
