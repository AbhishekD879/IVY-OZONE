import * as _ from 'underscore';

interface IElement {
  [key: string]: any;
}

export class JsonElement {

  static element(key: string, attr: string | IElement, children?: any): any {
    const obj = {};
    let result = {};

    if (children) {
      _.each(children, item => {
        _.extend(obj, item);
      });
      result[key] = _.extend(attr, obj);
    } else if (key === undefined) {
      result = attr;
    } else {
      result[key] = attr;
    }
    return result;
  }
}

export const el = JsonElement.element;
