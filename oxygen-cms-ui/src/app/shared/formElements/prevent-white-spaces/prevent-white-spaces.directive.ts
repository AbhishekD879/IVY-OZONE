import { Directive, HostListener } from '@angular/core';

@Directive({
    selector: '[preventWhiteSpaces]'
})
export class PreventWhiteSpacesDirective {

    @HostListener('keydown', ['$event']) onKeyDown(event) {
        if (event.keyCode === 32) {
            event.preventDefault();
        }
    }
}
