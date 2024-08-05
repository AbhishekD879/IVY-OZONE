import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { BehaviorSubject } from 'rxjs';

interface ILocalisation {
  [key: string]: any;
}

@Injectable({
  providedIn: 'root'
})
export class LocaleService {

  private locale = 'en-US';
  private localisation: ILocalisation = {};
  private readonly isTranslationLoaded: BehaviorSubject<boolean> = new BehaviorSubject(false);

  constructor(private coreToolsService: CoreToolsService) {}

  /**
   * Getter for detection load status of translation module
   * @returns {BehaviorSubject<boolean>} isTranslationLoaded
   */
  get isTranslationModuleLoaded(): BehaviorSubject<boolean> {
    return this.isTranslationLoaded;
  }

  set isTranslationModuleLoaded(value: BehaviorSubject<boolean> ){}

  /**
   * Sets translations
   * @param {ILocalisation} langData
   */
  setLangData(langData: ILocalisation): void {
    this.localisation[this.locale] = this.coreToolsService.deepMerge(this.localisation[this.locale], langData);
  }

  /**
   * For future multi language implementation
   * @param lang
   */
  setLocale(lang: string): void {
    this.locale = lang;
  }

  /**
   * For future multi language implementation
   * @returns {string}
   */
  getLocale(): string {
    return this.locale;
  }

  /**
   * Gets locale string by locale token
   * @param {string} token
   * @param {Array | Object} args
   * @returns {string}
   */
  getString(token: string, args?): string {
    const tokenParts = token && token.split('.') || [],
      moduleName = tokenParts.length && tokenParts.shift().toLowerCase(),
      moduleTranslations = this.localisation[this.locale] && this.localisation[this.locale][moduleName];

    if (tokenParts.length && moduleName && moduleTranslations) {
      let translationString = token
        .substring(token.indexOf('.') + 1)
        .split('.')
        .reduce((p, c) => (p && p[c]) || null, moduleTranslations);

      if (args && translationString) {
        translationString = this.applySubstitutions(translationString, args);
      }

      return translationString || 'KEY_NOT_FOUND';
    }

    return token;
  }

  /**
   * Substitute parameters passed into 'getString' method
   * @params {string} text
   * @params {Array | Object} subs
   * @
   */
  applySubstitutions(text, subs): string {
    let res = text,
      firstOfKind = 0;

    if (_.isArray(subs)) {
      _.each(subs, (sub, i) => {
        res = res.replace(new RegExp(`%${i + 1}`, 'g'), sub);
        res = res.replace(`{${i + 1}}`, sub);
      });
    } else if (_.isObject(subs)) {
      _.each(subs, (v, k) => {
        ++firstOfKind;
        res = res.replace(`{${k}}`, v);
        res = res.replace(`%${k}`, v);
        res = res.replace(`%${firstOfKind}`, v);
        res = res.replace(`{${firstOfKind}}`, v);
      });
    }

    return res;
  }

  /**
   * Emmit success translation complete (now it is called only in TranslationModule's constructor)
   */
  translationLoadComplete(): void {
    this.isTranslationLoaded.next(true);
    this.isTranslationLoaded.complete();
  }
}
