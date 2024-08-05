import { Directive, HostBinding, Input } from "@angular/core";
import { TimeService } from "@core/services/time/time.service";

@Directive({
  selector: '[dateTimeFmt]'
})
export class DateTimeChangeDirective {
  /*
     * converts date to Friday(Today/Tomorrow) or Friday(17th June) - HH:MM
     *
   */
  @Input() dateTimeFmt: string;
  @Input() showTime?: boolean;
  @Input() isMyBets?: boolean;
  constructor(private timeService: TimeService) { }

  @HostBinding()
  get innerText() {  
    const parsedDateString = this.timeService.convertDateStr(this.dateTimeFmt);
    const formatedDate = new Date(this.timeService.formatByPattern(parsedDateString, 'yyyy/MM/dd HH:mm:ss', '', false));
    return this.timeService.getDatetimeWithFormatSuffix(formatedDate, this.showTime, this.isMyBets);
  }

}