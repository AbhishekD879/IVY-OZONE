/**
 * AutoUnsubscribe
 * @param blackListedSubscriptions
 * @constructor
 */
export function AutoUnsubscribe(blackListedSubscriptions = []) {
  return (constructor) => {
    const ngOnDestroy = constructor.prototype.ngOnDestroy;

    constructor.prototype.ngOnDestroy = function () {
      for (const prop of Object.keys(this)) {
        const property = this[prop];

        if (!blackListedSubscriptions.includes(prop)) {
          if (property && (typeof property.unsubscribe === 'function')) {
            property.unsubscribe();
          }
        }
      }

      // eslint-disable-next-line prefer-rest-params
      ngOnDestroy && typeof ngOnDestroy === 'function' && ngOnDestroy.apply(this, arguments);
    };
  };
}
