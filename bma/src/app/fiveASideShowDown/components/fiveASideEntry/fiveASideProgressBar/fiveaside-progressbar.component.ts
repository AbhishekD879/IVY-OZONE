import { ChangeDetectorRef, Component, Input, OnChanges } from '@angular/core';
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
export class FiveASideProgressBarComponent extends ProgressBarComponent  implements OnChanges {
  @Input() origin: string;
  constructor(private changeDetectorRef: ChangeDetectorRef) {
    super();
  }
  ngOnChanges(): void {
    super.setProgress();
    this.changeDetectorRef.markForCheck();
  }
}
