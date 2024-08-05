import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { TwoUpSignPostingBlurbMsgComponent } from './components/signpostingBlurbMsg/twoup-signposting-blurbmsg.component';

@NgModule({
  declarations: [TwoUpSignPostingBlurbMsgComponent],
  imports: [
    SharedModule
  ],
  providers:[],
  exports: [
    TwoUpSignPostingBlurbMsgComponent
  ]
})
export class TwoUpSignPostingBlurbMsgModule {
  static entry = {TwoUpSignPostingBlurbMsgComponent};
}
