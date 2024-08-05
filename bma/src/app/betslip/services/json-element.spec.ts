import { JsonElement } from './json-element';

describe('JsonElement transformations', () => {
  describe('Generate JSON', () => {
    let el;

    beforeEach(() => {
      el = JsonElement.element;
    });

    it('should generate an element', () => {
      expect(
        el('ns:element-name', { prop: 'value' }, 'inner text')
      ).toEqual(
        { 'ns:element-name': { prop: 'value' } }
      );
    });

    it('should generate key/value element with no attributes', () => {
      expect(
        el('firstName', 'Robert')
      ).toEqual(
        { firstName: 'Robert' }
      );
    });

    it('should generate nested elements', () => {
      expect(
        el('parent-element', { level: 1 }, [
          el('child-element', { level: 2 }, 12345)
        ])
      ).toEqual(
        {
          'parent-element': {
            level: 1,
            'child-element': {
              level: 2
            }
          }
        }
      );
    });

    it('should generate a complex JSON structure', () => {
      const result =
        el('person', {
          created: '2006-11-11T19:23',
          modified: '2006-12-31T23:59'
        }, [
          el('firstName', 'Robert'),
          el('lastName', 'Smith'),
          el('address', { type: 'home' }, [
            el('street', '12345 Sixth Ave'),
            el('city', 'Anytown'),
            el('state', { code: 'CA' }, 'Califoornia'),
            el('postalCode', '98765-4321')
          ]),
          el('phones', { count: 2 }, [
            el('phone', { code: '12', type: 'office' }, '98-7654321'),
            el('phone', { code: '32', type: 'mobile' }, '12-3456789')
          ])
        ]);

      expect(result).toEqual(
        {
          person: {
            created: '2006-11-11T19:23',
            modified: '2006-12-31T23:59',
            firstName: 'Robert',
            lastName: 'Smith',
            address: {
              type: 'home',
              street: '12345 Sixth Ave',
              city: 'Anytown',
              state: {
                code: 'CA'
              },
              postalCode: '98765-4321'
            },
            phones: {
              count: 2,
              phone: {
                code: '32',
                type: 'mobile'
              }
            }
          }
        }
      );
    });

    it('should return attribute value if key is undefined', () => {
      expect(el(undefined, '123')).toBe('123');
    });
  });
});
