import { Injectable } from '@angular/core';

@Injectable()
export class TempStorageService {

    private map: { [key: string]: any } = {};

    /**
     * Retrieves a value stored in temporary map.
     * @param {string} key
     * @return {*}
     */
    get(key: string): any {
        return this.map[key];
    }

    /**
     * Stores a value in temporary map.
     * @param {string} key
     * @param {*} value
     */
    set(key: string, value: any) {
        this.map[key] = value;
    }
}
