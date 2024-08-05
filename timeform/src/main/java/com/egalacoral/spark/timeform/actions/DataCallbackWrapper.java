package com.egalacoral.spark.timeform.actions;

import com.egalacoral.spark.timeform.api.DataCallback;

public interface DataCallbackWrapper {

  <T> DataCallback<T> wrap(DataCallback<T> dataCallback);
}
