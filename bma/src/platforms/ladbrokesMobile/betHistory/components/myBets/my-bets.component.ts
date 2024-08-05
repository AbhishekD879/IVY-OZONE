import { Component, OnInit } from '@angular/core';
import { MyBetsComponent as AppMyBetsComponent } from '@app/betHistory/components/myBets/my-bets.component';
import { AREAS } from '@app/lazy-modules/racingFeatured/components/racingFeatured/constant';

@Component({
  selector: 'my-bets',
  templateUrl: '../cashOutBets/cash-out-bets.component.html',
  styleUrls: ['../../../../../app/betHistory/components/myBets/my-bets.component.scss']
})
export class MyBetsComponent extends AppMyBetsComponent implements OnInit {
  isHREDP = false;

  ngOnInit() {
    this.isHREDP = this.section === AREAS.HREDP;
    super.ngOnInit();
  }
}
