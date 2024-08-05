package com.ladbrokescoral.oxygen.questionengine.crm;

@FunctionalInterface
interface SupplierWithException<T, E extends Exception> {
  T get() throws E;
}
