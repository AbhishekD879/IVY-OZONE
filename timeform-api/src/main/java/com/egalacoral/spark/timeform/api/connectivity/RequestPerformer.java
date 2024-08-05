package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.DataCallback;
import retrofit2.Call;

public interface RequestPerformer {

  <T> T invokeSync(Call<T> call);

  <T> void invokeAsync(Call<T> call, DataCallback<T> dataCallback);

}
