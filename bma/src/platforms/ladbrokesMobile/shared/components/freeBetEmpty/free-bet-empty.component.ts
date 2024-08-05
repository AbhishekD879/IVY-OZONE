import { Component } from '@angular/core';
import { FreeBetEmptyComponent as AppFreeBetEmptyComponent } from '@app/shared/components/freeBetEmpty/free-bet-empty.component';

@Component({
    selector:'free-bet-empty',
    templateUrl: '../../../../../app/shared/components/freeBetEmpty/free-bet-empty.component.html',
    styleUrls: ['../../../../../app/shared/components/freeBetEmpty/free-bet-empty.component.scss','./free-bet-empty.component.scss']
})

export class FreeBetEmptyComponent extends AppFreeBetEmptyComponent {}