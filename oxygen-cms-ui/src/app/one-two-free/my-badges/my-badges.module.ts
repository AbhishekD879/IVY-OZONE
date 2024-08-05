import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyBadgesDetailComponent } from './my-badges-detail/my-badges-detail.component';
import { MyBadgesRoutingModule } from './my-badges-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@root/app/shared/shared.module';
import { MybadgesApiService } from '@root/app/one-two-free/service/mybadges.api.service'

@NgModule({
  declarations: [MyBadgesDetailComponent],
  imports: [
    CommonModule,
    MyBadgesRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule
  ],

  providers: [MybadgesApiService]
})
export class MyBadgesModule { }
