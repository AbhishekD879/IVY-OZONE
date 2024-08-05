import { Component, Input } from '@angular/core';
import { trigger,transition,style,animate } from '@angular/animations';
import { ProgressBarComponent } from '@app/lazy-modules/bybHistory/components/progressBar/progress-bar.component';

@Component({
    selector: 'fiveaside-progressbar',
    templateUrl: './fiveaside-progressbar.component.html',
    styleUrls: ['./fiveaside-progressbar.component.scss'],
    animations:[trigger('myInsertRemoveTrigger', [
      transition(':enter', [style({width:'0%'}),  animate(2000)])
    ])]
})
export class FiveASideProgressBarComponent extends ProgressBarComponent {
    @Input() origin:string;
}
