package com.egalacoral.spark.timeform.api.connectivity;

import java.io.IOException;

import com.egalacoral.spark.timeform.api.DataCallback;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.egalacoral.spark.timeform.api.TimeFormException;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SimpleRequestPerformer implements RequestPerformer {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(SimpleRequestPerformer.class);

  @Override
  public <T> T invokeSync(Call<T> call) {
    try {
      LOGGER.info("Request: {}", call.request());
      Response<T> response = call.execute();
      if (response.isSuccessful()) {
        T body = response.body();
        LOGGER.debug("Response: {}", body);
        return body;
      } else {
        throw new TimeFormException(response);
      }
    } catch (TimeFormException e) {
      throw e;
    } catch (Exception e) {
      throw new TimeFormException("TimeForm endpoint call failed.", e);
    }
  }

  @Override
  public <T> void invokeAsync(Call<T> call, DataCallback<T> dataCallback) {
    try {
      call.enqueue(new Callback<T>() {
        @Override
        public void onResponse(Call<T> call, Response<T> response) {
          if (response.isSuccessful()) {
            T body = response.body();
            LOGGER.debug("Response: {}", body);
            dataCallback.onResponse(body);
          } else {
            dataCallback.onError(new TimeFormException(response));
          }
        }

        @Override
        public void onFailure(Call<T> call, Throwable t) {
          LOGGER.error("Request failed", t);
          TimeFormException tfe;
          if (t instanceof TimeFormException) {
            tfe = (TimeFormException) t;
          } else {
            tfe = new TimeFormException(t);
          }
          dataCallback.onError(tfe);
        }
      });
    } catch (TimeFormException tfe) {
      dataCallback.onError(tfe);
    } catch (Exception e) {
      dataCallback.onError(new TimeFormException(e));
    }
  }
}
