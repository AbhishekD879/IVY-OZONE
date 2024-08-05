import { CoreToolsService } from './core-tools.service';

describe('CoreToolsService', () => {

  let service: CoreToolsService;

  beforeEach(() => {
    service = new CoreToolsService();
  });

  it('should check for json format', () => {
    expect(service.isJSON('{`12}')).toBe(false);
    expect(service.isJSON('{"x": 1}')).toBe(true);
  });

  it('should get correct currency symbol', () => {
    expect(service.getCurrencySymbolFromISO('USD')).toBe('$');
    expect(service.getCurrencySymbolFromISO('GBP')).toBe('£');
    expect(service.getCurrencySymbolFromISO('UAH')).toBe('UAH');
    expect(service.getCurrencySymbolFromISO('AUD')).toBe('AUD');
  });

  it('should convert string to camelcase', () => {
    expect(service.camelize('camelcase')).toBe('camelcase');
    expect(service.camelize('camel_case')).toBe('camelCase');
    expect(service.camelize('camel_ca_se')).toBe('camelCaSe');
  });

  describe('merge', () => {
    it('should merge two objects', () => {
      const obj1 = {
        a: 1,
        c: {
          d: 3,
        }
      };

      const obj2 = {
        b: 3,
        c: {
          f: 1,
        },
      };

      expect(JSON.stringify(service.merge(obj1, obj2))).toBe('{"a":1,"c":{"d":3,"f":1},"b":3}');
    });

    it('should merge two bigger objects', () => {
      const obj1 = {
        a: 1,
        k: {
          l: 1
        },
        d: 2,
        c: {
          d: 3,
        }
      };

      const obj2 = {
        i: {
          j: 6
        },
        b: 3,
        c: {
          f: 1,
          g: 3
        },
        h: 5,
        k: {
          m: 2
        },
      };

      expect(JSON.stringify(service.merge(obj1, obj2)))
        .toBe('{"a":1,"k":{"l":1,"m":2},"d":2,"c":{"d":3,"f":1,"g":3},"i":{"j":6},"b":3,"h":5}');
    });
  });

  describe('#deepMerge', () => {
    it('should merge two objects', () => {
      const obj1 = {
        a: 1,
        c: {
          d: 3,
        }
      };

      const obj2 = {
        b: 3,
        c: {
          f: 1,
        },
      };

      expect(JSON.stringify(service.deepMerge(obj1, obj2))).toBe('{"a":1,"c":{"d":3,"f":1},"b":3}');
    });

    it('should merge two bigger objects', () => {
      const obj1 = {
        a: 1,
        k: {
          l: 1
        },
        d: 2,
        c: {
          d: 3,
        }
      };

      const obj2 = {
        i: {
          j: 6
        },
        b: 3,
        c: {
          f: 1,
          g: 3
        },
        h: 5,
        k: {
          m: 2
        },
      };

      expect(JSON.stringify(service.deepMerge(obj1, obj2)))
        .toBe('{"a":1,"k":{"l":1,"m":2},"d":2,"c":{"d":3,"f":1,"g":3},"i":{"j":6},"b":3,"h":5}');
    });

    it('should set source to target if source unavailable', () => {
      const obj2 = {
        b: 3,
        c: {
          f: 1,
        }
      };

      expect(JSON.stringify(service.deepMerge(undefined, obj2))).toBe('{"b":3,"c":{"f":1}}');
    });
  });

  it('should generate correct UUID', () => {
    expect(typeof service.uuid()).toBe('string');
    expect(service.uuid().split('-').length).toBe(5);
  });

  it('should check if object has own deep property', () => {
    const obj = {
      prop1: 3,
      prop2: {
        childProp: 1,
      },
    };

    expect(service.hasOwnDeepProperty(obj, 'prop1')).toBe(true);
    expect(service.hasOwnDeepProperty(obj, 'prop2.childProp')).toBe(true);
    expect(service.hasOwnDeepProperty(obj, 'prop2.childProp.childChildProp')).toBe(false);
  });

  describe('getDeepSegment', () => {
    it('should get deep segment or default value', () => {
      const obj = {
        prop: [
          ['1', ['4', '4', '4'], '1'],
          ['2', '2', '2'],
          ['3', '3', '3']
        ]
      };

      expect(service.getDeepSegment(obj, 'prop[0][1][2]', 'test')).toBe('4');
      expect(service.getDeepSegment(obj, 'prop[1][4]', 'test')).toBe('test');
      expect(service.getDeepSegment(obj, 'prop[2][2]', 'test')).toBe('3');
    });

    it(`should return Not return default value if 'value[segment]' is equal 0`, () => {
      expect(service.getDeepSegment({ prop: 0 }, 'prop', 'test') as any).toBe(0);
    });
  });

  it('should get own deep property or default value', () => {
    const obj = {
      prop1: {
        childProp: 'val1'
      },
      prop2: {
        childProp: 'val2'
      }
    };

    expect(service.getOwnDeepProperty(obj, 'prop1.childProp', 'test')).toBe('val1');
    expect(service.getOwnDeepProperty(obj, 'prop2.childProp', 'test')).toBe('val2');
    expect(service.getOwnDeepProperty(obj, 'prop2.childProp1', 'test')).toBe('test');
  });

  it('should get correct day suffix', () => {
    expect(service.getDaySuffix(3)).toBe('rd');
    expect(service.getDaySuffix(4)).toBe('th');
    expect(service.getDaySuffix(13)).toBe('th');
    expect(service.getDaySuffix(21)).toBe('st');
    expect(service.getDaySuffix(22)).toBe('nd');
    expect(service.getDaySuffix(23)).toBe('rd');
  });

  it('should deep clone object without any reference', () => {
    const func = () => {};
    const obj = {
      prop: {
        childProp1: true,
        childProp2: {
          method : func
        }
      }
    };
    expect(JSON.stringify(service.deepClone(obj))).toBe(JSON.stringify(obj));
    expect(service.deepClone(obj).prop.childProp2.method).not.toBe(obj.prop.childProp2.method);
  });

  it('should round float to specified precision', () => {
    expect(service.roundDown(1.56)).toBe(1);
    expect(service.roundDown(1.56, 1)).toBe(1.5);
    expect(service.roundDown(5.06, 1)).toBe(5);
    expect(service.roundDown(5.06, 2)).toBe(5.06);
  });

  it('should round correctly', () => {
    expect(service.roundTo(1.56)).toBe(2);
    expect(service.roundTo(1.56, 1)).toBe(1.6);
    expect(service.roundTo(0.045, 2)).toBe(0.05);
  });
});
