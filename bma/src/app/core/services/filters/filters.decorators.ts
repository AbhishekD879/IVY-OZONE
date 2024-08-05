/**
 * filterStabilize decorator returns the input data provided to the method if the filtered result is falsy.
 */
export const filterStabilize: MethodDecorator = (target: Object, propertyKey: string, descriptor: PropertyDescriptor): void => {
  descriptor = descriptor || Object.getOwnPropertyDescriptor(target, propertyKey);

  const originalMethod: Function = descriptor.value;

  descriptor.value = (...args): any => {
    return originalMethod.apply(this, args) || args[0];
  };
};
