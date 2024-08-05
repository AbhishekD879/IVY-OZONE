import { Component } from '@angular/core';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';

@Component({
    selector: 'betpack-content',
    templateUrl: './betpack-content.component.html'
})
export class BetpackContentComponent {
    constructor(public betpackCmsService: BetpackCmsService){}
}
