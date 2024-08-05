import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'callBack'
})
export class CallBackPipe implements PipeTransform {

    /**
     * Run callback function wherever needed in template
     */
    transform(value: string, handler: (value: any) => any, context?: any): any {
        if (context) {
            return handler.call(context, value);
        }

        return handler(value);
    }
}
