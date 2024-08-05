import { Injectable } from '@angular/core';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { PROPERTY_TYPE } from '@lazy-modules/freeRide/constants/free-ride-constants';
import { IDOMData } from '@lazy-modules/freeRide/models/free-ride';

@Injectable({ providedIn: 'root' })
export class FreeRideDomService {

    constructor(
        private rendererService: RendererService
    ) { }

    /**
     * to update value of checkbox
     * @param {boolean} value
     * @returns {void}
     */
    public removeElem(parentElem: HTMLElement, childElem: HTMLElement): void {
        if (parentElem && childElem) {
            this.rendererService.renderer.removeChild(parentElem, childElem);
        }
    }

    /**
     * creates HTML elements
     * @param {Array<any>} listOfElems
     * Model- { elemName: [ELEM_TYPE, INNER_TEXT, CLASS_NAME, ID_NAME] } []
     * @returns {any}
     */
    public createDOMElements(listOfElems: Array<any>): Map<string, HTMLElement> | any {
        const listOfElementsCreated: Map<string, HTMLElement> = new Map();
        listOfElems.forEach((elem: {}) => {
            const [key, value] = Object.entries(elem)[0];
            const newElem: HTMLElement = this.rendererService.renderer.createElement(value[0]);
            value[1] && this.rendererService.renderer.setProperty(newElem, PROPERTY_TYPE.INNER_HTML, value[1]);
            value[2] && this.rendererService.renderer.addClass(newElem, value[2]);
            newElem.id = value[3] || '';
            listOfElementsCreated.set(key, newElem);
        });
        return listOfElementsCreated.size > 1 ? listOfElementsCreated : listOfElementsCreated.values().next().value;
    }

    /**
     * appends elems to DOM
     * @param {Array<IDOMData>} listOfElems
     * @returns {void}
     */
    public appendDomElems(listOfElems: Array<IDOMData>): void {
        listOfElems.forEach((elem: IDOMData) => {
            if (elem && elem.parentElem && elem.childElem) {
                this.rendererService.renderer.appendChild(elem.parentElem, elem.childElem);
            }
        });
    }

}
