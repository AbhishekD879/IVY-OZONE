/**
 * Auto methods binding decorator
 * @param target
 * @param methodName
 * @param descriptor
 * @constructor
 */
export function BindDecorator<T extends Function>(target: object, methodName: string,
                                                  descriptor: TypedPropertyDescriptor<T>): TypedPropertyDescriptor<T> {
  return {
    configurable: true,
    get(): T {
      const bound: T = descriptor.value.bind(this);
      Object.defineProperty(this, methodName, {
        value: bound,
        writable: true,
        enumerable: true
      });
      return bound;
    }
  };
}
