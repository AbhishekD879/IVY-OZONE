var angularProbe = ng.probe(arguments[0]);
var componentInstance = angularProbe.componentInstance;


// onChange() calls this.date.value; this.setDate(); this.validateDate();
// see bma: src/ng/shared/components/datePicker/date-picker.component.ts

componentInstance.onChange(arguments[1]);
